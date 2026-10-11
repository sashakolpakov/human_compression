#!/usr/bin/env python3
"""Emit an ordinary kernel-checked Lean certificate from explicit finite maps."""
import argparse
import json
from pathlib import Path
from phase186_witt_validate import dot4


def vec(items):
    return '![' + ', '.join(items) + ']'


def generate(data):
    field = ['(0, 0)', '(1, 0)', '(0, 1)', '(1, 1)']
    # GAP sorts its set of line supports, whereas Lean indexes linear forms
    # in coordinate-vector order. Bind the two conventions explicitly.
    coordinate_lines = [[i+1 for i,v in enumerate(data['plane_vectors']) if dot4(n,v)==0]
                        for n in data['plane_vectors']]
    out = ['import DeletedLineFourResidue', '',
           '/-! Explicit finite derived-plane incidence maps. The original Witt',
           'designs and their derivation remain GAP-checked inputs; this file',
           'checks every incidence against literal F4 coordinate arithmetic. -/', '',
           'namespace MathCompression.WittDerivedPlanes',
           'open MathCompression.DeletedLineFourResidue',
           'set_option maxRecDepth 1000000',
           'set_option maxHeartbeats 0', '',
           'def coordinate : Fin 21 → Fin 3 → F4 :=',
           '  ' + vec([vec([field[x] for x in v]) for v in data['plane_vectors']]), '',
           'def coordinateIncident (p l : Fin 21) : Prop :=',
           '  mul4 (coordinate p 0) (coordinate l 0) +',
           '  mul4 (coordinate p 1) (coordinate l 1) +',
           '  mul4 (coordinate p 2) (coordinate l 2) = 0', '',
           'instance (p l : Fin 21) : Decidable (coordinateIncident p l) :=',
           '  inferInstanceAs (Decidable (_ = _))', '',
           'structure IncidenceIso (source : Fin 21 → Fin 21 → Prop) where',
           '  points : Fin 21 ≃ Fin 21',
           '  lines : Fin 21 ≃ Fin 21',
           '  preserves : ∀ p l, source p l ↔ coordinateIncident (points p) (lines l)', '']
    for case in data['cases']:
        if case['v'] < 20:
            continue
        suffix = str(case['v'])
        lines = case['derived_blocks']
        pm = case['point_map']
        lm = [coordinate_lines.index(sorted(pm[x-1] for x in b)) for b in lines]
        out += [f'def nativeLines{suffix} : Fin 21 → List (Fin 21) :=',
                '  ' + vec(['[' + ', '.join(str(x-1) for x in b) + ']' for b in lines]), '',
                f'def pointMap{suffix} : Fin 21 → Fin 21 :=',
                '  ' + vec([str(x-1) for x in pm]), '',
                f'def lineMap{suffix} : Fin 21 → Fin 21 :=',
                '  ' + vec([str(x) for x in lm]), '',
                f'theorem maps{suffix}_bijective : Function.Bijective pointMap{suffix} ∧',
                f'    Function.Bijective lineMap{suffix} := by decide', '',
                f'theorem incidence{suffix} : ∀ p l : Fin 21,',
                f'    p ∈ nativeLines{suffix} l ↔ coordinateIncident (pointMap{suffix} p) (lineMap{suffix} l) := by',
                '  decide', '',
                f'noncomputable def iso{suffix} : IncidenceIso (fun p l => p ∈ nativeLines{suffix} l) where',
                f'  points := Equiv.ofBijective pointMap{suffix} maps{suffix}_bijective.1',
                f'  lines := Equiv.ofBijective lineMap{suffix} maps{suffix}_bijective.2',
                f'  preserves := incidence{suffix}', '',
                f'#print axioms maps{suffix}_bijective',
                f'#print axioms incidence{suffix}',
                f'#print axioms iso{suffix}', '']
    out += ['end MathCompression.WittDerivedPlanes', '']
    return '\n'.join(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('witness',type=Path)
    p.add_argument('output',type=Path)
    args = p.parse_args()
    args.output.write_text(generate(json.loads(args.witness.read_text())))


if __name__ == '__main__':
    main()
