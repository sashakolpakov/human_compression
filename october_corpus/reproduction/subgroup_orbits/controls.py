#!/usr/bin/env python3
"""Synthetic controls for parent replay and the shared linear-algebra budget."""
import time
START=time.monotonic()
import argparse,base64,copy,hashlib,os,stat,struct,sys,types
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    def need(value,message):
        if not value:
            raise ValueError(message)
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,'run with -E -B -S, without -O')
    path=ROOT/'verify.py';before=path.lstat()
    sig=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    need(path.resolve(strict=True)==path and stat.S_ISREG(before.st_mode)and before.st_nlink==1 and before.st_size<=22000,'bounded local verifier')
    with path.open('rb')as f:opened=os.fstat(f.fileno());raw=f.read(before.st_size+1);closed=os.fstat(f.fileno())
    need(sig(before)==sig(opened)==sig(closed)==sig(path.lstat())and len(raw)==before.st_size,'whole stable verifier')
    v=types.ModuleType('subgroup_orbit_control_kernel');v.__file__=str(path)
    exec(compile(raw,str(path),'exec'),v.__dict__);v.START=START
    args=v.arguments();b,s,m,shared=v.environment(args,controls=True);checks=[]
    def yes(name,value=True):need(value,name);checks.append(name)
    def no(name,f):
        try:f()
        except(ValueError,TypeError,IndexError,AssertionError):checks.append(name);return
        raise ValueError(name)
    def permutation(q):return tuple(tuple(int(j==q[i])for j in range(7))for i in range(7))
    def packet(rows):
        wire=b''.join(struct.pack('<HB',p,k)for p,k in rows)
        return dict(kind='REACHABLE_BOUND',count=3,seed_id=1,parents_labels_base64=base64.b64encode(wire).decode(),ordered_vector_ids_SHA256=hashlib.sha256(b''.join(struct.pack('<I',n)for n in(1,11,121))).hexdigest())
    A=permutation((1,0,2,3,4,5,6));B=permutation((0,2,1,3,4,5,6));marks=(A,B,s.I7);seed=(1,0,0,0,0,0,0)
    tree=packet([(65535,255),(0,0),(1,1)])
    yes('three fresh parent images',v.replay_tree(tree,seed,marks,b,3)['count']==3)
    no('wrong seed root',lambda:v.replay_tree(tree,(0,1,0,0,0,0,0),marks,b,3))
    no('parent must be earlier',lambda:v.replay_tree(packet([(65535,255),(1,0),(1,1)]),seed,marks,b,3))
    no('label must be a LEFT generator',lambda:v.replay_tree(packet([(65535,255),(0,3),(1,1)]),seed,marks,b,3))
    no('fresh vectors must be distinct',lambda:v.replay_tree(packet([(65535,255),(0,2),(1,1)]),seed,marks,b,3))
    changed=copy.deepcopy(tree);changed['ordered_vector_ids_SHA256']='0'*64
    no('ordered hash checked after images',lambda:v.replay_tree(changed,seed,marks,b,3))
    changed=copy.deepcopy(tree);changed['parents_labels_base64']=changed['parents_labels_base64'][:-4]
    no('complete parent bytes',lambda:v.replay_tree(changed,seed,marks,b,3))
    no('boolean count',lambda:v.replay_tree(tree,seed,marks,b,True))
    no('boolean seed',lambda:v.seed_vector([True,0,0,0,0,0,0]));no('zero seed',lambda:v.seed_vector([0]*7))
    no('canonical seed scale',lambda:v.seed_vector([2,0,0,0,0,0,0]))
    C=((0,1,0),(0,0,1),(1,9,10));Z=tuple(tuple(C[i][j]if i<3 and j<3 else int(i==j)if i>=3 and j>=3 else 0 for j in range(7))for i in range(7))
    yes('literal exact order19 word',v.word19(s,b,(s.I7,s.I7,Z,s.I7))[1]!=s.I7)
    no('identity has no order19',lambda:v.word19(s,b,(s.I7,)*4));no('seed fixed by same word',lambda:v.seed_fixed(seed,Z,b))
    D=tuple(tuple((10 if i==0 else 1)if i==j else 0 for j in range(7))for i in range(7))
    F=permutation(tuple((-i)%7 for i in range(7)));G=permutation(tuple((1-i)%7 for i in range(7)))
    ranks=v.no_left_line((D,F,G),b);first=b.linear
    yes('all eight sign systems',len(ranks)==8 and all(r['rank']==7 for r in ranks)and first>0)
    v.no_left_line((D,F,G),b)
    yes('linear counter accumulates across cases',b.linear>first)
    no('common invariant line rejected',lambda:v.no_left_line((s.I7,s.I7,s.I7),b))
    no('duplicate JSON key',lambda:v.decode(b'{"x":1,"x":2}'));no('nonfinite JSON',lambda:v.decode(b'{"x":NaN}'))
    b.recheck()
    proof=dict(schema='SUBGROUP_ORBIT_SYNTHETIC_CONTROLS_V1',checks=checks,original_case_search_calls=0)
    result=dict(schema='SUBGROUP_ORBIT_CONTROL_RESULT_V1',status='PASS',count=len(checks),checks=checks,
                original_case_search_calls=0,matrix_products=s.PRODUCTS,row_images=b.row_images,
                linear_field_operations=s.FIELD,field_inverses=s.INVERSES,
                input_read_bytes_after_recheck=b.read_bytes,input_paths=len(b.refs))
    v.publish(b,args.output,proof,result)
if __name__=='__main__':main()
