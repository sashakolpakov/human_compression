from pathlib import Path
import sys,json,importlib.util,subprocess
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');P=S/'geometry/primitive_pairs';A=P/'m11_graph_request01';B=P/'m11_graph_request02';O=P/'m11_graph_memory_controls_root02'
if O.exists():raise ValueError('fresh output')
O.mkdir()
for f in ['run.py','inputs.json','small_controls.py','owner_controls.py']:
 if (A/f).read_bytes()!=(B/f).read_bytes():raise ValueError('unexpected scientific or owner delta '+f)
for name in ['memory_controls','small_controls','owner_controls']:
 r=subprocess.run([sys.executable,'-B',str(B/(name+'.py'))],capture_output=True,timeout=30)
 (O/(name+'.stdout')).write_bytes(r.stdout);(O/(name+'.stderr')).write_bytes(r.stderr)
 if r.returncode or r.stderr:raise ValueError(name+' failed')
 report=json.loads(r.stdout)
 if not report['status'].startswith('PASS'):raise ValueError('no PASS '+name)
 print(name,report['status'],flush=True)
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/primitive_pairs/m11_graph_request02');c.packet('geometry/primitive_pairs/m11_graph_request_root_review')
for row in json.loads((B/'request.json').read_text())['bindings']:c.binding(row)
for p in O.iterdir():c.add(p)
c.add(Path(__file__))
c.finish('geometry/primitive_pairs/m11_graph_memory_root_review','ACCEPTED_L036_M11_SUPPORTED_MEMORY_GUARD',dict(
 reviewer='root',author='j3_recovery',review=[
 'Read the exact resource-only delta and supported self-memory implementation. Full owner, finite inputs and small/owner control programs are byte-identical to the acquired edition. The rejected setrlimit target was never launched.',
 'Memory observations are self peak RSS from getrusage, with Darwin byte units and other platforms converted from KiB. One GiB is checked every1024 existing require calls and at entry/serialization boundaries. This is cooperative sampled enforcement, not a kernel or continuous memory bound.',
 'Fresh memory controls passed, including forced one-byte rejection. Fresh mathematical small controls and all owner interruption/input/output controls passed. The external60second deadline,16MiB output,4GiB launch reserve plus output allowance and2GiB emergency floor remain unchanged.',
 'No finite loop, acquired permutation or source comparison premise changes. Only one initial invocation is authorized; its results still need independent acquisition and source joins.'
 ],supersedes_unexecuted_request01=True,authorized_initial_invocations=1,target_runs=0,source_credit=0))
