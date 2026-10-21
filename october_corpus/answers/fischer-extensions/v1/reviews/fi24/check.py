#!/usr/bin/env python3
"""Replay the distinct Fi24 review; full finite replay is opt-in."""
from pathlib import Path, PurePosixPath
import argparse, copy, hashlib, json, re, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parent
AUTHOR = '25da81ab175f8ea8ceedec22c4434780705910097ee45f5b4509db0573a68007'
PRIMARY = 'a0c307e0a41eeb8b190de4cb0b4af331973866993c55ee4f0fcb66b932c6db61'
MARKER = 'INDEPENDENT_FI24_LITERAL_COSETS PASS 98properIP 6all-flag-families 30full-subset-identities'

def need(ok, message):
    if not ok: raise RuntimeError(message)

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def load(path): return json.loads(path.read_text())

def bound(root, expected=None):
    mf = root/'manifest.json'
    if expected is not None: need(sha(mf) == expected, 'manifest differs')
    rows = load(mf)['exports']; seen = set()
    for row in rows:
        rel = PurePosixPath(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts and str(rel) not in seen, 'unsafe export')
        seen.add(str(rel))
        need(not any((root/Path(*rel.parts[:i])).is_symlink() for i in range(1,len(rel.parts)+1)), 'export symlink')
        p = root/rel
        need(p.is_file() and p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], 'export differs: '+str(rel))
    return len(rows)

def audit_words(path):
    text = path.read_text(encoding='ascii'); pos = 0; data = {}
    pattern = re.compile(r'\s*(F24[A-Za-z0-9]+)\s*:=\s*([\[\]\s,0-9-]+);')
    while pos < len(text) and text[pos:].strip():
        match = pattern.match(text,pos)
        need(match is not None, 'nonliteral witness syntax')
        key = match.group(1); need(key not in data, 'duplicate witness assignment')
        data[key] = json.loads(match.group(2)); pos = match.end()
    need(set(data) == {'F24aWord','F24aPower','F24BraySeeds','F24bFactors','F24bPower','F24Prime23','F24Prime29','F24Type'}, 'witness variable set')
    def word(w,n,length):
        need(isinstance(w,list) and len(w)==length and all(type(i) is int and 0<abs(i)<=n for i in w), 'invalid signed word')
    word(data['F24aWord'],2,50)
    need(len(data['F24BraySeeds'])==8, 'seed count')
    for w in data['F24BraySeeds']: word(w,2,40)
    word(data['F24bFactors'],8,10)
    need(all(i>0 for i in data['F24bFactors']), 'negative b factor')
    word(data['F24Prime23'][0],3,80); word(data['F24Prime29'][0],3,114)
    need([data['F24aPower'],data['F24bPower'],data['F24Prime23'][1],data['F24Prime29'][1],data['F24Type']]==[21,12,2,1,[6,35]], 'scalar data')
    return {'literal_assignments':len(data),'a_length':50,'seed_lengths':[40]*8,'b_factors':data['F24bFactors'],'prime_word_lengths':[80,114],'sha256':sha(path),'bytes':path.stat().st_size}

def scope_check(scope):
    need(scope['group']=='Fi24prime:2' and scope['source_id']=='N006', 'wrong group/source')
    need(scope['finite_counts']=={'proper_IP_pairs_per_marking':49,'elementary_full_subset_pairs_per_marking':15,'flag_equations_per_marking':3,'string_product_tests':1168,'triangle_product_tests':1824,'total_product_tests':2992}, 'finite scope')
    need(scope['maximal_classification_complete_retained'] is True and scope['external_classification_proof_cost'] is None, 'classification scope')
    need(scope['full_group_order_enumerated'] is False and scope['lean_declarations']==0 and scope['proof_kernel_checked'] is False, 'computational/formal scope')
    need(scope['priority_claim'] is False and scope['source_count_change']==0 and scope['question_credit_change']==0, 'unreviewed credit')
    need(scope['external_data_bytes']==4425390, 'external data')
    need([r['path'] for r in scope['program_roles']]==['programs/local_geometry.g','programs/verify.g','witnesses/F24_compact.g','check.py'], 'whole-program scope')

def command(args,cwd,log,marker=None):
    p = subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
    log.write_bytes(p.stdout); text=p.stdout.decode(errors='replace').replace('\\\n','')
    need(p.returncode==0 and 'Error,' not in text and 'Syntax error:' not in text, 'failed command: '+log.name)
    if marker: need(marker in text, 'missing marker')
    return {'path':log.name,'sha256':sha(log),'returncode':p.returncode}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet-root',type=Path,required=True)
    ap.add_argument('--atlas-root',type=Path);ap.add_argument('--primary',type=Path)
    ap.add_argument('--programs',action='store_true');ap.add_argument('--gap',default='gap')
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(), 'existing output')
    own=bound(ROOT) if (ROOT/'manifest.json').exists() else None
    count=bound(a.packet_root,AUTHOR);scope=load(a.packet_root/'scope.json');scope_check(scope)
    words=audit_words(a.packet_root/'witnesses/F24_compact.g')
    if (ROOT/'data_audit.json').exists(): need(words==load(ROOT/'data_audit.json'), 'word audit differs')
    if a.primary: need(sha(a.primary)==PRIMARY, 'source edition differs')
    retained=load(a.packet_root/'retained_inputs.json')
    orders=[row['order'] for row in retained['complete_maximal_subgroups']]
    need(len(orders)==21 and [i for i,n in enumerate(orders) if n%(23*29)==0]==[0], 'maximal divisibility')
    need(orders[0]==1255205709190661721292800, 'socle order')
    live=load(ROOT/'fresh_author/report.json')
    need(live['status']=='PASS' and live['named_group_and_maximal_classification_retained'] is True and live['lean_verified'] is False, 'fresh author evidence')
    need(len(live['controls'])==16 and all(r['rejected'] for r in live['controls']), 'author controls')
    need(sha(ROOT/'fresh_author'/live['finite_replay']['log'])==live['finite_replay']['sha256'], 'finite log binding')
    literal=(ROOT/'independent_literal.log').read_text().replace('\\\n','')
    need(MARKER in literal and '[ 35, 35, 70 ]' in literal and 'Error,' not in literal, 'independent literal evidence')
    mutations={'flags_missing':('finite_counts',dict(scope['finite_counts'],flag_equations_per_marking=0)),
               'classification_reproved':('maximal_classification_complete_retained',False),
               'unknown_cost_zero':('external_classification_proof_cost',0),
               'ambient_enumeration_claim':('full_group_order_enumerated',True),
               'Lean_claim':('lean_declarations',1),'priority_claim':('priority_claim',True),
               'wrong_group':('group','Fi24prime'),'pruned_program':('program_roles',scope['program_roles'][1:])}
    controls=[]
    for name,(key,value) in mutations.items():
        bad=copy.deepcopy(scope);bad[key]=value
        try: scope_check(bad)
        except (RuntimeError,KeyError): controls.append({'name':name,'rejected':True})
        else: raise RuntimeError('accepted invalid scope: '+name)
    out=a.out.resolve();out.mkdir(parents=True);replay={}
    if a.programs:
        need(a.atlas_root is not None, 'atlas-root required for finite replay')
        stage=out/'author';stage.mkdir()
        for row in load(a.packet_root/'manifest.json')['exports']:
            dst=stage/row['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a.packet_root/row['path'],dst)
        shutil.copyfile(a.packet_root/'manifest.json',stage/'manifest.json')
        replay['author']=command([sys.executable,'-B','-O',str(stage/'check.py'),'--atlas-root',str(a.atlas_root.resolve()),'--gap',a.gap,'--out',str(out/'author_replay')],out,out/'author.log')
        literal_stage=out/'literal';literal_stage.mkdir()
        for row in retained['permutation_files']:
            src=a.atlas_root/row['filename'];need(sha(src)==row['sha256'],'external permutation differs')
            shutil.copyfile(src,literal_stage/row['filename'])
        shutil.copyfile(stage/'witnesses/F24_compact.g',literal_stage/'F24_compact.g')
        replay['literal']=command([a.gap,'-q','-T','-m','256m','-o','4g',str(ROOT/'literal_cosets.g')],literal_stage,out/'literal.log',MARKER)
    report={'status':'PASS','author_manifest_sha256':AUTHOR,'author_exports':count,'review_exports':own,
            'primary_checked':a.primary is not None,'literal_word_audit':words,'scope_controls':controls,
            'fresh_replay':replay,'proper_IP_pairs':98,'elementary_full_subset_pairs':30,'anchored_flag_families':6,
            'retained_named_group_and_maximal_classification':True,'Lean_declarations':0,'priority_claim':False,
            'new_source_credit':0,'new_question_credit':0,'new_formal_credit':0}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':
    try:main()
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
