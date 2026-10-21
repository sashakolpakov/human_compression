#!/usr/bin/env python3
"""Independent exact check of the 35 displayed Lean cell hypotheses.

The group-word implication is replayed from those cells alone. This is not a
Lean parser or a replacement for compiling the bound source with Lean.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def reduce_word(word):
    result = []
    for x in word:
        require(type(x) is int and x != 0, 'Invalid free letter')
        if result and result[-1] == -x:
            result.pop()
        else:
            result.append(x)
    return result

def inverse(word):
    return [-x for x in reversed(word)]

def substitute(word, x, replacement):
    result = []
    for y in word:
        result.extend(replacement if y == x else inverse(replacement) if y == -x else [y])
    return reduce_word(result)

def closure(gens):
    identity = tuple(range(1,129))
    elements, seen = [identity], {identity}
    for x in elements:
        for y in gens:
            z = tuple(y[i-1] for i in x)
            if z not in seen:
                seen.add(z)
                elements.append(z)
    return elements

def verify(model, certificate, lean):
    markers = re.findall(r'Original orbit row (\d+); elementary elimination (\d+)\.', lean)
    require(len(markers) == 34, 'Expected 34 displayed eliminations')
    indices = [int(i) for _, i in markers]
    rows = [int(r) for r, _ in markers]
    require(indices == sorted(set(indices)), 'Eliminations not ordered and distinct')
    match = re.search(r'def requiredCells\s*:\s*List \(ℕ × ℕ × ℕ × ℕ\)\s*:=\s*\[(.*?)\]', lean, re.S)
    require(match is not None, 'Missing literal cell list')
    cells = [tuple(map(int, m)) for m in re.findall(r'\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)', match.group(1))]
    require(len(cells) == len(set(cells)) == 35, 'Expected 35 distinct cells')
    applications = [tuple(map(int, m)) for m in re.findall(r'have hh := hcells (\d+) (\d+) (\d+) (\d+) \(by decide\)', lean)]
    require(applications == cells, 'Displayed hypothesis uses differ from cell inventory')
    gens = model['generators']
    require(model['degree'] == 128 and len(gens) == 4, 'Wrong model dimensions')
    require(all(sorted(g) == list(range(1,129)) for g in gens), 'Non-permutation generator')
    group = closure(gens)
    require(len(group) == 1024, 'Wrong model order')
    base = (1, gens[3][0], gens[0][0], gens[0][gens[3][0]-1])
    orbit = sorted({tuple(g[i-1] for i in base) for g in group})
    require(len(orbit) == 1024, 'Wrong cell orbit size')
    require([tuple(q) for q in certificate['quads']] == orbit, 'Certificate orbit differs')
    require(cells == [orbit[r] for r in rows + [239]], 'Lean cells not exact selected original rows')
    original = [[-d,c,-a,b] for a,b,c,d in cells]
    current = original.copy()
    delta = [-1,40]
    eliminated = []
    for position, index in enumerate(indices):
        step = certificate['steps'][index]
        require(step['relation'] == rows[position], 'Comment/trace defining row differs')
        word = current[position]
        require(word == step['before'], 'Selected hypotheses omit a needed substitution')
        x = step['variable']
        require(x not in eliminated, 'Repeated elimination')
        places = [i for i,y in enumerate(word) if abs(y) == x]
        require(len(places) == 1, 'Variable not uniquely solvable')
        place = places[0]
        left, right = word[:place], word[place+1:]
        replacement = reduce_word(inverse(left)+inverse(right) if word[place] > 0 else right+left)
        require(replacement == step['replacement'], 'Incorrect substitution')
        require(substitute(word,x,replacement) == [], 'Solved equation is not a free identity')
        current = [substitute(w,x,replacement) for w in current]
        delta = substitute(delta,x,replacement)
        eliminated.append(x)
    require(all(w == [] for w in current[:34]), 'Defining equations did not vanish')
    require(delta == [-6,7], 'Wrong distinguished defect')
    require(current[34] == [-32,16,-6,7,-6,7,-16,32], 'Wrong final conjugate square')
    conjugator = [-16,32]
    require(reduce_word(conjugator+current[34]+inverse(conjugator)) == delta+delta,
            'Final conjugation does not prove defect square')
    return dict(status='PASS_35_cell_original_relation_implication',
                selected_elimination_indices=indices,selected_original_rows=rows+[239],
                cells=[list(c) for c in cells],model_group_order=len(group),
                original_orbit_size=len(orbit),cell_count=len(cells),eliminations=len(eliminated),
                marked_defect_after_eliminations=delta,final_relator=current[34],
                final_conjugator=conjugator,
                scope='Direct free-word replay from the exact 35 literal Lean cell hypotheses; cell membership in the fixed model is checked externally, not formalized here.',
                imports_author_code=False)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ['model','certificate','lean','report']:
        p.add_argument('--'+name,type=Path,required=True)
    a = p.parse_args()
    require(not a.report.exists() and not a.report.is_symlink(), 'Fresh report required')
    inputs = {name:getattr(a,name).read_bytes() for name in ['model','certificate','lean']}
    require(sha(inputs['model']) == '0247990a79729513799e8fe85d49dec74fade6b32a9aff8746a3fa4c0e8a2338', 'Frozen model differs')
    result = verify(json.loads(inputs['model']),json.loads(inputs['certificate']),inputs['lean'].decode())
    require(all(getattr(a,k).read_bytes() == v for k,v in inputs.items()), 'Input changed during replay')
    result['input_sha256'] = {k:sha(v) for k,v in inputs.items()}
    result['checker_sha256'] = sha(Path(__file__).read_bytes())
    a.report.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','cell_count','eliminations','input_sha256']}))

if __name__ == '__main__':
    main()
