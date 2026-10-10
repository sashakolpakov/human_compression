# Topic complexity and the value of reusable proofs

A module is a mathematical topic, not a single replacement manuscript.
For topic A, the historical papers are LA₁, …, LAₖ. Our corresponding
application papers are A₁, …, Aₖ, and U_A contains their shared theory.
Each correspondence names the results recovered, the exact source edition
and all earlier results used. A short section becomes an application paper only
after its definitions, hypotheses, exceptional cases and proofs are complete.

U_A need not be a section of the present umbrella manuscript. It may combine
relevant umbrella theorems with general arguments extracted from the existing
application drafts. U_A and U_B may overlap. Their costs are nevertheless
charged in full in their respective independent topic comparisons.

## 1. Independent topic comparison

Fix a length convention c before comparing. The principal topic measure is

$$
R_A=\frac{\sum_{i=1}^{k}c(LA_i)}
{c(U_A)+\sum_{i=1}^{k}c(A_i)}.
$$

Topic B uses the same formula with its own full U_B. We do not subtract its
overlap with U_A. Conversely, within A we do not charge U_A again to each Aᵢ.
The conditional application factors are

$$
r_{A,i}\mid U_A=\frac{c(LA_i)}{c(A_i)}.
$$

Display c(U_A) beside those conditional factors. A large conditional factor
does not establish that the umbrella has paid for itself. The cumulative
comparison after n applications is

$$
H_A(n)=\sum_{i\le n}c(LA_i),\qquad
O_A(n)=c(U_A)+\sum_{i\le n}c(A_i).
$$

The first n with H_A(n) ≥ O_A(n), if one exists, is the observed break-even
point for that fixed theory and source sequence. This is relative to the
actual historical manuscripts, not to a minimum possible proof length.
If the theory changes, record a new version and all resulting application
changes; do not carry an old denominator into the new comparison.

## 2. A separate GKM reuse account

For chronological reuse, record the proved library K available before an
application. A library item has a fixed statement, hypotheses, complete
proof, definitions, earlier results used and version. The dependency graph must
contain the material needed to use it, not just theorem names.

Let Dᵢ be the transitive dependency closure of the new application, including
its own proof, new interfaces and programs required by the proof.
Under an additive, fixed representation, define

$$
\Delta_i(K_{i-1})=c(D_i\setminus K_{i-1}),\qquad
K_i=K_{i-1}\cup D_i.
$$

Here the set difference is between identified proof components, not between
words in manuscripts. A theorem is reused only when its actual hypotheses
have been discharged. Those checks, any change of notation or coordinates
requiring an argument, and every new argument needed to apply a theorem are charged. Merely similar
proofs are not one component. Mutually dependent definitions and lemmas are
grouped into an acyclic unit.

This account can recognize reuse across topics, but is explicitly conditional
on the recorded earlier library. It does **not** change either topic's full
independent acquisition cost in §1. Freeze the task order and library
snapshots; report which nodes were already paid for and which were acquired
at each step. A dependency graph supplies admissible orders, not a unique
chronology. Different admissible orders can change the marginal profile.

For a fixed graph with no deletions or revisions, the costs telescope:

$$
c(K_0)+\sum_i\Delta_i=c\!\left(K_0\cup\bigcup_iD_i\right).
$$

Thus no acquired theory disappears from the sequential total. New versions
and refactorings need an explicit addition/removal ledger; the identity is
not applied across unrecorded rewrites. Also distinguish retained-library
size from cumulative development effort and from the cost of each new paper.

The relevant GKM precedent is its
[frozen transfer-value protocol](https://github.com/sashakolpakov/gkm/blob/2996828e4b8f6c5f9709587473721d5f7edccf62/transduction/TRANSFER_VALUE.md):
charge acquisition and later adapters, test later tasks against the retained
interface, and ask when the savings repay the acquisition. Its mechanism is
an explicit sequence of library states; externally numbered levels are not
essential. We borrow that accounting discipline, not its numerical units or
experimental conclusions. A historical reconstruction is labelled
retrospective; a genuinely later, previously unworked application can test
prospective transfer separately.

## 3. The graphs to produce

For every topic, fix the order of the corresponding historical and application
papers, specify the results being compared, and publish:

1. **Per-paper costs:** the historical heights c(LAᵢ), one separately visible
   acquisition bar c(U_A), and the application heights c(Aᵢ). Do not add U_A
   to every application bar. Unknown or incomplete costs are missing, not zero.
2. **Cumulative costs:** H_A(n) and O_A(n), including the full umbrella, so
   their crossing and the total factor can be read directly.
3. **Chronological reuse:** the actual acquisition increments Δᵢ, each tied
   to its pre-existing library snapshot. A peak followed by cheap applications
   is meaningful only if the earlier proof remains valid and genuinely used.
4. **Two theorem-dependency DAGs:** the source literature and the replacement,
   with corresponding output contracts aligned. Nodes name complete proof
   units; edges mean mathematical use. Distinguish retained theorems, proved
   local results, hypothesis checks, computations and unresolved dependencies.

Attach lengths to audited proof units and show retained background separately.
Bibliographic citations alone are not proof edges. Induction is represented
by its complete induction argument, not by a spurious self-loop. Node counts,
edge counts and graph depth describe structure; none substitutes for proof
length or measures the worth of the authors. The source graph must receive
the same recognition of genuine earlier reuse as ours.

A [first dependency pilot](DEPENDENCY_PILOT.md) traces the proof of one main
result. It shows dependencies for that particular result; the full topic has
not yet been divided into complete papers and measured.

## 4. Measurement and current status

Use identical length rules on comparable written material. Include necessary
definitions, interfaces, proof appendices and local computational proof
artifacts. Inventory optional Lean validation, audit records and rendering
machinery separately. Classical inputs remain explicitly retained on both
sides. A paper's use of an earlier result must not be hidden in the graph.

For the additive DAG ledger, use a fixed normalized text representation with
explicitly assigned boundaries; the full document is partitioned so that
context and exposition are not lost between nodes. Separately report rendered
pages and the established PDF-text sensitivities. Independently paginated PDF
counts need not add, so no conditional PDF denominator is obtained by
subtracting two extracted totals. A short nominal PDF is not a saving if its
necessary proof sits in an uncharged file.

Recovering earlier results, correcting a false statement and answering an open
question are different achievements. The graph does not change which has
been proved. When only some results are recovered, any comparison using the
full source length must say so; it is not a replacement of the whole paper.

The current A–D documents are reviewed assemblies from which to build these
topic families. Their frozen measurements remain valid at their recorded
scope, but do not yet supply c(U_A), c(A₁), … or the requested topic curves.
Dividing those documents into arbitrary text slices would not establish such
a decomposition. The next step is to identify shared complete arguments,
write the corresponding applications, audit both dependency graphs and then
measure their actual lengths.
