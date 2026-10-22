#!/usr/bin/env python3
"""UNRUN synthetic portable-wire controls; Root supplies a compiled current C binary."""
from pathlib import Path
import argparse
import hashlib
import json
import struct
import subprocess
import tempfile

def need(ok,why):
    if not ok:raise ValueError(why)
def input_bytes():
    # S4 on four points, transposition a=(01), c=(23), T=<a> of order2.
    head=struct.pack('<8s8I2Q',b'PCKIN001',4,6,3,3,4,2,1,2,24,4)
    arrays=[[1,0,2,3],[0,1,3,2],[1,2,3,0],[1,0,2,3],[1,0,2,3]]
    return head+struct.pack('<6I',0,1,2,4,3,2)+bytes([1,2,3])+b''.join(struct.pack('<4I',*a)for a in arrays)
def feed(raw,parent=b'',suffix=None):
    result=b'PCKFEED1'+struct.pack('<Q',len(raw))+raw+struct.pack('<Q',len(parent))+parent
    if suffix is not None:result+=struct.pack('<Q',len(suffix))+suffix
    return result
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--binary',required=True);ap.add_argument('--binary-sha256',required=True);a=ap.parse_args()
    binary=Path(a.binary).resolve(strict=True)
    need(hashlib.sha256(binary.read_bytes()).hexdigest()==a.binary_sha256,'actual compiled binary pin')
    raw=input_bytes();digest=hashlib.sha256(raw).hexdigest();names=[]
    with tempfile.TemporaryDirectory(prefix='l026_packed_io_controls_')as directory:
        root=Path(directory)
        def run(mode,data,path,nodes=6,ok=True):
            r=subprocess.run([str(binary),mode,digest,str(path),str(nodes),'16'],input=data,capture_output=True,timeout=10)
            need((r.returncode==0)==ok,'expected whole native control result')
            if ok:
                need(r.stderr==b'','empty positive stderr');j=json.loads(r.stdout)
                need(j['synthetic_only']is True,'toy result never a named census');return j
            need(r.stderr.startswith(b'PACKED_IO_REFUSAL '),'specific bounded refusal');return None
        allpath=root/'all.bin';j=run('control-produce',feed(raw),allpath)
        need(j['complete']is True and j['count']==6 and j['orbits']==4,'whole literal S4 catalogue');names.append('whole_S4_portable_class')
        whole=allpath.read_bytes();s=run('control-check',feed(raw,suffix=whole),root/'unused')
        expected=dict(j);expected['proposal_search']=False;need(s==expected,'entire supplied native record');names.append('whole_Saved_record_without_proposal')
        firstpath=root/'first.bin';f=run('control-produce',feed(raw),firstpath,nodes=3)
        need(1<=f['count']<6 and not f['complete'],'real closed partial prefix');first=firstpath.read_bytes()
        run('control-check',feed(raw,suffix=first),root/'unused2',nodes=3);names.append('partial_prefix_freshly_Saved_verified')
        lastpath=root/'last.bin';last=run('control-produce',feed(raw,parent=first),lastpath)
        need(last['complete']is True and last['parent_count']==f['count']and last['new_count']==6-f['count'],'exact closed-parent restore/extension');names.append('closed_parent_restore_and_extension')
        checked=run('control-check',feed(raw,parent=first,suffix=lastpath.read_bytes()),root/'unused3')
        expected=dict(last);expected['proposal_search']=False;need(checked==expected,'whole restored Saved coordinates');names.append('restored_parent_new_Saved_complete')
        changed=bytearray(whole);changed[131]^=1
        run('control-check',feed(raw,suffix=changed),root/'unused4',ok=False);names.append('literal_new_key_corruption_refused')
        run('control-produce',feed(raw[:-1]),root/'truncated.bin',ok=False);names.append('truncated_export_refused')
        run('control-check',feed(raw,suffix=whole)+b'x',root/'unused5',ok=False);names.append('trailing_feed_byte_refused')
        run('produce',feed(raw),root/'wrong-domain.bin',ok=False);names.append('synthetic_domain_refused_by_production_mode')
        changed=bytearray(whole);changed[8]=ord('f')if changed[8]!=ord('f')else ord('e')
        run('control-check',feed(raw,suffix=changed),root/'unused6',ok=False);names.append('wrong_input_digest_in_tape_refused')
    need(len(names)==len(set(names))==10,'exact ten distinct controls')
    print(json.dumps(dict(status='PASS_SYNTHETIC_PACKED_PORTABLE_IO_CONTROLS',names=names,controls=10,synthetic_only=True,whole_original_credit=0),sort_keys=True))
if __name__=='__main__':main()
