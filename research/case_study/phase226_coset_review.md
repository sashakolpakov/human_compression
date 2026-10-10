# Independent semantic review of the coset upper certificates

10 October 2026. **Accepted within the rank-three scope below.**
This review binds `phase219_manifest.json`, SHA256
`0e97c6931e3c0ae67ef9a33c429d1d017a43cc193f10e65101e39b05dd6d8469`.
The twenty-four exported files match that manifest. No frozen author file
was changed.

I read the complete general Lean source, the concrete examples, both
untrusted generators, the runner, the actual rank-three relator definition,
and the final proof-row assembly. I also inspected Mathlib's actual
`PresentedGroup` definition and the relevant universal-generator interface
at the pinned revision. The conclusion concerns the actual presented group,
not just a finite quotient action.

## 1. Why the bound is an upper bound

`RightCosets H` is the quotient by the genuine right-coset equivalence
relation for an arbitrary subgroup. Right multiplication is well defined
without normality. A name is interpreted as the coset of its supplied word;
no distinctness, completeness or transitivity of those names is assumed.

The `Derives` constructors introduce only empty paths, justified subgroup
loops at the root, literal representative-word definitions, concatenation,
reversal and a single missing edge in a stated relator. The tree constructor
requires equality of words, not a presumed coset-table equality. The gap
constructor requires membership of the reconstructed entire word in the
relator set and two previously derived paths from the same starting name.
The reversal is correct because each generator is an involution.

`derives_sound` proves the corresponding actual coset equality by induction.
In its gap case the relator identity turns the prefix followed by the
missing generator into the inverse of the suffix. This is precisely the
identity supplied by the two paths; the orientation of the suffix and of
right multiplication agrees throughout.

Completeness means an outgoing derived transition for each name and each
generator. `complete_words` then gives paths for all positive words.
`words_surjective` proves that positive words exhaust the group: their
values form a subgroup, because reversal supplies inverses, and they contain
the stipulated generators. This supplies a surjection from the finite name
set onto the actual cosets. The inverse-coset equivalence translates to
Mathlib's usual left-coset index. Both finiteness and the numerical bound
are proved. In particular the argument does not exploit the convention
that the natural cardinality of an infinite type is zero.

The finite-facet order theorem separately derives finiteness of the whole
group and uses the ordinary cardinality–index identity. Its hypotheses
include finiteness of the subgroup and the already proved finite quotient.
No expected group order is inserted as a premise.

## 2. The presentation and checker interfaces

`Universal rels` uses Mathlib's quotient of the free group by the normal
closure of the specified relations. Here those relations are exactly the
squares of the marked generators and the evaluations of the supplied
unsigned relator words. The generic proofs establish that the markers obey
them and generate this quotient. The facet is the subgroup closure of the
selected marked generators. There is no extra quotient map to a computed
finite group in this definition.

The executable checker begins with no known transitions. A path must be
continuous and use only edges already on its proved list. A tree instruction
checks the representative definition, and a gap instruction checks the
whole relator and both paths. `step_sound` and `replay_sound` carry this
invariant through the list. The final finite completeness test becomes the
hypothesis of the actual-coset theorem. Thus Boolean acceptance has the
claimed semantics, rather than merely testing relators in an action.

The four concrete rejection statements cover an incomplete one-name root
loop, removal of the relators, an empty trace and a false tree definition.
The two author mutation controls remove the tree-word or relator-membership
check from the program. Their logs show failures at the corresponding
premises in `step_sound`, not an unrelated parse error. The failed builds
may display `sorryAx` after their errors; they are explicitly rejected and
are not accepted proof artifacts.

## 3. The concrete rank-three certificate

The actual Lean list has exactly thirteen words: the three pair relations
with exponents eleven, two and eleven, followed by all ten words

\[
\bigl((r_1r_2)^k(r_0r_1)^k\bigr)^2,\qquad 1\leq k\leq10.
\]

The generator squares enter through `Universal`. This is the rank-three,
label-eleven specialization of Li–Zhang's arXiv v1 presentation. The
kernel-checked `relators_literal` equation identifies the concrete list
with this formula. No source rank-three order theorem is a premise.

The large file deliberately uses direct `Derives` proof terms. The naming
tree gives literal recursive word definitions. Each inverse deduction cites
an earlier proof; each gap cites its specific relator and earlier edge
proofs. The array entry at each name carries proofs of all three outgoing
transitions. Its length and the equation equating every retrieved name with
the requested name are checked in Lean. Projecting those entries supplies
`Complete`, which feeds the actual universal index theorem. There is no
unproved table-surjectivity assertion in the assembly.

As an additional independent check, I replayed all 3,072 JSON deduction
records without importing either author generator or checker. The replay
checked 2 subgroup loops, 1,023 tree definitions, 1,488 reversed edges and
559 relator deductions, including strictly earlier dependencies and every
path endpoint. It compared all the resulting declarations with the actual
Lean edge declarations and compared the actual Lean relator list with the
source formula. False tree data, a missing relator justification and
root-loop-only data were each rejected. This supplementary Python replay
has no role as a trusted Lean axiom.

The source table and the program used to discover the proofs are outside
the logical trust boundary after the generated proof terms have compiled.
The formal declaration binds the actual universal group and gives facet
index at most 1,024. It does not prove that the 1,024 names are distinct;
that would be a lower-bound assertion and is unnecessary here.

## 4. Formal scope and attribution

The canonical sources have 25 selected axiom reports: 13 in the general
kernel, 9 in the small examples and 3 in the rank-three file. Their frozen
successful logs contain only `propext`, `Classical.choice` and `Quot.sound`.
The larger proof's completeness and index declarations include the relevant
dependencies of the direct proof rows. No `native_decide`, new axiom or
proof hole occurs in the three canonical sources. Ordinary `decide` is
checked by kernel reduction. The two semantic mutations are failed builds.

The independent root process owns the fresh public compiler replay. This
review did not repeat that compilation; it independently reviewed the
actual proof sources, checked the frozen successful logs, and ran the
separate finite deduction audit. Pinned Mathlib sources and existing
compiled dependency objects remain the explicit infrastructure trust
boundary recorded by the author runner.

The concrete claims are the dihedral facet index at most eleven, dihedral
group order at most twenty-two, and rank-three facet index at most 1,024.
The generic finite-facet order theorem is present. The map from the
dihedral universal group onto the rank-three facet, and its composition
into a concrete Lean theorem giving rank-three order at most 22,528, have
**not** yet been formalized in this packet. Rank-four and rank-five tables,
finite-field image orders, simplicity and signed memberships are also
outside it. The complete conjecture refutation remains short of an
end-to-end Lean proof.

Classical coset enumeration supplies the inference principle; Mathlib
supplies the free-group, quotient and cardinality infrastructure;
Li–Zhang supplies the source presentation; the earlier phase214 work
supplies the candidate table and its reviewed deduction argument. The
present package contributes the formal inference system and concrete
certificates. This acceptance adds no new conjecture resolution, principal
source replacement or compression ratio. The generated proof text remains
part of the actual verification cost.

## 5. Reproduction

The supplementary independent check is:

```sh
python3 -B -O phase226_deduction_audit.py --out /fresh/result.json
```

It requires the twenty-four bound phase219 exports and their manifest, but
no Lean compiler, GAP, C++ scanner or primary PDF. The full compiler command
and its dependencies remain those in `phase219_scope.md`. The review's
finite replay must not be described as a substitute for that Lean build.
