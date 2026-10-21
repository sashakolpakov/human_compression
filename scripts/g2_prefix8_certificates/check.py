"""Public-only F004 prefix8 integrity and selected certificate replay.

Historical absolute paths are exact logical labels, never filesystem fallbacks.
No old Root/native execution, classification, weights or whole-paper claim is
recreated. This Source is uninvoked pending independent portability review.
"""
import argparse,ast,contextlib,hashlib,io,json,os,resource,stat,sys,time
from pathlib import Path,PurePosixPath

START=time.monotonic()
DATA='data/g2_prefix8_certificates/'
PROGRAM='scripts/g2_prefix8_certificates/check.py'
DOCUMENT_CAP=2**21
FILE_COUNT_CAP=256
INPUT_BYTES_CAP=32*2**20
SECONDS=100
RSS_CAP=128*2**20
OLD='/Users/sasha/medusa/research/leemans/computation/f004/small_inventory_work/cayley_centralizer_certificate/'
SCIENCE={
    'proper230':dict(path=OLD+'verify_prefix8_saved_proper_end_certificates.py',bytes=42657,sha256='edf45f69269c5a1c86f7ad5bc3f851b95160851f96aca813fae9d896175ed1cb'),
    'common118':dict(path=OLD+'verify_prefix8_remaining_line_and_intersection.py',bytes=50627,sha256='803888c1283f1b1cc9d90f8827273afa58d4b2bee4616134b9db0bb0e8c2fb95')}
GATES={
    'proper230':dict(path=OLD+'cases/prefix8_saved230_independent_verification/root_saved230_acceptance.json',bytes=13438,sha256='803e958b0e0b5cfb89adf47e8be7fed35bfec36d8a876ee6835b2d1c3a05d651'),
    'common118':dict(path=OLD+'cases/prefix8_remaining_line_and_intersection/root_certificate_acceptance.json',bytes=20169,sha256='ab4ef4b7a8c704b7fc898f272035c16c5e6d294c43acba7fb6b134f41776ee53')}
HISTORICAL_PROOF_ROLES=('independent_actual_review','independent_actual_execution',
    'terminal','clearance','late_root_workflow','adoption_source_packet',
    'adoption_source_review','adoption_source_execution','method','source_authentication','source_packet')
PUBLIC_READER="""def read_exact(ref,budget,work=True):
    refcheck(ref);budget.check(work)
    raw=PORTABLE_READ(ref)
    budget.check(work);return raw"""
SELF_BEFORE="""    source_path=Path(__file__).absolute();self_stat=source_path.lstat()
    need(self_stat.st_size<=65536,'bounded current verifier Source')
    with source_path.open('rb')as f:self_raw=f.read(65537)
    self_ref=file_pin(source_path,self_raw);read_exact(self_ref,budget)"""
SELF_AFTER="""    source_path=Path(__file__).absolute();self_ref=PORTABLE_SOURCE_REF
    need(str(source_path)==self_ref['path']and self_ref['bytes']<=65536,'exact borrowed Source label and bound')
    self_raw=read_exact(self_ref,budget)"""

def need(ok,message):
    if not ok:raise ValueError(message)

def tick():
    peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform!='darwin':peak*=1024
    need(time.monotonic()-START<SECONDS and peak<RSS_CAP,'observed100s/128MiB portable check')

def canonical(v):
    return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()

def decode(raw):
    def pairs(rows):
        d={}
        for k,v in rows:need(k not in d,'duplicate JSON key');d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in()).throw(ValueError(x)))

def refcheck(q):
    need(type(q)is dict and set(q)=={'path','bytes','sha256'}and type(q['path'])is str
         and type(q['bytes'])is int and 0<=q['bytes']<=DOCUMENT_CAP
         and type(q['sha256'])is str and len(q['sha256'])==64
         and all(c in'0123456789abcdef'for c in q['sha256']),'complete bounded exact pin')

class Archive:
    def __init__(self,root,manifest,manifest_sha):
        self.root=Path(root).absolute();self.reads=set()
        need(self.root.resolve(strict=True)==self.root,'canonical public root')
        manifest_ref=dict(path=manifest,bytes=self.local(manifest).lstat().st_size,sha256=manifest_sha)
        self.manifest_ref=manifest_ref;self.m=decode(self.exact(manifest_ref))
        m=self.m
        need(m['schema']=='F004_PREFIX8_PORTABLE_CERTIFICATE_COMPONENT_V1'
             and m['scope']=='CONDITIONAL_SELECTED230_AND118_CERTIFICATES'
             and m['private_path_fallback']is False and m['whole_original_credit']==0,
             'exact partial component boundary')
        self.files={q['path']:q for q in m['files']}
        need(len(self.files)==len(m['files'])<=FILE_COUNT_CAP
             and sum(q['bytes']for q in self.files.values())<=INPUT_BYTES_CAP,'finite whole publication readset')
        need(PROGRAM in self.files and self.exact(self.files[PROGRAM])==Path(__file__).read_bytes()
             and Path(__file__).absolute()==self.local(PROGRAM),'actual public adapter identity')
        for q in self.files.values():self.exact(q)
        self.labels={}
        for row in m['logical_sources']:
            need(set(row)=={'original','public_path','role'},'logical Source row')
            q=row['original'];refcheck(q)
            need(Path(q['path']).is_absolute()and str(Path(q['path']))==q['path']
                 and '..'not in Path(q['path']).parts and q['path']not in self.labels,'unique exact historical label')
            public=self.files.get(row['public_path'])
            need(public is not None and(q['bytes'],q['sha256'])==(public['bytes'],public['sha256']),
                 'same actual original/public bytes, never hash-only payload')
            self.labels[q['path']]=row
        for key in('proper230','common118'):
            route=m['routes'][key]
            need(route['source_program']==SCIENCE[key]and m['accepted'][key]['gate']==GATES[key],
                 'fixed acquired mathematical Sources and acceptance identities')
            for q in route['inputs']+[route['source_program']]:self.bound(q)
        need(len(m['mathematical_core'])==50 and sum(q['bytes']for q in m['mathematical_core'])==3005088,
             'unchanged exact50 mathematical closure')
        core={q['path']:q for q in m['mathematical_core']}
        need(len(core)==50 and m['routes']['common118']['inputs']==m['mathematical_core']
             and all(core.get(q['path'])==q for q in m['routes']['proper230']['inputs']),
             'old47 is subset of same50; executable Source roles separate')
        need(hashlib.sha256(canonical(m['mathematical_core'])).hexdigest()=='cf75762a65a50b3718c3cd9577002acd5444b363a364c41700765bb1a23a90b1',
             'exact unchanged50 tuple identity')
        self.originals_unchanged={q['path']:q for q in self.files.values()}

    def local(self,name):
        need(type(name)is str,'literal relative public path')
        q=PurePosixPath(name)
        need(not q.is_absolute()and str(q)==name and '..'not in q.parts
             and(name.startswith(DATA)or name==PROGRAM),'allowlisted component path')
        p=self.root.joinpath(*q.parts)
        need(all(not x.is_symlink()for x in(p,*p.parents))and p.resolve(strict=True)==p,
             'ordinary public path, no private or symlink fallback')
        return p

    def exact(self,q):
        refcheck(q);tick();p=self.local(q['path']);a=p.lstat()
        sig=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
        need(stat.S_ISREG(a.st_mode)and a.st_nlink==1 and a.st_size==q['bytes'],'ordinary exact public file')
        with p.open('rb')as f:
            if sys.platform=='darwin':
                import fcntl
                fcntl.fcntl(f.fileno(),48,1)
            b=os.fstat(f.fileno());raw=f.read(q['bytes']+1);z=os.fstat(f.fileno())
        need(sig(a)==sig(b)==sig(z)==sig(p.lstat())and len(raw)==q['bytes']
             and hashlib.sha256(raw).hexdigest()==q['sha256'],'stable complete exported bytes')
        self.reads.add(q['path']);tick();return raw

    def bound(self,q):
        refcheck(q);row=self.labels.get(q['path'])
        need(row is not None and row['original']==q,'declared logical label and complete original pin')
        return self.files[row['public_path']]

    def content(self,q):return self.exact(self.bound(q))
    def document(self,q):return decode(self.content(q))

    def unchanged(self):
        self.exact(self.manifest_ref)
        for q in self.originals_unchanged.values():self.exact(q)

def metadata(ar):
    m=ar.m;a=m['accepted']['proper230'];b=m['accepted']['common118']
    g1=ar.document(a['gate']);g2=ar.document(b['gate'])
    r1=ar.document(a['result']);r2=ar.document(b['result'])
    need(g1['root']==g2['root']=='/root'and g1['status']=='ROOT_ACCEPTED_PREFIX8_SAVED230_INDEPENDENT_CERTIFICATES'
         and g2['status']=='ROOT_ACCEPTED_PREFIX8_COMMON_LINE_AND_INTERSECTION_CERTIFICATES','genuine accepted component labels')
    need(g1['program']==m['routes']['proper230']['source_program']and g2['program']==m['routes']['common118']['source_program'],
         'same unchanged mathematical Source roles')
    need(g1['result']==a['result']and g1['journal']==a['journal']and g2['result']==b['result']and g2['journal']==b['journal'],
         'exact accepted result/journal bindings')
    x=g1['newly_rejected_orbits'];y=g2['newly_rejected_orbits'];unpaid=g2['unpaid_orbits']
    for values,n in((x,230),(y,118),(unpaid,148)):
        need(type(values)is list and len(values)==n and values==sorted(set(values))
             and all(type(i)is int and 1<=i<=14763 for i in values),'exact finite accepted identities')
    need(not set(x)&set(y)and not(set(x)|set(y))&set(unpaid)
         and sorted(y+unpaid)==g1['unpaid_orbits'],'disjoint selected sets and exact148 unpaid complement')
    need(g1['old_rejected_orbits']==3283 and g1['total_rejected_orbits']==3513
         and g2['old_rejected_orbits']==3513 and g2['total_rejected_orbits']==3631,
         'borrowed3283 plus230 plus118; no re-acquired history')
    need(r1['newly_verified_representatives']==x and r2['newly_verified_representatives']==y
         and r1['new_rejected_orbits']==230 and r2['new_rejected_orbits']==118,
         'accepted membership matches exact mathematical reports')
    need(g1['prefix_complete']is g2['prefix_complete']is False
         and all(g['whole_original_credit']==0 for g in(g1,g2)),'no whole prefix/original credit')
    for key,gate in(('proper230',g1),('common118',g2)):
        need(set(m['accepted'][key]['historical_proofs'])==set(HISTORICAL_PROOF_ROLES),
             'complete explicitly selected historical proof roles')
        for role,q in m['accepted'][key]['historical_proofs'].items():
            need(gate[role]==q,'exact selected historical proof role')
            ar.bound(q)
    return dict(status='PASS_PUBLIC_INPUT_AND_ACCEPTED_METADATA_INTEGRITY_ONLY',
        accepted_prior_borrowed=3283,accepted230=230,accepted118=118,total_rejected=3631,
        unpaid=148,mathematical_predicates_replayed=False,full_model_reidentified=False,
        original_weights_reproved=False,whole_original_credit=0)

def transported(ar,key):
    route=ar.m['routes'][key];q=route['source_program'];raw=ar.content(q);text=raw.decode()
    inv=route['transport'];before=text
    read_nodes=[n for n in ast.parse(before).body if isinstance(n,ast.FunctionDef)and n.name=='read_exact']
    need(len(read_nodes)==1,'one whole borrowed IO reader')
    required=[dict(before=ast.get_source_segment(before,read_nodes[0]),after=PUBLIC_READER,count=1),
              dict(before=SELF_BEFORE,after=SELF_AFTER,count=1)]
    need(inv['edits']==required,'only the two explicit public IO transport edits; no arbitrary main change')
    for e in inv['edits']:
        need(text.count(e['before'])==e['count'],'one exact IO Source transport site')
        text=text.replace(e['before'],e['after'])
    back=text
    for e in reversed(inv['edits']):
        need(back.count(e['after'])==e['count'],'invertible IO Source transport')
        back=back.replace(e['after'],e['before'])
    need(back==before and hashlib.sha256(text.encode()).hexdigest()==inv['effective_sha256'],
         'whole borrowed Source inverse; no mathematical edit')
    original=ast.parse(before);current=ast.parse(text)
    def definitions(t,s):
        return{n.name:ast.get_source_segment(s,n)for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))and n.name not in('read_exact','main')}
    need(definitions(original,before)==definitions(current,text),'all mathematical helper bodies unchanged')
    allowed={x['path']:x for x in route['inputs']+[q]}
    def portable_read(ref):
        need(allowed.get(ref['path'])==ref,'selected route exact readset, no private/undeclared fallback')
        return ar.content(ref)
    scope=dict(__name__='f004_portable_borrowed_mathematical_body',__file__=q['path'],
        PORTABLE_READ=portable_read,PORTABLE_SOURCE_REF=q)
    exec(compile(text,q['path']+'::explicit-public-IO-edition','exec',dont_inherit=True),scope)
    return scope

def selected_replay(ar,key,out):
    route=ar.m['routes'][key];scope=transported(ar,key)
    journal=out/'witnesses.jsonl';result=out/'mathematical_result.json'
    old_argv=sys.argv
    capture=io.StringIO()
    try:
        sys.argv=[PROGRAM,'--output',str(result),'--journal',str(journal)]
        with contextlib.redirect_stdout(capture):scope['main']()
    finally:sys.argv=old_argv
    need(len(capture.getvalue().encode())<=16384,'bounded borrowed-body stdout')
    data=result.read_bytes();witnesses=journal.read_bytes()
    need(len(data)<=32768 and len(data)+len(witnesses)<=256*2**10,'unchanged combined mathematical output cap')
    current=decode(data);accepted=ar.document(ar.m['accepted'][key]['result'])
    need(current['program']==route['source_program']and current['newly_verified_representatives']==accepted['newly_verified_representatives']
         and current['rejection_type_counts']==accepted['rejection_type_counts'],
         'complete selected accepted certificate set; misses/stops never confer a PASS')
    need(current['word_search_executed']is False and current['root_adoption']is None
         and current['candidate_credit']==current['census_credit']==current['whole_original_credit']==0,
         'replay only; no new search, adoption or original credit')
    if key=='common118':
        need(current['stop']is None and current['optional_pair_proposals']is None and current['supplied_word_pair_count']==0
             and current['stored_line_proposal_rows']==128,'only old untrusted line proposals; no new supplied search')
    return dict(status='PASS_SELECTED_MATHEMATICAL_CERTIFICATE_REPLAY',selected=key,
        execution_program=ar.files[PROGRAM],borrowed_mathematical_source=route['source_program'],
        borrowed_program_field_is_semantic_source_role=True,old_private_CLI_claimed_executed=False,
        reverified=len(current['newly_verified_representatives']),accepted_prior_borrowed=3283,
        full_model_reidentified=False,original_weights_reproved=False,whole_original_credit=0,
        result=dict(path=str(result),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()),
        journal=dict(path=str(journal),bytes=len(witnesses),sha256=hashlib.sha256(witnesses).hexdigest()),
        borrowed_body_stdout=capture.getvalue())

def main():
    ap=argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--manifest',required=True)
    ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--mode',choices=['metadata','proper230','common118'],required=True)
    a=ap.parse_args()
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,'ordinary isolated Python -E -B')
    need(len(a.manifest_sha256)==64 and all(c in'0123456789abcdef'for c in a.manifest_sha256),'explicit manifest SHA')
    root=a.repo.absolute();out=a.out.absolute()
    need(out==a.out and out.parent.resolve(strict=True)==out.parent and not os.path.lexists(out)
         and not out.is_relative_to(root),'fresh external output child')
    ar=Archive(root,a.manifest,a.manifest_sha256);integrity=metadata(ar)
    out.mkdir()
    result=integrity if a.mode=='metadata'else selected_replay(ar,a.mode,out)
    ar.unchanged();result.update(manifest=ar.manifest_ref,mode=a.mode,public_files_authenticated=len(ar.files),
        historical_paths_are_labels_only=True,private_fallback=False,
        imported_premises=ar.m['imported_premises'],whole_original_credit=0)
    data=canonical(result)+b'\n';need(len(data)<=128*2**10,'complete bounded public report')
    with(out/'report.json').open('xb')as f:need(f.write(data)==len(data),'exclusive whole public report')
    print(data.decode(),end='')

if __name__=='__main__':main()
