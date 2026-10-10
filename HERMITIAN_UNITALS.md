# Hermitian unitals and explicit unitary transport

For every prime power q > 2, the Van Nypelseer geometry built from the
Hermitian unital U_H(q) is firm, residually connected and flag-transitive.
The same proof works at q = 2 and shows that PGU(3,q) acts regularly on
chambers. This answers Conjecture 1 in *A Generalization of a Construction
due to Van Nypelseer* (2005), §4.6. Historical priority remains unverified.

The [complete geometric proof](research/case_study/phase275_hermitian_unital_proof.md)
now has a published [independent full review](research/case_study/phase210_hermitian_conjecture_review.md)
and [root semantic review](research/case_study/phase275_root_review.md).
The construction and classical finite-field facts retain their attribution.
The contribution is the uniform argument for the stated conjecture,
its precise geometric identifications and verified supporting formulas.

The difficult residue becomes a graph on vectors of fixed nonzero
Hermitian norm. Two vectors are joined when their difference is isotropic.
An [explicit unique unitary transport](research/case_study/phase210_norm_shell_transport.md)
between any two such vectors, together with elementary upper and lower
matrices, proves the graph connected. The same transport theorem is reused
in the later triangle-geometry application.

[Thirteen Lean declarations](research/case_study/formal/HermitianPlaneTransport.lean)
verify actual Gram equations, norm preservation, unique transport and
isotropic root moves over an arbitrary involutive field. Their
[scope](research/case_study/formal/HermitianPlaneTransport.scope.md) leaves
the finite-field generation and full geometric theorem written.
The independent computation checks four literal unital models, their PGU
chamber actions and all 18,612 vector-pair specializations.

```sh
python3 -B -O research/case_study/phase275_check.py \
  --out /tmp/NEW-Hermitian-review \
  --gap GAP --lean LEAN --packages PACKAGES
```

The [publication record](provenance/phase133_review.md) explains the exact
archive bindings and fresh replay. This upgrades an existing question's
verification; it does not count a second solution or a compression ratio.
