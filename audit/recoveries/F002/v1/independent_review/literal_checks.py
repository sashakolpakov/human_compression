"""Independent involution generation and deterministic marked graph transport."""
import argparse
import ast
import itertools
import json
import re
from pathlib import Path
from independent_oracle import SOURCE_EDGES, cycles, inv, mul


def bracketed(text, start):
    start = text.index('[', start)
    depth = 0
    for end in range(start, len(text)):
        if text[end] == '[':
            depth += 1
        elif text[end] == ']':
            depth -= 1
            if depth == 0:
                return text[start:end+1]
    raise ValueError('unclosed list')


def permutations(text, n):
    content = text.strip()[1:-1]
    pieces = re.split(r'(?<=\))\s*,\s*(?=\()', content)
    result = []
    for piece in pieces:
        pairs = []
        for c in re.findall(r'\(([^()]*)\)', piece):
            pair = [int(x) for x in c.split(',')]
            if len(pair) != 2:
                raise ValueError('expected disjoint transpositions')
            pairs.append(pair)
        if not pairs or len({v for p in pairs for v in p}) != 2*len(pairs):
            raise ValueError('malformed involution')
        result.append(cycles(n, pairs))
    return result


def transport(t, u):
    """All point bijections intertwining each generator, by one starting image."""
    n = len(t[0])
    if len(t) != len(u):
        return []
    answers = []
    for image in range(n):
        mapping = {0:image}; used = {image:0}; queue = [0]; valid = True
        for a in queue:
            for x,y in zip(t,u):
                b, c = x[a], y[mapping[a]]
                if b in mapping:
                    if mapping[b] != c:
                        valid = False; break
                elif c in used:
                    valid = False; break
                else:
                    mapping[b] = c; used[c] = b; queue.append(b)
            if not valid:
                break
        if valid and len(mapping) == n:
            answers.append(tuple(mapping[i] for i in range(n)))
    return answers


def matchings(vertices):
    if not vertices:
        yield []
    else:
        a = vertices[0]
        for j in range(1,len(vertices)):
            b = vertices[j]
            for tail in matchings(vertices[1:j]+vertices[j+1:]):
                yield [(a,b)]+tail


def check(generated_file, source_file, small_stdout, small_report):
    data = Path(generated_file).read_text()
    observed = permutations(bracketed(data,data.index('recordedInvolutions')),11)
    expected = set()
    classes = {}
    for moved in [4,8]:
        batch = {cycles(11,m) for subset in itertools.combinations(range(1,12),moved)
                 for m in matchings(subset)}
        classes[moved] = len(batch); expected |= batch
    if len(observed) != len(set(observed)) or set(observed) != expected:
        raise ValueError('entire involution inventory mismatch')
    source = [tuple(cycles(11,pairs) for pairs in row) for row in SOURCE_EDGES]
    source_data = Path(source_file).read_text()
    source_literal = bracketed(source_data, source_data.index('sourceMarks'))
    # Individual inner lists contain only disjoint two-cycles, not nested lists.
    source_read = [tuple(permutations(x,11)) for x in re.findall(r'\[[^\[\]]*\]',source_literal)]
    if source_read != source:
        raise ValueError('source diagram transcription mismatch')
    records = {}
    for r in [3,4,5]:
        ids = ast.literal_eval(bracketed(data,data.index(':=', data.index(f'recordedMarks[{r}]'))))
        records[r] = [tuple(observed[i-1] for i in row) for row in ids]
    matches = []
    for r, tuples in records.items():
        for i,t in enumerate(tuples):
            row_matches = [j+1 for j,u in enumerate(source)
                           if transport(t,u) or transport(t,tuple(reversed(u)))]
            if row_matches:
                if len(row_matches) != 1:
                    raise ValueError('overlapping source permutation classes')
                matches.append(dict(rank=r,record_index=i+1,source_row=row_matches[0]))
    if [len(records[r]) for r in [3,4,5]] != [130,2,0]:
        raise ValueError('record cardinalities')
    if [sum(x['source_row']==j for x in matches) for j in range(1,6)] != [2]*5:
        raise ValueError('source class multiplicities')
    if any(transport(t,tuple(reversed(t))) for t in source):
        raise ValueError('unexpected permutation self-duality')
    small = Path(small_stdout).read_text()
    small_ivs = permutations(bracketed(small,small.index('INVOLUTIONS_LITERAL')),5)
    all_s5 = list(itertools.permutations(range(5)))
    def canonical(t):
        return min(tuple(mul(mul(inv(p),x),p) for x in t) for p in all_s5)
    oracle = json.loads(Path(small_report).read_text())['small_exhaustion']['canonical_tuples']
    for r in [3,4,5]:
        ids = ast.literal_eval(bracketed(small,small.index(f'COMPLETE_MARKS_RANK_{r}')))
        actual = {canonical(tuple(small_ivs[j-1] for j in row)) for row in ids}
        want = {canonical(tuple(tuple(x-1 for x in p) for p in row)) for row in oracle[str(r)]}
        if actual != want:
            raise ValueError('small exhaustive class disagreement')
    return dict(status='PASS',involutions=len(expected),moved_point_classes=classes,
                source_rows=5,matched_records=matches,permutation_self_dual_rows=0,
                a5_complete_orbit_sets_match=True)


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--generated',required=True);p.add_argument('--source',required=True)
    p.add_argument('--small-stdout',required=True);p.add_argument('--small-report',required=True);p.add_argument('--out',required=True)
    a=p.parse_args();r=check(a.generated,a.source,a.small_stdout,a.small_report)
    Path(a.out).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'status':r['status'],'involutions':r['involutions'],'matched_records':len(r['matched_records'])}))
