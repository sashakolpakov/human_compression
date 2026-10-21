#!/usr/bin/env python3
"""Bounded literal-row computations. A timeout is recorded as an unresolved row."""
import argparse, hashlib, json, pathlib, subprocess, time
HERE=pathlib.Path(__file__).resolve().parent

def digest(p):
    b=p.read_bytes(); return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--rows',nargs='+',required=True);ap.add_argument('--out',type=pathlib.Path,required=True)
    ap.add_argument('--engine',type=pathlib.Path,default=HERE/'presentation_engine.g');ap.add_argument('--timeout',type=float,default=120);ap.add_argument('--coset-limit',type=int,default=100000);ap.add_argument('--gap',default='/opt/homebrew/bin/gap')
    ar=ap.parse_args(); ar.out.mkdir(parents=True,exist_ok=False)
    engine=ar.out/'engine.g';engine.write_bytes(ar.engine.read_bytes());
    local=ar.out/'local_residues.g';local.write_bytes((HERE/'local_residues.g').read_bytes());
    roster=json.loads((HERE/'table_roster.json').read_text()); byid={r['id']:r for r in roster['rows']}; records=[]
    for rid in ar.rows:
        r=byid[rid]; assert isinstance(r['rotational_presentation_order_expected'],int)
        rd=ar.out/rid;rd.mkdir();params=[[int(i) for i in p.split(',')] for p in r['literal_parameters'].split(';')]
        # All variable contents below are exact roster numbers or a restricted row identifier.
        inp='L003Input:=rec(id:='+json.dumps(rid)+',table:='+str(r['table'])+',params:='+str(params)+',expected_rotation_order:='+str(r['rotational_presentation_order_expected'])+',regular:='+str(r['source_regularity']=='regular').lower()+',coset_limit:='+str(ar.coset_limit)+');;\n'
        (rd/'input.g').write_text(inp)
        start=time.monotonic(); status='UNRESOLVED';rc=None
        with (rd/'stdout').open('wb') as out,(rd/'stderr').open('wb') as err:
            try:
                p=subprocess.run([ar.gap,'-q','-T',str(rd/'input.g'),str(local),str(engine)],stdout=out,stderr=err,timeout=ar.timeout)
                rc=p.returncode
                if rc==0 and ('PASS_L003_ROW '+rid) in (rd/'stdout').read_text() and not (rd/'stderr').read_text().strip():status='PASS'
                if status=='PASS' and 'MATCH false' in (rd/'stdout').read_text():status='PASS_WITH_SOURCE_DISCREPANCY'
            except subprocess.TimeoutExpired:status='TIMEOUT'
        record={'id':rid,'status':status,'returncode':rc,'seconds':round(time.monotonic()-start,6),'timeout_seconds':ar.timeout,'coset_limit':ar.coset_limit,'source_row':r,'engine':digest(engine),'local_residues':digest(local),'roster':digest(HERE/'table_roster.json'),'input':digest(rd/'input.g'),'stdout':digest(rd/'stdout'),'stderr':digest(rd/'stderr')}
        (rd/'receipt.json').write_text(json.dumps(record,indent=2)+'\n');records.append(record)
        (ar.out/'report.json').write_text(json.dumps({'status':'BOUNDED_BATCH','engine':digest(engine),'rows':records},indent=2)+'\n')
        print(rid,status,record['seconds'],flush=True)
if __name__=='__main__':main()
