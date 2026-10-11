// Deterministic DOM behavior test adapted from Topic B; not a browser layout test.
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const file=process.argv[2];if(!file)throw Error('Usage: node test_explorer.js explorer.html [static.svg]');
const html=fs.readFileSync(file,'utf8'),payload=html.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const script=html.split('<script>')[1].split('</script>')[0],D=JSON.parse(payload),elements={};
class El{constructor(id){this.id=id;this._html='';this.textContent='';this.value='';this.checked=false;this.options=[];this.dataset={};}set innerHTML(v){this._html=v;if(['doc','pair'].includes(this.id)){this.options=[...v.matchAll(/<option value="([^"]+)">/g)].map(x=>({value:x[1]}));if(!this.options.some(o=>o.value===this.value))this.value=this.options[0]?.value||'';}}get innerHTML(){return this._html}querySelectorAll(){return []}querySelector(){return {outerHTML:this._html}}}
for(const k of ['data','pair','side','doc','gran','context','external','nonlogical','zoom','metric','form','variant','search','canvas','detail','totals','ownership','conditional','headline','headlineScope','reviewStatus','counts','hashes','save','graphSummary','acquisition','routeStatement'])elements[k]=new El(k);
elements.data.textContent=payload;elements.side.value='new';elements.doc.value='all';elements.gran.value='named';elements.zoom.value='1';elements.metric.value='characters_without_whitespace';elements.form.value='NFC';elements.variant.value='calibrated_selected';
const ctx=vm.createContext({document:{getElementById:id=>elements[id],querySelectorAll:()=>[],createElement:()=>new El('download')},console,Blob,URL,setTimeout});
vm.runInContext(script,ctx,{timeout:10000});const views=[];
function check(name){const svg=elements.canvas.innerHTML;assert(svg.startsWith('<svg'));assert(!svg.includes('NaN'));assert(!svg.includes('undefined'));views.push({name,boxes:(svg.match(/data-id=/g)||[]).length});}
check('default_new_C4');if(process.argv[3])fs.writeFileSync(process.argv[3],elements.canvas.innerHTML);
assert(elements.headline.innerHTML.includes('(x + 60,256) / 71,277'));assert(html.includes('whole U_C'));
let selectedEdgeViews=0;
for(const pair of D.pairs)for(const side of ['historical','new'])for(const granularity of ['named','expanded']){
 elements.pair.value=pair.id;elements.side.value=side;elements.doc.value='all';elements.gran.value=granularity;vm.runInContext('initDocs();render()',ctx);check(pair.id+'_'+side+'_'+granularity);
 const route=new Set([...pair.historical_targets,...pair.new_targets]);let changed=true;while(changed){changed=false;for(const e of D.edges)if(D.logical_edge_kinds.includes(e.kind)&&route.has(e.target)&&!route.has(e.source)){route.add(e.source);changed=true;}}
 const shown=id=>{let n=id;if(granularity==='named')while(D.parents[n])n=D.parents[n];return n;};
 const expected=new Set();for(const id of route){const n=D.nodes.find(n=>n.id===id);if(n.external||n.side!==side)continue;expected.add(shown(id));}
 assert.deepEqual(new Set([...elements.canvas.innerHTML.matchAll(/data-id="([^"]+)"/g)].map(m=>m[1])),expected);
 // Select actual fine-route edges BEFORE grouping. A displayed parent does
 // not authorize dependencies of one of its unselected proof branches.
 const expectedEdges=new Set();
 for(const e of D.edges){
  if(!D.logical_edge_kinds.includes(e.kind)||!route.has(e.source)||!route.has(e.target))continue;
  const a=shown(e.source),b=shown(e.target);
  if(a!==b&&expected.has(a)&&expected.has(b))expectedEdges.add(a+'|'+b+'|'+(granularity==='named'?'logical':e.kind));
 }
 const actual=JSON.parse(vm.runInContext('JSON.stringify(visibleGraph().edges)',ctx));
 assert.deepEqual(new Set(actual.map(e=>e.a+'|'+e.b+'|'+(granularity==='named'?'logical':e.kind))),expectedEdges);
 assert.equal((elements.canvas.innerHTML.match(/<path class="edge /g)||[]).length,expectedEdges.size);
 if(pair.id==='clause:J9'&&side==='new'){
  assert(!actual.some(e=>e.a==='C.J1Setup'&&e.b==='C.Classification'));
  assert(!actual.some(e=>e.a==='program.construction'&&e.b==='C.Classification'));
 }
 if(pair.id==='clause:N16'&&side==='new')assert(!actual.some(e=>e.a==='C.Halving'&&e.b==='C.Scope'));
 selectedEdgeViews++;
}
vm.runInContext('detail("h.P.T1")',ctx);assert(elements.detail.innerHTML.includes('Unknown original-PDF cost'));assert(elements.detail.innerHTML.includes('browser'));
vm.runInContext('detail("C.Petrial")',ctx);assert(elements.detail.innerHTML.includes('../../../../../papers/topic-c/v2/'));assert(elements.detail.innerHTML.includes('Comparison and attribution links'));
const prereq=elements.detail.innerHTML.split('<h4>Direct prerequisites</h4>')[1].split('<h4>Used by</h4>')[0];
for(const e of D.edges.filter(e=>e.target==='C.Petrial'&&!D.logical_edge_kinds.includes(e.kind)))assert(!prereq.includes('data-node="'+e.source+'"'));
let metrics=0;for(const variant of ['raw_untrimmed','raw_selected','calibrated_selected'])for(const form of ['NFC','NFKC'])for(const metric of ['characters_without_whitespace','whitespace_tokens','alphanumeric_units','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']){
 elements.variant.value=variant;elements.form.value=form;elements.metric.value=metric;vm.runInContext('render()',ctx);
 for(const n of D.nodes.filter(n=>n.closure)){const sum=n.closure.unique_owner_ids.reduce((x,id)=>x+D.owner_weights[id][variant][form][metric],0);assert.equal(sum,n.closure.known_owned_text_subtotal[variant][form][metric]);}
 const last=D.acquisition.stages.at(-1);assert.equal(last.cumulative_cost[variant][form][metric],Object.entries(D.documents).filter(([k,d])=>d.side==='new').reduce((s,[k,d])=>s+d.weight[variant][form][metric],0));metrics++;
}
elements.side.value='all';elements.pair.value='all';elements.doc.value='all';elements.gran.value='expanded';elements.context.checked=true;elements.external.checked=true;elements.nonlogical.checked=true;vm.runInContext('initDocs();render()',ctx);check('all_fine_nodes');
assert.equal((elements.canvas.innerHTML.match(/data-id=/g)||[]).length,D.nodes.length);assert.equal((elements.canvas.innerHTML.match(/<path class="edge /g)||[]).length,D.edges.length);
assert(D.edges.every(e=>!e.source.startsWith('owned:')&&!e.target.startsWith('owned:')));
console.log(JSON.stringify({status:'PASS_JAVASCRIPT_INTERFACE_CHECKS',real_browser_layout_test:false,views,selected_named_and_expanded_edge_views:selectedEdgeViews,raw_route_endpoints_checked_before_grouping:true,metric_coordinates:metrics,closure_sums:metrics*D.logical_node_count,all_fine_edges_preserved:true,missing_source_unknown:true,whole_U_and_context_charged:true},null,2));
