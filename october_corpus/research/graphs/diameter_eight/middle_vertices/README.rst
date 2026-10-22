A local obstruction in the defect graph
======================================

``ARGUMENT.rst`` proves the following statement. In a triangle-free
k-regular graph of order 6k+2 with an eight-edge geodesic, k at least five,
take the neighborhoods A, B and C of the geodesic's vertices at positions
0, 4 and 8. Their union is independent. Its complement induces a graph F
with exactly k edges. A complementary vertex meeting B on both sides of
the geodesic has F-degree zero or one. The proof counts at least d(k-d)
distinct defect edges and excludes 2 <= d <= k-2.

For the prescribed 32-vertex seed this excludes any extension containing
the four edges 21--v, 25--v, v--u and v--w, with distinct u,v,w outside
the independent set and its three centers. ``families.frontier`` contains
the two complete original records to which the obstruction was applied.
Their permanent identities are SHA256 hashes of the individual lines;
small historical node indices are not substitutes for those identities.

The written proof and independent mathematical review are copied without
changes. ``SourceManifest.json`` records their provenance, every local
source hash and the earlier check of the complete 51-record frontier and
persistence at checkpoint 7727. Original absolute paths in that manifest
are provenance only. Reproduction below needs no external project files.

Standalone reproduction
-----------------------

From the root of a clone, create a fresh directory outside the checkout and
run the standard-library checker::

  MIDDLE_OUTPUT="$(mktemp -d /tmp/middle_vertices.XXXXXX)"
  python3 -E -B -S \
    october_corpus/research/graphs/diameter_eight/middle_vertices/check_families.py \
    --input october_corpus/research/graphs/diameter_eight/middle_vertices/families.frontier \
    --input-sha256 0934ae09a9a8a45e93571f7c5c30352e90b57e13068d38de053598bd831f4bb0 \
    --out "$MIDDLE_OUTPUT/result.json"

The checker authenticates both complete records, the entire seed, the
three saturated neighborhoods, the partial marked distance, the independent
set and a literal four-edge witness in each family. It writes one result
outside the checkout. It performs no completion search and imports no
project, group or graph library. The general theorem has a written proof
and independent review; this finite check is not its formalization in Lean.

The standalone check passed from an isolated copy of this package. Its
complete actual return, sampled guard receipt and result are retained in
``evidence/reproduction.json``. It used about 27 MiB of sampled resident
memory and returned in less than one tenth of a second.

The two families are mathematically empty under the stated contract. The
accepted census still has 51 pending families: its current transition
language does not record this new algebraic proof kind. This package
changes no census state, completes no original manuscript and claims no
compression factor or new solution of a source conjecture. The other
restrictions and proposed class covers in the frozen proof retain their
stated qualifications.
