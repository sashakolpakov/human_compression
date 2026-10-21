"""Pin five accepted publication handoffs; two review pins are supplied by root."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
from pathlib import Path
import argparse,hashlib,json
W=Path(__file__).resolve().parent;S=W.parents[1]
def pin(p):return dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def main():
 p=argparse.ArgumentParser();p.add_argument('--L027-review',nargs=2,required=True,metavar=('PACKET','SHA256'));p.add_argument('--L036-review',nargs=2,required=True,metavar=('PACKET','SHA256'));a=p.parse_args()
 rows=[('L027','L027_publication_work',['L027'],'ordinary_recovery',a.L027_review),('L076','L076_publication_work',['L076'],'ordinary_recovery',('corpus106_L076_portable_root_review','ca245c956028dd5c2d07a525b980ff85482d8bfed5812bc2105125b7a426aadd')),('L036','L036_publication_work',['L036'],'principal_statement_refuted',a.L036_review),('L046','L046_disposition_work',['L046'],'principal_statement_refuted',('corpus106_L046_disposition_root_review','99456f89173dc1f325c9ddb068d81bb62dbe054ded35cdb63fff0eec83bedbb7')),('planes','PSL2_subfield_planes_publication_work',['L063','L064'],'principal_statement_refuted',('corpus106_PSL2_planes_portable_root_review','51dfd9ba8acc7085fd669b1a8db614faf7e606ee52921836e246ef391311c9f4'))]
 packages=[]
 for ident,name,ids,kind,(packet,digest) in rows:
  work=W.parent/name;r=json.loads((work/'ready.json').read_text());op=S/packet/'manifest.json';assert pin(op)['sha256']==digest
  proposal=json.loads((work/r['proposal']['path']).read_text());transport=proposal.get('portable_transport',proposal.get('transport'));t=transport.get('path')if isinstance(transport,dict)else transport
  packages.append(dict(id=ident,source_ids=ids,kind=kind,work=str(work.relative_to(S)),ready=pin(work/'ready.json'),stage='stage01',stage_manifest=r['stage_manifest']['path'],stage_manifest_pin=pin(work/r['stage_manifest']['path']),proposal=r['proposal']['path'],proposal_pin=pin(work/r['proposal']['path']),transport=t,operational_review=dict(packet=packet,**pin(op),status=json.loads(op.read_text())['status'])))
 out=W/'bundle_config01.json';assert not out.exists();out.write_text(json.dumps(dict(baseline='ade9feeb7f8feaffa8f773932d57a50e60cb64c2',audit_base='audit/science87/v1',packages=packages),indent=2)+'\n');print(out)
if __name__=='__main__':main()
