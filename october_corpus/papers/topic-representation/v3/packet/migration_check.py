#!/usr/bin/env python3
"""Exact complete-proof relocation checks; no numerical scoring or proof automation."""
import difflib,hashlib,json,re
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError('RELOCATION_REJECT '+message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def statement(text,label):
    match=re.search(r'\\begin\{theorem\}(?:\[[^]]*\])?\\label\{'+re.escape(label)+r'\}[\s\S]*?\\end\{theorem\}',text)
    need(match is not None,'missing complete statement '+label)
    return match.group(0)
def semantic(oldtexts,newtexts,edits):
    expected=dict(oldtexts)
    for row in edits:
        text=expected[row['file']];need(text.count(row['before'])==row.get('all_occurrences',1),'edit occurrence '+row['file'])
        expected[row['file']]=text.replace(row['before'],row['after'])
    for path,text in expected.items():need(newtexts[path]==text,'complete transformed text '+path)
    section='volume/sections/05-pair-encoding.tex';local='volume/sections/05-finite-pair-application.tex'
    for label in ['R.FinitePairs','R.PairEncoding']:
        need(statement(oldtexts[section],label)==statement(newtexts[local],label),'local statement '+label)
    need('\\input{sections/05-pair-encoding.tex}' in newtexts['volume/umbrella.tex'],'full proof in U')
    need('\\input{sections/05-pair-encoding.tex}' not in newtexts['volume/finite-normal-pairs.tex'],'proof duplicated in app')
    need('\\input{sections/05-finite-pair-application.tex}' in newtexts['volume/finite-normal-pairs.tex'],'local application bridge')
    for path in ['volume/sections/21-projective.tex','volume/sections/23-source-scope.tex']:
        need('UR.FinitePairs' in newtexts[path] and 'proved in the first application' not in newtexts[path] and 'proved in the complete first' not in newtexts[path],'unpaid sibling premise '+path)
    return True

def audit(root,controls=False):
    root=Path(root);m=read(root/'migration.json');prev=read(root/'previous/author_manifest.json');exports={x['path']:x for x in prev['exports']}
    need(sha(root/'previous/author_manifest.json')==m['previous_manifest_sha256'],'previous manifest')
    oldtexts={x['path']:(root/'previous'/x['path']).read_text() for x in m['previous_tex']}
    newtexts={x['path']:(root/x['path']).read_text() for x in m['current_tex']}
    for x in m['previous_tex']:
        need(sha(root/'previous'/x['path'])==x['sha256']==exports[x['path']]['sha256'],'previous TeX binding '+x['path'])
    for x in m['current_tex']:need(sha(root/x['path'])==x['sha256'],'current TeX binding '+x['path'])
    edits=read(root/'migration_edits.json')['edits'];semantic(oldtexts,newtexts,edits)
    for x in m['unchanged_predecessor_exports']:
        need(x==exports[x['path']] and sha(root/x['path'])==x['sha256'],'unchanged predecessor '+x['path'])
    need(sha(root/'source_contract.json')==exports['source_contract.json']['sha256'],'all31 source dispositions')
    # All complete programs, mandatory data and formal scope/declarations are preserved.
    inv=read(root/'program_inventory.json');formal=read(root/'formal/scope.json')
    oldinv=read(root/'previous/program_inventory.json')
    need(sha(root/'previous/program_inventory.json')==exports['program_inventory.json']['sha256'],'previous program-role inventory')
    need(all(inv[k]==oldinv[k] for k in ['files','mandatory_data','required_computational_premises','counts']),'whole required/optional roles')
    for x in inv['files']+inv['mandatory_data']+formal['modules']:
        need(sha(root/x['path'])==exports[x['path']]['sha256'],'unchanged required/optional/formal bytes '+x['path'])
    diff=[]
    for path,text in sorted(newtexts.items()):
        if oldtexts.get(path,'')!=text:diff.extend(difflib.unified_diff(oldtexts.get(path,'').splitlines(True),text.splitlines(True),fromfile='v1/'+path,tofile='v2/'+path))
    need(''.join(diff)==(root/'scientific_changes.diff').read_text(),'complete scientific diff')
    report={'status':'PASS_EXACT_SHARED_PROOF_RELOCATION','previous_tex_files':len(oldtexts),'current_tex_files':len(newtexts),'unchanged_predecessor_exports':len(m['unchanged_predecessor_exports']),'L126_rows':31,'F010_blocks':6,'moved_full_proof':True,'two_local_statements_exact':True,'program_data_formal_bytes_unchanged':True,'no_sibling_application_premise':True,'controls':[]}
    if controls:
        mutations=[('missing moved proof','volume/sections/05-pair-encoding.tex',lambda t:t.replace('The degrees of old vertices','The omitted degrees of old vertices',1)),('lost q2 endpoint','volume/sections/05-pair-encoding.tex',lambda t:t.replace('including when $q=2$','except when $q=2$',1)),('lost trivial group','volume/sections/05-pair-encoding.tex',lambda t:t.replace('For $G=1$, use a single','For $G=2$, use a single',1)),('rank changed','volume/sections/05-finite-pair-application.tex',lambda t:t.replace('$[G:H]+3$','$[G:H]+2$',1)),('dropped U import','volume/umbrella.tex',lambda t:t.replace('\\input{sections/05-pair-encoding.tex}','',1)),('sibling reference restored','volume/sections/21-projective.tex',lambda t:t.replace('proved in common Theorem UR.FinitePairs','proved in the first application',1))]
        for name,path,f in mutations:
            changed=dict(newtexts);changed[path]=f(changed[path]);need(changed[path]!=newtexts[path],'ineffective fixture '+name)
            try:semantic(oldtexts,changed,edits)
            except ValueError as error:report['controls'].append({'name':name,'rejected':True,'message':str(error)})
            else:raise ValueError('accepted corruption '+name)
    return report
if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);args=a.parse_args();report=audit(Path(__file__).resolve().parent,True);need(not args.out.exists(),'fresh result');args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
