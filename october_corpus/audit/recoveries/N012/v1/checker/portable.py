"""Restore N012 exclusively from public payloads; replay its exact certificates.

Primary source reading remains in the frozen mathematical reviews. The public
checker verifies the declared hashes without reading a private source copy.
No retained program is patched and no private path is a runtime fallback.
"""
from pathlib import Path, PurePosixPath
import argparse
import copy
import difflib
import gzip
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

if sys.flags.optimize:
    raise RuntimeError('Validation does not support optimized Python')
BASE='audit/recoveries/N012/v1'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def child(root,name):
    p=PurePosixPath(name);need(name and not p.is_absolute() and '..'not in p.parts,'Unsafe path')
    q=(root/p).resolve();need(q.is_relative_to(root.resolve()),'Path escape');return q
def module(name,p):
    sp=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m

def main(a):
    need(not a.out.exists(),'Fresh output required')
    R=a.repo.resolve();P=(a.payload or a.repo).resolve();O=a.out.resolve()
    tp=child(P,BASE+'/transport.json');need(sha(tp)==a.expected_transport,'Changed transport')
    tr=load(tp);need(tr['logical_files']==len(tr['files']),'Complete logical inventory')
    O.mkdir(parents=True);S=O/'restored/study';C=O/'cache';S.mkdir(parents=True);C.mkdir()
    by_path={};decoded={};primary=[]
    for row in tr['files']:
        need(row['origin']=='study','Unknown namespace');name=row['path']
        need(name not in by_path,'Duplicate logical path');by_path[name]=row;dest=child(S,name)
        if row['transport']=='PRIVATE_PRIMARY_SOURCE_HASH_ONLY':primary.append(name);continue
        need(row['transport'] in ['EXISTING_PUBLIC','NEW_FROZEN_FILE'],'Unknown payload kind')
        key=(row['bytes'],row['sha256'])
        if key not in decoded:
            src=child(R if row['transport']=='EXISTING_PUBLIC' else P,row['public_path'])
            need(src.stat().st_size==row['stored_bytes'] and sha(src)==row['stored_sha256'],'Stored payload changed')
            need(row['encoding']in ['identity','gzip'],'Unknown encoding')
            dst=C/row['sha256'];opener=gzip.open if row['encoding']=='gzip'else open
            with opener(src,'rb')as inf,dst.open('wb')as outf:shutil.copyfileobj(inf,outf)
            need(dst.stat().st_size==row['bytes'] and sha(dst)==row['sha256'],'Decoded payload changed')
            decoded[key]=dst
        dest.parent.mkdir(parents=True,exist_ok=True);os.link(decoded[key],dest)
        need(not row['public_path'].endswith('.md'),'No new public Markdown evidence')
    need(set(primary)==set(tr['primary_sources_hash_only'])and len(primary)==49,'Exact primary-only exception set')
    author=S/'corpus106_N012_principal_v1';deps=load(author/'dependencies.json')
    additional={'reboot_20261013/N012_central_quotients_distinct/source_pages/page-69.png',
                'reboot_20261013/N012_central_quotients_distinct/source_pages/page-72.png'}
    need(set(primary)==set(deps['primary_files_hash_only'])|additional,'No omitted mathematical material')
    checked=0
    def verify_record(base,row):
        nonlocal checked
        q=child(base,row['path']);logical=str(q.relative_to(S));need(logical in by_path,'Absent transport route '+logical)
        r=by_path[logical];need(r['sha256']==row['sha256'] and r['bytes']==row.get('bytes',r['bytes']),'Logical record changed')
        if logical not in primary:need(q.is_file() and sha(q)==row['sha256']and q.stat().st_size==r['bytes'],'Restored file changed')
        else:need(not q.exists(),'Primary source unexpectedly restored')
        checked+=1
    expected=set(deps['acquired_packets'])|{'corpus106_N012_principal_v1/manifest.json','corpus106_N012_principal_root_review/manifest.json'}
    need({x['path']for x in tr['packets']}==expected and len(tr['packets'])==len(expected),'Complete acceptance chains')
    exports=0
    for row in tr['packets']:
        mp=child(S,row['path']);need(sha(mp)==row['sha256'],'Manifest changed');m=load(mp)
        need(len(m['exports'])==row['exports'],'Packet size')
        for x in m['exports']:verify_record(mp.parent,x);exports+=1
        dp=mp.parent/'dependencies.json'
        if dp.is_file():
            xs=load(dp).get('bindings',[])
            if isinstance(xs,list):
                for x in xs:verify_record(S,x)
    root_review=load(S/'corpus106_N012_principal_root_review/review.json')
    need(sha(S/'corpus106_N012_principal_root_review/manifest.json')=='ccddeeca1c116776789ec30e6edfe56618656bee9dfb92643ef82b3bbe359563','Exact whole mathematical acceptance')
    ac=module('n012_public_author_boundary',author/'check.py')
    scope=load(author/'scope.json');routes=load(author/'claim_routes.json');delta=load(author/'editorial_delta.json')
    ac.boundary(scope,routes,delta)
    for k in ['historical_ledger','closing_author','closing_review','closing_adoption']:verify_record(S,routes[k])
    before=child(S,delta['original']['path']).read_text();after=child(author,delta['copy']['path']).read_text()
    need(before.count(delta['old'])==1 and after==before.replace(delta['old'],delta['new']),'Exact editorial copy')
    diff=''.join(difflib.unified_diff(before.splitlines(keepends=True),after.splitlines(keepends=True),fromfile='corpus106_N012_finite_H_v2/finite_H.tex',tofile='corpus106_N012_principal_v1/finite_H_clarified.tex'))
    need((author/delta['delta_file']).read_text()==diff,'Exact editorial diff')
    controls=[]
    for name,fn in [
      ('wrong_quotient',lambda s,r,d:s.update(quotient_definition='H/Z(H)')),
      ('lost_principal_route',lambda s,r,d:r['rows'].pop()),
      ('uncorrected_centre',lambda s,r,d:s['centre_cases'].update(e_even='index-two extension')),
      ('q9_positive',lambda s,r,d:s['small_exceptions'].update(Q2='all q')),
      ('missing_closing_review',lambda s,r,d:r['closing_review'].update(sha256='0'*64)),
      ('wrong_subgroup_order',lambda s,r,d:d.update(dihedral_order='4p')),
      ('premature_admission',lambda s,r,d:s.update(whole_original_credit=1)),
      ('unmeasured_ratio',lambda s,r,d:s.update(compression_factor=12))]:
        s,r,d=copy.deepcopy((scope,routes,delta));fn(s,r,d)
        try:ac.boundary(s,r,d)
        except(ValueError,KeyError):controls.append(name)
        else:raise ValueError('Malformed boundary accepted '+name)
    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
    def run(name,cmd,cwd):
        out=O/(name+'.stdout');err=O/(name+'.stderr')
        with out.open('wb')as f,err.open('wb')as e:
            r=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=e,timeout=120)
        need(r.returncode==0 and not err.read_bytes(),'Certificate execution failed '+name)
        return out
    # The original integral checker needs no source path unless --study-root
    # is supplied. Its exports, scope and arithmetic are all present locally.
    I=S/'corpus106_N012_integral_v1';ir=O/'integral_replay'
    run('integral',[sys.executable,str(I/'check.py'),'--out',str(ir)],I)
    integral=load(ir/'report.json');need(integral['status']=='PASS'and integral['displayed_matrix_and_orbit_records']==57,'Complete integral certificate')
    # The polynomial script writes its own report: use a byte-identical
    # working copy, keeping every restored frozen input read-only.
    H=S/'corpus106_N012_finite_H_v2';hw=O/'finite_H_words';hw.mkdir()
    shutil.copyfile(H/'check_finite_H_words.py',hw/'check_finite_H_words.py')
    need(sha(hw/'check_finite_H_words.py')==sha(H/'check_finite_H_words.py'),'Exact runnable copy')
    run('finite_H_words',[sys.executable,str(hw/'check_finite_H_words.py')],hw)
    words=load(hw/'finite_H_words_report.json');need(words==load(H/'finite_H_words_report.json'),'Complete polynomial output')
    need(len(words['identities'])==42,'All polynomial identities')
    prime=load(run('prime_word',[sys.executable,str(H/'check_h6_prime_word.py')],H))
    need(prime['status']=='PASS'and prime['word_length']==131 and prime['damaged_controls']==3,'Exact prime word')
    # Ensure no run changed any restored mathematical input.
    for name,row in by_path.items():
        if name not in primary:
            q=child(S,name);need(q.stat().st_size==row['bytes']and sha(q)==row['sha256'],'Runtime input changed')
    report=dict(status='PASS_PUBLIC_N012_RESTORATION_AND_CERTIFICATES',transport_sha256=sha(tp),
      logical_records=len(by_path),restored_files=len(by_path)-len(primary),distinct_payloads=len(decoded),
      acquired_packets=len(tr['packets']),acquired_exports=exports,verified_binding_records=checked,
      primary_hash_only=primary,principal_claims=12,table_rows=12,exact_editorial_diff=True,
      integral=integral,finite_H_polynomial_identities=42,prime_word=prime,scope_controls=controls,
      private_runtime_fallback=False,retained_programs_patched=False,source_content_reread=False,
      new_native_page_review=False,long_searches_repeated=False,whole_original_credit=0)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in ['primary_hash_only','integral','scope_controls']}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--payload',type=Path)
    p.add_argument('--expected-transport',required=True);p.add_argument('--out',type=Path,required=True);main(p.parse_args())
