"""Verify all39 recorded double-proper ends by the reviewed q11 theorem.

Source only until Root review/admission. No search, exact-order engine,
permutation lift, original-weight transport or automatic adoption.
"""
import argparse
import ast
import fcntl
import hashlib
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time
from types import SimpleNamespace

HERE = Path(__file__).absolute().parent
THEORY = HERE.parent.parent/'theory'
SEARCH = dict(path=str(HERE/'search_prefix8_end_rejections.py'),bytes=18889,
    sha256='e63ef0bce9015003047b427ac87782e932bb83728293e29147b49c0191919233')
HELPERS = dict(path=str(HERE/'verify_indexed_frame_catalogue.py'),bytes=22496,
    sha256='1cebbda5fcda823b43713f03dd17893480c34d040f27501a0651ab69d8f496d3')
DOMAIN = dict(path=str(HERE/'cases/original_prefix8/output/result.json'),bytes=513255,
    sha256='e7124783eb2e9a5e1ca21c93d79a3e1ab1cf1460109b6ebc60dd451b5099c1f8')
EXPORT = dict(path=str(HERE.parent/'original_prefix8_matrix_export/indexed_prefix8_coordinates.json'),bytes=4345,
    sha256='6494e0d434e5b62a68d6966227e361bd3118c8afe936bc9900bd776924c2b8d6')
NORMAL = dict(path=str(HERE.parent/'cayley_normalization_acquisition/result.json'),bytes=10559,
    sha256='47c4f9848a304b7ca821db38271f85e672f29f241790a2203e2ace19307d25a1')
OLD_RESULT = dict(path=str(HERE/'cases/prefix8_end_rejections/output/result.json'),bytes=4886,
    sha256='d9d5dc7171a3659d278b4df05e63686125242ba2da17f98d84a3b5dad518d713')
OLD_JOURNAL = dict(path=str(HERE/'cases/prefix8_end_rejections/output/witnesses.jsonl'),bytes=191639,
    sha256='58a0c96fdbaec4fd3f0827f88b31ea5a985fd381c9ee5290b9c2918177cfedf8')
PARTIAL = dict(path=str(HERE/'cases/prefix8_end_rejections/root_partial_rejection_acceptance.json'),bytes=9314,
    sha256='bb7fab3d15834fac1ab12e8c41a966a48e16e5f1f6d24283315e4ab6d4479440')
GENERATION_ATTACHMENT = dict(path=str(HERE/'cases/prefix8_end_rejections/root_generation_source_attachment.json'),bytes=8398,
    sha256='3eb33961c12933b016e950b16c58175032b0f4b2c4e2b9bc3813de160a44bbf1')
PROOF = dict(path=str(THEORY/'double_unitary_end_intersection_obstruction.rst'),bytes=14424,
    sha256='d7e540f9ad61fbacf1f18ca1a184a0638581e6693a972a7705febd44e21c7126')
PROOF_REVIEW = dict(path=str(THEORY/'double_unitary_end_intersection_independent_review.rst'),bytes=4341,
    sha256='591ca8e3a02c9213789f926c8a4fd1f67b5672c0fdeb12f4e33a10f4009047f7')
GENERATION = dict(path=str(THEORY/'g2_11_generation_by_prime_witnesses.tex'),bytes=26437,
    sha256='f1b6c8a69780c7b8ac88f239627a7ce6889c24203f72ddc35c86fe93e661e76b')
MODEL = dict(path=str(THEORY/'acquired_cayley_full_group_bridge.rst'),bytes=9716,
    sha256='a754edb570ef9d30816c3897deeae2aec7958fb7cfb5fa756536ca8e0ab30801')
SCHEDULE_SOURCE = dict(path=str(HERE.parent/'matrix_end_certificate.g'),bytes=3831,
    sha256='d07cdbcaf1c25826e8917770adedec9b2ef4b159e13fe29c27181c88e17f137a')
READS = [SEARCH,HELPERS,DOMAIN,EXPORT,NORMAL,OLD_RESULT,OLD_JOURNAL,PARTIAL,
    GENERATION_ATTACHMENT,PROOF,PROOF_REVIEW,GENERATION,MODEL,SCHEDULE_SOURCE]
NAMES = ['peak_bytes','source_bytes','pin_bytes','borrowed_helpers','schedule','multiply',
    'power','pure7','end_letters','evaluate_word','verify_end37']
BORROWED = ['need','canonical','shape','exact','vec','mat','ident','scale','row','mm',
    'nullspace','mul2','bar2','det2','inv2','operator','jpair']
WORK_SECONDS,TOTAL_SECONDS,RSS_CAP,OUTPUT_CAP = 90,100,128*2**20,256*2**10


def require(value,message):
    if not value: raise ValueError(message)


def borrowed(tick):
    """Only unchanged whole definitions; neither predecessor main is loaded."""
    p=Path(SEARCH['path']);a=p.lstat()
    require(stat.S_ISREG(a.st_mode)and a.st_nlink==1 and a.st_size==SEARCH['bytes']<=65536,
        'ordinary exact predecessor Source')
    with p.open('rb')as f:
        if sys.platform=='darwin':fcntl.fcntl(f.fileno(),48,1)
        b=os.fstat(f.fileno());raw=f.read(65537);z=os.fstat(f.fileno())
    sig=lambda q:(q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns)
    require(sig(a)==sig(b)==sig(z)==sig(p.lstat())and len(raw)==a.st_size
        and hashlib.sha256(raw).hexdigest()==SEARCH['sha256'],'stable whole predecessor Source')
    tree=ast.parse(raw);nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in NAMES]
    require([n.name for n in nodes]==NAMES,'exact eleven whole definitions')
    names=next(n.value for n in tree.body if isinstance(n,ast.Assign)
        and any(isinstance(t,ast.Name)and t.id=='BORROWED'for t in n.targets))
    require(ast.literal_eval(names)==BORROWED,'unchanged seventeen arithmetic/IO names')
    scope=dict(__name__='prefix8_double_proper_whole_defs',__file__=SEARCH['path'],
        Path=Path,stat=stat,sys=sys,os=os,fcntl=fcntl,hashlib=hashlib,json=json,resource=resource,
        time=time,ast=ast,SimpleNamespace=SimpleNamespace,HELPERS=HELPERS,BORROWED=BORROWED)
    exec(compile(ast.Module(body=nodes,type_ignores=[]),SEARCH['path']+'::<whole_definitions>','exec'),scope)
    W=SimpleNamespace(**{name:scope[name]for name in NAMES})
    return W,W.borrowed_helpers(tick)


def decode(raw):
    def pairs(values):
        result={}
        for k,v in values:
            require(k not in result,'unique journal JSON key');result[k]=v
        return result
    return json.loads(raw,object_pairs_hook=pairs,
        parse_constant=lambda s:(_ for _ in()).throw(ValueError('nonfinite '+s)))


def checkpoint(fact,words,B):
    B.need(type(fact)is list and len(fact)==3 and type(fact[0])is int
        and 1<=fact[0]<=len(words)and fact[1]=='PROPER','whole recorded proper37 checkpoint')
    B.vec(fact[2],7)
    return words[fact[0]-1]


def partition(records,old,gate,reps,words,B,tick):
    """Derive all39 from the whole accepted535 unpaid list, never select them."""
    B.need(type(records)is list and len(records)==3779,'all complete old journal records')
    unpaid=[];selected=[];rejected=0
    for rep,record in zip(reps,records):
        B.need(type(record)is list and len(record)>=2 and type(record[0])is int
            and record[0]==rep,'exact original ordered journal representatives')
        if record[1]=='UNPAID':
            B.need(len(record)==4,'complete old unpaid row');unpaid.append(rep)
            for fact in record[2:]:
                if fact is not None:checkpoint(fact,words,B)
            if all(fact is not None for fact in record[2:]):selected.append(record)
        else:
            B.need(record[1]in('PREFIX_MEMBER','ADJACENT_LE2','END37'),'borrowed accepted rejection tag')
            rejected+=1
        tick()
    B.need(unpaid==old['unresolved_visited_orbits']==gate['unpaid_orbits']and len(unpaid)==535
        and rejected==old['rejected_orbits']==gate['rejected_orbits']==3244
        and len(selected)==39,'exact complete39/535 partition against Root acceptance')
    selected_reps={record[0]for record in selected}
    remaining=[rep for rep in unpaid if rep not in selected_reps]
    B.need(len(selected_reps)==39 and len(remaining)==496,'exact remaining unpaid complement')
    return selected,remaining


def main():
    began=time.monotonic()
    require(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,
        'ordinary isolated Python -E -B')
    ap=argparse.ArgumentParser(allow_abbrev=False,description=__doc__)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--journal',type=Path,required=True)
    args=ap.parse_args();paths=[args.output,args.journal]
    require(len(set(paths))==2 and all(p.is_absolute()and not os.path.lexists(p)
        and p.parent.resolve(strict=True)==p.parent and stat.S_ISDIR(p.parent.lstat().st_mode)
        for p in paths),'two fresh distinct files in existing ordinary absolute parents')
    def final_tick():
        value=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        peak=value if sys.platform=='darwin'else value*1024
        require(time.monotonic()-began<TOTAL_SECONDS and peak<RSS_CAP,'shared100s/observed128MiB bound')
    def tick():
        final_tick();require(time.monotonic()-began<WORK_SECONDS,'90s verification reserve')
    W,B=borrowed(tick)
    program_raw=W.source_bytes(__file__,65536);program=W.pin_bytes(__file__,program_raw)
    for ref in(PROOF,PROOF_REVIEW,GENERATION,MODEL,SCHEDULE_SOURCE,GENERATION_ATTACHMENT):
        B.exact(ref,tick,65536)
    domain=B.exact(DOMAIN,tick,2**20,True);export=B.exact(EXPORT,tick,65536,True)
    normal=B.exact(NORMAL,tick,65536,True);old=B.exact(OLD_RESULT,tick,65536,True)
    gate=B.exact(PARTIAL,tick,65536,True);raw=B.exact(OLD_JOURNAL,tick,256*2**10)
    B.need(domain['schema']=='F004_Q11_INDEXED_CAYLEY_CENTRALIZER_DOMAIN_CERTIFICATE_V1'
        and domain['status']=='VERIFIED_CAYLEY_FRAME_AND_AUTOMORPHISM_DOMAIN'
        and domain['certificate_verified']is True and domain['rank']==4
        and domain['original_job']==[8,4]and domain['original_prefix_index']==8
        and domain['selected_labels']==[1,4,2]and domain['prefix_export']==EXPORT
        and domain['normalization_result']==NORMAL and domain['model_bridge_source']==MODEL
        and domain['external_premises']['original_A_equals_G']is True,'one acquired original prefix8 domain')
    B.need(export['schema']=='F004_Q11_INDEXED_ORIGINAL_PREFIX_MATRICES_V1'
        and export['original_job']==[8,4]and export['original_prefix_index']==8 and export['rank']==4
        and export['selected_labels']==[1,4,2]and export['end_order']==[1,4,2,3]
        and export['convention']=='RIGHT_ROW'and export['origin']==domain['origin']
        and export['external_premises']==domain['external_premises'],'whole ordered actual prefix export')
    B.need(normal['certificate_verified']is True and normal['kappa']==7,'same acquired normalization')
    B.need(gate['root']=='/root'and gate['status']=='ROOT_ACCEPTED_QUALIFIED_PARTIAL_PREFIX8_MATRIX_REJECTIONS'
        and gate['domain']==DOMAIN and gate['result']==OLD_RESULT and gate['journal']==OLD_JOURNAL
        and gate['generation_source_attachment']==GENERATION_ATTACHMENT
        and gate['original_job']==[8,4]and gate['original_prefix_index']==8
        and gate['completed_orbits']==3779 and gate['unvisited_orbits']==[]and gate['prefix_complete']is False
        and gate['original_root_roster_omission_preserved']is True
        and gate['retroactive_root_roster_freshness_claimed']is False,'qualified Root partial premise preserved')
    B.need(old['schema']=='F004_PREFIX8_MATRIX_REJECTION_PASS_V1'
        and old['status']=='INCOMPLETE_WITH_EXPLICIT_UNPAID_ORBITS'and old['program']==SEARCH
        and old['domain']==DOMAIN and old['journal']==OLD_JOURNAL and old['original_job']==[8,4]
        and old['original_prefix_index']==8 and old['total_orbits']==old['completed_orbits']==3779
        and old['started_orbits']==3779 and old['total_raw_domain']==14763
        and old['unvisited_orbits']==[]and old['stop']is None,'complete old partial result, not an interrupted search')
    lines=raw.splitlines(keepends=True)
    B.need(len(lines)==3780 and all(line.endswith(b'\n')and len(line)<=16384 for line in lines),
        'whole LF-framed journal, no unfinished record')
    header=decode(lines[0]);records=[decode(line)for line in lines[1:]];words=W.schedule()
    B.need(header['schema']=='F004_PREFIX8_MATRIX_REJECTION_WITNESS_JOURNAL_V1'
        and header['program']==SEARCH and header['domain']==DOMAIN and header['original_export']==EXPORT
        and header['original_job']==[8,4]and header['original_prefix_index']==8
        and header['word_schedule_source']==SCHEDULE_SOURCE and header['word_schedule']==list(words)
        and header['word_power']==3 and header['prime']==37
        and GENERATION in header['direct_inputs'],'exact retained word encoding and current theorem Source')
    values=domain['catalogue'];orbits=domain['orbits']
    B.need(len(values)==domain['catalogue_size']==domain['selected_raw_domain_size']==14763
        and hashlib.sha256(B.canonical(values)).hexdigest()==domain['catalogue_sha256']
        and domain['selected_raw_domain_indices']==list(range(1,14764))and len(orbits)==3779
        and domain['endpoint_group_order']==288 and domain['prefix_stabilizer_order']==4,
        'same entire acquired finite domain')
    seen=set();reps=[]
    for orbit in orbits:
        B.need(type(orbit)is list and len(orbit)==4,'whole acquired orbit row')
        rep,indices,transporters,stabilizer=orbit
        B.need(type(rep)is int and type(indices)is list and indices and indices==sorted(set(indices))
            and rep==min(indices)and not seen.intersection(indices)
            and all(type(j)is int and 1<=j<=14763 for j in indices)
            and len(indices)==len(transporters)and len(indices)*stabilizer==4,'complete disjoint orbit identities')
        seen.update(indices);reps.append(rep);tick()
    B.need(seen==set(range(1,14764))and reps==sorted(reps),'whole once-only acquired cover')
    selected,remaining=partition(records,old,gate,reps,words,B,tick)
    r=B.mat(domain['standard_to_actual_row_map'],8);ir=B.mat(domain['actual_to_standard_row_map'],8)
    q=B.mat(normal['quadratic_form_matrix'],8)
    B.need(W.multiply(r,ir,B,tick)==W.multiply(ir,r,B,tick)==B.ident(8),'full inverse coordinate maps')
    a,e,b=[W.pure7(B.mat(m,8),r,ir,q,B,tick)for m in domain['standard_ordered_prefix_matrices']]
    prefix=[B.mat(m,7)for m in export['matrices']];identity=B.ident(7)
    B.need([a,e,b]==prefix and len(set(prefix))==3
        and all(m!=identity and W.multiply(m,m,B,tick)==identity for m in prefix)
        and W.multiply(a,e,B,tick)==W.multiply(e,a,B,tick)
        and W.multiply(b,e,B,tick)==W.multiply(e,b,B,tick),'whole actual prefix marks and distant commutations')
    journal_bytes=0;verified=[]
    with args.journal.open('xb')as journal:
        def append(record):
            nonlocal journal_bytes
            data=B.canonical(record)+b'\n'
            B.need(len(data)<=16384 and journal_bytes+len(data)<=OUTPUT_CAP,'whole bounded witness output')
            B.need(journal.write(data)==len(data),'whole journal write');journal.flush();journal_bytes+=len(data)
        append(dict(schema='F004_PREFIX8_DOUBLE_PROPER_WITNESSES_V1',program=program,domain=DOMAIN,
            original_export=EXPORT,old_journal=OLD_JOURNAL,partial_acceptance=PARTIAL,
            proof=PROOF,proof_review=PROOF_REVIEW,generation_source=GENERATION,
            original_job=[8,4],original_prefix_index=8,derived_rows=[x[0]for x in selected],
            old_unpaid_count=535,required_count=39,direct_inputs=READS,candidate_credit=0,census_credit=0))
        os.fsync(journal.fileno())
        for record in selected:
            rep=record[0];standard=B.operator(*B.jpair(values[rep-1]));c=W.pure7(standard,r,ir,q,B,tick)
            B.need(c!=identity and W.multiply(c,c,B,tick)==identity and a!=c and b!=e
                and W.multiply(a,c,B,tick)==W.multiply(c,a,B,tick),
                'all four nonidentity involutions, distinct commuting endpoint pairs')
            facts=[]
            for end,old_fact in zip(((a,b,c),(b,c,e)),record[2:]):
                text=checkpoint(old_fact,words,B);fact=W.verify_end37(end,text,B,tick)
                B.need(fact==old_fact[1:]and fact is not None and fact[0]=='PROPER',
                    'actual word exact37 and every end generator preserves the same nonzero pure line')
                facts.append(dict(checkpoint=old_fact[0],word=text,verified_fact=fact))
            append(dict(representative=rep,rejection='DOUBLE_PROPER_UNITARY_END_INTERSECTION',
                left=facts[0],right=facts[1],all_mark_hypotheses_checked=True,
                middle='<b,c>',end_type_from_written_theorem='SU3(11):2',
                end_size_formula='2*11^3*(11^3+1)*(11^2-1)',
                middle_order_upper_bound=264,intersection_order_strictly_greater_than=480))
            verified.append(rep);tick()
        journal.flush();os.fsync(journal.fileno())
    B.need(verified==[record[0]for record in selected]and len(verified)==39,'all39 required, no clipping or partial credit')
    for ref in READS:B.exact(ref,final_tick,2**20)
    B.need(W.source_bytes(__file__,65536)==program_raw,'whole current worker Source unchanged')
    journal_raw=W.source_bytes(args.journal,OUTPUT_CAP)
    result=dict(schema='F004_PREFIX8_DOUBLE_PROPER_CERTIFICATE_V1',status='VERIFIED_ALL39_DOUBLE_PROPER_END_REJECTIONS',
        program=program,domain=DOMAIN,original_export=EXPORT,old_result=OLD_RESULT,old_journal=OLD_JOURNAL,
        partial_acceptance=PARTIAL,proof=PROOF,proof_review=PROOF_REVIEW,generation_source=GENERATION,
        journal=W.pin_bytes(args.journal,journal_raw),original_job=[8,4],original_prefix_index=8,
        newly_verified_representatives=verified,new_rejected_orbits=39,old_rejected_orbits_preserved=3244,
        remaining_unpaid_orbits=remaining,remaining_unpaid_count=496,prefix_complete=False,
        scientific_direct_inputs=READS,scientific_direct_inputs_reauthenticated=True,
        exact_end_order_algorithm_executed=False,subgroup_closure_executed=False,permutation_weights_reproved=False,
        candidate_credit=0,census_credit=0,whole_original_credit=0,root_adoption=None,
        worker_limits=dict(verification_seconds=WORK_SECONDS,total_seconds=TOTAL_SECONDS,rss_bytes=RSS_CAP,
            combined_output_bytes=OUTPUT_CAP),outer_profile_required=dict(rss_mib=256,seconds=150),
        seconds=time.monotonic()-began,peak_self_bytes=W.peak_bytes(),
        qualification='Written q11 theorem applied only after all39 actual two-word proper37 and mark checks. '
        'Old3244 accepted rejections remain borrowed;496 orbits stay unpaid. Natural model/A/original lifts, '
        'orbit transports/weights, Source/runtime/closure and independent actual review remain Root duties. '
        'No partial output is a certificate and no original job, prefix or census is closed.')
    data=B.canonical(result)+b'\n';B.need(journal_bytes+len(data)<=OUTPUT_CAP,'combined256KiB output, never truncate')
    final_tick()
    with args.output.open('xb')as f:B.need(f.write(data)==len(data),'whole fresh final certificate');f.flush();os.fsync(f.fileno())
    print(B.canonical(dict(status=result['status'],new_rejected_orbits=39,remaining_unpaid_orbits=496,
        output=W.pin_bytes(args.output,data),candidate_credit=0,census_credit=0)).decode())


if __name__=='__main__':main()
