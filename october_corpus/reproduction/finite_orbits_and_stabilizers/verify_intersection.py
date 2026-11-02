"""Portable two-end-word matrix-intersection counterexample; no historical authority IO."""
import argparse,os,sys
from pathlib import Path
import runtime as rt
import field,algebra,end_words
ROOT=Path(__file__).resolve().parent
CORE={'runtime.py','field.py','algebra.py','end_words.py','verify_intersection.py'}
EXTRA={'case':set(),'arithmetic':{'intersection_controls.py'},'admission':{'intersection_admission.py'}}
MANIFEST={'case':'INTERSECTION_SOURCE_MANIFEST.json','arithmetic':'INTERSECTION_CONTROL_SOURCE_MANIFEST.json','admission':'INTERSECTION_ADMISSION_SOURCE_MANIFEST.json'}
GUARDS={'supervise_validation.py':(4806,'c3b626b86791ac355c3503a654136f49ad76abbcdfadf0455efb32dd5cca25f4'),'supervise_transient.py':(18361,'5c7eed80537835e1a78c8489621d34741eeafc01f47fb394fec519e83f2c9b42')}
def relative(name):
    rt.need(type(name)is str and name and not Path(name).is_absolute()and all(x not in('..','.')for x in Path(name).parts),'relative package path')
    p=ROOT/name;rt.need(p.resolve(strict=False).is_relative_to(ROOT),'path inside package');return p
def case_path(name):
    p=Path(name)
    if not p.is_absolute():p=ROOT/p
    rt.need(p.resolve(strict=True).is_relative_to(ROOT),'explicit case inside package');return p
def header(d):
    keys={'schema','original_job','position','original_row_id','marks','LEFT_word','RIGHT_word','RIGHT_positive_power','expected_middle_order','provenance','external_premises'}
    rt.need(type(d)is dict and set(d)==keys and d['schema']=='F004_PORTABLE_TWO_END_WORD_INTERSECTION_CASE_V1','case schema')
    rt.need(d['original_job']==[20,4]and type(d['position'])is int and 0<=d['position']<3779 and type(d['original_row_id'])is str and 1<=len(d['original_row_id'])<=160,'bounded descriptive subject')
    # Full matrix, string involution, word, power and complete-middle checks
    # are delegated to the same end_words.verify used by the controls.
    rt.need(type(d['expected_middle_order'])is int and 4<=d['expected_middle_order']<=512,'bounded expected middle scalar')
    p=d['provenance'];rt.need(type(p)is dict and len(p)<=16 and all(type(k)is str and len(k)<=64 and type(v)is str and len(v)==64 and set(v)<=set('0123456789abcdef')for k,v in p.items()),'hash provenance')
    rt.need(type(d['external_premises'])is str and len(d['external_premises'])<=4096,'external provenance text');return d
def decode_case(raw,sha,b):
    rt.need(type(raw)is bytes and len(raw)<=131072 and rt.digest(raw)==sha,'case size/SHA');b.scalar(len(raw));return header(rt.decode(raw))
def origin(module,name):
    rt.need(Path(module.__file__).resolve()==ROOT/name,'whole loaded module origin')
    for v in vars(module).values():
        if type(v).__name__=='function'and v.__module__==module.__name__:rt.need(v.__globals__ is vars(module)and Path(v.__code__.co_filename).resolve()==ROOT/name,'function origin')
        if isinstance(v,type)and v.__module__==module.__name__:
            for f in vars(v).values():
                if type(f).__name__=='function':rt.need(f.__globals__ is vars(module)and Path(f.__code__.co_filename).resolve()==ROOT/name,'method origin')
def start(argv,mode='case'):
    rt.need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize and not any(x in os.environ for x in rt.ENV4),'EBS/ENV4')
    ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--manifest',nargs=2,required=True);ap.add_argument('--case',nargs=2);ap.add_argument('--output',required=True);a=ap.parse_args(argv[1:])
    b=rt.Budget();mp=Path(a.manifest[0]);rt.need(mp.resolve(strict=True)==ROOT/MANIFEST[mode]and not(ROOT/'__pycache__').exists(),'manifest/clean namespace')
    raw=b.read(mp,cap=65536);rt.need(rt.digest(raw)==a.manifest[1],'exact Source manifest');m=rt.decode(raw)
    rt.need(set(m)=={'schema','caps','role','sources','guards'}and m['schema']=='F004_PORTABLE_TWO_END_WORDS_SOURCE_V1'and m['caps']==rt.CAPS and m['role']==mode,'exact portable role namespace')
    names=CORE|EXTRA[mode];rt.need(len(m['sources'])==len(names)and{r['path']for r in m['sources']}==names,'whole active Sources')
    total=0
    for r in m['sources']:rt.need(Path(r['path']).name==r['path'],'same-directory Source');total+=len(b.read(ROOT/r['path'],r))
    rt.need(len(m['guards'])==2 and{Path(r['path']).name for r in m['guards']}==set(GUARDS),'two unchanged guards')
    for r in m['guards']:
        n=Path(r['path']).name;rt.need((r['bytes'],r['sha256'])==GUARDS[n]and r['path']=='../fixed_line_orbits/runtime/'+n,'relative whole guard pins');b.read(ROOT/r['path'],r)
    rt.need(total+23167+512<=65536,'whole Source cap');reserved=total+59889+512;rt.need(b.read_bytes+reserved<=8388608,'shared bootstrap read bank');b.read_bytes+=reserved;b.import_source_reserved_bytes=reserved
    for mod in(rt,field,algebra,end_words,sys.modules[__name__]):origin(mod,Path(mod.__file__).name)
    pins=dict(Source_manifest_sha256=a.manifest[1],worker_Source_bytes=total,guard_Source_bytes=23167,entry_reserve=512)
    if mode!='case':rt.need(a.case is None,'Original-free control role');return b,a,pins
    rt.need(a.case is not None,'one explicit supplied bundle');cp=case_path(a.case[0])
    return b,a,pins,decode_case(b.read(cp,cap=131072),a.case[1],b)
def close(b):
    for r in list(b.reads):b.read(r['path'],r)
def emit(out,result,proof,b):
    p=Path(out);rt.need(p.is_absolute()and not os.path.lexists(p)and p.parent.resolve(strict=True)==p.parent,'fresh canonical output')
    bodies=[rt.encoded(result),rt.encoded(proof)];rt.need(all(len(v)<=131072 for v in bodies)and len(b.paths|{str(p/'result.json'),str(p/'proof.json')})<=96,'output bytes/paths');b.tick();p.mkdir();refs=[]
    for name,body in zip(('result.json','proof.json'),bodies):
        with(p/name).open('xb')as f:rt.need(f.write(body)==len(body),'whole output');f.flush();os.fsync(f.fileno())
        refs.append(dict(path=str(p/name),bytes=len(body),sha256=rt.digest(body)))
    return refs
def verify_case(d,b):
    verdict=end_words.verify(d['marks'],d['LEFT_word'],d['RIGHT_word'],d['RIGHT_positive_power'],b)
    rt.need(verdict['middle_order']==d['expected_middle_order'],'fresh complete middle matches expected scalar')
    return verdict
def main(argv):
    b,a,pins,d=start(argv);verdict=verify_case(d,b);close(b)
    result=dict(original_job=d['original_job'],position=d['position'],original_row_id=d['original_row_id'],**verdict)
    proof=dict(Source=pins,marks_sha256=rt.digest(rt.encoded(d['marks'])),LEFT_word_sha256=rt.digest(rt.encoded(d['LEFT_word'])),RIGHT_word_sha256=rt.digest(rt.encoded(d['RIGHT_word'])),provenance=d['provenance'],external_premises=d['external_premises'],counts=b.snapshot(),old_H_carrier_opened=False,old_SGS_or_discovery_or_R_word_search_replayed=False)
    outputs=emit(a.output,result,proof,b);sys.stdout.buffer.write(rt.encoded(dict(status=result['status'],position=d['position'],outputs=outputs)))
if __name__=='__main__':main(sys.argv)
