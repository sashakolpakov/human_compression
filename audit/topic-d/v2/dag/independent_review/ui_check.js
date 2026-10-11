#!/usr/bin/env node
// Minimal DOM shim reused in structure from prior accepted audits. Expectations
// come from the separate accepted graph, not the viewer's route implementation.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const [packet,graphPath,output]=process.argv.slice(2);
const html=fs.readFileSync(packet+'/explorer.html','utf8');
const payload=html.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const script=html.split('<script>')[1].split('</script>')[0],D=JSON.parse(payload),G=JSON.parse(fs.readFileSync(graphPath));
assert.equal(script.trim(),fs.readFileSync(packet+'/explorer.js','utf8').trim());
assert.deepEqual(D.edges,G.edges);assert.deepEqual(D.logical_edge_kinds,G.logical_edge_kinds);
const node=Object.fromEntries(D.nodes.map(n=>[n.id,n])),pred={};for(const n of G.nodes)pred[n.id]=[];
for(const e of G.edges)if(G.logical_edge_kinds.includes(e.kind))pred[e.target].push(e.source);
function ancestors(targets){const seen=new Set(),todo=[...targets];while(todo.length){const n=todo.pop();if(seen.has(n))continue;seen.add(n);todo.push(...pred[n]);}return seen}
class El{constructor(id){this.id=id;this._html='';this.value='';this.checked=false;this.textContent='';this.options=[];this.dataset={};}set innerHTML(v){this._html=v;if(['pair','doc'].includes(this.id)){this.options=[...v.matchAll(/<option value="([^"]+)">/g)].map(x=>({value:x[1]}));if(!this.options.find(x=>x.value===this.value))this.value=this.options[0]?.value||'';}}get innerHTML(){return this._html}querySelectorAll(){return []}querySelector(){return {outerHTML:this._html}}}
const E={};for(const id of ['data','pair','side','doc','gran','context','external','nonlogical','zoom','metric','form','variant','search','canvas','detail','totals','ownership','conditional','headline','headlineScope','reviewStatus','counts','hashes','save','graphSummary','acquisition','routeStatement'])E[id]=new El(id);
E.data.textContent=payload;Object.assign(E.side,{value:'new'});E.doc.value='all';E.gran.value='named';E.zoom.value='1';E.metric.value='characters_without_whitespace';E.variant.value='calibrated_selected';E.form.value='NFC';
const ctx=vm.createContext({document:{getElementById:id=>E[id],querySelectorAll:()=>[],createElement:()=>new El('a')},console,Blob,URL,setTimeout});vm.runInContext(script,ctx,{timeout:10000});
let views=0,edges=0;
function runViews(){let count=0;
 for(const pair of D.pairs)for(const side of ['new','historical'])for(const gran of ['expanded','named']){
  E.pair.value=pair.id;E.side.value=side;E.doc.value='all';E.gran.value=gran;E.external.checked=false;E.nonlogical.checked=false;E.context.checked=false;vm.runInContext('initDocs();render()',ctx);
  const route=ancestors([...pair.historical_targets,...pair.new_targets,...(pair.context_targets||[])]);
  function displayed(id){if(gran==='named'){while(D.parents[id])id=D.parents[id];}return id}
  const ids=new Set([...route].filter(id=>!node[id].external&&node[id].side===side).map(displayed));
  const actualIds=new Set([...E.canvas.innerHTML.matchAll(/data-id="([^"]+)"/g)].map(x=>x[1]));assert.deepEqual(actualIds,ids,pair.id+' '+side+' '+gran);
  const arrows=new Set();for(const e of G.edges){if(!G.logical_edge_kinds.includes(e.kind)||!route.has(e.source)||!route.has(e.target))continue;const a=displayed(e.source),b=displayed(e.target);if(a!==b&&ids.has(a)&&ids.has(b))arrows.add(a+'|'+b+'|'+(gran==='named'?'logical':e.kind));}
  const actual=JSON.parse(vm.runInContext('JSON.stringify(visibleGraph().edges)',ctx));assert.deepEqual(new Set(actual.map(e=>e.a+'|'+e.b+'|'+(gran==='named'?'logical':e.kind))),arrows,'exact selected fine-route arrows');
  assert.equal((E.canvas.innerHTML.match(/<path class="edge /g)||[]).length,arrows.size);assert(!/NaN|undefined/.test(E.canvas.innerHTML));count++;edges+=arrows.size;
 }
 return count;
}
views=runViews();
let details=0;for(const n of G.nodes){vm.runInContext('detail('+JSON.stringify(n.id)+')',ctx);const panel=E.detail.innerHTML;
 const incoming=panel.split('<h4>Direct prerequisites</h4>')[1].split('<h4>Used by</h4>')[0];
 const outgoing=panel.split('<h4>Used by</h4>')[1].split('<h4>Comparison and attribution links</h4>')[0];
 const links=s=>new Set([...s.matchAll(/data-node="([^"]+)"/g)].map(x=>x[1]));
 assert.deepEqual(links(incoming),new Set(G.edges.filter(e=>e.target===n.id&&G.logical_edge_kinds.includes(e.kind)).map(e=>e.source)));
 assert.deepEqual(links(outgoing),new Set(G.edges.filter(e=>e.source===n.id&&G.logical_edge_kinds.includes(e.kind)).map(e=>e.target)));details++;
}
let metricViews=0;for(const r of D.measurement.coordinates){E.variant.value=r.variant;E.form.value=r.normalization;E.metric.value=r.unit;vm.runInContext('render()',ctx);const num=x=>Number(x).toLocaleString('en-US');
 for(const key of ['written_papers','including_printed_program']){const c=r.comparisons[key];assert(E.headline.innerHTML.includes(num(c.numerator)+' / '+num(c.denominator)+' = '+c.factor.toFixed(3)));}
 assert(E.headline.innerHTML.indexOf('Written papers')<E.headline.innerHTML.indexOf('Including the complete printed program'));
 for(const c of r.per_result)assert(E.conditional.innerHTML.includes(num(c.source_cost)+' / '+num(c.application_cost)));metricViews++;
}
const controls=[];function reject(label,fn){let ok=false;try{fn()}catch(e){ok=true}assert(ok,label+' rejected');controls.push(label)}
vm.runInContext('D.edges[0].target="D2.Pairs"',ctx);reject('wrong prerequisite arrow',runViews);vm.runInContext('D.edges[0].target='+JSON.stringify(G.edges[0].target),ctx);
vm.runInContext('D.pairs.find(p=>p.id==="clause:L074.12").new_targets=[]',ctx);reject('dropped selected output',runViews);vm.runInContext('D.pairs.find(p=>p.id==="clause:L074.12").new_targets='+JSON.stringify(D.pairs.find(p=>p.id==='clause:L074.12').new_targets),ctx);
assert.equal(runViews(),168);
const report={status:'PASS_INDEPENDENT_ACCEPTED_GRAPH_UI_PROJECTION',selected_views:views,detail_panels:details,metric_views:metricViews,regression_controls:controls,arrows:'Prerequisite to use; raw selected endpoint membership checked before any parent contraction.',browser_scope:'Minimal DOM behavioral harness, not a real browser or layout test; two reader pages and final static PNG separately viewed.'};
fs.writeFileSync(output,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
