# Independent review of the eight-dimensional tensor model

Verdict: PASS for the complete written theorem, literal checker, and stated limitations. Exact reviewed bytes are bound in the companion JSON. This review is separate from any subsequent global intersection or flag-transitivity construction.

I read every section of the tensor-model proof and the complete standalone checker. A fresh execution reproduced the authored report byte for byte, SHA256 f17554f799771737f287235b72322c8effcc30c9087869434a83f033b6abe2fd. It checks all 576 entries of the nine integral relators, the reversal identities, the four nonidentity integral involutions, the two exact tensor words, all three fixed integral subgroup closures and reductions, and the stated 23 Fibonacci samples.

The finite computations support exactly the uses made of them. They are not being used to extrapolate the all-parameter statement. That statement follows from the separate written reasoning, which I checked as follows:

- Over a nonzero commutative ring, the three full factor algebras are distinct. Centralizing the matrix units forces an invertible factor to be a scalar unit; conjugation also detects every nontrivial factor permutation. No cancellation using field inverses or a characteristic restriction is hidden.
- The Fibonacci identity makes \(N^s\) scalar modulo \(F_s\). No smaller positive power is scalar, since its off-diagonal entry lies strictly between zero and \(F_s\). This applies to every composite modulus as well as primes.
- The exact tensor formulas give a translation subgroup \(C_s^2\): if its product is identity, each factor is scalar, forcing both exponents divisible by \(s\).
- Pure permutations give the full \(S_3\), normalize the exponent-sum-zero lattice and meet the pure translations trivially. Thus the intermediate subgroup has order \(6s^2\).
- The extra tensor \(z\) is outside that subgroup for \(F_s>2\): its first factor is the nonsymmetric matrix \(S\), whereas every scalar unit times any integral power of symmetric \(N\) remains symmetric. This argument does not require normality of the intermediate subgroup.
- The resulting lower bound \(12s^2\) equals the retained marked toroidal presentation upper bound. Therefore this is an exact marked local isomorphism, rather than an identification from order alone.
- The three other local groups remain injective for every Fibonacci modulus with \(s\ge4\). The integer entry-difference bound handles moduli at least five, and the actual modulus-three calculation handles \(s=4\). The modulus-two collapse at \(s=3\) is explicitly and correctly excluded from the local-group assertion.

I also compared the nine displayed words and the four local adapters with the already checked L003 presentation used by the frozen even-family proof. This was not a new full-paper reading or priority audit.

The result supplies every exact parameter \(s\ge3\) and all four prescribed local groups for \(s\ge4\). It does not prove global subgroup IP, typed coset Helly, an all-parameter hypertope theorem, faithfulness of the universal presentation, or a universal-group order formula. The authored note preserves all these boundaries.
