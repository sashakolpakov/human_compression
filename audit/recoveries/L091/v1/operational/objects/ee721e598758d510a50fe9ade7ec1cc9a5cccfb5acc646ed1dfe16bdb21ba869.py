"""Measure new exact streams into a counter; never create payload packs."""
from pathlib import Path
import collections, hashlib, json, time, zlib
P = Path(__file__).resolve().parent
H = P.parent
S = H.parent.parent


def pin(p):
    h=hashlib.sha256();n=0
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):
            n+=len(b);h.update(b)
    return dict(path=str(p),bytes=n,sha256=h.hexdigest())


def main():
    start=time.monotonic()
    x=json.loads((P/'inventory01.json').read_text())
    originals={str(S/p) for p in [
        'sources/catalogue_L096.pdf','sources/catalogue_L096.txt','sources/L096_supplementary_archive.tar',
        'corpus106_L096_recovery/private_auxiliary/hssupp_archived.pdf',
        'corpus106_L096_recovery/private_auxiliary/hssupp_archived.ps',
        'corpus106_L096_recovery/private_auxiliary/hssupp_archived.byte_reading.txt',
        'corpus106_L096_recovery/private_auxiliary/j3supp_archived.pdf',
        'corpus106_L096_recovery/private_auxiliary/j3supp_archived.ps',
        'corpus106_L096_recovery/private_auxiliary/j3supp_archived.byte_reading.txt']}
    policy=list(x['prior_exact_premises']);new=[];premise_additions=[]
    for k,r in enumerate(x['new_contents']):
        path=r['path'];p=Path(path)
        software=path.startswith('/opt/homebrew/Cellar/nauty/2.9.3/') or path=='/usr/bin/clang++'
        if path in originals or software:
            assert pin(p)=={a:r[a] for a in ['path','bytes','sha256']}
            z=dict(kind='INSTALLED_SOFTWARE_ENVIRONMENT_PREMISE' if software else 'DOCUMENTARY_SOURCE_PREMISE',
                   sha256=r['sha256'],bytes=r['bytes'],exact_locator=path,aliases=r['aliases'],
                   reason='Exact installed nauty/compiler file; algorithm correctness remains an explicit software premise.' if software else
                   'Exact original scholarly document, author supplement or documentary conversion/archive; numerical parsed tables and conversion receipts remain payload.')
            policy.append(z);premise_additions.append(z);continue
        h=hashlib.sha256();c=zlib.compressobj(level=6,wbits=31);n=raw=0
        with p.open('rb') as f:
            for b in iter(lambda:f.read(1<<20),b''):
                h.update(b);raw+=len(b);n+=len(c.compress(b))
        n+=len(c.flush())
        assert (raw,h.hexdigest())==(r['bytes'],r['sha256']),path
        new.append(dict(path=path,bytes=raw,sha256=r['sha256'],stored_bytes=min(n,raw),
                        encoding='gzip' if n<raw else 'identity',gzip6_bytes=n))
        if k%1000==0:print(json.dumps(dict(processed=k,total=len(x['new_contents']),seconds=time.monotonic()-start)),flush=True)
    premise=dict(status='EXPLICIT_EXACT_L091_PREMISES_PENDING_OPERATIONAL_REVIEW',root=x['root_acceptance'],
                 prior_public_policy=x['prior_premise_inventory'],premises=policy,new_exact_additions=premise_additions,
                 boundary='Only exact listed original documents and installed environment files are premise-only. All derived mathematical tables, generators, proof/code, transcripts, controls and review bytes have public payload routes. Existing original-page rasters not on this exact list remain payload.')
    (P/'premises.json').write_text(json.dumps(premise,separators=(',',':'))+'\n')
    result=dict(status='EXACT_L091_STREAM_MEASUREMENT_NO_PAYLOAD',root=x['root_acceptance'],inventory=pin(P/'inventory01.json'),
                premise_inventory=pin(P/'premises.json'),objects=new,new_objects=len(new),
                new_decoded_bytes=sum(r['bytes'] for r in new),new_stored_bytes=sum(r['stored_bytes'] for r in new),
                existing_public_objects=len(x['reuse_candidates']),premise_objects=len(policy),
                new_premise_objects=len(premise_additions),seconds=time.monotonic()-start,
                scope='Storage size only; no mathematical compression factor or source-count change.')
    (P/'measurement01.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='objects'}),flush=True)


if __name__=='__main__':main()
