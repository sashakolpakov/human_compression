"""A finite intersection-property obstruction; named-group premises are explicit imports."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time
import types

SOURCE_NAMES={'verify.py','schreier.py','controls.py'}
MATH_SHA='f4c493fc984100e509b3ccbd2c0d1621feffddeb7178df3320e87fa1dfef4904'
MARKS_SHA='4945afd588f07a3edfd886c2123629dd7a4d9b51dc1aeaa990e4094f068a6b63'
GUARDS={
    'supervise_validation.py':(4806,'c3b626b86791ac355c3503a654136f49ad76abbcdfadf0455efb32dd5cca25f4'),
    'supervise_transient.py':(18361,'5c7eed80537835e1a78c8489621d34741eeafc01f47fb394fec519e83f2c9b42')}
CAPS=dict(matrix_products=400000,row_images=200000,linear_units=200000,
    read_bytes=8388608,paths=96,rss_bytes=134217728,seconds=100,
    source_bytes=65536,output_files=2,output_bytes_each=131072)
IMPORTED_PREMISES=[
    'The original four matrices lie in the named inner G2(11) in its faithful natural Cayley frame over F11.',
    'The complete attributed maximal-subgroup classification and rational natural-module descriptions apply.',
    'The J1 maximal-subgroup row has elementary abelian Sylow2 subgroups, hence no element of order4.']
class Limit(RuntimeError):pass

def need(ok,message):
    if not ok:raise ValueError(message)

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode('ascii')
def digest(body):return hashlib.sha256(body).hexdigest()
def sha(value):
    need(type(value)is str and len(value)==64 and all(c in '0123456789abcdef'for c in value),'whole SHA256')
    return value

def decode(body):
    def pairs(rows):
        out={}
        for key,value in rows:
            need(key not in out,'duplicate JSON key');out[key]=value
        return out
    def bad(_):raise ValueError('only integer JSON numbers')
    return json.loads(body,object_pairs_hook=pairs,parse_float=bad,parse_constant=bad)

def signature(s):return(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)

class Budget:
    """One shared compound-product/image, scalar, IO and cooperative resource bank."""
    def __init__(self):
        self.started=time.monotonic();self.calls=0;self.products=0;self.rows=0;self.linear=0
        self.explicit_read_bytes=0;self.reserved_bootstrap_bytes=0;self.paths=set();self.reads=[]
        self.peak_rss=0
    def tick(self):
        self.calls+=1
        if time.monotonic()-self.started>90:raise Limit('90 second cooperative deadline')
        if self.calls%256==1:
            value=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            if sys.platform!='darwin':value*=1024
            self.peak_rss=max(self.peak_rss,value)
            if value>117440512:raise Limit('112 MiB cooperative RSS')
    def scalar(self,n):
        self.tick();need(type(n)is int and n>=0,'nonnegative scalar debit')
        if self.linear+n>200000:raise Limit('200000 scalar-unit bank')
        self.linear+=n
    def multiply(self,a,b):
        self.tick()
        if self.products>=400000:raise Limit('400000 full matrix-product bank')
        self.products+=1
        return bytes(sum(a[7*i+k]*b[7*k+j]for k in range(7))%11 for i in range(7)for j in range(7))
    def image(self,v,a):
        self.tick()
        if self.rows>=200000:raise Limit('200000 full row-image bank')
        self.rows+=1
        return bytes(sum(v[k]*a[7*k+j]for k in range(7))%11 for j in range(7))
    def read(self,path,expected=None,cap=262144):
        self.tick();p=Path(path).absolute();before=p.lstat()
        need(p.resolve(strict=True)==p and stat.S_ISREG(before.st_mode)and before.st_nlink==1,
            'canonical single-link regular input')
        need(before.st_size<=cap,'input extent before read')
        need(self.explicit_read_bytes+self.reserved_bootstrap_bytes+before.st_size<=8388608,
            'one8MiB charged-read bank')
        need(len(self.paths|{str(p)})+2<=96,'96 paths including two reserved external guard Sources')
        fd=os.open(p,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0))
        try:
            first=os.fstat(fd)
            with os.fdopen(fd,'rb',closefd=False)as stream:body=stream.read(before.st_size+1)
            last=os.fstat(fd)
        finally:os.close(fd)
        need(signature(before)==signature(first)==signature(last)==signature(p.lstat())
            and len(body)==before.st_size,'stable whole input including exact EOF')
        got=dict(path=str(p),bytes=len(body),sha256=digest(body))
        if expected is not None:
            need(set(expected)=={'path','bytes','sha256'}and got==expected,'exact whole input pin')
        self.explicit_read_bytes+=len(body);self.paths.add(str(p));self.reads.append(got)
        return body,got
    def reserve_bootstrap(self,worker_bytes):
        # Conservative nominal Source bodies: all3project files, validation,
        # plus transient twice for checks and once for its actual load.
        self.reserved_bootstrap_bytes=worker_bytes+4806+3*18361
        need(self.explicit_read_bytes+self.reserved_bootstrap_bytes<=8388608,'bootstrap in same8MiB bank')
    def close_inputs(self):
        for pin in list(self.reads):self.read(pin['path'],pin)
    def snapshot(self):
        self.tick()
        return dict(matrix_products=self.products,row_images=self.rows,linear_units=self.linear,
            explicit_read_bytes=self.explicit_read_bytes,reserved_bootstrap_bytes=self.reserved_bootstrap_bytes,
            charged_read_bytes=self.explicit_read_bytes+self.reserved_bootstrap_bytes,
            distinct_input_paths=len(self.paths),external_guard_Source_path_reserve=2,
            whole_reads=self.reads,elapsed_seconds=time.monotonic()-self.started,peak_rss_bytes=self.peak_rss)

def load_sources(expected_sha,b):
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
        and not sys.flags.optimize,'use Python-E-B-S without-O')
    base=Path(__file__).resolve().parent
    raw,mr=b.read(base/'SOURCE_PROVENANCE.json',cap=65536);need(digest(raw)==sha(expected_sha),'Root/user selected Source manifest hash')
    m=decode(raw);need(type(m)is dict and set(m)=={'schema','sources','external_root_replay_sources','attribution'}
        and m['schema']=='F004_INTERSECTION_CERTIFICATE_SOURCE_V1','complete portable Source provenance')
    files=m['sources'];need(type(files)is list and len(files)==3
        and {x['path']for x in files}==SOURCE_NAMES,'all3 complete project Source bodies')
    bodies={};pins=[]
    for row in files:
        need(type(row)is dict and set(row)=={'path','bytes','sha256'}and row['path']in SOURCE_NAMES
            and type(row['bytes'])is int and 0<row['bytes']<=65536,'same-directory Source descriptor')
        body,pin=b.read(base/row['path'],dict(path=str(base/row['path']),bytes=row['bytes'],sha256=sha(row['sha256'])),65536)
        bodies[row['path']]=body;pins.append(pin)
    external=m['external_root_replay_sources'];need(type(external)is list and len(external)==2,'two separately acquired Root replay guard Sources')
    need(all(type(x)is dict and set(x)=={'name','bytes','sha256'}for x in external),'complete external guard descriptors')
    need({x['name']:(x['bytes'],x['sha256'])for x in external}==GUARDS,'unchanged external guard identities')
    total=sum(x['bytes']for x in pins)
    need(total+23167<=65536 and digest(bodies['schreier.py'])==MATH_SHA,'complete Source union and literal retained math')
    b.reserve_bootstrap(total)
    # Execute only this already hashed literal module; no project cache/import search.
    module=types.ModuleType('schreier');module.__file__=str(base/'schreier.py')
    exec(compile(bodies['schreier.py'],module.__file__,'exec'),module.__dict__)
    return module,dict(manifest=mr,project_Sources=pins,worker_Source_bytes=total,
        external_guard_Source_bytes=23167,combined_Source_union_bytes=total+23167)

def four_marks(raw,b,sc):
    need(type(raw)is list and len(raw)==4,'four ordered original marks')
    marks=[]
    for matrix in raw:
        need(type(matrix)is list and len(matrix)==7,'complete7x7 original matrix')
        marks.append(b''.join(sc.row(row,b)for row in matrix))
    need(len(set(marks))==4 and all(x!=sc.I for x in marks),'four distinct nonidentity original marks')
    return tuple(marks)

def normalized(v,b):
    need(type(v)is bytes and len(v)==7 and any(v),'nonzero complete row for projective normalization')
    # At most7 pivot tests,8 field multiplications for exponent9,7 coordinate
    # multiplications, plus7 reductions:32 scalar units bound this fixed work.
    b.scalar(32);pivot=next(x for x in v if x);inverse=pow(pivot,9,11)
    return bytes((x*inverse)%11 for x in v)

def matrix(raw,b,sc):
    need(type(raw)is list and len(raw)==7,'canonical complete7x7 matrix')
    return b''.join(sc.row(row,b)for row in raw)

def original_marks(raw,b,sc):
    marks=four_marks(raw,b,sc)
    for g in marks:need(b.multiply(g,g)==sc.I,'all four original involutions')
    ac=None
    for i,j in((0,2),(0,3),(1,3)):
        forward=b.multiply(marks[i],marks[j]);reverse=b.multiply(marks[j],marks[i])
        need(forward==reverse,'all actual original string commutations')
        if(i,j)==(0,2):ac=forward
    need(len({sc.I,marks[0],marks[2],ac})==4,'four distinct actual AC Klein-four matrices')
    return marks

def joint_sign(v,a,c,b):
    b.scalar(7);minus=bytes((-x)%11 for x in v)
    left=b.image(v,a);right=b.image(v,c)
    need(left in(v,minus)and right in(v,minus),'actual simultaneous AC sign eigenvector')
    return(1 if left==v else 10,1 if right==v else 10)

def complete_AC(raw,a,c,b,sc):
    need(type(raw)is list and len(raw)==4,'all four sign-space basis blocks')
    expected=((1,1),(1,10),(10,1),(10,10));dimensions=(1,2,2,2)
    for block,signs,dimension in zip(raw,expected,dimensions):
        need(type(block)is dict and set(block)=={'signs','basis'}and type(block['signs'])is list
            and len(block['signs'])==2 and all(type(x)is int for x in block['signs'])
            and tuple(block['signs'])==signs and type(block['basis'])is list
            and len(block['basis'])==dimension,'exact ordered AC dimensions1/2/2/2')
        lines=set()
        for row in block['basis']:
            v=sc.seed(row,b);need(joint_sign(v,a,c,b)==signs,'actual supplied sign-space row')
            line=normalized(v,b);need(line not in lines,'nonproportional basis rows');lines.add(line)
    # Seven independent eigenvectors: within each dimension<=2 block the
    # lines are independent; distinct sign spaces are in direct sum.
    return expected

def cyclic_basis(cert,left,b,sc):
    need(type(cert)is dict and set(cert)=={'kind','dimension','basis','right_inverse','parent_edges',
        'nongeneration_claim','ambient_generation_claim','IP_claim'}
        and cert['kind']=='FULL_CYCLIC_SPAN_MATRIX_ALGEBRA_ONLY'
        and type(cert['dimension'])is int and cert['dimension']==7
        and all(cert[x]is False for x in('nongeneration_claim','ambient_generation_claim','IP_claim')),
        'exact supplied cyclic-basis identity certificate')
    A=matrix(cert['basis'],b,sc);R=matrix(cert['right_inverse'],b,sc);seed=A[:7]
    b.scalar(7);need(any(seed),'nonzero actual cyclic root')
    edges=cert['parent_edges'];need(type(edges)is list and len(edges)==6,'six complete earlier-parent edges')
    for index,edge in enumerate(edges,1):
        need(type(edge)is list and len(edge)==2 and all(type(x)is int for x in edge)
            and 0<=edge[0]<index and 0<=edge[1]<4,'earlier parent and original LEFT projection label')
        # The retained LEFT supplier used(a,b,c,c); label3 is the same c.
        mark=left[edge[1]if edge[1]<3 else 2]
        need(b.image(sc.at(A,edge[0],7),mark)==sc.at(A,index,7),'fresh full cyclic parent image')
    need(b.multiply(A,R)==sc.I,'complete right inverse proves seven independent actual word rows')
    return seed

def left_irreducible(blocks,certs,marks,b,sc):
    expected=complete_AC(blocks,marks[0],marks[2],b,sc)
    need(type(certs)is list and len(certs)==37,'complete37 cyclic certificates')
    counts={s:0 for s in expected};seen=set()
    for cert in certs:
        root=cyclic_basis(cert,marks[:3],b,sc)
        signs=joint_sign(root,marks[0],marks[2],b);line=normalized(root,b)
        need(line not in seen,'37 distinct actual normalized projective lines')
        seen.add(line);counts[signs]+=1
    need([counts[s]for s in expected]==[1,12,12,12],'all projective lines in the complete four AC spaces')
    return dict(AC_dimensions=[1,2,2,2],projective_line_counts=[1,12,12,12],
        cyclic_bases_verified=37,ordinary_irreducibility_conditional_on_elementary_projection_argument=True)

def point_prefix(raw_seed,cert,marks,b,sc,target):
    need(type(target)is int and 1<=target<=3025,'bounded point-prefix target')
    v=sc.seed(raw_seed,b)
    need(b.image(v,marks[0])==v and b.image(v,marks[2])==v,'actual seed fixed by AC')
    # Production has already verified the original AC Klein four.
    need(type(cert)is dict and set(cert)=={'n','parent_tree_b64'}and type(cert['n'])is int
        and cert['n']==target,'whole exact requested point-prefix count')
    tree=sc.blob(cert['parent_tree_b64'],3*target);need(tree[:3]==b'\xff\xff\xff','single exact root marker')
    points=bytearray(v);seen={v}
    for index in range(1,target):
        b.tick();parent=tree[3*index]|tree[3*index+1]<<8;label=tree[3*index+2]
        need(parent<index and label<3,'strict earlier parent and original LEFT label')
        image=b.image(sc.at(points,parent,7),marks[label])
        need(image not in seen,'all full seven-coordinate reached points are distinct')
        points.extend(image);seen.add(image)
    return dict(distinct_reached_vectors=target,parent_images=target-1,point_stabilizer_lower_bound=4,
        group_order_lower_bound=4*target,orbit_closure_claim=False)

def middle_order_four(word,marks,b,sc):
    need(type(word)is list and all(type(x)is int for x in word)
        and word==[1,2,1,2,1,2],'actual original-label word(bc)^3')
    value=sc.I
    for label in word:value=b.multiply(value,marks[label])
    square=b.multiply(value,value);fourth=b.multiply(square,square)
    need(square!=sc.I and fourth==sc.I,'literal(bc)^3 has exact order4')
    return dict(exact_word_order=4,rotation_order_divides=12,middle_order_upper_bound=24)

def finite_component(case,b,sc):
    marks=original_marks(case['marks'],b,sc)
    IR=left_irreducible(case['ac_bases'],case['cyclic_certificates'],marks,b,sc)
    size=point_prefix(case['point_seed'],case['point_certificate'],marks,b,sc,3025)
    middle=middle_order_four(case['order4_word'],marks,b,sc)
    right_seed=sc.seed(case['right_seed'],b);cert=case['right_certificate']
    need(type(cert)is dict and type(cert.get('n'))is int and cert['n']==1320,'the original complete1320-point RIGHT certificate')
    coverage={};right=sc.consume(marks[1:4],right_seed,cert,b,coverage)
    need(right['orbit_size']==right['stabilizer_order']==1320 and right['subgroup_order']==1742400
        and right['full_Schreier_loops']==3960,'all original RIGHT loops give exact1320*1320 order')
    need(size['group_order_lower_bound']>12096 and right['subgroup_order']>middle['middle_order_upper_bound'],
        'strict numerical hypotheses of the attributed criterion and endpoint intersection')
    return dict(irreducibility=IR,left_size=size,middle=middle,right=right,right_coverage=coverage,
        concrete_arithmetic_verified=True,named_group_or_classification_established_by_arithmetic=False)

def emit(out,value,proof,b):
    directory=Path(out).absolute();need(not directory.exists()and directory.parent.resolve(strict=True)==directory.parent,'fresh canonical output directory')
    bodies=[encoded(value)+b'\n',encoded(proof)+b'\n'];need(all(len(x)<=131072 for x in bodies),'two128KiB output caps')
    names=[directory/'result.json',directory/'proof.json']
    need(len(b.paths|{str(p)for p in names})+2<=96,'96paths including output and external guard Sources')
    b.tick();directory.mkdir()
    refs=[]
    for p,body in zip(names,bodies):
        with p.open('xb')as stream:need(stream.write(body)==len(body),'complete output write')
        refs.append(dict(path=str(p),bytes=len(body),sha256=digest(body)))
    return refs

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case');parser.add_argument('--case-sha256',required=True)
    parser.add_argument('--source-sha256',required=True);parser.add_argument('--out',required=True)
    args=parser.parse_args(argv);b=Budget();sc,sources=load_sources(args.source_sha256,b)
    body,case_ref=b.read(args.case);need(digest(body)==sha(args.case_sha256),'whole projected original case hash')
    case=decode(body)
    need(type(case)is dict and set(case)=={'schema','field','dimension','original_marking','marks','ac_bases',
        'cyclic_certificates','point_seed','point_certificate','order4_word','right_seed','right_certificate','provenance'}
        and case['schema']=='F004_POSITION2352_IP_CASE_V1'and type(case['field'])is int and case['field']==11
        and type(case['dimension'])is int and case['dimension']==7,'exact portable original-case schema')
    marking=case['original_marking']
    need(type(marking)is dict and marking==dict(job=24,rank=4,position=2352,
        representative_J_index=7302,marks_sha256=MARKS_SHA)
        and all(type(marking[k])is int for k in('job','rank','position','representative_J_index')),
        'exact original marking locator; hashes do not establish named-group membership')
    need(digest(encoded(case['marks']))==MARKS_SHA,'same original ordered quartet')
    need(type(case['provenance'])is dict and len(encoded(case['provenance']))<=16384,'bounded inert provenance')
    finite=finite_component(case,b,sc);b.close_inputs()
    answer=dict(status='VERIFIED_FINITE_INTERSECTION_OBSTRUCTION',position=2352,representative_J_index=7302,
        left_irreducible=True,left_group_order_lower_bound=12100,left_word_exact_order=4,
        right_exact_order=1742400,middle_group_order_upper_bound=24,
        conditional_conclusion='Under the three imported premises LEFT=G2(11), and LEFT intersect RIGHT=RIGHT differs from the middle subgroup. The rank4 intersection property fails.',
        imported_premises=IMPORTED_PREMISES,named_group_membership_verified_here=False,
        classification_verified_here=False,whole_manuscript_or_conjecture_claim=False,
        original_case_ledger_credit=0,Lean_claim=False)
    result=dict(answer=answer,counts=b.snapshot())
    proof=dict(schema='F004_PORTABLE_INTERSECTION_OBSTRUCTION_PROOF_V1',case=case_ref,Sources=sources,
        finite=finite,provenance=case['provenance'],imported_premises=IMPORTED_PREMISES,
        original_case_ledger_credit=0,named_group_membership_or_classification_verified_by_hashes=False)
    print(encoded(dict(status='PASS',outputs=emit(args.out,result,proof,b))).decode())

if __name__=='__main__':
    try:main()
    except Exception as error:
        print(encoded(dict(status='FAIL_CLOSED_UNPAID',error=str(error))).decode(),file=sys.stderr);raise SystemExit(1)
