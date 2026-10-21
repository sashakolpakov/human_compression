"""Small execution control of the actual history adapter, without old censuses."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
from pathlib import Path
import hashlib,importlib.util,json,tempfile
W=Path(__file__).resolve().parent;D=W/'registration_drafts';AUD='audit/science87/v1'
spec=importlib.util.spec_from_file_location('history',D/'check_science87_history.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
reader='''from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def check_previous_suzuki_dispositions():
 a=ROOT/'audit/topic-e/topic_E_full_manuscript_protocol.json'
 b=ROOT/'research/leemans'
 assert a.is_symlink()and str(a.readlink())=='protocol.json'
 assert b.is_symlink()and str(b.readlink())=='case_study'
 assert a.read_text()=='literal old protocol'
 assert (b/'sentinel').read_text()=='literal old research'
 return {'status':'TWO_LITERAL_SYMLINKS_PRESERVED'}
def check_suzuki_dispositions():
 return {'counts':{'corrected_recoveries':85,'refuted':5,'handled':90,'mathematical_pending':15}}
'''
with tempfile.TemporaryDirectory(prefix='science87-history-control-')as tmp:
 r=Path(tmp)/'repo';r.mkdir();(r/'.git').mkdir()
 files={'scripts/verify_snapshot.py':reader,'audit/topic-e/protocol.json':'literal old protocol','research/case_study/sentinel':'literal old research'}
 for name,text in files.items():p=r/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
 (r/'audit/topic-e/topic_E_full_manuscript_protocol.json').symlink_to('protocol.json');(r/'research/leemans').symlink_to('case_study',target_is_directory=True)
 p=r/AUD/'previous/scripts/verify_snapshot.py';p.parent.mkdir(parents=True);p.write_text(reader);data=dict(baseline_commit='fixture',routes={'scripts/verify_snapshot.py':dict(path=str(p.relative_to(r)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())})
 (r/AUD/'history_routes.json').write_text(json.dumps(data));out=m.verify(r);assert out['previous']['status']=='TWO_LITERAL_SYMLINKS_PRESERVED'
 p.write_text(reader+'\n# damaged\n')
 try:m.verify(r)
 except ValueError:damaged=True
 else:raise AssertionError('Damaged history accepted')
 report=dict(status='PASS',actual_adapter_sha256=hashlib.sha256((D/'check_science87_history.py').read_bytes()).hexdigest(),literal_symlinks=2,damaged_historical_input_rejected=damaged,old_censuses_repeated=False)
 (W/'history_symlink_control01.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
