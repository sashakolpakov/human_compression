"""Exact packet rehash and focused controls only, never the L100 target."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
if not __debug__:raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);ns=a.parse_args()
 for r in json.loads((HERE/'manifest.json').read_text())['exports']:
  p=Path(r['path']);assert not p.is_absolute() and '..' not in p.parts
  b=(HERE/p).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
 q=subprocess.run([sys.executable,str(HERE/'controls.py'),'--out',str(ns.out.absolute())],timeout=65)
 if q.returncode:raise SystemExit(q.returncode)
if __name__=='__main__':main()
