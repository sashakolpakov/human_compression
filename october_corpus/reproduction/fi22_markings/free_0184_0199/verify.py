#!/usr/bin/env python3
"""Replay one of 16 accepted Fi22 marking certificates using local repository data.

No supplier, search, SGS, full virtual middle vector or private cache is used.
The named group, original member/Reader/class and two-fibre premises are imports.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import struct
import sys
import time

START=time.monotonic()
SCOPE='7795d9d9d4bbf392cb5a943053372149950eef15d4bd468a63e0cc41f5fcce3a'
SELECTOR=dict(first_block_index=2,endpoint_position=18,local_class_position=164,middle_block_index=2,first_ambient_class_position=13,middle_ambient_class_position=13)
if sys.flags.optimize:
    raise SystemExit('Run without -O.')

def need(ok,message):
    if not ok:raise ValueError(message)

def decode_operands(raw,work,n=3510,root=2961):
    need(type(n)is int and 24<=n<=3510 and type(root)is int and 0<=root<n,'bounded literal point frame')
    need(type(raw)is bytes and len(raw)==8+15*n and raw[:8]==b'L026CYC1','whole exact five-vector/tree frame')
    work.charge(len(raw),'complete_operand_bytes')
    maps=[]
    for k in range(5):
        vector=struct.unpack_from('<'+'H'*n,raw,8+2*n*k);seen=bytearray(n)
        for point in vector:
            work.charge(4,'whole_vector_field_range_and_unique_slot')
            need(point<n and not seen[point],'whole actual permutation range and bijection');seen[point]=1
        maps.append(vector)
    d0,a,c,A0,A1=maps
    for vector in(d0,a,c):
        moved=False
        for point in range(n):
            work.charge(6,'whole_nonidentity_involution_two_point_lookups')
            target=vector[point];need(vector[target]==point,'entire involution equation');moved=moved or target!=point
        need(moved,'actual nonidentity involution')
    work.charge(2*n,'whole_endpoint_vector_distinctness_scan')
    need(a!=c,'actual distinct original endpoints')
    for point in range(n):
        work.charge(10,'whole_distant_endpoint_commutation_four_lookups')
        need(a[c[point]]==c[a[point]],'whole original endpoint string relation')
    inverses=[]
    for vector in(A0,A1):
        inverse=[0]*n
        for point,target in enumerate(vector):
            work.charge(4,'whole_inverse_construction_read_and_write');inverse[target]=point
        for point in range(n):
            work.charge(8,'both_whole_inverse_composition_equations')
            need(inverse[vector[point]]==point and vector[inverse[point]]==point,'fresh entire signed ambient inverse')
        inverses.append(tuple(inverse))
    paths=[];by_point=[None]*n;depth=0;at=8+10*n
    for i in range(n):
        vertex,parent,label=struct.unpack_from('<HHb',raw,at+5*i);work.charge(12,'complete_tree_record_and_parent_role')
        need(vertex<n and by_point[vertex]is None,'whole distinct tree vertex fields')
        if i==0:
            need(vertex==root and parent==65535 and label==0,'same original bridge root');path=()
        else:
            need(parent<i and label in(-2,-1,1,2),'strict earlier signed original tree edge')
            path=paths[parent]+(label,)
        work.charge(2*len(path)+2,'whole_short_tree_path_copy_and_point_slot')
        need(len(path)<=10,'acquired original ambient path maximum10');depth=max(depth,len(path))
        paths.append(path);by_point[vertex]=path
    work.charge(2*n,'whole_vertex_path_slot_cover')
    need(all(path is not None for path in by_point),'all original point labels once')
    return dict(n=n,root=root,d0=d0,a=a,c=c,ambient=(A0,A1,*inverses),paths=tuple(by_point),path_max=depth)

def prepare_triangle(ctx,triangle,work):
    work.charge(32,'whole_three_vertex_and_path_pair_shape')
    need(type(triangle)in(list,tuple)and len(triangle)==3
         and all(type(x)is int and 0<=x<ctx['n']for x in triangle)
         and len(set(triangle))==3,'three distinct actual bound partner vertices')
    out=[]
    for vertex in triangle:
        work.charge(2,'bound_original_triangle_path_lookup');path=ctx['paths'][vertex]
        work.charge(2*len(path),'whole_inverse_short_literal_path')
        out.append((tuple(-j for j in reversed(path)),path))
    return tuple(out)

def ambient_word(ctx,word,point,work):
    need(type(point)is int and 0<=point<ctx['n'],'literal original point label')
    for label in word:
        need(type(label)is int and label in(-2,-1,1,2),'same literal signed A generator')
        work.charge(2,'one_original_ambient_map_image')
        point=ctx['ambient'][label-1 if label>0 else 1-label][point]
    return point

def D_image(ctx,path_pair,point,work):
    inverse,path=path_pair
    point=ambient_word(ctx,inverse,point,work)
    work.charge(2,'one_original_d0_map_image');point=ctx['d0'][point]
    return ambient_word(ctx,path,point,work)

def middle_image(ctx,triangle_paths,point,work,inverse=False):
    for pair in reversed(triangle_paths)if inverse else triangle_paths:
        point=D_image(ctx,pair,point,work)
    return point

def rotation_word(ctx,triangle_paths,letters,point,work):
    work.charge(2,'literal_rotation_start_point')
    need(type(point)is int and 0<=point<ctx['n'],'literal original start point')
    need(type(letters)is list and 1<=len(letters)<=64
         and all(type(j)is int and j in(-2,-1,1,2)for j in letters),'bounded strict signed actual rotation word')
    work.charge(2*len(letters),'whole_literal_rotation_word_scan')
    for label in letters:
        if label==1:
            work.charge(2,'actual_a_point_image');point=ctx['a'][point]
            point=middle_image(ctx,triangle_paths,point,work)
        elif label==-1:
            point=middle_image(ctx,triangle_paths,point,work,True)
            work.charge(2,'actual_a_inverse_point_image');point=ctx['a'][point]
        elif label==2:
            point=middle_image(ctx,triangle_paths,point,work)
            work.charge(2,'actual_c_point_image');point=ctx['c'][point]
        else:
            work.charge(2,'actual_c_inverse_point_image');point=ctx['c'][point]
            point=middle_image(ctx,triangle_paths,point,work,True)
    return point

def check_cycle(ctx,triangle_paths,part,prime,work):
    need(prime in(11,13)and type(part)is dict and set(part)=={'word','cycle'},'exact prime/word/cycle part')
    cycle=part['cycle'];letters=part['word']
    need(type(cycle)is list and len(cycle)==prime
         and all(type(x)is int and 0<=x<ctx['n']for x in cycle)
         and len(set(cycle))==prime,'exact distinct closed prime-cycle point list')
    work.charge(8*len(cycle),'complete_cycle_field_and_distinctness_checks')
    for i,point in enumerate(cycle):
        work.charge(4,'supplied_consecutive_and_closing_point_fields')
        need(rotation_word(ctx,triangle_paths,letters,point,work)==cycle[(i+1)%prime],
             'every actual signed-word cycle edge INCLUDING last return')

def verify_pair(ctx,triangle,row,work):
    work.charge(16,'whole_two_prime_part_shape')
    need(type(row)is dict and set(row)=={'prime11','prime13'},'two exact supplied prime parts')
    paths=prepare_triangle(ctx,triangle,work)
    check_cycle(ctx,paths,row['prime11'],11,work)
    check_cycle(ctx,paths,row['prime13'],13,work)
    return dict(primes=[11,13],closed_cycle_lengths=[11,13])

def check_subset(K, ctx, triangle, points, work, cap=3509):
    need(type(cap) is int and 1 <= cap <= 3509, 'finite proper-subset cap')
    need(type(points) is list and 1 <= len(points) <= cap < ctx['n'],
         'nonempty proper bounded supplied point set')
    work.charge(ctx['n'] + 24 * len(points), 'complete_subset_shape_slots_and_distinctness')
    seen = bytearray(ctx['n'])
    previous = -1
    for point in points:
        need(type(point) is int and previous < point < ctx['n'],
             'strict increasing original integer point labels')
        seen[point] = 1
        previous = point
    paths = K['prepare_triangle'](ctx, triangle, work)
    for point in points:
        for label in (1, 2):
            work.charge(12, 'every_supplied_subset_point_and_positive_rotation_edge')
            target = K['rotation_word'](ctx, paths, [label], point, work)
            need(seen[target] == 1, 'every actual ab and bc image belongs to the supplied set')
    return dict(points=len(points), checked_positive_rotation_edges=2 * len(points))

class Work:
    def __init__(self,check,cap=10000000,seconds=20):
        need(type(cap)is int and 0<cap<=10000000 and type(seconds)in(int,float)and 0<seconds<=20,'unchanged finite shared work cap')
        self.units=0;self.cap=cap;self.seconds=seconds;self.start=time.monotonic();self.check=check;self.labels={}
    def charge(self,amount,label):
        need(type(amount)is int and amount>=0,'typed nonnegative complete work charge');self.check()
        need(amount<=self.cap-self.units and time.monotonic()-self.start<self.seconds,'shared10M/20s point/field/framing budget')
        self.units+=amount;self.labels[label]=self.labels.get(label,0)+amount

def bound_row(raw,index,work):
    work.charge(96,'whole_exact_free_owner_record_and_digest')
    record=raw[16*index:16*index+16];owner,partner,mass,x,y,z=struct.unpack('<IIHHHH',record)
    need(owner<500178 and partner<500178 and mass==1024,'actual adopted free product witness')
    return owner,hashlib.sha256(record).hexdigest(),(x,y,z)

def decode(raw):
    def pairs(items):
        out={}
        for key,value in items:need(key not in out,'unique JSON keys');out[key]=value
        return out
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))

def refused(call):
    try:call()
    except(ValueError,KeyError,IndexError,TypeError):return
    raise ValueError('malformed or false synthetic claim was accepted')

def fixture(changed_ambient=False):
    n=26;I=list(range(n));d=I.copy();a=I.copy()
    for start,p in[(0,11),(11,13)]:
        for i in range(p):d[start+i]=start+(-i)%p;a[start+i]=start+(1-i)%p
    c=a.copy();c[24],c[25]=25,24
    A0,A1=I.copy(),I.copy()
    if changed_ambient:
        A0[0],A0[1],A0[2]=1,2,0
        A1[0],A1[3],A1[4]=3,4,0
    tree=b''.join(struct.pack('<HHb',i,65535 if i==0 else 0,0 if i==0 else(2 if changed_ambient and i==2 else 1))for i in range(n))
    raw=b'L026CYC1'+b''.join(struct.pack('<26H',*v)for v in[d,a,c,A0,A1])+tree
    return raw,[d,a,c,A0,A1]

def tick():
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)
    need(rss<128*2**20 and time.monotonic()-START<140, '128-MiB/140-second process bounds')


def signature(s):
    return(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)


class Inputs:
    def __init__(self,work):
        self.base=Path(__file__).resolve().parent
        self.work=work;self.bytes=Path(__file__).stat().st_size;self.refs={};self.stats={}
        self.work.charge(self.bytes,'interpreter_Source_bootstrap')
    def read(self,name,ref=None):
        need(type(name)is str and 0<len(name)<=160,'bounded relative input name')
        prefix='../../../data/proof_objects/sha256/'
        if name.startswith(prefix):
            sha=name[len(prefix):]
            need(len(sha)==64 and set(sha)<=set('0123456789abcdef'),'literal shared proof-object name')
            path=self.base.parents[2]/'data/proof_objects/sha256'/sha
        else:
            need('/'not in name and '\\'not in name and name not in('.','..')and not name.startswith('.'),'flat local input name')
            path=self.base/name
        need(path.resolve(strict=True)==path,'canonical local or shared input')
        s=path.lstat();need(stat.S_ISREG(s.st_mode)and s.st_nlink==1 and 0<s.st_size<=2**21,'regular two-MiB input')
        if ref is not None:
            need(type(ref)is dict and set(ref)=={'path','bytes','sha256'}and ref['path']==name
                and type(ref['bytes'])is int and ref['bytes']==s.st_size
                and type(ref['sha256'])is str and len(ref['sha256'])==64
                and set(ref['sha256'])<=set('0123456789abcdef'),'exact portable whole-file descriptor')
        need(self.bytes+s.st_size+1<=8*2**20,'eight-MiB cumulative physical reads')
        with path.open('rb')as f:
            need(signature(os.fstat(f.fileno()))==signature(s),'same opened input')
            raw=f.read(s.st_size+1)
            need(signature(os.fstat(f.fileno()))==signature(s),'same final opened input')
        self.bytes+=len(raw);self.work.charge(len(raw),'whole_physical_input_bytes')
        need(signature(path.lstat())==signature(s)and len(raw)==s.st_size,'whole stable input')
        actual=dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
        need(ref is None or actual==ref,'whole input SHA256')
        need(self.refs.get(name,actual)==actual and self.stats.get(name,signature(s))==signature(s),'one immutable input edition')
        self.refs[name]=actual;self.stats[name]=signature(s)
        need(len(self.refs)+1<=32,'32 input paths including package directory')
        tick();return raw
    def doc(self,ref):return decode(self.read(ref['path'],ref))
    def close(self):
        for name,ref in list(self.refs.items()):self.read(name,ref)


def maximal_premise(table,work):
    need(table.get('schema')=='FI22_COMPLETE_SIMPLE_MAXIMAL_ORDER_PREMISE_V1'
        and table.get('named_group')=='Fi22'and table.get('classification_is_borrowed')is True
        and table.get('Aut_Fi22_substitution_permitted')is False
        and table.get('conjugacy_classes')==14 and len(table['rows'])==12,'complete imported simple-Fi22 cover')
    classes=0
    for row in table['rows']:
        work.charge(64,'complete_maximal_order_prime_and_minimum_index_checks')
        n=row['order'];k=row['conjugacy_classes']
        need(type(n)is type(k)is int and n>0 and k>0 and not(n%11==n%13==0)
            and row['divisible_by_11']==(n%11==0)and row['divisible_by_13']==(n%13==0), 'every maximal omits11or13')
        need(64561751654400%n==0 and 64561751654400//n>=3510,'imported minimal proper index3510')
        classes+=k
    need(classes==14,'all fourteen conjugacy classes')


def ambient_tree(raw,ctx,work):
    # Validate the exact A-tree edges; full named A/G identification remains imported.
    vertices=[]
    for i in range(ctx['n']):
        vertex,parent,label=struct.unpack_from('<HHb',raw,8+10*ctx['n']+5*i)
        work.charge(12,'actual_ambient_spanning_tree_edge_and_fields')
        if i:
            need(ambient_word(ctx,[label],vertices[parent],work)==vertex,'actual signed A-tree edge')
        vertices.append(vertex)
    return dict(A_transitivity_from_exact_tree=True,
        G_transitivity_from_imported_normal_index2_and_minimum_index3510=True)


def controls(work):
    names=[];raw,maps=fixture();ctx=decode_operands(raw,work,26,0)
    need(ctx['n']==26 and ctx['path_max']==1,'generic complete frame')
    names.append('whole_generic_frame')
    triangle=(0,1,2)
    pair=dict(prime11=dict(word=[1],cycle=[0]+list(range(10,0,-1))),prime13=dict(word=[1],cycle=[11]+list(range(23,11,-1))))
    verify_pair(ctx,triangle,pair,work);names.append('both_closed_prime_cycles')
    refused(lambda:decode_operands(raw[:-1],work,26,0));names.append('truncated_frame')
    bad=bytearray(raw);struct.pack_into('<H',bad,8+2*26,0)
    refused(lambda:decode_operands(bytes(bad),work,26,0));names.append('duplicate_permutation_value')
    bad=bytearray(raw);noninv=list(range(26));noninv[:3]=[1,2,0];struct.pack_into('<26H',bad,8+2*26,*noninv)
    refused(lambda:decode_operands(bytes(bad),work,26,0));names.append('noninvolutory_endpoint')
    for offset,value,fmt in[(8+10*26+5+2,2,'H'),(8+10*26+5+4,0,'b'),(8+10*26,1,'H')]:
        bad=bytearray(raw);struct.pack_into('<'+fmt,bad,offset,value)
        refused(lambda bad=bad:decode_operands(bytes(bad),work,26,0))
    names.append('malformed_tree')
    wrong=copy.deepcopy(pair);wrong['prime11']['cycle'][1]=wrong['prime11']['cycle'][0]
    refused(lambda:verify_pair(ctx,triangle,wrong,work));names.append('repeated_cycle_point')
    wrong=copy.deepcopy(pair);wrong['prime11']['cycle']=[11]+list(range(23,13,-1))
    refused(lambda:verify_pair(ctx,triangle,wrong,work));names.append('false_last_return_edge')
    for target,value in[('point',True),('letter',True),('letter',0),('letter',3)]:
        wrong=copy.deepcopy(pair)
        if target=='point':wrong['prime11']['cycle'][0]=value
        else:wrong['prime11']['word'][0]=value
        refused(lambda wrong=wrong:verify_pair(ctx,triangle,wrong,work))
    names.append('strict_point_and_word_types')
    wrong=copy.deepcopy(pair);wrong['prime11']['word']=[-1]
    refused(lambda:verify_pair(ctx,triangle,wrong,work));names.append('wrong_rotation_orientation')
    raw2,maps2=fixture(True);ctx2=decode_operands(raw2,work,26,0);paths=prepare_triangle(ctx2,triangle,work)
    A=maps2[3];inverse=[0]*26
    for i,j in enumerate(A):inverse[j]=i
    expected=[A[maps2[0][inverse[i]]]for i in range(26)]
    opposite=[inverse[maps2[0][A[i]]]for i in range(26)]
    actual=[D_image(ctx2,paths[1],i,work)for i in range(26)]
    need(actual==expected and actual!=opposite,'exact right conjugation')
    names.append('right_conjugation_noncommuting_fixture')
    for i in range(26):
        x=rotation_word(ctx2,paths,[1,2],i,work)
        need(rotation_word(ctx2,paths,[-2,-1],x,work)==i,'signed inverse')
    names.append('signed_inverse_reverses_middle_factors')
    for word in([], [1]*65):
        wrong=copy.deepcopy(pair);wrong['prime11']['word']=word
        refused(lambda wrong=wrong:verify_pair(ctx,triangle,wrong,work))
    refused(lambda:prepare_triangle(ctx,[0,0,1],work));names.append('word_and_triangle_bounds')
    kernel=dict(prepare_triangle=prepare_triangle,rotation_word=rotation_word)
    check_subset(kernel,ctx,triangle,list(range(11)),work,25);names.append('proper_invariant_subset')
    for points,label in[([], 'empty_subset'),(list(range(26)), 'full_subset'),([True], 'Boolean_subset_point'),([0,0], 'duplicate_subset_point'),([1,0], 'unsorted_subset'),([26], 'out_of_range_subset'),([0], 'noninvariant_subset')]:
        refused(lambda points=points:check_subset(kernel,ctx,triangle,points,work,25));names.append(label)
    refused(lambda:decode(b'{"x":1,"x":2}'));names.append('duplicate_JSON_key')
    refused(lambda:decode(b'{"x":NaN}'));names.append('nonfinite_JSON')
    # The fixture's nominal tree is not an ambient spanning tree: catch that separately.
    refused(lambda:ambient_tree(raw,ctx,work));names.append('unverified_tree_does_not_prove_transitivity')
    tiny=Work(tick,1);refused(lambda:decode_operands(raw,tiny,26,0));names.append('work_admission')
    return names


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    choice=parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--controls',action='store_true')
    choice.add_argument('--index',type=int,choices=range(184,200))
    args=parser.parse_args();work=Work(tick);inputs=Inputs(work)
    manifest=decode(inputs.read('manifest.json'))
    need(manifest.get('schema')=='PORTABLE_FI22_MARKINGS_184_199_MANIFEST_V1'
        and manifest.get('scope_digest')==SCOPE and manifest.get('original_selector')==SELECTOR
        and manifest.get('indices')==list(range(184,200)),'exact original16-case subject')
    need(manifest['Source']['path']==Path(__file__).name=='verify.py','actual portable Source')
    inputs.read('verify.py',manifest['Source'])
    carrier=inputs.doc(manifest['certificates'])
    need(carrier.get('schema')=='PORTABLE_FI22_ACCEPTED_184_199_CARRIERS_V1'
        and carrier.get('scope_digest')==SCOPE,'exact carrier scope')
    rows=carrier['records'];need(type(rows)is list and [r['free_index']for r in rows]==list(range(184,200)),'all16records once')
    if args.controls:
        names=controls(work);result=dict(status='PASS',mode='controls',controls=len(names),names=names)
    else:
        row=rows[args.index-184]
        need(type(row['free_index'])is int and row['free_index']==args.index
            and row['kind']in('GEN','NEG'),'typed selected original record')
        table=inputs.doc(manifest['maximal_orders']);maximal_premise(table,work)
        encoded=inputs.read(manifest['operands']['path'],manifest['operands']);ctx=decode_operands(encoded,work)
        tree=ambient_tree(encoded,ctx,work)
        bank=inputs.read(manifest['witnesses']['path'],manifest['witnesses'])
        need(len(bank)==462528,'whole original28908-record witness bank')
        owner,digest,triangle=bound_row(bank,args.index,work)
        need(type(row['owner'])is int and row['owner']==owner and row['witness_row_sha256']==digest,'exact original owner/witness row')
        if row['kind']=='GEN':
            need(set(row)=={'kind','free_index','owner','witness_row_sha256','prime11','prime13'},'exact generation carrier')
            proof=verify_pair(ctx,triangle,dict(prime11=row['prime11'],prime13=row['prime13']),work)
            result=dict(status='PASS',mode='GEN',free_index=args.index,owner=owner,witness_row_sha256=digest,finite_prime_cycles=proof,
                generation='NAMED_ORIGINAL_SIMPLE_FI22_UNDER_IMPORTED_MODEL_AND_MAXIMAL_COVER',
                intersection_property='SEPARATE_RETAINED_SIMPLE_RANK3_THEOREM',strict_point_kernel_IP_credit=0)
        else:
            need(set(row)=={'kind','free_index','owner','witness_row_sha256','points'},'exact nongeneration carrier')
            proof=check_subset(dict(prepare_triangle=prepare_triangle,rotation_word=rotation_word),ctx,triangle,row['points'],work)
            result=dict(status='PASS',mode='NEG',free_index=args.index,owner=owner,witness_row_sha256=digest,invariant_subset=proof,
                conclusion='ROTATION_SUBGROUP_PROPER;ORIGINAL_MARKING_NONGENERATING_UNDER_IMPORTED_INVOLUTION_AND_SIMPLE_G')
        result['transitivity']=tree
    work.charge(262144,'full128KiB_stdout_serialization_reserve')
    inputs.close();tick();work.charge(0,'final_work_guard')
    result.update(Source=manifest['Source'],scope_digest=SCOPE,physical_read_bytes=inputs.bytes,paths=len(inputs.refs)+1,
        shared_work_units=work.units,shared_work_cap=work.cap,work_labels=work.labels,
        imported_named_group_full_Aut_Reader_member_class_two_fibre_and_H_equals_B=True,
        new_whole_Original_conjecture_Lean_or_compression_credit=0)
    raw=(json.dumps(result,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
    need(len(raw)<=128*2**10,'128-KiB stdout cap');sys.stdout.buffer.write(raw)

if __name__=='__main__':main()
