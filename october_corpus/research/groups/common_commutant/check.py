"""Portable finite certificate checker. New IO/field/provenance wrapper;
exact borrowed arithmetic/table/commutant/control bodies are separate files.
No Root SDK, absolute origin path, group package or original acquisition call.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import runpy
import sys
import time

D=Path(__file__).resolve().parent
START=time.monotonic()

def need(ok,why):
    if not ok:raise ValueError(why)

def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()+b'\n'

def strict(raw):
    def pairs(items):
        result={}
        for key,value in items:need(key not in result,'duplicate JSON key');result[key]=value
        return result
    def bad(value):raise ValueError('integer-only finite data: '+value)
    return json.loads(raw,object_pairs_hook=pairs,parse_float=bad,parse_constant=bad)

def pin(path):
    path=Path(path);need(path.is_file()and not path.is_symlink()and path.resolve(strict=True)==path,'ordinary canonical package file')
    raw=path.read_bytes();need(len(raw)<=2*2**20,'bounded package leaf')
    return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())

def local(name):
    p=Path(name);need(not p.is_absolute()and '..'not in p.parts,'relative package path only')
    return D/p

def read(name):
    p=local(name);r=pin(p);value=strict(p.read_bytes());need(pin(p)==r,'unchanged data');return value

class Budget:
    def __init__(self):self.used=0
    def charge(self,n):
        need(type(n)is int and n>=0,'strict charge');self.used+=n
        need(self.used<=10000000 and time.monotonic()-START<20,'bounded finite arithmetic20s/10M')

def manifest():
    v=read('SourceManifest.json');need(v['schema']=='PORTABLE_COMMON_COMMUTANT_SOURCE_MANIFEST_V1','manifest schema')
    expected=set(v['files'])|{'SourceManifest.json'}
    actual={str(p.relative_to(D))for p in D.rglob('*')if p.is_file()}
    need(actual==expected,'whole portable file set, no hidden dependencies')
    for name,r in v['files'].items():need(pin(local(name))==r,'whole local file hash: '+name)
    return v

def derivation():
    v=read('provenance/source_derivation.json')
    need(v['schema']=='COMMON_COMMUTANT_EXACT_SOURCE_SPAN_DERIVATION_V1','source derivation schema')
    for entry in v['entries']:
        text=entry['whole_original_source'];raw=text.encode();origin=entry['original']
        need(len(raw)==origin['bytes']and hashlib.sha256(raw).hexdigest()==origin['sha256'],'whole origin Source hash')
        nodes={}
        for n in ast.parse(text).body:
            if isinstance(n,(ast.FunctionDef,ast.ClassDef)):nodes[n.name]=n
            elif isinstance(n,ast.Assign):
                for t in n.targets:
                    if isinstance(t,ast.Name):nodes[t.id]=n
        fragments=[]
        for item in entry['fragments']:
            n=nodes[item['name']];part=ast.get_source_segment(text,n)
            need((n.lineno,n.end_lineno,n.col_offset,n.end_col_offset)==(item['start_line'],item['end_line'],item['start_column'],item['end_column'])
                 and part==item['fragment']and hashlib.sha256(part.encode()).hexdigest()==item['fragment_sha256'],'exact Source span')
            fragments.append(part)
        body=entry['portable_header']+'\n\n'.join(fragments)+'\n'
        need(local(entry['portable_file']).read_bytes()==body.encode(),'ONLY exact selected definitions in portable module')
        need(pin(local(entry['portable_file']))==dict(bytes=entry['portable_bytes'],sha256=entry['portable_sha256']),'portable Source pin')

def field(codec,budget):
    keys={'schema','zero','one','z','nonzero_exponents','gap_sorted_codes','addition','multiplication','square','square_root'}
    need(type(codec)is dict and set(codec)==keys and codec['schema']=='F004_GF8_EXPONENT_CODEC_V1','actual complete codec schema')
    need(type(codec['zero'])is int and codec['zero']==0 and type(codec['one'])is int and codec['one']==1,'typed field identities')
    add,mul=codec['addition'],codec['multiplication']
    for table in [add,mul]:need(type(table)is list and len(table)==8 and all(type(row)is list and len(row)==8 and all(type(x)is int and 0<=x<8 for x in row)for row in table),'typed field tables')
    for x in range(8):
        need(add[0][x]==x and add[x][x]==0 and mul[1][x]==x and mul[0][x]==0,'identities/characteristic two')
        if x:need(any(mul[x][y]==1 for y in range(1,8)),'all nonzero inverses')
        for y in range(8):
            need(add[x][y]==add[y][x]and mul[x][y]==mul[y][x],'commutativity')
            for z in range(8):
                need(add[add[x][y]][z]==add[x][add[y][z]]and mul[mul[x][y]][z]==mul[x][mul[y][z]]and mul[x][add[y][z]]==add[mul[x][y]][mul[x][z]],'all field associativity/distributivity equations');budget.charge(1)
    for key in ['square','square_root','gap_sorted_codes']:
        need(type(codec[key])is list and len(codec[key])==8 and all(type(x)is int and 0<=x<8 for x in codec[key]),'typed codec list')
    need(sorted(codec['gap_sorted_codes'])==list(range(8))and codec['square']==[mul[x][x]for x in range(8)],'square table/sorted-code permutation')
    need(all(codec['square'][codec['square_root'][x]]==x for x in range(8)),'whole square-root table')
    need(type(codec['z'])is int and 1<=codec['z']<8 and codec['nonzero_exponents']==list(range(7))and all(type(x)is int for x in codec['nonzero_exponents']),'typed primitive-root convention')
    powers=[];x=1
    for _ in range(7):powers.append(x);x=mul[x][codec['z']]
    need(x==1 and sorted(powers)==list(range(1,8))and powers==list(range(1,8)),'actual nonzero exponent-code order')

def main():
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,'run with-I-B-S or-E-B-S, no optimization')
    p=argparse.ArgumentParser(allow_abbrev=False);p.add_argument('--controls-only',action='store_true');p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    out=args.out;need(out.is_absolute()and out.parent.resolve(strict=True)==out.parent and not out.exists()and out!=D and D not in out.parents,'new external output, outside package')
    m=manifest();derivation();budget=Budget()
    T=runpy.run_path(str(D/'arithmetic.py'),run_name='portable_exact_arithmetic_definitions')
    C=runpy.run_path(str(D/'commutant.py'),run_name='portable_exact_commutant_definitions')
    CTL=runpy.run_path(str(D/'controls.py'),run_name='portable_exact_synthetic_controls')
    controls=CTL['run'](T,C,budget.charge,dict(canonical=canonical))
    need(controls['all_passed']is True and controls['TEST_ONLY']is True and len(controls['controls'])==12,'twelve actual retained controls')
    result=dict(schema='PORTABLE_COMMON_COMMUTANT_VERIFICATION_V1',controls=12,all_controls_passed=True,controls_only=args.controls_only,
        original_group_acquisition_reproduced=False,original_centralizer_equality_reproduced=False,original_named_G2_identification_reproduced=False,
        new_Original_or_job_or_Lean_or_compression_credit=0,retained_premises=read('provenance/retained_premises.json'),package_manifest_sha256=pin(D/'SourceManifest.json')['sha256'])
    if not args.controls_only:
        codec=read('data/codec.json');field(codec,budget);a=T['Arithmetic'](codec,budget.charge)
        matrices=read('data/matrices.json');tables=read('data/tables.json');witness=read('data/witness.json')
        need(set(matrices)=={'schema','dimension','member_order','members','ambient_generator_order','ambient_generators'}and matrices['schema']=='COMMON_COMMUTANT_ORIGINAL_MATRIX_IMAGES_V1'and type(matrices['dimension'])is int and matrices['dimension']==6,'matrix schema')
        need(matrices['member_order']==['a','e','b']+['K'+str(i)for i in range(1,10)]+['H'+str(i)for i in range(1,10)]and matrices['ambient_generator_order']==['original_G_generator_1','original_G_generator_2'],'exact named image order')
        members=matrices['members'];marks=C['member_images'](a,members)
        need(type(matrices['ambient_generators'])is list and len(matrices['ambient_generators'])==2,'two ambient images');ambient=[a.flat(x)for x in matrices['ambient_generators']]
        for x in marks+ambient:a.symplectic(x)
        need(set(tables)=={'schema','K','H'}and tables['schema']=='COMMON_COMMUTANT_COMPLETE_FINITE_IMAGE_TABLES_V1','finite table envelope')
        K=T['check_table'](a,tables['K'],members[3:12],'K');H=T['check_table'](a,tables['H'],members[12:21],'H')
        T['check_prefix'](a,members[:3],members[3:12],members[12:21],K,H)
        need([len(K[0]),len(H[0]),len(K[2]),len(H[2])]==[512,512,511,119],'complete finite image orders and involutions')
        need(C['verify'](a,marks,ambient,witness)is True,'direct all21 commutations and original ambient escape')
        result.update(status='VERIFIED_CONDITIONAL_WHOLE_PREFIX_COMMON_COMMUTANT',field_order=8,field_axioms_checked=True,dimension=6,checked_members=21,ambient_generators=2,
            group_orders=[512,512],nonidentity_involution_counts=[511,119],raw_image_pair_slots=len(K[2])*len(H[2]),all21_commutations_verified=True,ambient_escape=witness['ambient_escape'],
            witness_in_K_image=a.literal(witness['X'])in K[1],witness_in_H_image=a.literal(witness['X'])in H[1],properness_conditional_on_retained_original_correspondences=True,
            pair_enumeration_performed=False,whole_original_manuscript_recovered=False)
    else:result['status']='VERIFIED_TEST_ONLY_COMMON_COMMUTANT_CONTROLS'
    budget.charge(0);result['charged_units']=budget.used;raw=canonical(result)
    with out.open('xb')as f:need(f.write(raw)==len(raw),'whole external output')
    budget.charge(0);manifest()
    print(json.dumps(dict(status=result['status'],result=dict(path=str(out),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()),controls=12),sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
