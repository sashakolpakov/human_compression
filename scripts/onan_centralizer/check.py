"""Public-only I/O facade for exact retained ON centralizer check bodies.

No private-data fallback. The named model and inner centralizer order are
borrowed premises; this entrypoint supplies no complete L026 or45D claim.
"""
import argparse
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import resource
import stat
import sys
import time
import types

ROOT=Path(__file__).resolve().parents[2]
MANIFEST='data/onan_centralizer/manifest.json'
MANIFEST_SHA='788e353f24676a2676ae4314fa5e3e9b89de4278dc7831d635b93087b7455bb9'
START=time.monotonic()
MODES=('standard-controls','standard-pair','pair-controls','check-centralizer')


def need(ok,why):
    if not ok:raise ValueError(why)
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak=peak if sys.platform=='darwin'else peak*1024
    if time.monotonic()-START>=30 or peak>=128*2**20:
        raise RuntimeError('portable30s/128MiB budget')


def relative(name):
    p=PurePosixPath(name)
    need(type(name)is str and not p.is_absolute()and str(p)==name
         and '..'not in p.parts and '\0'not in name and '\n'not in name,
         'canonical repository-relative path')
    return ROOT/name


def source_bytes(name,expected=None,cap=65536):
    p=relative(name);a=p.lstat()
    need(p.resolve(strict=True)==p and all(not x.is_symlink()for x in(p,*p.parents))
         and stat.S_ISREG(a.st_mode)and a.st_nlink==1 and a.st_size<=cap,
         'ordinary bounded public Source/manifest')
    signature=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    with p.open('rb')as f:
        b=os.fstat(f.fileno());raw=f.read(cap+1);z=os.fstat(f.fileno())
    need(signature(a)==signature(b)==signature(z)==signature(p.lstat())
         and len(raw)==a.st_size<=cap,'stable entire public Source/manifest')
    q=dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    if expected is not None:need(q==expected,'exact declared public Source bytes')
    return raw,q


def module_from_source(name,raw,path):
    module=types.ModuleType(name)
    module.__file__=str(path)
    exec(compile(raw,str(path),'exec',dont_inherit=True),module.__dict__)
    return module


def bind(manifest):
    need(manifest['schema']=='ONAN_CENTRALIZER_PORTABLE_INPUT_MANIFEST_V1'
         and manifest['degree']==245520 and manifest['goal']==161280
         and manifest['seed']==[0,1],'fixed full-degree centralizer certificate manifest')
    standard_ref=manifest['programs']['standard']
    pair_ref=manifest['programs']['pair']
    need(standard_ref['path']=='scripts/onan_centralizer/check_standard_pair.py'
         and standard_ref['sha256']=='acc28b910d81fe4c67b065f8da76cec5e62683d24a50729d70dab98b1546065c'
         and pair_ref['path']=='scripts/onan_centralizer/check_centralizer_pair_orbit.py'
         and pair_ref['sha256']=='2dfcf3f91d69c2652109023ccd542ee7040cb2bcc1cfd5cdeace0632f70083b2',
         'two exact unchanged retained complete Source bodies')
    standard_raw,_=source_bytes(standard_ref['path'],standard_ref)
    pair_raw,_=source_bytes(pair_ref['path'],pair_ref)
    standard=module_from_source('public_on_standard_body',standard_raw,relative(standard_ref['path']))
    pair=module_from_source('public_on_pair_body',pair_raw,relative(pair_ref['path']))
    # Only these explicit I/O bindings change. All scientific function bodies
    # and both complete main bodies are the exact authenticated originals.
    standard.S=ROOT
    standard.FILES=[(relative(manifest['models'][key]['path']),manifest['models'][key]['sha256'])
                    for key in('c','d')]
    def public_helper():
        return standard
    pair.helper=public_helper
    need(standard.N==245520 and pair.GOAL==161280 and pair.RECORD.size==5
         and pair.SOURCE==relative(standard_ref['path'])
         and pair.SOURCE_SHA==standard_ref['sha256']and pair.helper is public_helper,
         'explicit repo-only helper facade; no inherited private resolver called')
    return standard,pair


def fresh_output(path):
    need(path.is_absolute()and path.parent.resolve(strict=True)==path.parent
         and not os.path.lexists(path)and not path.is_relative_to(ROOT),
         'fresh external absolute output with existing ordinary parent')


def invoke(mode,out,manifest,standard,pair):
    fresh_output(out)
    if mode.startswith('standard-'):
        out.mkdir()
        module=standard
        argv=[standard.__file__,'--mode','controls'if mode=='standard-controls'else'check',
              '--output',str(out/'result.json')]
    else:
        module=pair
        argv=[pair.__file__,'--mode','controls'if mode=='pair-controls'else'check','--out',str(out)]
        if mode=='check-centralizer':
            argv+=['--seed',str(manifest['seed'][0]),str(manifest['seed'][1]),
                   '--certificate',str(relative(manifest['tree']['path'])),
                   '--certificate-sha256',manifest['tree']['sha256']]
    if mode in('standard-pair','check-centralizer'):
        data=[manifest['models']['c'],manifest['models']['d']]
        if mode=='check-centralizer':data.append(manifest['tree'])
        for q in data:
            p=relative(q['path'])
            need(p.resolve(strict=True)==p and p.lstat().st_size==q['bytes'],
                 'exact declared repository-local payload size before original full hashing')
    old_argv=sys.argv
    captured=io.StringIO()
    try:
        sys.argv=argv
        with contextlib.redirect_stdout(captured):
            module.main()
    finally:
        sys.argv=old_argv
    text=captured.getvalue()
    need(len(text.encode())<=4096,'bounded original returned stdout')
    reported=json.loads(text)
    result_path=out/'result.json'
    a=result_path.lstat();raw=result_path.read_bytes()
    need(a==result_path.lstat()and stat.S_ISREG(a.st_mode)and a.st_nlink==1
         and len(raw)==a.st_size<=1024**2,'stable bounded original result metadata')
    result=json.loads(raw)
    expected={
      'standard-controls':'PASS_FOCUSED_LITERAL_PERMUTATION_CONTROLS',
      'standard-pair':'VERIFIED_CACHED_ON_STANDARD_PAIR_WORD_ORDERS',
      'pair-controls':'PASS_FOCUSED_CENTRALIZER_PAIR_ORBIT_CONTROLS',
      'check-centralizer':'VERIFIED_REACHABLE_CENTRALIZER_PAIR_TREE'}[mode]
    ref=dict(path=str(result_path),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
    need(result['status']==reported['status']==expected,'exact returned original route status')
    need(reported.get('output',reported.get('result'))==ref,'original stdout binds exact result bytes')
    if mode=='standard-controls':need(result['count']==9,'all nine original standard controls')
    if mode=='pair-controls':need(result['count']==13,'all thirteen original pair controls')
    if mode=='standard-pair':
        need(result['degree']==245520 and result['named_group_identification_reproved']is False,
             'original standard-pair qualification retained')
    if mode=='check-centralizer':
        need(result['degree']==245520 and result['seed']==manifest['seed']
             and result['reached_pairs']==161280 and result['verified_edges']==161279
             and result['centralizer_upper_bound_borrowed']==161280
             and result['named_model_reproved']is False,'full saved pair tree independently reconstructed')
    return dict(mode=mode,status=expected,result=ref,original_stdout=text,
                source_body_program=manifest['programs']['standard'if mode.startswith('standard-')else'pair'])


def main():
    ap=argparse.ArgumentParser(allow_abbrev=False,description=__doc__)
    ap.add_argument('--mode',choices=['all',*MODES],default='all')
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,
         'ordinary isolated -E -B Python')
    fresh_output(args.out)
    raw,manifest_ref=source_bytes(MANIFEST)
    need(manifest_ref['sha256']==MANIFEST_SHA,'fixed reviewed portable manifest')
    manifest=json.loads(raw)
    standard,pair=bind(manifest)
    modes=MODES if args.mode=='all'else(args.mode,)
    if args.mode=='all':args.out.mkdir()
    results=[invoke(mode,args.out/mode if args.mode=='all'else args.out,
                    manifest,standard,pair)for mode in modes]
    need(source_bytes(MANIFEST)[1]==manifest_ref,'unchanged whole manifest after selected replay')
    for q in manifest['programs'].values():source_bytes(q['path'],q)
    own_path=Path(__file__).resolve()
    own_raw,own_ref=source_bytes(str(own_path.relative_to(ROOT)))
    report=dict(schema='ONAN_CENTRALIZER_PUBLIC_ONLY_REPLAY_V1',
        status='PASS_SELECTED_ONAN_CENTRALIZER_PORTABLE_REPLAY',mode=args.mode,
        execution_program=own_ref,manifest=manifest_ref,selected_results=results,
        original_source_bodies_unchanged=True,
        io_transport=['standard.S=repository_root','standard.FILES=manifest_relative_model_pins',
                      'pair.helper=the_same_exact_public_standard_module','sys.argv=explicit_original_main_argv'],
        private_fallback=False,named_model_reidentified=False,centralizer_upper_bound_reproved=False,
        matrix45D_homomorphism_proved=False,L026_complete=False,census_credit=0,
        conjecture_credit=0,whole_original_credit=0,
        seconds=time.monotonic()-START,limits=dict(seconds=30,rss_bytes=128*2**20),
        qualification='Exact original standard-library bodies with declared repository-local I/O only. Full named ATLAS model and inner centralizer-order161280 classification remain borrowed. This selected replay does not identify a45D cover or complete the ON/Fi22 census or L026.')
    encoded=(json.dumps(report,sort_keys=True,indent=2)+'\n').encode()
    need(len(encoded)<=65536,'bounded portable receipt')
    p=args.out/'portable_receipt.json'
    with p.open('xb')as f:
        need(f.write(encoded)==len(encoded),'whole fresh portable receipt')
        f.flush();os.fsync(f.fileno())
    print(json.dumps(dict(status=report['status'],mode=args.mode,
        receipt=dict(path=str(p),bytes=len(encoded),sha256=hashlib.sha256(encoded).hexdigest()),
        private_fallback=False,whole_original_credit=0)))


if __name__=='__main__':main()
