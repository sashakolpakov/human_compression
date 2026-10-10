#!/usr/bin/env python3
"""Generate a kernel-checkable 35-cell consequence; no source is overwritten."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    spec = importlib.util.spec_from_file_location('elimination', ROOT / 'phase83_word_elimination.py')
    e = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(e)
    data = json.loads((ROOT / 'phase83_word_elimination.json').read_text())
    steps = data['steps']

    def used(word, count):
        indices = []
        for i, s in enumerate(steps[:count]):
            if s['variable'] in map(abs, word):
                indices.append(i)
                word = e.subst(word, s['variable'], s['replacement'])
        return indices, word

    deps = [used(data['originals'][s['relation']], i)[0] for i, s in enumerate(steps)]
    delta_deps, delta = used((-1, 40), len(steps))
    last_row = 239
    row_deps, row = used(data['originals'][last_row], len(steps))
    selected = set(delta_deps + row_deps)
    queue = list(selected)
    while queue:
        for i in deps[queue.pop()]:
            if i not in selected:
                selected.add(i)
                queue.append(i)
    selected = sorted(selected)
    cells = [steps[i]['relation'] for i in selected] + [last_row]
    if len(selected) != 34 or len(set(cells)) != 35 or tuple(delta) != (-6, 7):
        raise RuntimeError('Unexpected trace dependency graph')

    def word(w):
        return ' * '.join(f'(t {x})' if x > 0 else f'(t {-x})⁻¹' for x in w) or '(1 : K)'

    def hyp(row_index):
        a, b, c, d = data['quads'][row_index]
        return f'hcells {a} {b} {c} {d} (by decide)'

    def simplify(indices):
        return '    simp only [' + ', '.join(f'e{i}' for i in indices) + '] at hh\n' if indices else ''

    header = '''import Mathlib.Tactic.Group
import Mathlib.Tactic.Convert
import Mathlib.GroupTheory.OrderOfElement
import Mathlib.GroupTheory.Coset.Card

/-!
An exact, noncommutative word consequence of 35 explicitly listed cells in
the reviewed 128-point Gamma2 complement presentation. The cell orbit and
its geometric interpretation are separately checked written/computational
inputs. This file assumes the displayed cell relations and proves the
involution defect, with a finite odd-order specialization. It does not
formalize Sylow normalization or polytope recognition.

Generated from phase83_word_elimination.json by phase83_generate_lean.py.
No native evaluation or unproved declaration is used.
-/

namespace MathCompression.OddKernelWord

variable {K : Type*} [Group K]

private theorem solve_pos (a b x : K) (h : a * x * b = 1) :
    x = a⁻¹ * b⁻¹ := by
  calc
    x = a⁻¹ * (a * x * b) * b⁻¹ := by group
    _ = a⁻¹ * b⁻¹ := by rw [h]; simp

private theorem solve_neg (a b x : K) (h : a * x⁻¹ * b = 1) :
    x = b * a := by
  have hi := solve_pos a b x⁻¹ h
  calc
    x = (x⁻¹)⁻¹ := by group
    _ = (a⁻¹ * b⁻¹)⁻¹ := congrArg Inv.inv hi
    _ = b * a := by group

/-- The literal 35 cells sufficient for the defect identity. -/
def requiredCells : List (ℕ × ℕ × ℕ × ℕ) := [
'''
    header += ',\n'.join('  (' + ', '.join(map(str, data['quads'][r])) + ')' for r in cells) + ']\n\n'
    hypotheses = '''(t : ℕ → K)
    (hcells : ∀ a b c d, (a, b, c, d) ∈ requiredCells →
      (t d)⁻¹ * t c * (t a)⁻¹ * t b = 1)'''
    out = header + '/-- These noncommutative cell equations force the marked defect to square to one. -/\n'
    out += 'theorem defect_square ' + hypotheses + ' :\n    ((t 1)⁻¹ * t 40) ^ 2 = 1 := by\n'
    for i in selected:
        s = steps[i]
        out += f'  -- Original orbit row {s["relation"]}; elementary elimination {i}.\n'
        out += f'  have e{i} : t {s["variable"]} = {word(s["replacement"])} := by\n'
        out += f'    have hh := {hyp(s["relation"])}\n' + simplify(deps[i])
        middle = f'(t {s["variable"]})' + ('⁻¹' if s['sign'] < 0 else '')
        out += f'    have hr : ({word(s["left"])}) * {middle} * ({word(s["right"])}) = 1 := by\n'
        out += '      convert hh using 1 ; group\n'
        rule = 'solve_pos' if s['sign'] > 0 else 'solve_neg'
        out += f'    have hs := {rule} ({word(s["left"])}) ({word(s["right"])}) (t {s["variable"]}) hr\n'
        out += '    convert hs using 1 ; group\n'
    out += f'  have hh := {hyp(last_row)}\n'
    out += '  simp only [' + ', '.join(f'e{i}' for i in row_deps) + '] at hh\n'
    out += f'  have hr : {word(row)} = 1 := by\n    convert hh using 1 ; group\n'
    out += '  have hs : ((t 6)⁻¹ * t 7) ^ 2 = 1 := by\n'
    out += '    calc\n      ((t 6)⁻¹ * t 7) ^ 2 = (t 16)⁻¹ * t 32 * (' + word(row) + ') * (t 32)⁻¹ * t 16 := by simp only [pow_two]; group\n'
    out += '      _ = 1 := by rw [hr]; group\n'
    out += '  have hd : (t 1)⁻¹ * t 40 = (t 6)⁻¹ * t 7 := by\n'
    out += '    simp only [' + ', '.join(f'e{i}' for i in delta_deps) + ']\n    group\n'
    out += '  rw [hd]\n  exact hs\n\n'
    out += '/-- In a finite group of odd order, the two distinguished entries coincide. -/\n'
    out += 'theorem defect_trivial_of_odd_card [Finite K] ' + hypotheses + '\n    (hodd : Odd (Nat.card K)) : t 1 = t 40 := by\n'
    out += '''  have hs := defect_square t hcells
  have hd := orderOf_dvd_of_pow_eq_one hs
  have hone : (t 1)⁻¹ * t 40 = 1 := by
    rcases (Nat.dvd_prime Nat.prime_two).mp hd with h | h
    · exact orderOf_eq_one_iff.mp h
    · have htwo : 2 ∣ Nat.card K := by
        simpa only [h] using orderOf_dvd_natCard ((t 1)⁻¹ * t 40)
      exact False.elim ((Nat.not_even_iff_odd.mpr hodd) (even_iff_two_dvd.mpr htwo))
  exact inv_mul_eq_one.mp hone

#print axioms defect_square
#print axioms defect_trivial_of_odd_card

end MathCompression.OddKernelWord
'''
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('x') as f:
        f.write(out)
    print(json.dumps({'file': str(args.output), 'sha256': hashlib.sha256(out.encode()).hexdigest(),
                      'eliminations': len(selected), 'original_cells': cells,
                      'trace_sha256': hashlib.sha256((ROOT / 'phase83_word_elimination.json').read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
