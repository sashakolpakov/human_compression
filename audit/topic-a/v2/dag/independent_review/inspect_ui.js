// Independent semantic inspection of the exported explorer, not a browser layout test.
'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('assert'),crypto=require('crypto');
const [htmlPath,outputPath]=process.argv.slice(2);
if(!htmlPath||!outputPath||fs.existsSync(outputPath))throw Error('HTML and fresh output required');
const html=fs.readFileSync(htmlPath,'utf8');
const D=JSON.parse(html.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const script=html.split('<script>')[1].split('</script>')[0];
const functions=script.slice(0,script.indexOf("$('pair').innerHTML="));
assert(functions.length>1000);
const els={};
function element(id){return els[id]??=( {value:'',checked:false,textContent:'',innerHTML:'',querySelectorAll:()=>[],selectedOptions:[{textContent:'metric'}]} );}
element('data').textContent=JSON.stringify(D);
Object.assign(element('form'),{value:'NFC'});Object.assign(element('metric'),{value:'characters_without_whitespace'});
for(const id of ['side','doc'])element(id).value='all';
element('pair').value='all';element('gran').value='expanded';element('search').value='';
const context=vm.createContext({document:{getElementById:element,querySelectorAll:()=>[]}});
vm.runInContext(functions,context,{timeout:1000});
const evaluate=code=>vm.runInContext(code,context,{timeout:1000});
const nodes=new Map(D.nodes.map(n=>[n.id,n])),logical=new Set(D.logical_edge_kinds);
function ancestors(id){while(D.parents[id])id=D.parents[id];return id;}
function independentlyFindPremises(targets){
 const answer=new Set(targets);
 let before=-1;
 while(before!==answer.size){before=answer.size;for(const e of D.edges)if(logical.has(e.kind)&&answer.has(e.target))answer.add(e.source);}
 return answer;
}
const observations=[];
for(const p of D.pairs)for(const side of ['historical','new','all'])for(const gran of ['named','expanded']){
 element('pair').value=p.id;element('side').value=side;element('gran').value=gran;
 const got=evaluate('visibleGraph()');
 const closure=independentlyFindPremises([...p.historical_targets,...p.new_targets]);
 const expected=new Set([...closure].filter(id=>!nodes.get(id).external&&(side==='all'||nodes.get(id).side===side)).map(id=>gran==='named'?ancestors(id):id));
 assert.deepStrictEqual([...got.ids].sort(),[...expected].sort());
 for(const e of got.edges){
  assert(expected.has(e.a)&&expected.has(e.b));
  assert(D.edges.some(f=>logical.has(f.kind)&&(gran==='named'?ancestors(f.source):f.source)===e.a&&(gran==='named'?ancestors(f.target):f.target)===e.b));
 }
 observations.push({pair:p.id,side,gran,nodes:got.ids.length,edges:got.edges.length});
}
element('pair').value='A2';element('side').value='new';element('gran').value='named';
assert(evaluate('visibleGraph().ids.includes("A2.s2")'));
assert(evaluate('visibleGraph().edges.some(e=>e.b==="A2.s2")'));
const forms=['NFC','NFKC'],metrics=['characters_without_whitespace','whitespace_tokens','alphanumeric_units','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace'];
let closureChecks=0;
for(const form of forms)for(const metric of metrics){
 element('form').value=form;element('metric').value=metric;
 assert.strictEqual(evaluate('sumOwners(["code.appendix","code.appendix"])'),D.owner_weights['code.appendix'][form][metric]);
 for(const n of D.nodes)if(n.closure){
  const own=new Set(n.closure.unique_owner_ids);
  const total=[...own].reduce((a,b)=>a+D.owner_weights[b][form][metric],0);
  assert.strictEqual(total,n.closure.known_owned_text_subtotal[form][metric]);
  assert.strictEqual(evaluate('sumOwners('+JSON.stringify([...own])+')'),total);closureChecks++;
 }
}
let nonlogicalDetailChecks=0;
for(const id of new Set(D.edges.filter(e=>!logical.has(e.kind)).flatMap(e=>[e.source,e.target]))){
 evaluate('detail('+JSON.stringify(id)+')');
 const result=element('detail').innerHTML;
 const prerequisites=result.split('<h4>Direct prerequisites</h4>')[1].split('<h4>Used by</h4>')[0];
 const consumers=result.split('<h4>Used by</h4>')[1].split('<h4>Comparison and attribution links</h4>')[0];
 for(const e of D.edges){
  if(e.target===id&&!logical.has(e.kind)&&!D.edges.some(f=>f.source===e.source&&f.target===id&&logical.has(f.kind)))assert(!prerequisites.includes('data-node="'+e.source+'"'));
  if(e.source===id&&!logical.has(e.kind)&&!D.edges.some(f=>f.source===id&&f.target===e.target&&logical.has(f.kind)))assert(!consumers.includes('data-node="'+e.target+'"'));
 }
 assert(result.includes('These links do not assert a proof prerequisite.'));nonlogicalDetailChecks++;
}
let externalChecks=0;
for(const n of D.nodes.filter(n=>n.external)){
 assert.strictEqual(n.weight,null);assert.deepStrictEqual(n.owners,[]);
 evaluate('detail('+JSON.stringify(n.id)+')');assert(element('detail').innerHTML.includes('Unknown external proof cost; never zero.'));externalChecks++;
}
evaluate('detail("A2.recognition")');assert(element('detail').innerHTML.includes('../../../../papers/topic-a/v2/'));
evaluate('detail("F013.4.2c")');assert(element('detail').innerHTML.includes('class="warning"'));
evaluate('detail("h.MagmaN009")');assert(element('detail').innerHTML.includes('GAP'));
element('pair').value='all';element('side').value='all';element('gran').value='expanded';
for(const id of ['context','external','nonlogical'])element(id).checked=true;
const all=evaluate('visibleGraph()');
assert.strictEqual(all.ids.length,D.nodes.length);assert.strictEqual(all.edges.length,D.edges.length);
assert(html.includes('whole common theory and whole complete program appendix'));
assert(html.includes('Unknown means unknown, not zero.'));
const report={status:'PASS_INDEPENDENT_INTERFACE_SEMANTICS',html_sha256:crypto.createHash('sha256').update(html).digest('hex'),route_views:observations,metric_coordinates:10,closure_checks:closureChecks,nonlogical_detail_nodes:nonlogicalDetailChecks,external_unknown_nodes:externalChecks,complete_display_nodes:all.ids.length,all_original_edges:all.edges.length,shared_appendix_deduplicated:true,real_browser_layout_test:false,scope:'Independent route/edge/cost/detail semantics; no mathematical proof or minimal-dependency claim.'};
fs.writeFileSync(outputPath,JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({...report,route_views:report.route_views.length}));
