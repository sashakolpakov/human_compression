#!/usr/bin/env python3
"""Uninvoked Source: authenticated bounded binary transport, no Root adoption."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import resource
import stat
import struct
import subprocess
import sys
import time

MIB=1048576
MAX_TAPE=384*MIB
PIECE=64*MIB
STATUS='PASS_DISTINCT_L026_PACKED_CLASS_PORTABLE_SOURCE'
EXSTATUS='COMPLETED_GENUINE_DISTINCT_L026_PACKED_CLASS_PORTABLE_SOURCE_REVIEW'
START=time.monotonic()
def need(ok,message):
    if not ok:raise ValueError(message)
def bounded():
    rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':rss*=1024
    need(rss<=128*MIB and time.monotonic()-START<140,'128MiB/140s metadata transport bound')
def canonical(j):return json.dumps(j,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()+b'\n'
def equal(a,b):return canonical(a)==canonical(b)
def strict(raw):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'no duplicate JSON keys');d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def integer(n,lo,hi):return type(n)is int and lo<=n<=hi
def refshape(r):
    need(type(r)is dict and set(r)=={'path','bytes','sha256'},'exact pin fields')
    need(type(r['path'])is str and type(r['sha256'])is str and len(r['sha256'])==64
      and all(c in '0123456789abcdef' for c in r['sha256']) and integer(r['bytes'],0,MAX_TAPE),'typed full pin')
    p=Path(r['path']);need(p.is_absolute() and str(p.resolve(strict=True))==r['path'],'canonical absolute input')
    return p
class Inputs:
    def __init__(self):self.rows={};self.kinds={}
    def add(self,r,kind='source'):
        p=refshape(r);old=self.rows.get(str(p));need(old is None or old==r,'one exact pin per path')
        cap=MAX_TAPE if kind=='data' else 128*MIB
        need(r['bytes']<=cap,'explicit opaque leaf domain')
        st=p.stat();need(stat.S_ISREG(st.st_mode)and st.st_nlink==1,'ordinary nlink-one input')
        self.rows[str(p)]=r;self.kinds[str(p)]=kind
        need(len(self.rows)<=1024,'1024 whole input paths')
        need(sum(x['bytes'] for k,x in self.rows.items() if self.kinds[k]!='data')<=128*MIB,'128MiB current Source/runtime/metadata')
        need(sum(x['bytes'] for k,x in self.rows.items() if self.kinds[k]=='data')<=2*1024*MIB,'2GiB logical whole data domain')
        return p
    def chunks(self,r,kind='source'):
        p=self.add(r,kind);h=hashlib.sha256();total=0
        with p.open('rb',buffering=0)as f:
            before=os.fstat(f.fileno())
            while True:
                b=f.read(524288)
                if not b:break
                total+=len(b);need(total<=r['bytes'],'whole bounded read');h.update(b);bounded();yield b
            after=os.fstat(f.fileno())
        need((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns)==
          (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns),'stable whole opened file')
        need(total==r['bytes'] and h.hexdigest()==r['sha256'],'whole exact opened-byte pin')
    def auth(self,r,kind='source'):
        for _ in self.chunks(r,kind):pass
    def doc(self,r):
        need(r['bytes']<=2*MIB,'2MiB JSON document cap');raw=b''.join(self.chunks(r));j=strict(raw)
        need(type(j)is dict,'JSON record');return j
    def final(self):
        for p in sorted(self.rows):self.auth(self.rows[p],self.kinds[p])
def pin(p):
    h=hashlib.sha256();n=0
    with p.open('rb')as f:
        while True:
            b=f.read(524288)
            if not b:break
            n+=len(b);h.update(b);bounded()
    return dict(path=str(p.resolve()),bytes=n,sha256=h.hexdigest())
def given(path,sha):return dict(path=str(Path(path).resolve(strict=True)),bytes=Path(path).stat().st_size,sha256=sha)
def source(io,args):
    packetref=given(args.source_packet,args.source_packet_sha256)
    peerref=given(args.source_review,args.source_review_sha256)
    exref=given(args.source_execution,args.source_execution_sha256)
    packet=io.doc(packetref);peer=io.doc(peerref);ex=io.doc(exref)
    need(packet['program']['path']==str(Path(__file__).resolve()),'actual current portable program')
    need(peer['status']==STATUS and ex['status']==EXSTATUS and peer['source_author']=='C5'
      and type(peer['reviewer'])is str and bool(peer['reviewer'])and peer['reviewer']!='C5'
      and peer['blockers']==[] and ex['blockers']==[],'genuine distinct current Source statuses')
    for j in [peer,ex]:
        need(equal(j['program'],packet['program'])and equal(j['programs'],packet['programs'])and equal(j['source_packet'],packetref),'complete current Source map')
    need(equal(ex['review'],peerref)and ex['reviewer']==peer['reviewer']and ex['actor']==peer['reviewer']and ex['source_author']=='C5','canonical Source review/actor/author join')
    for r in packet['required_current_source_inputs']:io.auth(r)
    for r in packet['programs'].values():io.auth(r)
    late=peer['late_author_preparation'];need(equal(ex['late_author_preparation'],late),'same mandatory actual late preparation');io.auth(late)
    return packet,dict(program=packet['program'],source_packet=packetref,source_review=peerref,source_execution=exref)
def tape(io,manifest):
    need(type(manifest)is dict and type(manifest['tape'])is list and 1<=len(manifest['tape'])<=6,'bounded portable tape pieces')
    need(integer(manifest['tape_bytes'],1,MAX_TAPE),'strict complete tape byte count')
    need(all(r['bytes']<=PIECE for r in manifest['tape']),'64MiB piece limit')
    need(sum(r['bytes'] for r in manifest['tape'])==manifest['tape_bytes']<=MAX_TAPE,'whole tape extent')
    for r in manifest['tape']:refshape(r)
    return manifest['tape']
def core_authority(io,roles,packet):
    need(type(roles)is dict and set(roles)=={'program','source_packet','source_review','source_execution'},'explicit closed core Source4')
    cp=io.doc(roles['source_packet']);cr=io.doc(roles['source_review']);ce=io.doc(roles['source_execution'])
    expected={'kernel':packet['programs']['kernel'],'header':packet['programs']['header'],'controls':packet['programs']['core_controls']}
    need(equal(cp['programs'],expected)and equal(roles['program'],expected['kernel']),'whole exact frozen core map')
    need(cr['status']=='PASS_DISTINCT_L026_PACKED_CONJUGACY_KEYS_SOURCE'and ce['status']=='COMPLETED_GENUINE_DISTINCT_L026_PACKED_CONJUGACY_KEYS_SOURCE_REVIEW','closed genuine core Source statuses')
    for j in [cr,ce]:
        need(equal(j['program'],roles['program'])and equal(j['programs'],expected)and equal(j['source_packet'],roles['source_packet'])and j['source_author']=='C5'
          and type(j['reviewer'])is str and bool(j['reviewer'])and j['reviewer']!='C5'and j['blockers']==[],'full closed core Source roles')
    need(equal(ce['review'],roles['source_review'])and ce['actor']==cr['reviewer']and equal(cr['late_author_preparation'],ce['late_author_preparation']),'canonical core Source execution/actor/late join')
    io.auth(cr['late_author_preparation'])
def allchunks(io,refs):
    for r in refs:yield from io.chunks(r,'data')
def remainder(io,producer,parent):
    """Compare EVERY borrowed prefix byte, then yield only actual new suffix."""
    old=iter(allchunks(io,parent));new=iter(allchunks(io,producer));a=b=b''
    while True:
        if not a:
            try:a=next(old)
            except StopIteration:break
        if not b:
            try:b=next(new)
            except StopIteration:raise ValueError('producer lost parent prefix')
        n=min(len(a),len(b));need(a[:n]==b[:n],'entire exact accepted parent byte prefix');a=a[n:];b=b[n:]
    if b:yield b
    yield from new
def split_tape(out,parts):
    refs=[];f=None;size=0;total=0;index=0
    try:
        for b in parts:
            pos=0
            while pos<len(b):
                if f is None:
                    index+=1;need(index<=6,'at most six whole tape pieces');p=out/f'tape_{index:02d}.bin';f=p.open('xb');size=0
                n=min(PIECE-size,len(b)-pos);f.write(b[pos:pos+n]);size+=n;pos+=n;total+=n
                need(total<=MAX_TAPE,'384MiB full checkpoint');bounded()
                if size==PIECE:f.flush();os.fsync(f.fileno());f.close();f=None;refs.append(pin(p))
        if f is not None:f.flush();os.fsync(f.fileno());f.close();f=None;refs.append(pin(p))
    finally:
        if f is not None:f.close()
    need(total>=1,'nonempty whole checkpoint');return refs,total
def write_json(path,j):
    raw=canonical(j);need(len(raw)<=MIB,'1MiB complete current metadata');tmp=path.with_name(path.name+'.partial')
    with tmp.open('xb')as f:f.write(raw);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
def run_core(io,args,binary,inputref,parentrefs,suffixrefs,suffixbytes,suffixout):
    command=[binary['path'],args.mode,inputref['sha256'],str(suffixout),str(args.max_new_nodes),str(args.max_new_orbits)]
    proc=subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True)
    try:
        proc.stdin.write(b'PCKFEED1'+struct.pack('<Q',inputref['bytes']))
        for b in io.chunks(inputref,'data'):proc.stdin.write(b)
        proc.stdin.write(struct.pack('<Q',sum(r['bytes'] for r in parentrefs)))
        for b in allchunks(io,parentrefs):proc.stdin.write(b)
        if args.mode=='check':
            proc.stdin.write(struct.pack('<Q',suffixbytes));n=0
            for b in remainder(io,suffixrefs,parentrefs):proc.stdin.write(b);n+=len(b)
            need(n==suffixbytes,'exact whole producer suffix bytes')
        proc.stdin.close();proc.stdin=None
        stdout,stderr=proc.communicate(timeout=max(.1,138-(time.monotonic()-START)))
    except BaseException:
        proc.kill();proc.communicate();raise
    need(len(stdout)<=4096 and len(stderr)<=4096,'bounded native stdout/stderr')
    write_json(suffixout.parent/'native_subprocess.json',dict(schema='L026_PACKED_NATIVE_SUBPROCESS_V1',
      command=command,pid=proc.pid,returncode=proc.returncode,stdout_ascii=stdout.decode('ascii'),
      stderr_ascii=stderr.decode('ascii'),qualification='Actual local subprocess return, not an MCP/tool receipt or Root closure. External guard owns birth/group/physical closure.'))
    need(proc.returncode==0 and stderr==b'','native whole contract/physical scope must also pass external Root guard')
    result=strict(stdout);need(type(result)is dict and set(result)=={'blocks','complete','count','cursor','new_count','new_orbits','next','orbits','parent_count','parent_orbits','proposal_search','synthetic_only'},'whole exact native result fields')
    need(stdout==canonical(result),'whole canonical native result')
    need(type(result['complete'])is bool and type(result['proposal_search'])is bool and result['synthetic_only']is False,'strict actual result boolean fields')
    for k in set(result)-{'complete','proposal_search','synthetic_only'}:need(integer(result[k],0,2857240),'strict native integer field')
    need(result['new_count']>=1 and result['new_orbits']>=1 and result['proposal_search']==(args.mode=='produce'),'nonempty completed native result')
    return result,command
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--mode',choices=['plan','produce','check'],required=True)
    ap.add_argument('--plan-for',choices=['produce','check'],default='produce')
    for role in ['source-packet','source-review','source-execution','input-gate','runtime-plan']:
        ap.add_argument('--'+role,required=True);ap.add_argument('--'+role+'-sha256',required=True)
    for role in ['parent-acceptance','producer-manifest']:
        ap.add_argument('--'+role);ap.add_argument('--'+role+'-sha256')
    ap.add_argument('--max-new-nodes',type=int,default=65536);ap.add_argument('--max-new-orbits',type=int,default=65536)
    ap.add_argument('--out',required=True);args=ap.parse_args()
    checking=args.mode=='check'or(args.mode=='plan'and args.plan_for=='check')
    need(integer(args.max_new_nodes,256,65536)and integer(args.max_new_orbits,1,65536),'prospective finite chunk limits')
    need(bool(args.parent_acceptance)==bool(args.parent_acceptance_sha256),'complete optional parent pin')
    need(checking==bool(args.producer_manifest)and bool(args.producer_manifest)==bool(args.producer_manifest_sha256),'exact Saved-only producer arguments')
    io=Inputs();packet,roles=source(io,args)
    gateref=given(args.input_gate,args.input_gate_sha256);gate=io.doc(gateref)
    need(gate['schema']=='ROOT_ACCEPTED_L026_PACKED_BASE_FACTOR_EXPORT_V1'and gate['root']is True and gate['adopted']is True,'genuine closed actual input export required')
    need(equal(gate['source'],roles)and integer(gate['endpoint'],1,2)
      and type(gate['endpoint_order'])is int and gate['endpoint_order']==[256,144][gate['endpoint']-1]
      and type(gate['degree'])is int and gate['degree']==122760 and type(gate['class_size'])is int and gate['class_size']==2857239,'same actual endpoint/model/Source boundary')
    for k in ['faithful_base_verified','whole_maps_verified','same_original_endpoint_words']:need(gate[k]is True,'complete actual export premise '+k)
    need(gate['old_rank_checkpoint_transferred']is False,'no phantom old4097 transfer')
    for k in ['root_terminal','actual_review','actual_execution','export_report','endpoint_setup_acceptance']:io.auth(gate[k])
    setup=io.doc(gate['endpoint_setup_acceptance'])
    need(setup['status']=='ROOT_ACCEPTED_CONDITIONAL_ONAN_ENDPOINT_SETUP'and setup['inner_stabilizer_orders']==[256,144],'actual full T orders, not observed orbit weights')
    need(gate['endpoint_setup_acceptance']['sha256']=='42d0261db2ef8a613df9382e08fddb5dfda8c3e87215a715a43464d74a56e21c','exact borrowed endpoint setup authority')
    inputref=gate['input'];io.add(inputref,'data');need(inputref['bytes']<=16*MIB,'16MiB exported maps domain')
    rtref=given(args.runtime_plan,args.runtime_plan_sha256);runtime=io.doc(rtref)
    need(runtime['schema']=='ROOT_ACCEPTED_L026_PACKED_RUNTIME_PLAN_V1'and runtime['root']is True and runtime['adopted']is True,'closed actual compiler/loader/runtime admission')
    need(equal(runtime['source'],roles)and equal(runtime['outer_rss_bytes'],512*MIB)and equal(runtime['outer_wall_seconds'],150),'same true Source and physical profile')
    need(equal(runtime['compiled_native_source'],packet['programs']['native'])and equal(runtime['included_frozen_core'],packet['programs']['kernel']),'actual compiled Source composition')
    core_authority(io,runtime['core_source'],packet)
    binary=runtime['binary'];io.auth(binary)
    for r in runtime['runtime_inputs']:io.auth(r)
    for k in ['compiler_capture','compiler_terminal','controls_acceptance','source_before']:io.auth(runtime[k])
    controls=io.doc(runtime['controls_acceptance'])
    need(controls['schema']=='ROOT_ACCEPTED_L026_PACKED_PORTABLE_CONTROLS_V1'and controls['root']is True and controls['adopted']is True
      and equal(controls['source'],roles)and equal(controls['binary'],binary)and equal(controls['core_source'],runtime['core_source'])
      and equal(controls['core_controls'],18)and equal(controls['portable_controls'],10),'actual controls for both separate implementations/current binary')
    parentref=None;parentmanifest=None;parentrefs=[]
    if args.parent_acceptance:
        parentref=given(args.parent_acceptance,args.parent_acceptance_sha256);parent=io.doc(parentref)
        need(parent['schema']=='ROOT_ACCEPTED_L026_PACKED_CLASS_CHECKPOINT_V1'and parent['root']is True and parent['adopted']is True,'exact Root-closed parent certificate')
        need(equal(parent['input_gate'],gateref)and equal(parent['source'],roles)and equal(parent['endpoint'],gate['endpoint']),'same parent input/T/Source namespace')
        for k in ['root_terminal','actual_review','actual_execution','producer_result','saved_result']:io.auth(parent[k])
        parentmanifest=io.doc(parent['manifest']);parentrefs=tape(io,parentmanifest)
        need(parentmanifest['schema']=='L026_PACKED_CLASS_MANIFEST_V1'and equal(parentmanifest['source'],roles)and equal(parentmanifest['input_gate'],gateref),'same complete accepted parent manifest')
        need(equal(parentmanifest['native'],parent['native'])and integer(parentmanifest['native']['count'],1,2857238),'exact unfinished accepted parent coordinates')
    produced=None;producerrefs=[];suffixbytes=0
    if checking:
        producedref=given(args.producer_manifest,args.producer_manifest_sha256);produced=io.doc(producedref)
        need(set(produced)=={'schema','source','input_gate','runtime_plan','binary','parent_acceptance','native','tape','tape_bytes','limits','old_rank_checkpoint_transferred','generation_counted','whole_original_credit'},'entire exact producer manifest fields')
        need(produced['schema']=='L026_PACKED_CLASS_MANIFEST_V1'and equal(produced['source'],roles)and equal(produced['input_gate'],gateref)and equal(produced['runtime_plan'],rtref)and equal(produced['binary'],binary)and equal(produced['parent_acceptance'],parentref),'whole current producer lineage')
        need(equal(produced['limits'],{'max_new_nodes':args.max_new_nodes,'max_new_orbits':args.max_new_orbits}),'actual same producer limits')
        need(produced['old_rank_checkpoint_transferred']is False and produced['generation_counted']is False and type(produced['whole_original_credit'])is int and produced['whole_original_credit']==0,'exact unpaid census scope')
        producerrefs=tape(io,produced);suffixbytes=produced['tape_bytes']-sum(r['bytes'] for r in parentrefs)
        need(1<=suffixbytes<=16*MIB,'whole exact nonempty new suffix')
    out=Path(args.out);need(out.is_absolute()and not out.exists(),'fresh absolute output directory');out.mkdir(mode=0o700)
    if args.mode=='plan':
        for r in parentrefs+producerrefs:io.add(r,'data')
        io.final();bounded()
        result=dict(schema='L026_PACKED_PORTABLE_INPUT_PLAN_V1',phase=args.plan_for,source=roles,input_gate=gateref,runtime_plan=rtref,
          parent_acceptance=parentref,inputs=[io.rows[k]for k in sorted(io.rows)],data_paths=sorted(k for k in io.rows if io.kinds[k]=='data'),
          native_invoked=False,outer_rss_bytes=512*MIB,outer_wall_seconds=150,physical_admission_and_known_scope_closure_owed=True,
          old_rank_checkpoint_transferred=False,whole_original_credit=0)
        write_json(out/'input_plan.json',result)
        print(canonical(dict(status='COMPLETED_PACKED_PORTABLE_INPUT_PLAN',result=pin(out/'input_plan.json'))).decode(),end='');return
    native,command=run_core(io,args,binary,inputref,parentrefs,producerrefs,suffixbytes,out/'new_suffix.bin')
    need(native['parent_count']==(0 if parentmanifest is None else parentmanifest['native']['count'])and native['parent_orbits']==(0 if parentmanifest is None else parentmanifest['native']['orbits']),'exact child parent counts')
    if args.mode=='produce':
        suffixpin=pin(out/'new_suffix.bin');need(suffixpin['bytes']<=16*MIB,'whole suffix domain')
        def parts():
            yield from allchunks(io,parentrefs)
            with (out/'new_suffix.bin').open('rb')as f:
                while True:
                    b=f.read(524288)
                    if not b:break
                    yield b
        pieces,total=split_tape(out,parts())
        result=dict(schema='L026_PACKED_CLASS_MANIFEST_V1',source=roles,input_gate=gateref,runtime_plan=rtref,binary=binary,
          parent_acceptance=parentref,native=native,tape=pieces,tape_bytes=total,
          limits=dict(max_new_nodes=args.max_new_nodes,max_new_orbits=args.max_new_orbits),
          old_rank_checkpoint_transferred=False,generation_counted=False,whole_original_credit=0)
        resultpath=out/'manifest.json'
    else:
        expected=dict(produced['native']);expected['proposal_search']=False
        need(canonical(native)==canonical(expected),'entire producer native scientific record including all coordinates')
        result=dict(schema='L026_PACKED_CLASS_SAVED_V1',source=roles,input_gate=gateref,runtime_plan=rtref,binary=binary,
          parent_acceptance=parentref,producer_manifest=producedref,native=native,
          entire_parent_prefix_byte_equal=True,whole_new_suffix_checked=True,complete_saved_verification=True,
          borrowed_parent_word_arithmetic_replayed=False,generation_counted=False,whole_original_credit=0)
        resultpath=out/'saved.json'
    io.final();bounded()
    write_json(out/'opened_inputs.json',dict(schema='L026_PACKED_PORTABLE_OPENED_INPUTS_V1',inputs=[io.rows[k]for k in sorted(io.rows)],data_paths=sorted(k for k in io.rows if io.kinds[k]=='data'),
      closed_parent_arithmetic_attributed=True,exact_authenticated_bytes_streamed_to_child=True,native_command=command))
    write_json(resultpath,result)
    print(canonical(dict(status='COMPLETED_PACKED_PORTABLE_'+args.mode.upper(),result=pin(resultpath))).decode(),end='')
if __name__=='__main__':main()
