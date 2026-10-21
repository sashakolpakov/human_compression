"""Public-only replay of the bounded O'Nan map-count correction."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not accepted')
sys.dont_write_bytecode=True
from pathlib import Path,PurePosixPath
import argparse,copy,csv,hashlib,importlib.util,json,os,re,shutil,subprocess
HERE=Path(__file__).resolve().parent
BASE='corrections/onan-map-count/v1'
EDITION='Ars Mathematica Contemporanea 10 (2016), 211–222; published online 24 September 2015'
CONVENTION='Ordered generating pairs under Aut(G), p<=q, precisely the source formula (2.4); no additional equal-type duality quotient'
PACKETS={'proof':'d7e826cec742417d68173aa748de3b6b44b6a348d63cd6fc85394ff5bd279919','independent_review':'76572289d9f351b7d73eb01ffd029b1ae0870a3d66fd1dc62a8de4dc726408d9','common':'fb3672cceb3087ad73cf32bc99e6d9276d90170c94cef0f215ccb6ae81c1745f','common_review':'3b5fd80efd187845ff3a58d96d0875fa3e73c48c9d3fe20dd389a106161616b9'}
def need(ok,msg):
    if not ok:raise ValueError(msg)
def load(path):return json.loads(path.read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def local(name):
    p=PurePosixPath(name);need(not p.is_absolute()and'..'not in p.parts,'unsafe relative path')
    q=(HERE/p).resolve();need(q.is_relative_to(HERE),'path escaped correction');return q
def bind(path,r):need(path.is_file()and path.stat().st_size==r['bytes']and sha(path)==r['sha256'],'changed public binding '+str(path))
def semantic(source,proposal,remaining):
    need(source['original_id']=='L046'and source['edition']==EDITION,'fixed edition')
    need(source['source_pdf_sha256']=='412775233715c6d925377a9588cf98e7af7491c4041789a29dfeb34b7dd36812','fixed source hash')
    need(source['source_convention']==CONVENTION,'count convention')
    need(source['source_claimed_total']==796772 and source['proved_lower_total']==798370,'total bound')
    need(source['corrected_cell']==dict(p=20,q=31,source=7246,proved=9118),'exact cell')
    need(not source['exact_total_claimed'],'lower bound is not exact total')
    need(proposal['classification']=='PRINCIPAL_NUMERICAL_ASSERTION_REFUTED_WITH_VALID_PRINCIPAL_OBLIGATIONS_PENDING','bounded disposition')
    for key in ['ordinary_recovery_credit','terminal_principal_disposition_credit','handled_original_credit','new_measurement_credit','new_question_credit','new_Lean_credit']:need(proposal[key]==0,'unearned '+key)
    for key in ['whole_paper_recovered','all_L046_work_finished','root_is_distinct_mathematical_reviewer','current_catalogue_mutated']:need(proposal[key]is False,'unsupported '+key)
    need(proposal['compression_factor']is proposal['software_inclusive_factor']is None,'unearned compression factor')
    need(remaining['status']=='L046_REMAINS_PENDING_COMPLETE_PRINCIPAL_RECOVERY'and remaining['keep_in_accessible_pending_original_ids']is True,'must remain pending')
    need(remaining['remaining_exact_table_cells']==116 and not remaining['exact_full_total_known'],'remaining exact counts')
    need(remaining['zero_types_not_excluded_by_this_component']==[[3,4],[3,5],[3,6],[3,7],[3,12],[4,4]],'remaining zero types')
    need(len(remaining['remaining_principal_claims'])==6 and 'chirality'in remaining['remaining_principal_claims'][-1],'remaining chirality scope')
    need(not remaining['whole_paper_recovered']and not remaining['all_L046_work_finished'],'remaining work')
def main(a):
    out=a.out.resolve();need(not out.is_relative_to(HERE),'output must be outside correction');out.mkdir(parents=True,exist_ok=False)
    if(HERE/'manifest.json').exists():
        for r in load(HERE/'manifest.json')['exports']:bind(local(r['path']),r)
    t=load(HERE/'transport.json');need(t['base_public_path']==BASE,'transport root');mapping={};primary=[];environment=[]
    for r in t['files']:
        logical=r['logical_path'];need(logical not in mapping,'duplicate logical binding');mapping[logical]=r
        if r['transport']=='PRIMARY_SOURCE_HASH_ONLY':
            need(logical.startswith('sources/')or(PurePosixPath(logical).suffix=='.png'and PurePosixPath(logical).name.startswith('source-')),'non-source omitted');primary.append(logical)
        elif r['transport']=='EXTERNAL_SOFTWARE_OR_DATA_HASH_ONLY':
            need(logical.startswith('environment:/opt/homebrew/Cellar/gap/4.15.1/'),'undeclared environment omission');environment.append(logical)
        else:
            need(r['transport']=='EXACT_PUBLIC_COPY','unsupported transport kind')
            public=PurePosixPath(r['public_path']);need(public.is_relative_to(PurePosixPath(BASE)),'public route outside correction');bind(local(str(public.relative_to(BASE))),r)
    need(len(mapping)==226 and len(primary)==10 and len(environment)==117,'frozen transport boundary')
    exports=0;dependency_records=0
    for packet in t['complete_packets']:
        route=str(PurePosixPath(packet['public_directory']).relative_to(BASE));d=local(route)
        need(route in PACKETS and sha(d/'manifest.json')==PACKETS[route]==packet['manifest_sha256'],'exact accepted edition')
        manifest=load(d/'manifest.json');need(len(manifest['exports'])==packet['exports'],'complete packet exports')
        for r in manifest['exports']:bind(local(route+'/'+r['path']),r);exports+=1
        deps=load(d/'dependencies.json')
        for r in deps.get('bindings',[])+deps.get('installed_software',[]):
            name=r.get('absolute_path',r.get('path'))
            if name.startswith('/Users/sasha/medusa/research/leemans/'):name=name[len('/Users/sasha/medusa/research/leemans/'):]
            elif name.startswith('/'):name='environment:'+name
            need(name in mapping and all(mapping[name][k]==r[k]for k in ['bytes','sha256']),'missing dependency closure '+name);dependency_records+=1
    need(len(t['complete_packets'])==4,'four complete packets')
    source=load(HERE/'source_statement.json');proposal=load(HERE/'admission_proposal.json');remaining=load(HERE/'remaining_obligations.json');semantic(source,proposal,remaining)
    controls=[]
    mutations=[('false ordinary recovery','proposal','ordinary_recovery_credit',1),('terminal refutation original','proposal','terminal_principal_disposition_credit',1),('handled original','proposal','handled_original_credit',1),('new question','proposal','new_question_credit',1),('Lean','proposal','new_Lean_credit',1),('factor','proposal','compression_factor',2),('whole paper','proposal','whole_paper_recovered',True),('all work finished','proposal','all_L046_work_finished',True),('wrong convention','source','source_convention','unordered pairs'),('exact total','source','exact_total_claimed',True),('drop remaining counts','remaining','remaining_exact_table_cells',0),('remove pending','remaining','keep_in_accessible_pending_original_ids',False),('wrong count','source','proved_lower_total',796772)]
    for label,target,key,value in mutations:
        ss,pp,rr=copy.deepcopy((source,proposal,remaining));{'source':ss,'proposal':pp,'remaining':rr}[target][key]=value
        try:semantic(ss,pp,rr)
        except ValueError:controls.append(label)
        else:raise ValueError('negative scope control accepted '+label)
    gap=a.gap or shutil.which('gap');need(gap is not None,'Install GAP with CTblLib for fresh table extraction')
    env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';runs=[]
    scripts=[('proof/maximal_vectors.g','proof/maximal_vectors.g.stdout','COMPLETE EXACT ORDER VECTORS'),('proof/maximal_controls.g','proof/maximal_controls.g.stdout','COMPLETE MAXIMAL UNION CONTROLS'),('independent_review/class_constants.g','independent_review/class_constants.stdout','COMPLETE DISTINCT CLASS CONSTANT COUNTS'),('common/character_probe.g','common/expected/character_probe.g.stdout','COMPLETE ON CHARACTER AND INVERSION PROBE'),('common/incidence_control.g','common/expected/incidence_control.g.stdout','COMPLETE ALL SUBGROUP INCIDENCE CONTROLS')]
    for i,(script,expected,marker)in enumerate(scripts):
        p=subprocess.run([str(gap),'-q','-b',str(local(script))],cwd=out,env=env,capture_output=True,timeout=60)
        (out/f'run{i}.stdout').write_bytes(p.stdout);(out/f'run{i}.stderr').write_bytes(p.stderr)
        need(p.returncode==0 and not p.stderr and p.stdout.decode().count(marker)==1,'GAP complete clean execution '+script)
        # The frozen common checker used text=True (universal newlines).
        # Retain raw stdout, but reproduce that exact declared output contract.
        compared=p.stdout
        if script.startswith('common/'):
            compared=p.stdout.decode().replace('\r\n','\n').replace('\r','\n').encode()
            (out/f'run{i}.normalized.stdout').write_bytes(compared)
        need(compared==local(expected).read_bytes(),'fresh exact output '+script);runs.append(script)
    spec=importlib.util.spec_from_file_location('reviewed_bounds',local('proof/bounds.py'));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    tables,maxes=module.read_vectors((out/'run0.stdout').read_text());bounds=module.derive(tables,maxes)
    need(bounds==load(local('proof/bounds.json')),'fresh exact interval ledger')
    independent=load(local('independent_review/independent_report.json'))
    for new,old in zip(bounds['rows'],independent['integer_intervals']):need(all(new[k]==old[k]for k in old),'independent interval match')
    constant_keys=set()
    for line in(out/'run2.stdout').read_text().splitlines():
        parts=line.split()
        if not parts or parts[0]!='COUNT':continue
        _,name,p,q,n=parts;p,q,n=map(int,[p,q,n]);need(module.all_count(tables[name],p,q)==n,'class constant mismatch');constant_keys.add((name,p,q))
    need(len(constant_keys)==574,'complete independent class counts')
    sourcevals={(x['p'],x['q']):x['source_count']for x in load(local('proof/source_table1.json'))['rows']}
    need(len(sourcevals)==136 and sum(sourcevals.values())==796772,'source literal table')
    differences=[(x['p'],x['q'])for x in bounds['rows']if not x['lower']<=sourcevals[x['p'],x['q']]<=x['upper']];need(differences==[(20,31)],'exact source discrepancy')
    with(HERE/'results.csv').open(newline='')as f:flat=list(csv.DictReader(f))
    need(len(flat)==136,'reader table coverage')
    for r,b in zip(flat,bounds['rows']):
        need([int(r[k])for k in ['p','q','proved_lower','proved_upper']]==[b['p'],b['q'],b['lower'],b['upper']],'reader table exact')
        need(int(r['source_count'])==sourcevals[b['p'],b['q']],'reader source exact')
    native_pages={}
    if a.render:
        from pypdf import PdfReader
        tex=shutil.which('pdflatex');need(tex is not None,'pdflatex required for native replay')
        for route,stem in [('proof','maximal_bounds'),('common','generating_pairs')]:
            native=out/('native_'+route);native.mkdir()
            for i in [1,2]:
                p=subprocess.run([tex,'-interaction=nonstopmode','-halt-on-error','-output-directory',str(native),stem+'.tex'],cwd=local(route),env=env,capture_output=True,timeout=60)
                (native/f'build{i}.stdout').write_bytes(p.stdout);(native/f'build{i}.stderr').write_bytes(p.stderr);need(p.returncode==0 and not p.stderr,'native execution')
            old=PdfReader(local(route+'/'+stem+'.pdf'));new=PdfReader(native/(stem+'.pdf'));need(len(old.pages)==len(new.pages)==4,'complete native pages')
            need([p.extract_text()for p in old.pages]==[p.extract_text()for p in new.pages],'native text unchanged');need('Overfull'not in(native/(stem+'.log')).read_text(),'native overflow');native_pages[route]=4
    report=dict(status='PASS_PUBLIC_L046_BOUNDED_NUMERICAL_CORRECTION',complete_packets=4,complete_packet_exports=exports,logical_bindings=226,dependency_records=dependency_records,primary_hash_only=10,external_software_or_data_hash_only=117,private_source_files_read=False,private_mathematical_proof_fallback=False,installed_GAP_CTblLib_used=True,historical_absolute_software_paths_read=False,fresh_GAP_programs=runs,independent_class_constant_counts=574,lower_total=bounds['lower_total'],source_total=796772,corrected_cell=dict(p=20,q=31,source=7246,proved=9118),positive_types=129,exact_type_counts=20,remaining_exact_type_counts=116,full_chirality_unpaid=True,L046_remains_pending=True,ordinary_recovery_credit=0,terminal_principal_disposition_credit=0,handled_original_credit=0,new_measurement_credit=0,new_question_credit=0,new_Lean_credit=0,compression_factor=None,scope_controls=controls,native_pages=native_pages,public_catalogue_mutated=False)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);parser.add_argument('--gap',type=Path);parser.add_argument('--render',action='store_true');main(parser.parse_args())
