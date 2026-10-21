"""Bounded sufficient matrix rejections for the one acquired original prefix8.

Source only until distinct review and Root admission. No permutation/group
enumeration, original-index reinterpretation, or automatic job adoption.
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
DOMAIN = dict(path=str(HERE/'cases/original_prefix8/output/result.json'), bytes=513255,
    sha256='e7124783eb2e9a5e1ca21c93d79a3e1ab1cf1460109b6ebc60dd451b5099c1f8')
HELPERS = dict(path=str(HERE/'verify_indexed_frame_catalogue.py'), bytes=22496,
    sha256='1cebbda5fcda823b43713f03dd17893480c34d040f27501a0651ab69d8f496d3')
NORMAL = dict(path=str(HERE.parent/'cayley_normalization_acquisition/result.json'), bytes=10559,
    sha256='47c4f9848a304b7ca821db38271f85e672f29f241790a2203e2ace19307d25a1')
GENERATION = dict(path=str(THEORY/'g2_11_generation_by_prime_witnesses.tex'), bytes=26437,
    sha256='f1b6c8a69780c7b8ac88f239627a7ce6889c24203f72ddc35c86fe93e661e76b')
MODEL = dict(path=str(THEORY/'acquired_cayley_full_group_bridge.rst'), bytes=9716,
    sha256='a754edb570ef9d30816c3897deeae2aec7958fb7cfb5fa756536ca8e0ab30801')
SCHEDULE_SOURCE = dict(path=str(HERE.parent/'matrix_end_certificate.g'), bytes=3831,
    sha256='d07cdbcaf1c25826e8917770adedec9b2ef4b159e13fe29c27181c88e17f137a')
BORROWED = ['need','canonical','shape','exact','vec','mat','ident','scale','row','mm',
    'nullspace','mul2','bar2','det2','inv2','operator','jpair']
OUTPUT_CAP = 2**20  # Combined journal and final summary; never clip a record.
WORK_SECONDS, TOTAL_SECONDS, RSS_CAP = 90, 100, 128*2**20


class SearchBudgetStop(RuntimeError):
    pass


def peak_bytes():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value if sys.platform == 'darwin' else value*1024


def source_bytes(path, cap):
    p = Path(path); a = p.lstat()
    if not (stat.S_ISREG(a.st_mode) and a.st_nlink == 1 and a.st_size <= cap):
        raise ValueError('ordinary whole bounded Source')
    with p.open('rb') as stream:
        if sys.platform == 'darwin': fcntl.fcntl(stream.fileno(),48,1)
        b = os.fstat(stream.fileno()); raw = stream.read(cap+1); z = os.fstat(stream.fileno())
    key = lambda q:(q.st_dev,q.st_ino,q.st_mode,q.st_nlink,q.st_size,q.st_mtime_ns,q.st_ctime_ns)
    if not (key(a) == key(b) == key(z) == key(p.lstat()) and len(raw) == a.st_size):
        raise ValueError('stable full Source bytes')
    return raw


def pin_bytes(path, raw):
    return dict(path=str(Path(path).absolute()),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())


def borrowed_helpers(tick):
    raw = source_bytes(HELPERS['path'],65536)
    if pin_bytes(HELPERS['path'],raw) != HELPERS: raise ValueError('whole acquired arithmetic/IO Source')
    nodes = [n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name in BORROWED]
    if [n.name for n in nodes] != BORROWED: raise ValueError('exact seventeen whole definitions')
    scope = dict(P=11,I2=(1,0,0,1),ZERO4=(0,0,0,0),DOC_CAP=2**21,
        Path=Path,stat=stat,sys=sys,os=os,fcntl=fcntl,hashlib=hashlib,json=json)
    # Define only the declared unchanged functions in a new explicit namespace.
    # No predecessor imports, main, certify, catalogue or orbit search executes.
    exec(compile(ast.Module(body=nodes,type_ignores=[]),HELPERS['path']+'::<whole_borrowed_defs>','exec'),scope)
    tick()
    return SimpleNamespace(**{name:scope[name] for name in BORROWED})


def schedule():
    """Exact old three-mark160-step rule, not the interval rule."""
    state,last,letters = 17,0,[]
    for i in range(1,161):
        state = (1103515245*state+12345) % 2147483648
        k = 1+(state//65536)%4
        if (last,k) in ((1,2),(2,1),(3,4),(4,3)): k = ((k+1)%4)+1
        letters.append(str(k)); last = k
    return tuple(''.join(letters[:i]) for i in range(4,161,4))


def multiply(a,b,B,tick):
    tick(); value = B.mm(a,b); tick(); return value


def power(a,n,B,tick):
    if type(n) is not int or n < 0: raise ValueError('nonnegative literal power')
    out = B.ident(len(a)); value = a
    while n:
        if n&1: out = multiply(out,value,B,tick)
        n >>= 1
        if n: value = multiply(value,value,B,tick)
    return out


def exact_prefix_order(a,b,B,tick):
    r = multiply(a,b,B,tick)
    n = 11**6*(11**6-1)*(11**2-1)
    identity = B.ident(7)
    B.need(power(r,n,B,tick) == identity,'prefix product lies in the imported G2(11) exponent bound')
    for p in (2,3,5,7,11,19,37):
        while n%p == 0 and power(r,n//p,B,tick) == identity: n //= p
    B.need(n > 2,'original adjacent fixed-prefix order')
    factors = []; rest = n
    for p in (2,3,5,7,11,19,37):
        count = 0
        while rest%p == 0: rest //= p; count += 1
        if count: factors.append([p,count])
    B.need(rest == 1 and power(r,n,B,tick) == identity,'complete exact-order factorization')
    B.need(all(power(r,n//p,B,tick) != identity for p,_ in factors),'all prime-divisor exact-order witnesses')
    return r,n,factors


def prefix_members(a,e,r,m,B,tick):
    rotations = [B.ident(7)]
    if m%2 == 0: rotations.append(power(r,m//2,B,tick))
    result = []
    for z in rotations:
        for u in (B.ident(7),a):
            for v in (B.ident(7),e):
                value = multiply(multiply(z,u,B,tick),v,B,tick)
                if value not in result: result.append(value)
    B.need(len(result) <= 8,'proved complete prefix centralizer bound')
    return tuple(result)


def pure7(standard,r,ir,q,B,tick):
    """standard8 -> paid actual8 -> scalar-fixed, norm-preserving pure7."""
    actual = multiply(multiply(ir,standard,B,tick),r,B,tick)
    B.need(actual[0] == (1,0,0,0,0,0,0,0)
        and all(actual[i][0] == 0 for i in range(1,8)), 'exact scalar plus pure splitting')
    transposed = tuple(zip(*actual))
    B.need(multiply(multiply(actual,q,B,tick),transposed,B,tick) == q,'whole actual eight-dimensional norm')
    return tuple(tuple(row[1:]) for row in actual[1:])


def end_letters(end,B,tick):
    a,b,c = end
    return (multiply(a,b,B,tick),multiply(b,a,B,tick),
            multiply(b,c,B,tick),multiply(c,b,B,tick))


def evaluate_word(text,letters,B,tick):
    B.need(type(text) is str and 1 <= len(text) <= 160
        and all(k in '1234' for k in text),'complete bounded end-word encoding')
    out = B.ident(7)
    for k in text: out = multiply(out,letters[ord(k)-ord('1')],B,tick)
    return out


def verify_end37(end,text,B,tick):
    """Re-evaluate a proposed word, then verify every sufficient equality."""
    letters = end_letters(end,B,tick)
    word = evaluate_word(text,letters,B,tick)
    y = power(word,3,B,tick); identity = B.ident(7)
    if y == identity or power(y,37,B,tick) != identity: return None
    equations = [[(y[i][j]-int(i == j))%11 for i in range(7)] for j in range(7)]
    basis = B.nullspace(equations,7)
    B.need(len(basis) == 1,'exact one-dimensional pure fixed space, never the unital8-space')
    v = basis[0]; first = next(x for x in v if x)
    v = B.scale(pow(first,-1,11),v)
    B.need(any(v) and B.row(v,y) == v,'whole nonzero pure fixed-vector witness')
    for k,h in enumerate(end):
        vh = B.row(v,h)
        for i in range(7):
            for j in range(i+1,7):
                if (v[i]*vh[j]-v[j]*vh[i])%11:
                    return ['FULL',list(v),k,[i,j]]
    # The actual37 witness and every generator-line check are complete.
    # SU3(11):2 is the proper stabilizer exception, not a rejection.
    return ['PROPER',list(v)]


def search_end(end,words,B,tick):
    letters = end_letters(end,B,tick)
    word = B.ident(7); last_length = 0
    for checkpoint,text in enumerate(words,1):
        for k in text[last_length:]: word = multiply(word,letters[ord(k)-ord('1')],B,tick)
        last_length = len(text)
        y = power(word,3,B,tick)
        if y != B.ident(7) and power(y,37,B,tick) == B.ident(7):
            fact = verify_end37(end,text,B,tick)
            B.need(fact is not None,'proposed and independently re-evaluated word agree')
            return [checkpoint,*fact]
    return None  # No negative inference from these forty attempted words.


def candidate(rep,c,a,b,e,members,words,B,tick):
    identity = B.ident(7)
    if c in members: return [rep,'PREFIX_MEMBER',members.index(c)]
    bc = multiply(b,c,B,tick)
    if multiply(bc,bc,B,tick) == identity: return [rep,'ADJACENT_LE2','bc']
    ec = multiply(e,c,B,tick)
    if multiply(ec,ec,B,tick) == identity: return [rep,'ADJACENT_LE2','ec']
    left = search_end((a,b,c),words,B,tick)
    if left is not None and left[1] == 'FULL': return [rep,'END37','L',*left]
    right = search_end((b,c,e),words,B,tick)
    if right is not None and right[1] == 'FULL': return [rep,'END37','R',*right]
    return [rep,'UNPAID',left,right]


def main():
    began = time.monotonic()
    if sys.flags.optimize or not sys.flags.ignore_environment or not sys.dont_write_bytecode:
        raise ValueError('ordinary isolated Python -E -B')
    ap = argparse.ArgumentParser(allow_abbrev=False,description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--journal',type=Path,required=True)
    args = ap.parse_args()
    paths = [args.output,args.journal]
    if not (all(p.is_absolute() and not os.path.lexists(p) and p.parent.resolve(strict=True) == p.parent
        and stat.S_ISDIR(p.parent.lstat().st_mode) for p in paths) and len(set(paths)) == 2):
        raise ValueError('two distinct fresh output files in existing ordinary parents')
    def final_tick():
        if time.monotonic()-began >= TOTAL_SECONDS or peak_bytes() >= RSS_CAP:
            raise SearchBudgetStop('shared100s/observed128MiB bound; any partial journal stays unpaid')
    def tick():
        final_tick()
        if time.monotonic()-began >= WORK_SECONDS:
            raise SearchBudgetStop('90s search reserve within the same100s total budget')
    B = borrowed_helpers(tick)
    raw_program = source_bytes(__file__,65536); program = pin_bytes(__file__,raw_program)
    reads = [HELPERS,DOMAIN,NORMAL,GENERATION,MODEL,SCHEDULE_SOURCE]
    for q in (GENERATION,MODEL,SCHEDULE_SOURCE): B.exact(q,tick,65536)
    domain = B.exact(DOMAIN,tick,2**20,True)
    normal = B.exact(NORMAL,tick,65536,True)
    B.need(domain['schema'] == 'F004_Q11_INDEXED_CAYLEY_CENTRALIZER_DOMAIN_CERTIFICATE_V1'
        and domain['status'] == 'VERIFIED_CAYLEY_FRAME_AND_AUTOMORPHISM_DOMAIN'
        and domain['certificate_verified'] is True and domain['rank'] == 4
        and domain['original_job'] == [8,4] and domain['original_prefix_index'] == 8
        and domain['selected_labels'] == [1,4,2] and domain['normalization_result'] == NORMAL
        and domain['model_bridge_source'] == MODEL and domain['external_premises']['original_A_equals_G'] is True,
        'the one genuine original prefix8 domain and imported exact model/A joins')
    export_ref = domain['prefix_export']; B.shape(export_ref)
    export = B.exact(export_ref,tick,65536,True); reads.append(export_ref)
    B.need(export['schema'] == 'F004_Q11_INDEXED_ORIGINAL_PREFIX_MATRICES_V1'
        and export['original_job'] == [8,4] and export['original_prefix_index'] == 8
        and export['rank'] == 4 and export['selected_labels'] == [1,4,2]
        and export['end_order'] == [1,4,2,3] and export['convention'] == 'RIGHT_ROW'
        and export['origin'] == domain['origin']
        and export['external_premises'] == domain['external_premises'], 'whole original ordered export bindings')
    B.need(normal['certificate_verified'] is True and normal['kappa'] == 7,'acquired normalized full norm')
    r = B.mat(domain['standard_to_actual_row_map'],8)
    ir = B.mat(domain['actual_to_standard_row_map'],8)
    q = B.mat(normal['quadratic_form_matrix'],8)
    B.need(multiply(r,ir,B,tick) == multiply(ir,r,B,tick) == B.ident(8),'full inverse coordinate maps')
    a,e,b = [pure7(B.mat(m,8),r,ir,q,B,tick) for m in domain['standard_ordered_prefix_matrices']]
    actual_prefix = [B.mat(m,7) for m in export['matrices']]
    B.need([a,e,b] == actual_prefix and len(set(actual_prefix)) == 3,'all whole actual prefix matrices in original order')
    identity = B.ident(7)
    B.need(all(m != identity and multiply(m,m,B,tick) == identity for m in actual_prefix)
        and multiply(a,e,B,tick) == multiply(e,a,B,tick)
        and multiply(b,e,B,tick) == multiply(e,b,B,tick),'original fixed prefix involutions/distant relations')
    values = domain['catalogue']; orbits = domain['orbits']
    B.need(len(values) == domain['catalogue_size'] == domain['selected_raw_domain_size'] == 14763
        and hashlib.sha256(B.canonical(values)).hexdigest() == domain['catalogue_sha256']
        and domain['selected_raw_domain_indices'] == list(range(1,14764))
        and len(orbits) == 3779 and domain['endpoint_group_order'] == 288
        and domain['prefix_stabilizer_order'] == 4,'complete acquired finite domain, not a selected subset')
    members_seen = set(); representatives = []
    for orbit in orbits:
        B.need(type(orbit) is list and len(orbit) == 4,'whole compact acquired orbit row')
        rep,indices,transporters,stabilizer = orbit
        B.need(type(rep) is int and type(indices) is list and indices and indices == sorted(set(indices))
            and rep == min(indices) and not members_seen.intersection(indices)
            and all(type(j) is int and 1 <= j <= 14763 for j in indices)
            and len(indices) == len(transporters) and len(indices)*stabilizer == 4,'complete disjoint orbit identities')
        members_seen.update(indices); representatives.append(rep); tick()
    B.need(members_seen == set(range(1,14764)) and representatives == sorted(representatives), 'entire acquired orbit cover')
    product,m,factors = exact_prefix_order(a,b,B,tick)
    members = prefix_members(a,e,product,m,B,tick)
    words = schedule()
    header = dict(schema='F004_PREFIX8_MATRIX_REJECTION_WITNESS_JOURNAL_V1',program=program,
        domain=DOMAIN,original_job=[8,4],original_prefix_index=8,original_export=export_ref,
        word_schedule_source=SCHEDULE_SOURCE,word_schedule=list(words),word_power=3,prime=37,
        exact_prefix_product_order=m,exact_prefix_order_factorization=factors,
        representation='RIGHT_ROW ACTUAL_PURE7; standard8 conjugated by actual_to_standard * M * standard_to_actual',
        direct_inputs=reads,root_original_model_and_scope_duties_remain_external=True,
        scientific_credit=0,old_indices_reinterpreted=False)
    journal_bytes = 0; rejected = 0; complete = 0; started = 0; visited = []; unpaid = []
    stop = None
    with args.journal.open('xb') as journal:
        def append(value):
            nonlocal journal_bytes
            raw = B.canonical(value)+b'\n'
            B.need(len(raw) <= 16384 and journal_bytes+len(raw) <= OUTPUT_CAP,'complete bounded witness journal, never truncate')
            B.need(journal.write(raw) == len(raw),'complete journal record'); journal.flush(); journal_bytes += len(raw)
        append(header); os.fsync(journal.fileno())
        for rep in representatives:
            try:
                tick(); started += 1
                standard = B.operator(*B.jpair(values[rep-1]))
                c = pure7(standard,r,ir,q,B,tick)
                B.need(c != identity and multiply(c,c,B,tick) == identity
                    and multiply(a,c,B,tick) == multiply(c,a,B,tick),'whole genuine candidate involution centralizing a')
                record = candidate(rep,c,a,b,e,members,words,B,tick)
                append(record); complete += 1; visited.append(rep)
                if record[1] == 'UNPAID': unpaid.append(rep)
                else: rejected += 1
                if complete%32 == 0: os.fsync(journal.fileno())
            except SearchBudgetStop as exc:
                stop = str(exc)
                if started > complete:
                    append([rep,'UNPAID_INTERRUPTED']); unpaid.append(rep); visited.append(rep)
                break
        journal.flush(); os.fsync(journal.fileno())
    final_tick()
    # Same exact direct inputs before and after; no historical payload or
    # full Root readset is falsely described as reopened by this worker.
    for reference in reads: B.exact(reference,final_tick,2**20)
    B.need(source_bytes(__file__,65536) == raw_program,'whole worker Source unchanged')
    journal_raw = source_bytes(args.journal,OUTPUT_CAP)
    unvisited = representatives[len(visited):]
    all_rejected = rejected == len(representatives) and not unpaid and not unvisited
    summary = dict(schema='F004_PREFIX8_MATRIX_REJECTION_PASS_V1',
        status='ALL3779_ORBITS_REJECTED' if all_rejected else 'INCOMPLETE_WITH_EXPLICIT_UNPAID_ORBITS',
        domain=DOMAIN,program=program,journal=pin_bytes(args.journal,journal_raw),
        original_job=[8,4],original_prefix_index=8,total_orbits=3779,total_raw_domain=14763,
        started_orbits=started,completed_orbits=complete,rejected_orbits=rejected,
        unresolved_visited_orbits=unpaid,unvisited_orbits=unvisited,stop=stop,
        all_orbits_rejected=all_rejected,original_guard_order='prefix-membership,adjacent,full-left,full-right',
        no37_witness_is_not_nongeneration=True,proper37_line_is_not_rejection=True,
        exact_intersections_executed=False,whole_quartet_generation_executed=False,
        no_original_permutation_lifts=True,original_weights_reproved=False,
        root_zero_prefix_adoption_owed=all_rejected,census_credit=0,candidate_credit=0,whole_original_credit=0,
        scientific_direct_inputs_reauthenticated=True,seconds=time.monotonic()-began,peak_self_bytes=peak_bytes(),
        worker_limits=dict(search_seconds=WORK_SECONDS,total_seconds=TOTAL_SECONDS,rss_bytes=RSS_CAP,
            combined_output_bytes=OUTPUT_CAP),outer_profile_required=dict(rss_mib=256,seconds=150),
        qualification='Sufficient verified matrix rejection witnesses only. Imported acquired catalogue/model/faithful original-prefix and Source/runtime premises remain. No miss is negative credit. Root actual review and a complete zero-prefix composition are separate; partial journal records never close an unpaid orbit.')
    raw = B.canonical(summary)+b'\n'
    B.need(journal_bytes+len(raw) <= OUTPUT_CAP,'combined final and journal cap; retained partial is not clipped')
    final_tick()
    with args.output.open('xb') as stream:
        B.need(stream.write(raw) == len(raw),'whole fresh final report'); stream.flush(); os.fsync(stream.fileno())
    print(B.canonical(dict(status=summary['status'],rejected_orbits=rejected,
        unpaid_orbits=len(unpaid)+len(unvisited),output=pin_bytes(args.output,raw),census_credit=0)).decode())


if __name__ == '__main__':
    main()
