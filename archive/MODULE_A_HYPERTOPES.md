> **Historical reader — archived from `5401cc9`.** This records the earlier
> compilation programme and its dated scope. Its rates, counts and “current”
> wording do not describe the active topic architecture. Use the
> [current programme](../MANUSCRIPT_PROGRAM.md) or the [archive index](README.md).

# Earlier Module A attachment: Supported kernels and regular three-generator hypertopes

The [complete attachment](../research/case_study/phase130_typed_helly_L034.md),
with its **[mandatory geometric correction](../research/case_study/phase130_geometry_erratum.md)**,
derives the principal construction of Hou–Feng–Leemans,
*Existence of regular 3-hypertopes with 2^n chambers* (2019).
The [independent root review](../research/case_study/phase134_L034_root_review.md)
checks the whole argument and exact arXiv-v1 statement. A
[second independent review](../research/case_study/phase136_typed_helly_review.md)
passes the corrected proof and checks twelve square/diagonal affine examples.

The derivation is:

    U + A's square models + coordinate-kernel coset Helly
        -> L034, Theorem 3.2, with explicit source corrections.

It recovers the original presentation, exact group order and pair orders,
the regular hypertope, the direct product of three cyclic kernels and
the quotient's full semidirect-product description. The two structural
parity rows printed in the source are reversed; the corrected formulas
are proved explicitly. The auxiliary square decompositions retain their
earlier attribution.

The extra common theorem moves intersecting cosets into a single fiber
over the base group. Kernel coordinates then turn their compatibility
into agreement of fixed coordinate values. It works for nonabelian kernel
factors. To obtain a hypertope, the local marked generators must also be
involutions. Independent review found this missing hypothesis in the first
version; the attached dihedral groups satisfy it.

The complete construction is now integrated in the
[24-page second edition of Module A](../MODULE_A.md). This page preserves the
earlier standalone attachment and its historical additive accounting.
The [21-page first edition](../MODULE_A_V1.md) retains its original five-source
intake. The earlier admission of this sixth source raised principal-result
coverage from seventeen to eighteen; integration changes no source count.

The original additive inventory was 208,750 raw UTF-8 bytes, including U,
A, its four required computational artifacts, this attachment and the
mandatory involutivity correction. The subsequent
[N009 diagonal-factor correction](../research/case_study/phase138_N009_decomposition_erratum.md)
is also required for the quoted background in A. Charging its full 5,967
bytes gives **214,717 bytes** for the complete additive package.
This is an inventory, not a compression ratio.
No end-to-end Lean proof of the new geometry or application is claimed.
The separate older proposed answer to Conjecture 3.3 is not re-audited or
counted as a new result by this construction.

To verify the public proof inputs and corrected accounting, use a fresh
output path:

```sh
python3 -B -O research/case_study/phase134_L034_verify.py --output /tmp/NEW-L034-integrity.json
python3 -B -O research/case_study/phase136_typed_helly_affine_check.py --report /tmp/NEW-L034-affine.json
```

The first checks bytes and cost. The second recomputes twelve bounded
affine examples; the all-parameter conclusions use the written proofs.
Primary publication files remain separately acquired inputs.
