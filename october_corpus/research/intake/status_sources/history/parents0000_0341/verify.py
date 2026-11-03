"""Verify four saved metadata editions and print their active status fields.

Historical absolute paths are labels. No original path or archived program is
opened or executed. No mathematical certificate is replayed.
"""
from pathlib import Path
import hashlib,json,os,resource,signal,stat,sys,time,zlib

if sys.flags.optimize:
    raise SystemExit('Run without -O: verification requires assertions.')
BASE=Path(__file__).resolve().parent
START=time.monotonic();EXPANDED=0;READ=0
FILE_CAP=4*2**20;TOTAL_CAP=16*2**20
def checkpoint():
    assert time.monotonic()-START<125
    assert resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin'else 1024)<=256*2**20
def timeout(signum,frame):raise TimeoutError('125 second metadata limit')
signal.signal(signal.SIGALRM,timeout);signal.alarm(125)
def signature(s):return(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
def raw(name):
    global READ
    checkpoint();assert Path(name).name==name
    p=BASE/name;s=p.lstat();assert p.resolve(strict=True)==p and stat.S_ISREG(s.st_mode)and s.st_size<=FILE_CAP
    assert READ+s.st_size<=TOTAL_CAP
    with p.open('rb')as f:
        a=os.fstat(f.fileno());b=f.read(s.st_size+1);z=os.fstat(f.fileno())
    assert signature(s)==signature(a)==signature(z)==signature(p.lstat())and len(b)==s.st_size
    READ+=len(b);return b
def descriptor(body):return dict(bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
def expanded(source):
    global EXPANDED
    r=source['compressed'];b=raw(r['path']);assert descriptor(b)=={k:r[k]for k in('bytes','sha256')}
    dec=zlib.decompressobj(16+zlib.MAX_WBITS);parts=[];size=0
    for i in range(0,len(b),65536):
        pending=b[i:i+65536]
        while pending:
            checkpoint();chunk=dec.decompress(pending,min(65536,FILE_CAP-size+1));pending=dec.unconsumed_tail
            size+=len(chunk);assert size<=FILE_CAP and EXPANDED+size<=TOTAL_CAP;parts.append(chunk)
    assert dec.eof and not dec.unused_data and not dec.unconsumed_tail
    body=b''.join(parts);EXPANDED+=len(body)
    assert descriptor(body)=={k:source['original'][k]for k in('bytes','sha256')}
    return json.loads(body)

m=json.loads(raw('manifest.json'));assert m['schema']=='OCTOBER_INTAKE_STATUS_SOURCES_V1'
assert [s['role']for s in m['sources']]==['intake','controller','runtime','job20_selector']
sources={s['role']:s for s in m['sources']};docs={k:expanded(s)for k,s in sources.items()}
i,c,r,s=(docs[k]for k in('intake','controller','runtime','job20_selector'))
assert c['checkpoint']==i['active_controller_checkpoint']==sources['runtime']['original']
assert i['F004']['job20']['current_selector']==sources['job20_selector']['original']
assert i['L026']['current_typed_ledger']['current']==r['next_L026_current_snapshot']['CURRENT']
assert i['intake']['complete_reviewed_treatments']==r['counts']['complete_manuscripts']
assert i['intake']['mathematical_originals']==r['counts']['total_mathematical']
job=i['F004']['job20'];f=i['F009'];l=i['L026'];rc=r['counts']
assert job['now_unresolved']==s['unresolved_positions']==rc['F004_current_job_unresolved']
assert s['unresolved_position_runs']==[[n,n]for n in job['remaining_positions']]
assert job['partition']==[s['original_paid_count'],len(s['accepted_new_paid_positions']),s['unresolved_positions']]
assert sum(job['partition'])==s['original_orbit_positions']
assert f['R5_canonical_pairs_reviewed']==rc['R5_canonical_pairs_reviewed']==f['R5_canonical_next_parent']
assert f['R5_prefix_strict_slots_reviewed']==rc['R5_prefix_strict_slots_reviewed']
for a,b in [('generation','L026_GEN'),('subset_NEG','L026_NEG'),('separate_IP','L026_separate_IP'),('paid','L026_paid'),('unpaid','L026_unpaid')]:assert l[a]==rc[b]
assert l['generation']+l['subset_NEG']==l['paid']and l['paid']+l['unpaid']==l['bank_total']
counts=dict(intake=i['intake'],measurements=i['measurements_frozen'],F004=dict(complete_jobs=i['F004']['registered_jobs'],required_jobs=i['F004']['required_jobs'],pending_jobs=i['F004']['pending_jobs'],job20_partition=job['partition'],job20_remaining=job['remaining_positions'],selector_sha256=sources['job20_selector']['original']['sha256']),F009=dict(R5_reviewed_registered_parents=f['R5_canonical_pairs_reviewed'],R5_total_parents=f['R5_canonical_total_parents'],R5_strict_slots=f['R5_prefix_strict_slots_reviewed'],whole_R5_complete=f['R5_whole_level_complete']),L026=dict(GEN=l['generation'],NEG=l['subset_NEG'],separate_IP=l['separate_IP'],paid=l['paid'],unpaid=l['unpaid'],current_bank_rows=l['bank_total'],selectors_without_complete_census=l['selectors_without_complete_census'],CURRENT_sha256=l['current_typed_ledger']['current']['sha256']),runtime_cache_values=len(r['cache_entries'])+sum(b['entries']for b in r['cache_banks']))
assert counts==m['expected_counts'];checkpoint();signal.alarm(0)
print(json.dumps(dict(status='PASS',counts=counts,source_pointer_joins_verified=True,compressed_and_original_hashes_verified=True,expanded_bytes=EXPANDED,mathematical_replay_performed=False),sort_keys=True,indent=2))
