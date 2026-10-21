"""Bounded proper19 split/mixed certificates on the adopted496 complement.

Source only until distinct review/controls/Root admission. A moved19 line
is unpaid, never FULL_G2. No order engine, old main, or automatic adoption.
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

HERE=Path(__file__).absolute().parent
THEORY=HERE.parent.parent/'theory'
SEARCH=dict(path=str(HERE/'search_prefix8_end_rejections.py'),bytes=18889,sha256='e63ef0bce9015003047b427ac87782e932bb83728293e29147b49c0191919233')
HELPERS=dict(path=str(HERE/'verify_indexed_frame_catalogue.py'),bytes=22496,sha256='1cebbda5fcda823b43713f03dd17893480c34d040f27501a0651ab69d8f496d3')
DOMAIN=dict(path=str(HERE/'cases/original_prefix8/output/result.json'),bytes=513255,sha256='e7124783eb2e9a5e1ca21c93d79a3e1ab1cf1460109b6ebc60dd451b5099c1f8')
EXPORT=dict(path=str(HERE.parent/'original_prefix8_matrix_export/indexed_prefix8_coordinates.json'),bytes=4345,sha256='6494e0d434e5b62a68d6966227e361bd3118c8afe936bc9900bd776924c2b8d6')
NORMAL=dict(path=str(HERE.parent/'cayley_normalization_acquisition/result.json'),bytes=10559,sha256='47c4f9848a304b7ca821db38271f85e672f29f241790a2203e2ace19307d25a1')
OLD_RESULT=dict(path=str(HERE/'cases/prefix8_end_rejections/output/result.json'),bytes=4886,sha256='d9d5dc7171a3659d278b4df05e63686125242ba2da17f98d84a3b5dad518d713')
OLD_JOURNAL=dict(path=str(HERE/'cases/prefix8_end_rejections/output/witnesses.jsonl'),bytes=191639,sha256='58a0c96fdbaec4fd3f0827f88b31ea5a985fd381c9ee5290b9c2918177cfedf8')
PARTIAL=dict(path=str(HERE/'cases/prefix8_end_rejections/root_partial_rejection_acceptance.json'),bytes=9314,sha256='bb7fab3d15834fac1ab12e8c41a966a48e16e5f1f6d24283315e4ab6d4479440')
GENERATION_ATTACHMENT=dict(path=str(HERE/'cases/prefix8_end_rejections/root_generation_source_attachment.json'),bytes=8398,sha256='3eb33961c12933b016e950b16c58175032b0f4b2c4e2b9bc3813de160a44bbf1')
PROOF=dict(path=str(THEORY/'double_unitary_end_intersection_obstruction.rst'),bytes=14424,sha256='d7e540f9ad61fbacf1f18ca1a184a0638581e6693a972a7705febd44e21c7126')
PROOF_REVIEW=dict(path=str(THEORY/'double_unitary_end_intersection_independent_review.rst'),bytes=4341,sha256='591ca8e3a02c9213789f926c8a4fd1f67b5672c0fdeb12f4e33a10f4009047f7')
GENERATION=dict(path=str(THEORY/'g2_11_generation_by_prime_witnesses.tex'),bytes=26437,sha256='f1b6c8a69780c7b8ac88f239627a7ce6889c24203f72ddc35c86fe93e661e76b')
MODEL=dict(path=str(THEORY/'acquired_cayley_full_group_bridge.rst'),bytes=9716,sha256='a754edb570ef9d30816c3897deeae2aec7958fb7cfb5fa756536ca8e0ab30801')
SCHEDULE_SOURCE=dict(path=str(HERE.parent/'matrix_end_certificate.g'),bytes=3831,sha256='d07cdbcaf1c25826e8917770adedec9b2ef4b159e13fe29c27181c88e17f137a')
PRIOR_PROGRAM=dict(path=str(HERE/'verify_prefix8_double_proper_ends.py'),bytes=18457,sha256='2481375f2203fda2920289ce9b15c02c2a3f081bd58ea625da267b4607d2f0d7')
PRIOR_GATE=dict(path=str(HERE/'cases/prefix8_double_proper_ends/root_double_proper_acceptance.json'),bytes=10008,sha256='cc7bedda717a6bb757185fdf22f73c4efaa0871e540e21f5ba890ef253ae9b94')
PRIOR_RESULT=dict(path=str(HERE/'cases/prefix8_double_proper_ends/output/result.json'),bytes=9816,sha256='ec933e426cffddaca7d44b4cc76dee7f3ed3426334f18ce2e6bb39d1f68c1a20')
PRIOR_JOURNAL=dict(path=str(HERE/'cases/prefix8_double_proper_ends/output/witnesses.jsonl'),bytes=25935,sha256='7222493162a76defebcfafd0cdd82c377155153d86a501d5e747f57291864320')
PRIOR_AUTHORITY=dict(path=str(HERE/'cases/prefix8_double_proper_ends/root_adoption_source_authentication.json'),bytes=717911,sha256='80706683a676867f7ea8be15de26c4241978171e8b1d6cc8a36ff74f6869512f')
SPLIT_PROOF=dict(path=str(THEORY/'split_and_unitary_end_intersection_obstruction.rst'),bytes=14302,sha256='c8d38efd6049367e7caad1e07f5fe93275108b6e2ef112e9d436dc578177a9db')
SPLIT_ROOT_REVIEW=dict(path=str(THEORY/'split_and_unitary_end_intersection_root_review.rst'),bytes=3432,sha256='0cfae243663fc710b5581ece4ab02366c831a067fa6121dbf8ca95523c85b113')
SPLIT_UNIT_REVIEW=dict(path=str(THEORY/'split_and_unitary_end_intersection_independent_review.rst'),bytes=6801,sha256='9feeff10defddf990b76114f90e78e4191f55d3ee9c34851ca6f86fdb8a85ce6')
NORMALIZER_SOURCE=dict(path=str(HERE.parent/'verify_cayley_normalization.py'),bytes=10508,sha256='ad8030d47175e58bd22fee6030f7b12a804076b42deaa707774c3eabd2957a67')
READS=[SEARCH,HELPERS,DOMAIN,EXPORT,NORMAL,OLD_RESULT,OLD_JOURNAL,PARTIAL,
 GENERATION_ATTACHMENT,PROOF,PROOF_REVIEW,GENERATION,MODEL,SCHEDULE_SOURCE,
 PRIOR_PROGRAM,PRIOR_GATE,PRIOR_RESULT,PRIOR_JOURNAL,PRIOR_AUTHORITY,
 SPLIT_PROOF,SPLIT_ROOT_REVIEW,SPLIT_UNIT_REVIEW,NORMALIZER_SOURCE]
NAMES=['peak_bytes','source_bytes','pin_bytes','borrowed_helpers','schedule','multiply',
 'power','pure7','end_letters','evaluate_word','verify_end37']
BORROWED=['need','canonical','shape','exact','vec','mat','ident','scale','row','mm',
 'nullspace','mul2','bar2','det2','inv2','operator','jpair']
WORK_SECONDS,TOTAL_SECONDS,RSS_CAP,OUTPUT_CAP=90,100,128*2**20,2**20
MAX_RECORD,REPORT_RESERVE=16384,65536


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


class SearchBudgetStop(RuntimeError):
    pass


def framed(raw,count,B):
    lines=raw.splitlines(keepends=True)
    B.need(len(lines)==count and all(x.endswith(b'\n')and len(x)<=MAX_RECORD for x in lines),
        'whole LF-framed accepted journal')
    values=[decode(line)for line in lines]
    B.need(all(B.canonical(v)+b'\n'==line for v,line in zip(values,lines)),'canonical whole accepted records')
    return values


def partition(records,reps,old,partial,prior,gate,prior_records,words,B,tick):
    B.need(len(records)==len(reps)==3779,'whole accepted original representative order')
    unpaid=[];selected=[];old_paid=[]
    for rep,record in zip(reps,records):
        B.need(type(record)is list and len(record)>=2 and type(record[0])is int and record[0]==rep,
            'one complete accepted representative')
        if record[1]=='UNPAID':
            B.need(len(record)==4,'whole old unpaid record');unpaid.append(record)
            for fact in record[2:]:
                if fact is not None:checkpoint(fact,words,B)
            if all(fact is not None for fact in record[2:]):selected.append(record)
        else:
            B.need(record[1]in('PREFIX_MEMBER','ADJACENT_LE2','END37'),'borrowed accepted old rejection')
            old_paid.append(rep)
        tick()
    unpaid_reps=[r[0]for r in unpaid];selected_reps=[r[0]for r in selected]
    B.need(unpaid_reps==old['unresolved_visited_orbits']==partial['unpaid_orbits']and len(unpaid)==535
        and len(old_paid)==old['rejected_orbits']==partial['rejected_orbits']==3244,'whole accepted old535/3244')
    B.need(len(selected)==len(prior_records)==39 and selected_reps==prior['newly_verified_representatives']==gate['newly_rejected_orbits'],
        'all39 actually verified/adopted, not a prospective pin')
    for before,after in zip(selected,prior_records):
        B.need(after['representative']==before[0]and after['rejection']=='DOUBLE_PROPER_UNITARY_END_INTERSECTION'
            and after['all_mark_hypotheses_checked']is True,'whole accepted39 journal identity')
        for fact,previous in zip((after['left'],after['right']),before[2:]):
            B.need(fact['checkpoint']==previous[0]and fact['word']==checkpoint(previous,words,B)
                and fact['verified_fact']==previous[1:],'accepted39 whole checkpoint/fact joins')
    remaining=[r for r in unpaid if r[0]not in set(selected_reps)]
    B.need([r[0]for r in remaining]==prior['remaining_unpaid_orbits']==gate['unpaid_orbits']and len(remaining)==496,
        'exact currently adopted496 complement')
    B.need(not(set(old_paid)&set(selected_reps)or set(old_paid)&{r[0]for r in remaining}),
        'old3244 and new39 and remaining496 disjoint')
    return remaining


def verify19(end,text,q,W,B,tick):
    """Positive proper split fact, or unpaid diagnostic; never FULL_G2."""
    word=W.evaluate_word(text,W.end_letters(end,B,tick),B,tick)
    y=W.power(word,7,B,tick);identity=B.ident(7)
    if y==identity or W.power(y,19,B,tick)!=identity:return None
    equations=[[(y[i][j]-int(i==j))%11 for i in range(7)]for j in range(7)]
    basis=B.nullspace(equations,7)
    B.need(len(basis)==1,'unique actual pure19 fixed line, not unital8')
    v=basis[0];v=B.scale(pow(next(x for x in v if x),-1,11),v)
    B.need(any(v)and B.row(v,y)==v,'whole normalized pure19 fixed witness')
    for k,h in enumerate(end):
        vh=B.row(v,h)
        for i in range(7):
            for j in range(i+1,7):
                if(v[i]*vh[j]-v[j]*vh[i])%11:
                    return ['MOVED19_UNPAID',list(v),k,[i,j]]
    # q is exactly47c's Q=diag(1,7*beta), NOT beta or the polar2Q.
    # pure7 already returns ACTUAL coordinates; no additional R acts on v.
    v8=(0,*v);tick();norm=sum(x*z for x,z in zip(B.row(v8,q),v8))%11;tick()
    root=next((r for r in range(1,11)if r*r%11==(-norm)%11),None)
    if norm==0 or root is None:return ['LINE_TYPE_UNPAID',list(v),norm]
    B.need(root*root%11==(-norm)%11,'explicit split quadratic square witness')
    return ['PROPER19',list(v),norm,root]


def search19(end,words,q,W,B,tick):
    letters=W.end_letters(end,B,tick);word=B.ident(7);last=0
    for number,text in enumerate(words,1):
        for k in text[last:]:word=W.multiply(word,letters[ord(k)-ord('1')],B,tick)
        last=len(text);y=W.power(word,7,B,tick)
        if y!=B.ident(7)and W.power(y,19,B,tick)==B.ident(7):
            fact=verify19(end,text,q,W,B,tick)
            B.need(fact is not None,'independent whole proposed19 word reevaluation')
            # Unique pure19 fixed line plus a moved generator rules out only
            # this common-line leg. J1 remains; no FULL or IP rejection follows.
            return dict(kind=fact[0],checkpoint=number,word=text,power=7,prime=19,fact=fact[1:])
    return dict(kind='NO19_WITNESS_UNPAID',checkpoints=len(words))


def end_fact(end,old_fact,words,q,W,B,tick):
    if old_fact is None:return search19(end,words,q,W,B,tick)
    text=checkpoint(old_fact,words,B);fact=W.verify_end37(end,text,B,tick)
    B.need(fact==old_fact[1:]and fact is not None and fact[0]=='PROPER',
        'actual acquired37 sideword reevaluated, never a tag-only U premise')
    return dict(kind='PROPER37',checkpoint=old_fact[0],word=text,power=3,prime=37,fact=fact[1:])


def main():
    began=time.monotonic()
    require(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,'ordinary isolated Python -E -B')
    ap=argparse.ArgumentParser(allow_abbrev=False,description=__doc__)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--journal',type=Path,required=True)
    args=ap.parse_args();paths=[args.output,args.journal]
    require(len(set(paths))==2 and all(p.is_absolute()and not os.path.lexists(p)
        and p.parent.resolve(strict=True)==p.parent and stat.S_ISDIR(p.parent.lstat().st_mode)for p in paths),
        'two fresh distinct output files in ordinary existing absolute parents')
    def final_tick():
        peak=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform!='darwin':peak*=1024
        if time.monotonic()-began>=TOTAL_SECONDS or peak>=RSS_CAP:
            raise SearchBudgetStop('shared100s/observed128MiB bound; retained partial never closes rows')
    def tick():
        final_tick()
        if time.monotonic()-began>=WORK_SECONDS:raise SearchBudgetStop('90s work reserve within same100s total')
    W,B=borrowed(tick);program_raw=W.source_bytes(__file__,65536);program=W.pin_bytes(__file__,program_raw)
    docs={}
    decoded={DOMAIN['path'],EXPORT['path'],NORMAL['path'],OLD_RESULT['path'],PARTIAL['path'],PRIOR_GATE['path'],PRIOR_RESULT['path']}
    for ref in READS:
        value=B.exact(ref,tick,2**20,ref['path']in decoded)
        if ref['path']in decoded:docs[ref['path']]=value
    domain,export,normal,old,partial,gate,prior=[docs[x['path']]for x in(DOMAIN,EXPORT,NORMAL,OLD_RESULT,PARTIAL,PRIOR_GATE,PRIOR_RESULT)]
    B.need(domain['schema']=='F004_Q11_INDEXED_CAYLEY_CENTRALIZER_DOMAIN_CERTIFICATE_V1'
        and domain['status']=='VERIFIED_CAYLEY_FRAME_AND_AUTOMORPHISM_DOMAIN'and domain['certificate_verified']is True
        and domain['rank']==4 and domain['original_job']==[8,4]and domain['original_prefix_index']==8
        and domain['selected_labels']==[1,4,2]and domain['prefix_export']==EXPORT and domain['normalization_result']==NORMAL
        and domain['model_bridge_source']==MODEL and domain['external_premises']['original_A_equals_G']is True,
        'actual natural Cayley/A=G original prefix8 domain')
    B.need(export['schema']=='F004_Q11_INDEXED_ORIGINAL_PREFIX_MATRICES_V1'and export['original_job']==[8,4]
        and export['original_prefix_index']==8 and export['rank']==4 and export['selected_labels']==[1,4,2]
        and export['end_order']==[1,4,2,3]and export['convention']=='RIGHT_ROW'
        and export['origin']==domain['origin']and export['external_premises']==domain['external_premises'],
        'whole original ordered export and origin premises')
    B.need(normal['certificate_verified']is True and normal['kappa']==7
        and normal['coordinates']=='[scalar,v0,v1,v2,v3,v4,v5,v6]; right row coordinates'
        and normal['quadratic_matrix_convention']=='N(x)=x*Q*transpose(x); full polar matrix=2*Q',
        'actual canonical normalization scale/convention, never beta or polar form')
    B.need(partial['root']=='/root'and partial['status']=='ROOT_ACCEPTED_QUALIFIED_PARTIAL_PREFIX8_MATRIX_REJECTIONS'
        and partial['domain']==DOMAIN and partial['result']==OLD_RESULT and partial['journal']==OLD_JOURNAL
        and partial['generation_source_attachment']==GENERATION_ATTACHMENT and partial['prefix_complete']is False,
        'old qualified3244/535 premise preserved')
    B.need(gate['schema']=='ROOT_F004_PREFIX8_DOUBLE_PROPER_ACCEPTANCE_V1'and gate['root']=='/root'
        and gate['status']=='ROOT_ACCEPTED_PREFIX8_DOUBLE_PROPER_END_REJECTIONS'
        and gate['domain']==DOMAIN and gate['result']==PRIOR_RESULT and gate['journal']==PRIOR_JOURNAL
        and gate['source_authentication']==PRIOR_AUTHORITY and gate['prior_partial_acceptance']==PARTIAL
        and gate['proof']==PROOF and gate['proof_review']==PROOF_REVIEW and gate['original_job']==[8,4]
        and gate['original_prefix_index']==8 and gate['new_rejected_orbits']==39 and gate['old_rejected_orbits']==3244
        and gate['total_rejected_orbits']==3283 and gate['unvisited_orbits']==[]and gate['prefix_complete']is False
        and gate['original_root_roster_omission_preserved']is True and gate['retroactive_root_roster_freshness_claimed']is False,
        'genuinely Root-adopted39 and full inherited Source authority')
    B.need(prior['schema']=='F004_PREFIX8_DOUBLE_PROPER_CERTIFICATE_V1'and prior['status']=='VERIFIED_ALL39_DOUBLE_PROPER_END_REJECTIONS'
        and prior['program']==PRIOR_PROGRAM and prior['domain']==DOMAIN and prior['original_export']==EXPORT
        and prior['old_result']==OLD_RESULT and prior['old_journal']==OLD_JOURNAL and prior['journal']==PRIOR_JOURNAL
        and prior['partial_acceptance']==PARTIAL and prior['proof']==PROOF and prior['proof_review']==PROOF_REVIEW
        and prior['original_job']==[8,4]and prior['original_prefix_index']==8 and prior['new_rejected_orbits']==39
        and prior['old_rejected_orbits_preserved']==3244 and prior['remaining_unpaid_count']==496 and prior['prefix_complete']is False,
        'whole actual39 result, no hypothetical case')
    B.need(old['program']==SEARCH and old['domain']==DOMAIN and old['journal']==OLD_JOURNAL
        and old['status']=='INCOMPLETE_WITH_EXPLICIT_UNPAID_ORBITS'and old['total_orbits']==old['completed_orbits']==3779
        and old['unvisited_orbits']==[]and old['stop']is None,'complete original accepted journal')
    old_values=framed(B.exact(OLD_JOURNAL,tick,256*2**10),3780,B)
    previous=framed(B.exact(PRIOR_JOURNAL,tick,65536),40,B);words=W.schedule()
    old_header=old_values[0];prior_header=previous[0]
    B.need(old_header['program']==SEARCH and old_header['domain']==DOMAIN and old_header['original_export']==EXPORT
        and old_header['original_job']==[8,4]and old_header['original_prefix_index']==8
        and old_header['word_schedule_source']==SCHEDULE_SOURCE and old_header['word_schedule']==list(words)
        and old_header['word_power']==3 and old_header['prime']==37,'exact unchanged40 checkpoint word schedule')
    B.need(prior_header['schema']=='F004_PREFIX8_DOUBLE_PROPER_WITNESSES_V1'and prior_header['program']==PRIOR_PROGRAM
        and prior_header['domain']==DOMAIN and prior_header['partial_acceptance']==PARTIAL and prior_header['old_journal']==OLD_JOURNAL,
        'accepted39 complete journal header')
    values=domain['catalogue'];orbits=domain['orbits'];seen=set();reps=[]
    B.need(len(values)==domain['catalogue_size']==domain['selected_raw_domain_size']==14763
        and hashlib.sha256(B.canonical(values)).hexdigest()==domain['catalogue_sha256']
        and domain['selected_raw_domain_indices']==list(range(1,14764))and len(orbits)==3779
        and domain['endpoint_group_order']==288 and domain['prefix_stabilizer_order']==4,'whole acquired catalogue/orbit domain')
    for rep,indices,transporters,stabilizer in orbits:
        B.need(type(rep)is int and indices and indices==sorted(set(indices))and rep==min(indices)
            and not seen.intersection(indices)and all(type(j)is int and 1<=j<=14763 for j in indices)
            and len(indices)==len(transporters)and len(indices)*stabilizer==4,'complete once-only accepted orbit identities')
        seen.update(indices);reps.append(rep);tick()
    B.need(seen==set(range(1,14764))and reps==sorted(reps),'entire accepted raw cover')
    remaining=partition(old_values[1:],reps,old,partial,prior,gate,previous[1:],words,B,tick)
    r=B.mat(domain['standard_to_actual_row_map'],8);ir=B.mat(domain['actual_to_standard_row_map'],8)
    q=B.mat(normal['quadratic_form_matrix'],8);identity=B.ident(7)
    B.need(q[0]==(1,0,0,0,0,0,0,0)and all(q[i][0]==0 for i in range(1,8)),'canonical scalar/pure Q block')
    B.need([list(row[1:])for row in q[1:]]==normal['pure_quadratic_form_matrix'],'same acquired kappa-normalized pure block')
    B.need(W.multiply(r,ir,B,tick)==W.multiply(ir,r,B,tick)==B.ident(8),'whole inverse coordinate maps')
    a,e,b=[W.pure7(B.mat(m,8),r,ir,q,B,tick)for m in domain['standard_ordered_prefix_matrices']]
    prefix=[B.mat(m,7)for m in export['matrices']]
    B.need([a,e,b]==prefix and len(set(prefix))==3 and all(m!=identity and W.multiply(m,m,B,tick)==identity for m in prefix)
        and W.multiply(a,e,B,tick)==W.multiply(e,a,B,tick)and W.multiply(b,e,B,tick)==W.multiply(e,b,B,tick),
        'actual original prefix involutions/labels/distant relations')
    targets=[row[0]for row in remaining];journal_bytes=0;started=complete=0;visited=[];unpaid=[];rejected=[];stop=None
    with args.journal.open('xb')as journal:
        def append(record):
            nonlocal journal_bytes
            data=B.canonical(record)+b'\n'
            B.need(len(data)<=MAX_RECORD and journal_bytes+len(data)<=OUTPUT_CAP-REPORT_RESERVE,'whole bounded record with final-report reserve')
            B.need(journal.write(data)==len(data),'whole fresh witness record');journal.flush();journal_bytes+=len(data)
        append(dict(schema='F004_PREFIX8_PROPER19_WITNESS_JOURNAL_V1',program=program,domain=DOMAIN,
            original_export=EXPORT,prior_gate=PRIOR_GATE,prior_result=PRIOR_RESULT,old_journal=OLD_JOURNAL,
            original_job=[8,4],original_prefix_index=8,target_representatives=targets,
            word_schedule_source=SCHEDULE_SOURCE,word_checkpoint_count=40,word_max_length=160,new_word_power=7,new_prime=19,
            cached37_word_power=3,proofs=[SPLIT_PROOF,SPLIT_ROOT_REVIEW,SPLIT_UNIT_REVIEW,PROOF,PROOF_REVIEW],
            canonical_norm=NORMAL,normalization_source=NORMALIZER_SOURCE,direct_inputs=READS,
            moved19_is_not_FULL_G2=True,no_candidate_or_census_credit=True))
        os.fsync(journal.fileno())
        for old_record in remaining:
            rep=old_record[0]
            try:
                tick()
                if journal_bytes+MAX_RECORD>OUTPUT_CAP-REPORT_RESERVE:raise SearchBudgetStop('complete-record space reserved before starting next row')
                started+=1
                c=W.pure7(B.operator(*B.jpair(values[rep-1])),r,ir,q,B,tick)
                B.need(c!=identity and W.multiply(c,c,B,tick)==identity and a!=c and b!=e
                    and W.multiply(a,c,B,tick)==W.multiply(c,a,B,tick),'actual four nonidentity involutions and distinct commuting end pairs')
                left=end_fact((a,b,c),old_record[2],words,q,W,B,tick)
                right=end_fact((b,c,e),old_record[3],words,q,W,B,tick)
                kinds=(left['kind'],right['kind'])
                B.need(kinds!=('PROPER37','PROPER37'),'no duplicate acquired39 row')
                sufficient=all(k in('PROPER19','PROPER37')for k in kinds)and 'PROPER19'in kinds
                record=dict(representative=rep,status='REJECTED_END_INTERSECTION'if sufficient else'UNPAID',
                    left=left,right=right,all_mark_hypotheses_checked=True)
                if sufficient:
                    record.update(theorem=SPLIT_PROOF,middle='<b,c>',
                        case='SPLIT_SPLIT'if kinds==('PROPER19','PROPER19')else'SPLIT_UNITARY',
                        middle_order_upper_bound=266 if kinds==('PROPER19','PROPER19')else 264,
                        intersection_lower_comparison='>479'if kinds==('PROPER19','PROPER19')else'>=480')
                append(record);complete+=1;visited.append(rep)
                if sufficient:rejected.append(rep)
                else:unpaid.append(rep)
                if complete%32==0:os.fsync(journal.fileno())
            except SearchBudgetStop as exc:
                stop=str(exc)
                if started>complete:append(dict(representative=rep,status='UNPAID_INTERRUPTED'));visited.append(rep);unpaid.append(rep)
                break
        journal.flush();os.fsync(journal.fileno())
    final_tick()
    for ref in READS:B.exact(ref,final_tick,2**20)
    B.need(W.source_bytes(__file__,65536)==program_raw,'whole new worker Source unchanged')
    journal_raw=W.source_bytes(args.journal,OUTPUT_CAP);unvisited=targets[len(visited):]
    B.need(not(set(rejected)&set(unpaid)or set(rejected)&set(unvisited)or set(unpaid)&set(unvisited))
        and sorted(rejected+unpaid+unvisited)==targets,'exact remaining496 outcome partition, never clip')
    result=dict(schema='F004_PREFIX8_PROPER19_SEARCH_RESULT_V1',status='BOUNDED_PROPER19_END_CERTIFICATES_WITH_EXPLICIT_UNPAID',
        program=program,domain=DOMAIN,original_export=EXPORT,prior_gate=PRIOR_GATE,prior_result=PRIOR_RESULT,
        journal=W.pin_bytes(args.journal,journal_raw),original_job=[8,4],original_prefix_index=8,
        prior_accepted_orbits=3283,target_orbits=496,started_orbits=started,completed_orbits=complete,
        newly_rejected_representatives=rejected,new_rejected_orbits=len(rejected),unresolved_visited_orbits=unpaid,
        unvisited_orbits=unvisited,stop=stop,prefix_complete=False,root_adoption=None,
        proofs=[SPLIT_PROOF,SPLIT_ROOT_REVIEW,SPLIT_UNIT_REVIEW,PROOF,PROOF_REVIEW],
        scientific_direct_inputs=READS,scientific_direct_inputs_reauthenticated=True,
        moved19_is_not_FULL_G2=True,miss_is_not_negative=True,exact_end_order_engine_executed=False,
        subgroup_closure_executed=False,original_weights_reproved=False,automatic_resume=False,
        canonical_norm_convention='N(v)=v8*Q*v8^T, v8=(0,v_actual7), Q=diag(1,7*beta), never beta or2Q',
        seconds=time.monotonic()-began,peak_self_bytes=W.peak_bytes(),
        worker_limits=dict(search_seconds=WORK_SECONDS,total_seconds=TOTAL_SECONDS,rss_bytes=RSS_CAP,
            combined_output_bytes=OUTPUT_CAP,max_record_bytes=MAX_RECORD,report_reserve_bytes=REPORT_RESERVE),
        outer_profile_required=dict(rss_mib=256,seconds=150),candidate_credit=0,census_credit=0,whole_original_credit=0,
        qualification='Only complete verified S/S or S/U end facts imply IP rejection by reviewed q11 theorem. '
        'Moved19, type mismatch, misses and incomplete/unvisited rows stay unpaid; J1 is not excluded by a moved19 line. '
        'Old3283 and full source/model/original lifts/orbit weights remain borrowed. Root actual review, disjoint adoption '
        'and all complete prefix/original/census recovery duties remain separate.')
    data=B.canonical(result)+b'\n';B.need(len(data)<=REPORT_RESERVE and journal_bytes+len(data)<=OUTPUT_CAP,'bounded complete report, never truncate')
    final_tick()
    with args.output.open('xb')as f:B.need(f.write(data)==len(data),'whole fresh final report');f.flush();os.fsync(f.fileno())
    print(B.canonical(dict(status=result['status'],new_rejected_orbits=len(rejected),
        unpaid_orbits=len(unpaid)+len(unvisited),output=W.pin_bytes(args.output,data),census_credit=0)).decode())


if __name__=='__main__':main()
