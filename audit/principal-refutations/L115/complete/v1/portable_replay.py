"""Replay exact acquired mathematical readers from selected portable bytes."""
from pathlib import Path
import importlib.util,json,subprocess,sys,time
sys.dont_write_bytecode=True
S='/Users/sasha/medusa/research/leemans';Z=S+'/geometry/suzuki_subgroups';A=Z+'/principal_v2'
def need(v,s):
    if not v:raise ValueError(s)
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def replay(ar,out):
    start=time.monotonic();local=out/'selected';local.mkdir();selected={}
    def extract(original):
        need(original.startswith(S+'/'),'selected study object')
        dest=local/original[len(S)+1:]
        if original not in selected:ar.extract(original,dest);selected[original]=dest
        return dest
    def load(original):return ar.load(original)
    # The original modules retain their relative directory layout and are
    # imported without executing their private filesystem-acquisition mains.
    for relative in ['principal_v2/check.py','numerical_table_work/prime_certificates.py',
                     'numerical_table_partial_v1/audit.py','numerical_table_complete_v1/audit.py',
                     'numerical_table_work/gp_work/protocol.py','diagram_application_v1/join.py']:
        extract(Z+'/'+relative)
    assembly=module('portable_source_assembly',extract(A+'/check.py'))
    arithmetic=module('portable_complete_arithmetic',extract(Z+'/numerical_table_complete_v1/audit.py'))
    cert=arithmetic.old.cert
    previous=load(Z+'/numerical_table_partial_v1/author_prime_counts.json')
    for row in previous:
        original=Z+'/numerical_table_work/factor_proposals01/e%02d_%s.json'%(row['e'],row['kind'])
        record=load(original);verified=cert.verify_factor_record(record)
        need(verified['integer']==row['integer'] and verified['factors']==row['factors']
             and verified['distinct_prime_factors']==row['verified_prime_count'],'same prior literal factor')
    g=Z+'/numerical_table_work/gp_work'
    new=arithmetic.protocol.parse(ar.content(Z+'/numerical_table_work/factor_proposals02_gp/stdout'),
                                 load(g+'/base_certificates.json'),load(g+'/targets.json'))
    need(new==load(Z+'/numerical_table_complete_v1/author01/gp_literal.json'),'entire exact new literal arithmetic result')
    source=load(Z+'/numerical_table_request_distinct_review/source_audit01.json')['rows']
    factors,geometry=arithmetic.join(new,previous,source)
    need(factors==load(A+'/table12_prime_counts.json') and geometry==load(A+'/table12_comparison.json'),
         'all 180 factors and 60 exact numerical substitutions')
    # Independently revalidate the accepted failed/clean historical bindings by
    # content identity. They do not cause any producer to run.
    for original in [Z+'/numerical_table_work/factor_proposals01/receipt.json',
                     Z+'/numerical_table_work/factor_proposals02_gp/receipt.json']:
        receipt=load(original)
        need(receipt['returncode']==0 and receipt['resource_stop']is None and receipt['inputs_unchanged'],
             'accepted clean arithmetic proposal receipt')
        for q in receipt['inputs']+receipt['outputs']:ar.exact(q)
    # Run the unmodified finite reader on retained pair and graph certificates.
    method=Z+'/diagram_method_v2'
    for name in ['read_certificates.py','pairs.py','graphs.py','finite_actions.py',
                 'inputs01/elements.bin','inputs01/groups.json']:extract(method+'/'+name)
    proposal=Z+'/diagram_proposal02/proposal'
    proposal_files=[p for p in ar.originals if p.startswith(proposal+'/')]
    need(proposal_files,'actual retained diagram proposal')
    for original in proposal_files:extract(original)
    report=out/'diagrams.json'
    command=[sys.executable,'-B',str(extract(method+'/read_certificates.py')),'--input',str(local/proposal[len(S)+1:]),'--out',str(report)]
    with(out/'diagrams.stdout').open('wb')as so,(out/'diagrams.stderr').open('wb')as se:
        result=subprocess.run(command,stdin=subprocess.DEVNULL,stdout=so,stderr=se,timeout=180)
    need(result.returncode==0 and not(out/'diagrams.stderr').read_bytes(),'clean literal graph reader')
    diagrams=json.loads(report.read_text());expected=load(A+'/certified_diagrams.json')
    for key,value in diagrams.items():
        if key!='seconds':need(value==expected[key],'entire literal diagram output: '+key)
    source_diagrams=load(A+'/printed_diagrams.json')
    joiner=module('portable_diagram_join',extract(Z+'/diagram_application_v1/join.py'))
    joined=joiner.join(source_diagrams,diagrams);old_join=load(A+'/diagram_comparison.json')
    need(all(value==old_join[key]for key,value in json.loads(json.dumps(joined)).items()),'exact complete source diagram join after JSON key normalization')
    claims=load(A+'/source_claims.json');imports=load(A+'/proof_imports.json')
    semantic=assembly.semantic(claims,geometry,source_diagrams,diagrams,imports)
    controls=assembly.controls(claims,geometry,source_diagrams,diagrams,imports)
    lemma=next(r for r in claims['claims']if r['label']=='Lemma6.1')
    need(lemma['kind']=='rank_greater_than_one_obstruction','exact corrected source rank domain')
    return dict(status='PASS_PORTABLE_L115_MATHEMATICAL_READERS',certified_integers=len(factors),
         certified_primes=new['known_primes'],numerical_rows=len(geometry),diagrams=29,inner_classes=75,
         source_claims=semantic['claims'],source_damage_controls=controls['damage_checks'],
         selected_files=len(selected),selected_bytes=sum(p.stat().st_size for p in selected.values()),
         new_group_searches=0,new_factorizations=0,reader_command=command,seconds=time.monotonic()-start)
