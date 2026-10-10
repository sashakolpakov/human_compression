# Bounded literature check for the abelian-Frattini cyclic-TPP theorem

10 October 2026. This is a search record, not a publication-priority claim.

The exact-phrase searches `"triple product property" "Frattini"`,
`"cyclic" "triple product property" "2-groups"`, and
`"triple product property" "abelian" "Frattini subgroup"` did not identify
the exact theorem proved in phase11_abelian_frattini.md. This limited search
does not establish that the theorem is new.

Two nearby primary manuscripts were checked:

- Sandeep R. Murthy, [On the triple product property for subgroups of finite
  nilpotent groups of class 2](https://arxiv.org/html/2602.15796v1),
  arXiv:2602.15796v1, submitted 17 February 2026. The abstract, introduction,
  and preliminary statements through Proposition 2.7 were read. Its stated
  principal results concern arbitrary subgroup TPP triples under class-two,
  center, commutator-order or character-degree hypotheses. The stated results
  do not supply the present all-abelian-Frattini cyclic theorem. No full-proof
  correctness audit of that manuscript is claimed here.
- Murthy, [A note on the triple product property for finite groups with
  abelian normal subgroups of prime index](https://arxiv.org/html/2512.16730v7),
  arXiv:2512.16730v7, dated 9 January 2026. The abstract and the exact
  Corollary 4.3 with its proof were read. Corollary 4.3(2) proves the subgroup
  TPP bound for a p-group with an abelian subgroup of index p. The present
  argument assumes instead that the Frattini subgroup is abelian, and its
  minimum counterexample has Frattini index p². No inference from abelian
  Frattini subgroup to existence of an abelian maximal subgroup is used.

These works are contextual references, not retained dependencies of the
new binary-action proof. The theorem in phase11_abelian_frattini.md is a
written group-theoretic argument with separate finite diagnostics. It has
internal mathematical review, not external peer review or a verified
priority determination. The full cyclic-TPP conjecture and the unrestricted
Hou–Feng–Leemans Conjecture 3.3 remain unresolved in this phase.

## Reproduction of the original diagnostics

Run from the directory containing the scripts:

```sh
python3 phase11_binary_action_check.py --output /tmp/phase11_binary_action_check.json
python3 phase11_cyclic_tpp_check.py --output /tmp/phase11_cyclic_tpp_check.json
gap -q phase11_tpp_equality_witness.g
```

The first command uses only Python 3's standard library. The second also
requires the byte-identical phase10_cyclic_tpp_check.py and the proof files
whose hashes it records. GAP must be available on PATH for the last command,
with its SmallGrp package. The witness was checked with GAP 4.15.1 and
SmallGrp 1.5.4. The reports include input hashes, so they can be compared
without overwriting the saved reports. No group catalogue is used by the
uniform abelian-Frattini proof or its binary checker.
