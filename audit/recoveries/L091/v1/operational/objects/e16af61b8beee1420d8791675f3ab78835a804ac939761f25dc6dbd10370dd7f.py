"""Read-only L091 closure/reuse inventory. This writes no publication payload."""
from pathlib import Path
import collections, hashlib, json, sys
sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
H = P.parent
S = H.parent.parent
R = Path('/Users/sasha/medusa/math_compression')


def load(p):
    return json.loads(p.read_text())


def pin(p):
    h = hashlib.sha256(); n = 0
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):
            n += len(b); h.update(b)
    return dict(path=str(p),bytes=n,sha256=h.hexdigest())


def main():
    root = H/'principal_root_review'
    rows = load(root/'dependencies.json')
    rows += [dict(r,path=str(root/r['path'])) for r in load(root/'manifest.json')['exports']]
    rows.append(pin(root/'manifest.json'))
    assert len({r['path'] for r in rows}) == len(rows)
    unique = {}
    aliases = collections.defaultdict(list)
    for r in rows:
        aliases[r['sha256']].append(r)
        if r['sha256'] in unique:
            assert unique[r['sha256']]['bytes'] == r['bytes']
        else:
            unique[r['sha256']] = r
    needed = set(unique)
    public_manifest = R/'provenance/publication_manifest.json'
    public = load(public_manifest)['files']
    tracked = {r['file']:r for r in public if all(k in r for k in ['file','bytes','sha256'])}
    reuse = {}
    for r in tracked.values():
        if r['sha256'] in needed and (R/r['file']).is_file():
            reuse.setdefault(r['sha256'],dict(kind='EXISTING_PUBLIC',bytes=r['bytes'],sha256=r['sha256'],
                  encoding='identity',stored_bytes=r['bytes'],stored_sha256=r['sha256'],
                  segments=[dict(path=r['file'],offset=0,bytes=r['bytes'])] if r['bytes'] else [],
                  public_files=[dict(path=r['file'],bytes=r['bytes'],sha256=r['sha256'])],
                  index='provenance/publication_manifest.json'))
    indexes = []
    # Latest segmented transport first; reuse its public packs in place.
    candidates = [n for n in tracked if n.endswith('/transport.json')]
    candidates.sort(key=lambda n:(n != 'audit/recoveries/L070/v1/transport.json',n))
    for n in candidates:
        q = R/n
        if not q.is_file():
            continue
        x = load(q)
        indexes.append(pin(q))
        if isinstance(x,dict) and isinstance(x.get('objects'),dict):
            for sha,r in x['objects'].items():
                if sha not in needed or sha in reuse or 'segments' not in r:
                    continue
                paths = {s['path'] for s in r['segments']}
                if not all(p in tracked and (R/p).is_file() for p in paths):
                    continue
                reuse[sha] = dict(kind='EXISTING_PUBLIC',**{k:r[k] for k in
                    ['bytes','sha256','encoding','stored_bytes','stored_sha256','segments']},
                    public_files=[dict(path=p,bytes=tracked[p]['bytes'],sha256=tracked[p]['sha256'])
                                  for p in sorted(paths)],index=n)
        if isinstance(x,dict) and isinstance(x.get('files'),list):
            for r in x['files']:
                if not isinstance(r,dict) or r.get('sha256') not in needed or r['sha256'] in reuse:
                    continue
                if not all(k in r for k in ['public_path','stored_bytes','stored_sha256']):
                    continue
                p = r['public_path']
                if p not in tracked or not (R/p).is_file():
                    continue
                reuse[r['sha256']] = dict(kind='EXISTING_PUBLIC',bytes=unique[r['sha256']]['bytes'],
                    sha256=r['sha256'],encoding=r.get('encoding','identity'),stored_bytes=r['stored_bytes'],
                    stored_sha256=r['stored_sha256'],
                    segments=[dict(path=p,offset=0,bytes=r['stored_bytes'])] if r['stored_bytes'] else [],
                    public_files=[dict(path=p,bytes=tracked[p]['bytes'],sha256=tracked[p]['sha256'])],index=n)
    old_premises = load(R/'audit/recoveries/L070/v1/premises.json')
    prior = {r['sha256']:r for r in old_premises['premises']}
    policy = []
    novel = []
    for sha,r in unique.items():
        if sha in reuse:
            continue
        if sha in prior:
            old = prior[sha]
            policy.append(dict(kind=old['kind'],sha256=sha,bytes=r['bytes'],exact_locator=old['exact_locator'],
                               reason=old['reason'],aliases=aliases[sha],
                               previous_public_policy='audit/recoveries/L070/v1/premises.json'))
        else:
            novel.append(dict(r,aliases=aliases[sha]))
    categories = collections.defaultdict(lambda:dict(objects=0,decoded_bytes=0))
    for kind,rs in [('verified_route_candidates',reuse.values()),('existing_exact_premise_policy',policy),('new_content_for_review',novel)]:
        for r in rs:
            categories[kind]['objects'] += 1
            categories[kind]['decoded_bytes'] += r['bytes']
    result = dict(status='READ_ONLY_L091_PUBLICATION_INVENTORY_NO_PAYLOAD',root_acceptance=pin(root/'manifest.json'),
                  public_manifest=pin(public_manifest),public_indexes=indexes,prior_premise_inventory=pin(R/'audit/recoveries/L070/v1/premises.json'),
                  logical_files=rows,unique_contents=unique,reuse_candidates=reuse,
                  prior_exact_premises=policy,new_contents=novel,summary=dict(categories),
                  scope='Reuse routes still require full actual stored/decoded verification. No new content is omitted. All derived proof/code/evidence remains exact payload; any further documentary or environment premise needs an explicit exact list.')
    (P/'inventory01.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
    print(json.dumps(dict(logical_files=len(rows),unique_contents=len(unique),summary=dict(categories),
                          report=pin(P/'inventory01.json'))),flush=True)


if __name__ == '__main__':
    main()
