#!/usr/bin/env python3
"""Independently replay elementary original-relator elimination, without GAP.

This checks the free-word implication. The source-family transport and finite
odd-kernel complement argument remain written mathematics.
"""
import argparse
import hashlib
import json
from pathlib import Path

def require(condition, message):
    if not condition: raise ValueError(message)

def digest(data): return hashlib.sha256(data).hexdigest()

def freely_reduce(word):
    stack = []
    for letter in word:
        require(type(letter) is int and letter != 0, 'Invalid free-group letter')
        if stack and stack[-1] + letter == 0: stack.pop()
        else: stack.append(letter)
    return stack

def reverse_word(word): return [-letter for letter in word[::-1]]

def replace_letter(word, generator, image):
    values = []
    negative = reverse_word(image)
    for letter in word:
        values.extend(image if letter == generator else negative if letter == -generator else [letter])
    return freely_reduce(values)

def cyclic_core(word):
    result = freely_reduce(word)
    removed = []
    while len(result) >= 2 and result[0] == -result[-1]:
        removed.append(result[0]); result = result[1:-1]
    return removed, result

def closed_permutations(generators, degree):
    identity = tuple(range(1,degree+1))
    pending = [identity]
    found = {identity}
    for element in pending:
        for generator in generators:
            composed = tuple(generator[element[i]-1] for i in range(degree))
            if composed not in found:
                found.add(composed); pending.append(composed)
    return found

def verify(model, cert):
    degree = model['degree']; generators = [tuple(g) for g in model['generators']]
    require(degree == 128 and len(generators) == 4, 'Model size')
    require(all(sorted(g) == list(range(1,129)) for g in generators), 'Permutations')
    require(all(all(g[g[i]-1] == i+1 for i in range(128)) for g in generators), 'Marked involutions')
    group = closed_permutations(generators,degree)
    medial = closed_permutations(generators[1:3],degree)
    require(len(group) == 1024 and len(medial) == 8, 'Fixed group orders')
    require({g for g in group if g[0] == 1} == medial, 'Exact C stabilizer')
    require({g[0] for g in group} == set(range(1,129)), 'Transitivity')
    defect_point = 1
    for letter in model['z_word_1based']:
        require(type(letter) is int and 1 <= letter <= 4, 'Defect word index')
        defect_point = generators[letter-1][defect_point-1]
    require(defect_point == 40, 'Exact defect coset')
    base = (1, generators[3][0], generators[0][0], generators[0][generators[3][0]-1])
    quads = sorted({tuple(g[i-1] for i in base) for g in group})
    relations = [[-quad[3],quad[2],-quad[0],quad[1]] for quad in quads]
    require(len(quads) == 1024 and cert['group_order'] == 1024, 'Original orbit size')
    require([list(q) for q in quads] == cert['quads'], 'Original quad orbit differs')
    require(relations == cert['originals'], 'Original free relators differ')
    current = dict(enumerate(relations))
    current_defect = [-1,defect_point]
    eliminated = set()
    for number, step in enumerate(cert['steps']):
        generator, relation = step['variable'], step['relation']
        require(type(generator) is int and 1 <= generator <= 128 and generator not in eliminated, 'Invalid elimination variable')
        require(relation in current, 'Missing defining relation')
        old = current[relation]
        require(old == step['before'], 'Stale defining word')
        positions = [i for i,x in enumerate(old) if abs(x)==generator]
        require(len(positions)==1, 'Defining variable not unique')
        at = positions[0]; left,right = old[:at],old[at+1:]
        sign = 1 if old[at] > 0 else -1
        require(left == step['left'] and right == step['right'] and sign == step['sign'], 'Decomposition mismatch')
        image = freely_reduce(reverse_word(left)+reverse_word(right)) if sign==1 else freely_reduce(right+left)
        require(generator not in map(abs,image) and image == step['replacement'], 'Invalid solved word')
        require(replace_letter(old,generator,image)==[], 'Solved equation is not a free identity')
        next_relations = {}
        for identifier,word in current.items():
            if identifier == relation: continue
            replaced = replace_letter(word,generator,image)
            if replaced: next_relations[identifier]=replaced
        current = next_relations
        current_defect = replace_letter(current_defect,generator,image)
        eliminated.add(generator)
        require(all(generator not in map(abs,w) for w in current.values()), 'Eliminated letter survives')
    require({str(k):v for k,v in current.items()} == cert['remaining'], 'Final relation inventory mismatch')
    require(current_defect == cert['delta'], 'Final marked defect mismatch')
    conjugator, square_core = cyclic_core(current_defect+current_defect)
    require([conjugator,square_core] == cert['delta_squared_cyclic'], 'Defect square reduction mismatch')
    witnesses = []
    for identifier,word in current.items():
        prefix,core = cyclic_core(word)
        for inverse_flag,orientation in [(False,core),(True,reverse_word(core))]:
            for shift in range(len(orientation)):
                if orientation[shift:]+orientation[:shift] == square_core:
                    witnesses.append(dict(original_relation=identifier, final_word=word,
                                          stripped_conjugator=prefix,invert=inverse_flag,cyclic_rotation=shift))
                    break
    require(witnesses, 'No original-relator consequence proves defect square')
    witness = min(witnesses,key=lambda r:(len(r['final_word']),r['original_relation']))
    return dict(status='PASS_exact_original_relator_implication',fixed_group_order=len(group),
                medial_order=len(medial),coset_degree=degree,defect_coset=defect_point,
                original_relators=len(relations),eliminations=len(eliminated),
                surviving_generators=128-len(eliminated),remaining_nontrivial_relators=len(current),
                marked_defect=current_defect,defect_squared_cyclic_core=square_core,
                witness=witness,independent_GAP_or_author_imports=False,
                mathematical_consequence='Every assignment in any group satisfying all original relators has (t1^-1*t40)^2=1.',
                limitations='The coset-model identification with the full source family and odd-kernel complement argument remain written proofs; this routine does not prove a free-product decomposition.')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model',type=Path,required=True)
    p.add_argument('--certificate',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();require(not a.report.exists() and not a.report.is_symlink(),'New report required')
    model_raw=a.model.read_bytes();cert_raw=a.certificate.read_bytes();cert=json.loads(cert_raw)
    require(digest(model_raw)=='0247990a79729513799e8fe85d49dec74fade6b32a9aff8746a3fa4c0e8a2338','Fixed model changed')
    require(cert['model_sha256']==digest(model_raw),'Certificate model mismatch')
    result=verify(json.loads(model_raw),cert)
    require(a.model.read_bytes()==model_raw and a.certificate.read_bytes()==cert_raw,'Input changed during check')
    result.update(model_sha256=digest(model_raw),certificate_sha256=digest(cert_raw),checker_sha256=digest(Path(__file__).read_bytes()))
    a.report.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
