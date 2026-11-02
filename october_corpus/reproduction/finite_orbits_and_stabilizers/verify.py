"""Portable supplied-certificate checker. No Original or named-group discovery."""
import argparse,os,sys
from pathlib import Path
import runtime as rt
import field,algebra,solve,schreier
ROOT=Path(__file__).resolve().parent
BASE_NAMES={'runtime.py','field.py','algebra.py','solve.py','schreier.py','verify.py'}
GUARDS={'supervise_validation.py':(4806,'c3b626b86791ac355c3503a654136f49ad76abbcdfadf0455efb32dd5cca25f4'),'supervise_transient.py':(18361,'5c7eed80537835e1a78c8489621d34741eeafc01f47fb394fec519e83f2c9b42')}
def relative(name):
    rt.need(type(name)is str and name and not Path(name).is_absolute()and all(x not in('..','.')for x in Path(name).parts),'relative package path')
    p=ROOT/name;rt.need(p.resolve(strict=False).is_relative_to(ROOT),'path inside package');return p
def header(d):
    rt.need(type(d)is dict and set(d)=={'schema','original_job','position','original_row_id','marks','word','cofactor','end_labels','carrier','expected','provenance','external_premises'},'complete portable case')
    rt.need(d['schema']=='F004_FINITE_ORBIT_CASE_V1'and d['original_job']==[20,4]and type(d['position'])is int and 1<=d['position']<=3779 and type(d['original_row_id'])is str and 1<=len(d['original_row_id'])<=160,'original subject metadata')
    labels=d['end_labels'];rt.need(type(labels)is list and all(type(i)is int for i in labels)and labels in([0,1,2],[1,2,3]),'literal LEFT or RIGHT labels')
    rt.need(type(d['word'])is list and 1<=len(d['word'])<=32 and all(type(i)is int and i in labels for i in d['word'])and type(d['cofactor'])is int and d['cofactor']in(1,7),'bounded word and cofactor')
    r=rt.ref(d['carrier']);relative(r['path']);rt.need(19<=r['bytes']<=121315,'whole bounded binary carrier')
    e=d['expected'];rt.need(type(e)is dict and set(e)=={'orbit_size','stabilizer_size','exact_end_order','omitted_mark_in_certified_end','fixed_space_dimension'},'expected matrix facts')
    rt.need(all(type(e[k])is int for k in('orbit_size','stabilizer_size','exact_end_order','fixed_space_dimension'))and 1<=e['orbit_size']<=10000 and 1<=e['stabilizer_size']<=128 and e['exact_end_order']==e['orbit_size']*e['stabilizer_size']and 0<=e['fixed_space_dimension']<=7 and type(e['omitted_mark_in_certified_end'])is bool,'typed expected scalar facts')
    rt.need(type(d['provenance'])is dict and all(type(k)is str and type(v)is str and len(v)==64 and set(v)<=set('0123456789abcdef')for k,v in d['provenance'].items()),'path-free hash provenance')
    rt.need(type(d['external_premises'])is str and len(d['external_premises'])<=4096,'explicit unproved model/cover premises');return d
def origin(module,name):
    rt.need(Path(module.__file__).resolve()==ROOT/name,'whole loaded module origin')
    for v in vars(module).values():
        if type(v).__name__=='function'and v.__module__==module.__name__:rt.need(v.__globals__ is vars(module)and Path(v.__code__.co_filename).resolve()==ROOT/name,'actual function body/globals')
        if isinstance(v,type)and v.__module__==module.__name__:
            for f in vars(v).values():
                if type(f).__name__=='function':rt.need(f.__globals__ is vars(module)and Path(f.__code__.co_filename).resolve()==ROOT/name,'actual class method origin')
def start(argv,controls=False):
    rt.need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize and not any(x in os.environ for x in rt.ENV4),'EBS/ENV4')
    ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--manifest',nargs=2,required=True);ap.add_argument('--case',nargs=2);ap.add_argument('--output',required=True);a=ap.parse_args(argv[1:])
    b=rt.Budget();mp=Path(a.manifest[0]);rt.need(mp.resolve(strict=True)==ROOT/('CONTROL_SOURCE_MANIFEST.json'if controls else'SOURCE_MANIFEST.json'),'selected relative source manifest')
    raw=b.read(mp,cap=65536);rt.need(rt.digest(raw)==a.manifest[1],'exact Source manifest');mf=rt.decode(raw)
    rt.need(mf['schema']=='F004_FINITE_ORBIT_PORTABLE_SOURCE_V1'and mf['caps']==rt.CAPS and mf['role']==('controls'if controls else'case')and set(mf)=={'schema','caps','role','sources','guards'},'closed portable namespace')
    names=BASE_NAMES|({'controls.py'}if controls else set());rt.need(len(mf['sources'])==len(names)and{r['path']for r in mf['sources']}==names,'all loaded whole Source bodies')
    total=0
    for r in mf['sources']:rt.need(Path(r['path']).name==r['path'],'same-directory Source');total+=len(b.read(ROOT/r['path'],r))
    rt.need(len(mf['guards'])==2 and{Path(r['path']).name for r in mf['guards']}==set(GUARDS),'two exact shared guards')
    for r in mf['guards']:
        name=Path(r['path']).name;rt.need((r['bytes'],r['sha256'])==GUARDS[name]and r['path']=='../fixed_line_orbits/runtime/'+name,'literal shared guard path/hash');b.read(ROOT/r['path'],r)
    rt.need(total+23167+512<=65536,'complete Source plus entry reserve');reserved=total+59889+512;rt.need(b.read_bytes+reserved<=8388608,'same8MiB bootstrap bank');b.read_bytes+=reserved;b.import_source_reserved_bytes=reserved
    for module,name in[(rt,'runtime.py'),(field,'field.py'),(algebra,'algebra.py'),(solve,'solve.py'),(schreier,'schreier.py'),(sys.modules[__name__],'verify.py')]:origin(module,name)
    pins=dict(Source_manifest_sha256=a.manifest[1],worker_Source_bytes=total,guard_Source_bytes=23167,entry_reserve=512)
    if controls:rt.need(a.case is None,'controls carry no Original case');return b,a,pins
    rt.need(a.case is not None,'one supplied case');p=Path(a.case[0]);rt.need(p.resolve(strict=True).is_relative_to(ROOT),'case remains in package');data=b.read(p,cap=65536);rt.need(rt.digest(data)==a.case[1],'whole case identity');d=header(rt.decode(data));return b,a,pins,d
def close(b):
    for r in list(b.reads):b.read(r['path'],r)
def emit(out,result,proof,b):
    p=Path(out);rt.need(p.is_absolute()and not os.path.lexists(p)and p.parent.resolve(strict=True)==p.parent,'fresh output under existing canonical parent')
    bodies=[rt.encoded(result),rt.encoded(proof)];rt.need(all(len(v)<=131072 for v in bodies)and len(b.paths|{str(p/'result.json'),str(p/'proof.json')})<=96,'same two128KiB outputs and96paths');b.tick();p.mkdir();refs=[]
    for name,body in zip(('result.json','proof.json'),bodies):
        with(p/name).open('xb')as f:rt.need(f.write(body)==len(body),'whole exclusive output');f.flush();os.fsync(f.fileno())
        refs.append(dict(path=str(p/name),bytes=len(body),sha256=rt.digest(body)))
    return refs
def main(argv):
    b,a,pins,d=start(argv);g=algebra.marking(d['marks'],b);labels=d['end_labels'];r=d['carrier'];raw=b.read(relative(r['path']),r,121315)
    facts,seed=schreier.check(tuple(g[i]for i in labels),raw,b,g[3 if labels==[0,1,2]else 0]);Y=schreier.prime_value(g,d['word'],d['cofactor'],labels,b)
    rt.need(b.image(seed,Y)==seed and facts['exact_end_order']%19==0,'fresh prime19 fixes seed/order');facts.update(prime19_exact=True,fixed_space_dimension=len(schreier.fixed_basis(Y,b)))
    rt.need(all(facts[k]==v for k,v in d['expected'].items()),'fresh strict facts equal supplied expectations');close(b)
    result=dict(status='VERIFIED_FINITE_ORBIT_AND_SMALL_STABILIZER_MATRIX_FACTS',original_job=d['original_job'],position=d['position'],facts=facts,named_model_or_classification_verified=False,rank4_IP_proved=False,new_case_or_census_credit=0)
    proof=dict(result,Source=pins,carrier_sha256=r['sha256'],Original_marks_sha256=rt.digest(rt.encoded(d['marks'])),word_and_end_sha256=rt.digest(rt.encoded(dict(word=d['word'],cofactor=d['cofactor'],end_labels=labels))),provenance=d['provenance'],external_premises=d['external_premises'],counts=b.snapshot())
    refs=emit(a.output,result,proof,b);sys.stdout.buffer.write(rt.encoded(dict(status=result['status'],position=d['position'],outputs=refs)))
if __name__=='__main__':main(sys.argv)
