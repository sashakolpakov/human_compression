import Mathlib.Data.List.Nodup

/- Literal finite data from the separately hash-bound affine-map report.
   XOR masks encode vectors in F₂^13. Only the displayed finite predicates
   are checked here; no group, quotient-code or geometry theorem is imported. -/
set_option maxRecDepth 1000000
set_option maxHeartbeats 0
namespace Phase30AffineData

def columns : List Nat := [1, 2, 4, 8, 16, 32, 64, 112, 128, 131, 256, 512, 1024, 1027, 2048, 2816, 4096, 4108, 1109, 1113, 2497, 2545, 7300, 8068, 3863, 3112, 7116, 6387, 629, 330]

def vertexBlocks : List (List Nat) := [[0, 4, 19, 23, 26], [1, 5, 18, 22, 27], [0, 2, 7, 11, 28], [1, 3, 6, 10, 29], [2, 4, 13, 15, 24], [3, 5, 12, 14, 25], [6, 8, 15, 17, 26], [7, 9, 14, 16, 27], [8, 10, 19, 21, 25], [9, 11, 18, 20, 24], [12, 16, 21, 23, 28], [13, 17, 20, 22, 29]]

def faceBlocks : List (List Nat) := [[0, 11, 17, 20, 26], [1, 10, 16, 21, 27], [2, 8, 15, 21, 28], [3, 9, 14, 20, 29], [4, 9, 16, 23, 24], [5, 8, 17, 22, 25], [3, 6, 12, 23, 26], [2, 7, 13, 22, 27], [4, 10, 13, 19, 29], [5, 11, 12, 18, 28], [0, 7, 14, 19, 25], [1, 6, 15, 18, 24]]

def incidentPairs : List (Nat × Nat) := [(0, 0), (0, 4), (0, 6), (0, 8), (0, 10), (1, 1), (1, 5), (1, 7), (1, 9), (1, 11), (2, 0), (2, 2), (2, 7), (2, 9), (2, 10), (3, 1), (3, 3), (3, 6), (3, 8), (3, 11), (4, 2), (4, 4), (4, 7), (4, 8), (4, 11), (5, 3), (5, 5), (5, 6), (5, 9), (5, 10), (6, 0), (6, 2), (6, 5), (6, 6), (6, 11), (7, 1), (7, 3), (7, 4), (7, 7), (7, 10), (8, 1), (8, 2), (8, 5), (8, 8), (8, 10), (9, 0), (9, 3), (9, 4), (9, 9), (9, 11), (10, 1), (10, 2), (10, 4), (10, 6), (10, 9), (11, 0), (11, 3), (11, 5), (11, 7), (11, 8)]

def blocks : List (List Nat) := vertexBlocks ++ faceBlocks

def vectors (b : List Nat) : List Nat := b.map (fun i => columns[i]!)

def xorSpan : List Nat → List Nat
  | [] => [0]
  | x :: xs => let s := xorSpan xs; s ++ s.map (Nat.xor x)

def blockSpan (b : List Nat) : List Nat := xorSpan (vectors b)

def commonIndices (i j : Nat) : List Nat :=
  vertexBlocks[i]!.filter (fun k => faceBlocks[j]!.contains k)

def membershipChecks : Bool := blocks.all fun b =>
  (List.range 30).all fun i => (blockSpan b).contains columns[i]! == b.contains i

def intersectionChecks : Bool := incidentPairs.all fun (i, j) =>
  let left := blockSpan vertexBlocks[i]!
  let right := blockSpan faceBlocks[j]!
  let expected := blockSpan (commonIndices i j)
  (left.all fun x => !(right.contains x) || expected.contains x) &&
  (expected.all fun x => left.contains x && right.contains x)

def oddChecks : Bool := blocks.all fun b =>
  b.length == 5 && (vectors b).foldl Nat.xor 0 == 0

def rankChecks : Bool := blocks.all fun b => (blockSpan b).eraseDups.length == 16

def shapeChecks : Bool :=
  columns.length == 30 && vertexBlocks.length == 12 && faceBlocks.length == 12 &&
  incidentPairs.length == 60 && columns.all (fun x => 0 < x && x < 8192) &&
  blocks.all (fun b => b.all (fun i => i < 30)) &&
  incidentPairs.all (fun (i,j) => i < 12 && j < 12 && (commonIndices i j).length == 2)

theorem finite_shapes : shapeChecks = true := by decide

theorem columns_distinct : columns.Nodup := by decide

theorem all_720_memberships : membershipChecks = true := by decide

theorem all_60_intersections : intersectionChecks = true := by decide

theorem all_24_odd_relations : oddChecks = true := by decide

theorem all_24_span_sizes : rankChecks = true := by decide

#print axioms finite_shapes
#print axioms columns_distinct
#print axioms all_720_memberships
#print axioms all_60_intersections
#print axioms all_24_odd_relations
#print axioms all_24_span_sizes
end Phase30AffineData
