"""Portable exact L063_L064 completion; no private-file fallback or new acquisition."""
import sys
if sys.flags.optimize:
    raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode = True
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import io
import json
import shutil
import subprocess
import time
from pypdf import PdfReader
import pack_codec as codec
from prior_transport_reader import Archive

S = '/Users/sasha/medusa/research/leemans'
R = '/Users/sasha/medusa/math_compression'
F = S + '/geometry/psl2_rank_two'
A = F + '/source_synthesis'
ROOT = F + '/source_synthesis_root_review'
ROOT_SHA = '613fc1bdfade1514db77089b0f1c969a993a90ded8e1426287d42ffbd6489f7a'
AUTHOR_SHA = '2945e2fb811e92bc783b67f5edda97b638802f341652e7efba39ecd0acd8535e'
PREFIX = 'audit/principal-refutations/L063-L064/complete/v1'
PAPER = 'papers/corrections/psl2_rank_two/v1'
need = codec.need


def load(path):
    return json.loads(path.read_text())


def pin(path):
    size, digest = codec.digest_file(path)
    return dict(path=str(path), bytes=size, sha256=digest)


def exact(path, row):
    need(codec.digest_file(path) == (row['bytes'], row['sha256']), 'exact file: ' + str(path))


def metadata(ar):
    t = ar.t
    need(t['format'] == 'L063_L064_COMPLETION_EXACT_CONTENT_V1', 'known transport format')
    need(t['root_acceptance']['sha256'] == ROOT_SHA and t['author_manifest']['sha256'] == AUTHOR_SHA,
         'exact accepted root and author')
    root = ar.load(ROOT + '/manifest.json')
    need(root['status'] == 'ACCEPTED_L063_L064_COMPLETE_FIXED_SOURCE_TREATMENT', 'accepted complete-source status')
    rows = ar.load(ROOT + '/dependencies.json')
    rows += [dict(r, path=ROOT + '/' + r['path']) for r in root['exports']]
    rows.append(t['root_acceptance'])
    declared = {r['path']: r for r in rows}
    need(len(rows) == len(declared) and set(declared) == set(ar.originals), 'exact whole accepted closure')
    for row in rows:
        ar.exact(row)
    author = ar.load(A + '/manifest.json')
    for row in author['exports']:
        ar.exact(dict(row, path=A + '/' + row['path']))
    for row in ar.load(A + '/dependencies.json'):
        ar.exact(row)
    candidate = load(ar.stage / PREFIX / 'premise_candidates.json')
    need(candidate['author_sha256'] == AUTHOR_SHA, 'bound premise candidate edition')
    expected = {}
    source_occurrences = environment_occurrences = 0
    for row in candidate['premises']:
        ar.exact({k: row[k] for k in ['path','bytes','sha256']})
        if row['kind'] == 'PINNED_ENVIRONMENT_OR_LIBRARY_PREMISE':
            need((row['path'].startswith('/opt/homebrew/') or row['path']=='/Users/sasha/.venvs/global/bin/python'), 'environment is installed software or library')
            environment_occurrences += 1
        else:
            need(row['kind'] == 'ORIGINAL_SOURCE_DOCUMENTARY_PREMISE', 'explicit documentary kind')
            need(row['path'].endswith(('.pdf','.txt','.png','-spans.json')), 'original document form')
            source_occurrences += 1
        item = dict(kind=row['kind'], bytes=row['bytes'], sha256=row['sha256'],
                    exact_locator=row['path'], reason=row['reason'])
        expected.setdefault(row['sha256'], item)
    need(source_occurrences == candidate['documentary_count'] == 137 and
         environment_occurrences == candidate['environment_count'] == 116, 'exact premise occurrence counts')
    actual = {h:r for h,r in ar.objects.items() if r['kind'] not in ['NEW_PACKED_EXACT_CONTENT','EXISTING_PUBLIC']}
    premises = {r['sha256']:r for r in t['premises']}
    need(actual == expected == premises and len(t['premises']) == 232,
         'all and only exact original-document and environment premises')
    return dict(root_closure=len(rows), author_exports=len(author['exports']))


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--stage', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--expected-stage', required=True)
    parser.add_argument('--expected-transport', required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    start = time.monotonic()
    repo = args.repo.resolve()
    stage = args.stage.resolve() if args.stage else repo
    d = stage / PREFIX
    need(args.out.is_absolute() and not args.out.exists(), 'fresh absolute output')
    need(shutil.disk_usage(args.out.parent).free >= 4 * 2**30 + 40 * 2**20, 'unchanged 4GiB replay reserve')
    need(pin(d / 'manifest.json')['sha256'] == args.expected_stage, 'externally pinned stage')
    need(pin(d / 'transport.json')['sha256'] == args.expected_transport, 'externally pinned transport')
    manifest = load(d / 'manifest.json')
    need(manifest['status'] == 'PRIVATE_L063_L064_COMPLETION_STAGE_PENDING_OPERATIONAL_REVIEW', 'known stage status')
    exports = {r['path']: r for r in manifest['exports']}
    need(len(exports) == len(manifest['exports']), 'unique stage exports')
    for row in exports.values():
        exact(codec.resolve(row['path'], [stage]), row)
    for row in load(d / 'reused_tools.json'):
        exact(d / row['path'], row)
    t = load(d / 'transport.json')
    policy = load(d / 'premises.json')
    need(policy == dict(root=t['root_acceptance'], premises=t['premises']), 'exact premise inventory')
    ar = Archive(stage, repo, t)
    closure = metadata(ar)
    packs = {r['path']: r for r in t['packs']}
    need(len(packs) == len(t['packs']), 'unique packs')
    need({str(p.relative_to(stage)) for p in (d / 'packs').rglob('*') if p.is_file()} == set(packs), 'complete physical pack inventory')
    for name, row in packs.items():
        need(exports.get(name) == row and 0 < row['bytes'] <= 48 * 2**20, 'bounded exact pack')
    public = {r['path']: r for r in t['existing_public_files']}
    need(len(public) == len(t['existing_public_files']), 'unique public reuse files')
    tracked = set(subprocess.run(['git', '-C', str(repo), 'ls-files', '-z'], check=True,
                                capture_output=True).stdout.decode().split('\0'))
    for name, row in public.items():
        need(name in tracked, 'reused content is tracked')
        exact(codec.resolve(name, [repo]), row)
    spans = {name: [] for name in packs}
    used_public = set()
    verified = decoded = 0
    for h, row in ar.objects.items():
        need(h == row['sha256'], 'object hash identity')
        if row['kind'] == 'NEW_PACKED_EXACT_CONTENT':
            for segment in row['segments']:
                need(segment['path'] in packs, 'declared new pack')
                spans[segment['path']].append((segment['offset'], segment['offset'] + segment['bytes']))
            roots = [stage]
        elif row['kind'] == 'EXISTING_PUBLIC':
            name = row['public_path']
            old = public[name]
            need(row['encoding'] == 'identity' and (row['bytes'], h) == (old['bytes'], old['sha256']), 'exact old complete object')
            need(row['segments'] == ([dict(path=name, offset=0, bytes=old['bytes'])] if old['bytes'] else []), 'complete old public file')
            used_public.add(name)
            roots = [repo]
        else:
            continue
        codec.verify(row, roots)
        verified += 1
        decoded += row['bytes']
    for name, ranges in spans.items():
        end = 0
        for lo, hi in sorted(ranges):
            need(lo == end and hi > lo, 'nonoverlapping exact pack coverage')
            end = hi
        need(end == packs[name]['bytes'], 'no unindexed packed bytes')
    need(used_public == set(public), 'no unused public declarations')
    args.out.mkdir()
    selected = args.out / 'selected'
    selected.mkdir()
    def select(original, name):
        dest=selected/name
        dest.parent.mkdir(parents=True,exist_ok=True)
        ar.extract(original,dest)
        return dest

    for name in ['proof_routes.json', 'source_arc_rows.json']:
        select(A+'/'+name,name)
    joined=module(select(A+'/check.py','assembly.py'),'accepted_L063_L064_assembly')
    ledgers=[ar.load(A+'/'+sid+'_claims.json') for sid in ['L063','L064']]
    for claims in ledgers: joined.ledger_check(claims)
    gates=ar.load(A+'/gates.json');need(len(gates)==11,'all eleven accepted gates')
    for row in gates:
        ar.exact(row['manifest'])
        need(ar.load(row['manifest']['path'])['status']==row['status'],'accepted distinct component gate')
    imports=ar.load(A+'/imports.json');need(len(imports)==20,'all twenty exact proof imports')
    for row in imports:
        ar.exact(row['source'])
        need(row['mode']=='EXACT' and ar.content(row['source']['path'])==ar.content(A+'/'+row['destination']['path']),'exact accepted proof import')
    deltas=ar.load(A+'/edition_deltas.json')
    need(deltas['accepted_proofs_modified'] is False and deltas['exact_accepted_proofs']==10,
         'ten frozen accepted proof editions unchanged')
    need(deltas['source_ledgers']==['L063_claims.json','L064_claims.json'] and deltas['new_markdown_files']==0,
         'two separate original ledgers without new Markdown paths')
    runs=[]
    def run(label,command,cwd=None,timeout=30):
        before=time.monotonic()
        result=subprocess.run(command,cwd=cwd,stdin=subprocess.DEVNULL,capture_output=True,timeout=timeout)
        (args.out/(label+'.stdout')).write_bytes(result.stdout);(args.out/(label+'.stderr')).write_bytes(result.stderr)
        runs.append(dict(label=label,command=command,returncode=result.returncode,seconds=time.monotonic()-before))
        need(result.returncode==0 and not result.stderr,'clean replay: '+label)
    principal=S+'/corpus106_PSL2_subfield_planes_v1'
    finite_reader=select(principal+'/finite.py','planes/finite.py')
    run('subfield_planes',[sys.executable,str(finite_reader),'--out',str(args.out/'subfield_planes.json')],timeout=60)
    need(load(args.out/'subfield_planes.json')==ar.load(principal+'/expected.json'),'exact four accepted field models')
    q9=F+'/q9_geometry'
    for name in ['check_duality.py','duality.json','doily.tex']:select(q9+'/'+name,'q9/'+name)
    run('duality',[sys.executable,str(selected/'q9/check_duality.py'),'--out',str(args.out/'duality.json')])
    need(load(args.out/'duality.json')==ar.load(q9+'/literal_check.json'),'exact accepted thirty-object duality')
    bounds=select(F+'/overgroups/finite_bounds.py','bounds/finite_bounds.py')
    run('finite_bounds',[sys.executable,str(bounds),'--out',str(args.out/'finite_bounds.json')])
    need(load(args.out/'finite_bounds.json')==ar.load(F+'/overgroups/finite_bounds.json'),'exact accepted elementary order bounds')
    damages=[]
    for name,index,mutation in [
        ('missing_source_claim',0,lambda d:d['claims'].pop()),
        ('ordered_convention',0,lambda d:d['source_scope_conventions'].update(unordered_parabolics=False)),
        ('new_principal_credit',1,lambda d:d.update(new_principal_refutation_credit=1)),
        ('false_recovery_credit',0,lambda d:d.update(ordinary_recovery_credit=1)),
        ('missing_auxiliary_correction',1,lambda d:next(r for r in d['claims'] if r['label']=='Lemma24 item2 PGL exclusion').update(status='RECOVERED')),
    ]:
        bad=copy.deepcopy(ledgers[index]);mutation(bad)
        try:joined.ledger_check(bad)
        except ValueError:damages.append(name)
        else:raise ValueError('damaged scope accepted')
    paper=stage/PAPER
    readable=['completion.tex','completion.pdf','complete.tex','complete.pdf',
              'L063_claims.json','L064_claims.json','edition_deltas.json','imports.json','parts.json','proof_routes.json','source_arc_rows.json']
    readable += [row['destination']['path'] for row in imports]
    for name in readable:exact(paper/name,ar.record(A+'/'+name))
    volume=PdfReader(paper/'complete.pdf');need(len(volume.pages)==52,'full readable volume')
    parts=ar.load(A+'/parts.json');need(len(parts)==11,'opening manuscript and ten exact proofs')
    offset=1
    for row in parts:
        doc=PdfReader(paper/row['path'])
        need(len(doc.pages)==row['pages'] and row['first_page']==offset+1,'complete component order and page count')
        for page in doc.pages:joined.embedded_page_check(page,volume.pages[offset]);offset+=1
    need(offset==52,'all fifty-one mathematical pages included')
    native_pages=0
    if args.render:
        native=args.out/'native';(native/'proofs').mkdir(parents=True)
        texbin,gs=shutil.which('pdflatex'),shutil.which('gs');need(texbin and gs,'native tools available')
        for name in readable:
            if name.endswith(('.tex','.pdf')):
                target=native/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(paper/name,target)
        for name in ['completion','complete']:
            tex=native/(name+'.tex')
            for n in [1,2]:run(tex.stem+'_tex'+str(n),[texbin,'-interaction=nonstopmode','-halt-on-error',tex.name],cwd=tex.parent)
            if name in ['completion','realizations','complete']:
                log=tex.with_suffix('.log').read_text();need('Overfull' not in log and 'undefined' not in log,'new native document warnings')
            need([p.extract_text() for p in PdfReader(paper/(name+'.pdf')).pages]==[p.extract_text() for p in PdfReader(tex.with_suffix('.pdf')).pages], 'native mathematical text unchanged')
        run('native_render',[gs,'-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r105','-sOutputFile='+str(native/'page-%02d.png'),str(native/'complete.pdf')],timeout=60)
        images=sorted(native.glob('page-*.png'),key=lambda p:int(p.stem.split('-')[1]));need(len(images)==52,'all fifty-two native pages')
        for n,path in enumerate(images,1):need(path.read_bytes()==ar.content(f'/private/tmp/psl2_source_synthesis_root01/complete-{n:02d}.png'),'exact accepted native raster')
        native_pages=len(images)
    run('codec_controls',[sys.executable,str(d/'codec_controls.py'),'--out',str(args.out/'codec_controls')])
    for flag in ['-O','-OO']:
        guard=subprocess.run([sys.executable,flag,str(d/'portable_check.py')],capture_output=True,timeout=10)
        need(guard.returncode!=0 and b'ordinary Python required' in guard.stderr,'portable optimization guard')
    report=dict(status='PASS_PORTABLE_L063_L064_SOURCE_COMPLETION',stage_manifest=pin(d/'manifest.json'),transport=pin(d/'transport.json'),root_acceptance=t['root_acceptance'],**closure,
                logical_files=len(ar.rows),unique_objects=len(ar.objects),verified_payload_objects=verified,verified_decoded_bytes=decoded,premise_objects=len(t['premises']),documentary_premise_occurrences=137,environment_premise_occurrences=116,existing_public_files=len(public),
                restored_selected_files=sum(f.is_file() for f in selected.rglob('*')),finite_field_models=4,duality_vertices=30,duality_edges=45,order_bound_cases=6,path_adapters=[],
                claim_damage_controls=damages,native_entry_points=2,retained_exact_proof_pairs=10,native_pages=native_pages,mathematical_pages=51,volume_pages=52,page_streams_and_font_programs_match=True,codec_controls=load(args.out/'codec_controls/report.json'),optimization_guards=2,
                source_claims={d['source_id']:len(d['claims']) for d in ledgers},new_group_acquisitions=0,principal_acquisition_repeated=False,ordinary_recovery_delta=0,principal_refutation_delta=0,surviving_claim_registration_delta=0,new_Lean=0,mathematical_compression_measurement=None,seconds=time.monotonic()-start,runs=runs)
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['runs','finite_results','path_adapters','codec_controls']}))

if __name__=='__main__':main()
