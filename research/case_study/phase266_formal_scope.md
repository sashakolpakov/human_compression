# Polynomial algebra in the primitive-square argument

The six declarations in `phase266_formal/PrimitiveSquarePolynomial.lean`
verify the actual quartic used in the retained proof of Conjecture 6.1.
They hold over an arbitrary field, with characteristic different from two
where explicitly required. No finite-field package or numerical witness is
assumed by these declarations.

Write f_s(X) = (s−4)(X²+1)²−4sX² and
z = (s−4)x²−s−4. The formal statements establish:

| Declaration | Mathematical content |
|---|---|
| `evaluated_polynomial` | Evaluation of the actual polynomial expression equals the displayed quartic function. |
| `evaluated_derivative` | Evaluation of its actual formal derivative equals 4xz. |
| `trace_identity` | For x≠0, f_(u²)(x) equals x² times the source expression u²(x+x⁻¹)²−4(u²+(x+x⁻¹)²). |
| `bezout_identity` | (s−4)f_s(x) = z²−16s. |
| `distinct_parameters_no_shared_root` | In characteristic different from two, distinct s,t give no common quartic root. |
| `no_common_derivative_root` | If the characteristic is different from two and s≠0,4, a zero of f_s is not a zero of its derivative. |

The last two statements can be applied over a splitting field. The written
proof uses them to infer distinct simple roots of all conjugate factors.
The file does not assert a `Polynomial.Squarefree` theorem for the norm
polynomial. Its construction over the base field, degree and norm identity,
the finite-field degree argument and quadratic-character norm identity
remain written. So do the primitive-character expansion, Weil estimate,
uniform integer reduction and verification of all eleven exceptional
witnesses. This is not a full Lean proof of Conjecture 6.1 or of the chiral
classification that uses it.

The author replay compiles all six declarations under Lean 4.32.2 with the
pinned Mathlib revision and transitive dependencies. Axiom reports contain
only `propext`, `Classical.choice` and `Quot.sound`. Cached dependency objects
and the compiler remain trusted. No `native_decide`, new axiom or proof hole
is used. Four exact counterexamples in the driver show why characteristic,
parameter and nonzero-variable hypotheses cannot simply be discarded.

The quartic and written argument are retained from `psl2_square_proof.md`.
The new contribution of this packet is the formal verification of these
specified algebraic steps. It adds no conjecture count, principal-source
recovery, historical-priority claim or compression factor.
