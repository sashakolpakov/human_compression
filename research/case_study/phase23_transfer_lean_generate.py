#!/usr/bin/env python3
"""Render the frozen transfer graph as literal Lean data, without proving it."""
import argparse
import hashlib
import json
from pathlib import Path

EXPECTED = 'b3cf789f5278c773636a9e440a06115dd023b11c0519bbe3c68a51ce33b3c0d6'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--graph', type=Path, default=Path(__file__).with_name(
        'phase22_excess3_final.graph.json'))
    p.add_argument('--output', type=Path, default=Path(__file__).parent /
                   'formal' / 'Phase23TransferAnnihilator.lean')
    args = p.parse_args()
    raw = args.graph.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXPECTED
    initial, states, edges, _ = json.loads(raw)
    assert (len(initial), len(states), len(edges)) == (706, 708, 1522)
    assert all(1 <= s <= 708 and 0 <= k <= 3 for s, k in initial)
    assert all(1 <= s <= 708 and 1 <= t <= 708 and 0 <= w <= 3
               for s, t, w in edges)
    pairs = ',\n  '.join(f'({s}, {k})' for s, k in initial)
    triples = ',\n  '.join(f'({s}, {t}, {w})' for s, t, w in edges)
    text = r'''import Mathlib.Tactic

/-!
Exact integer transfer for the saved third-excess state graph.
Input graph SHA256: GRAPH_SHA
Generated literal data: 706 initial rows and 1522 weighted edges.
The group-to-graph completeness theorem is NOT asserted by this module.
The four large arithmetic checks use native_decide and its compiler-evaluation
axioms. See the companion scope note; this is NOT kernel-only arithmetic.
Column coordinate 4*(state-1)+excess has state in 1..708 and excess in 0..3.
-/

set_option maxRecDepth 1000000
set_option maxHeartbeats 0

namespace MathCompression.Phase23Transfer

def stateCount : Nat := 708
def dimension : Nat := 4 * stateCount

def initialRows : Array (Nat × Nat) := #[
  INITIAL_ROWS]

def edges : Array (Nat × Nat × Nat) := #[
  EDGE_ROWS]

abbrev V := Array Int

def zero : V := Array.replicate dimension 0

def transfer (v : V) : V := Id.run do
  let mut out := zero
  for (source, target, weight) in edges do
    for k in [:4-weight] do
      let src := 4 * (source-1) + k
      let dst := 4 * (target-1) + k + weight
      out := out.set! dst (out[dst]! + v[src]!)
  return out

def delta (v : V) : V := (transfer v).zipWith (fun a b => a-b) v

def v5 : V := Id.run do
  let mut out := zero
  for (state, excess) in initialRows do
    let i := 4 * (state-1) + excess
    out := out.set! i (out[i]! + 1)
  return out

def v7 : V := transfer (transfer v5)

def terminalBasis : V := zero.set! 3 1

def excessSum (v : V) (k : Nat) : Int :=
  (List.range stateCount).foldl (fun n s => n + v[4*s+k]!) 0

theorem literal_data_dimensions :
    dimension = 2832 ∧ initialRows.size = 706 ∧ edges.size = 1522 := by
  decide +kernel

theorem third_difference :
    delta (delta (delta v7)) = terminalBasis.map (fun x => 125*x) := by
  native_decide

theorem terminal_basis_fixed : transfer terminalBasis = terminalBasis := by
  native_decide

theorem fourth_difference : delta (delta (delta (delta v7))) = zero := by
  native_decide

theorem newton_coefficients :
    [excessSum v7 3, excessSum (delta v7) 3,
     excessSum (delta (delta v7)) 3,
     excessSum (delta (delta (delta v7))) 3] = [2499, 1780, 715, 125] := by
  native_decide

#print axioms literal_data_dimensions
#print axioms third_difference
#print axioms terminal_basis_fixed
#print axioms fourth_difference
#print axioms newton_coefficients

end MathCompression.Phase23Transfer
'''
    text = text.replace('GRAPH_SHA', EXPECTED).replace(
        'INITIAL_ROWS', pairs).replace('EDGE_ROWS', triples)
    args.output.write_text(text)
    print(json.dumps({'output': args.output.name,
                      'sha256': hashlib.sha256(text.encode()).hexdigest(),
                      'graph_sha256': EXPECTED,
                      'initial_rows': len(initial), 'edges': len(edges)}))


if __name__ == '__main__':
    main()
