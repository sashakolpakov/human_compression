# Two minimal covers throughout an odd-prime family

For every odd prime `p`, integer `α ≥ 2` and `1 ≤ k ≤ p−1`, the specified
tight chiral polytope of type `{2p,p^α,2p}` has **two distinct minimal regular
polytope covers**. They are dual to one another. This is an all-parameter
written theorem, conditional on the explicitly retained source construction.
The [complete proof](research/case_study/phase49_cover_family_theorem.md),
[independent review](research/case_study/phase59_cover_family_recent_audit.md)
and [root admission](research/case_study/phase67_cover_family_root_audit.md)
record the result and its boundaries.

The input is precisely the equal-parameter Γ1 presentation in Table 2 and
Theorem 4.7 of Cunningham–Pellicer, [*Tight chiral polytopes*, author
version](https://arxiv.org/pdf/2009.04566). Its existence theorem, intersection
property, tight normal form and exact orders are retained. This does not
assert a result for every polytope with that Schläfli type.

Put `q=p^α`. The theorem constructs the following rotation groups:

| Object | Order | Conclusion |
|---|---:|---|
| Source polytope P | `4p²q` | Retained construction |
| Smallest regular maniplex cover R | `4p³q` | Fails the polytope intersection property |
| Regular covers Q and Q′ | `4p⁴q` each | Distinct rank-preserving minimal covers of P |
| Shared cover H=Q⋄Q′ | `4p⁵q` | Polytopal, with kernel `C_p²` over R |

Each of Q and Q′ has prime degree p over R. Since R is not polytopal, this
proves global minimality. Distinct conjugation characters on their order-p
kernels separate them as marked covers. Within the quotients of H, these
are exactly the two minimal covers. Other covers of P need not be quotients
of H, so the theorem does not classify every minimal cover of P.

The shared kernel illustrates the [general cover-kernel theory](COVER_KERNELS.md):
two distinct one-dimensional modules give two invariant axes, and the axes
are exactly the maximal kernels that avoid the intersection defect. Their
join also proves the stated universal-kernel join-density for this family.

## Attribution and verification

Cunningham's [earlier smallest-cover manuscript](https://gabrielcunningham.com/WhichChiralPolytopes.pdf)
already uses a mix with a trivial facet extension and its dual in one finite
example. Prime-degree minimality is part of that earlier strategy. The
repository contribution is the uniform calculation: the full mirror fiber
product, exact normal closure and common quotient, cover intersections,
distinct characters and shared interval. The [claim ledger](research/case_study/phase59_cover_family_recent_audit_attribution.json)
separates those contributions from borrowed construction and geometry.

The complete GAP program rebuilds eight finite examples from bare
presentations. Author, independent and public replays agree exactly after
line-ending normalization. These are diagnostics for the written proof.
Run the public verifier using stock GAP 4.15.1:

```sh
python3 research/case_study/phase67_cover_family_verify.py \
  --output-dir /tmp/human-compression-cover-family-new
```

Choose a new output directory. The verifier needs only the distributed
program, theorem and review; it retains its executed input, raw logs and
report. The older author wrapper also checks private source captures and
is preserved as a historical artifact.

The separate [Lean certificate](research/case_study/formal/CoverCharacterSeparation.scope.md)
proves the algebraic obstruction to a marked isomorphism when one generator
inverts an odd-prime-order kernel element and its counterpart fixes the other
kernel. Family construction, action tables, geometry and minimality remain
written proofs. The [independent interface review](research/case_study/phase69_cover_family_interfaces_recent_audit.md)
checks both the public wrapper and the exact formal statement.

This establishes the multiplicity assertion for the specified first family.
The other four families and the general conjecture remain unresolved here.
The [bounded literature check](research/case_study/phase55_cover_family_source_status.md)
does not establish historical priority or comprehensive current openness;
no newly solved open-conjecture marker is cleared. This separate theorem
adds no manuscript to Compress_10 and has no measured compression factor.
Frozen author files retain their earlier pending-review wording; the linked
independent review and root admission record the later status.
