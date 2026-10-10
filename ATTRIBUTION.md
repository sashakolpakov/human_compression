# Attribution and proof annotations

Use these signs in the new application papers only when an exact source,
proof and verification record supports them. The original edition-specific
annotation experiment is in the [historical archive](archive/ATTRIBUTION.md).

| Sign | Meaning | Evidence needed |
|---|---|---|
| **[B]** | Borrowed result, idea or construction | Original authors and reference, stating exactly what is used |
| **[I]** | Our contribution to the proof or exposition | Description of the contribution and the older ingredients it uses; historical novelty stated separately |
| **[R]** | One shared argument yields multiple earlier results | Named targets and the internal common argument; no numerical saving implied |
| **[C]** | Corrected assertion, range of validity or reference | The original assertion, the problem with it and the precise correction |
| **[V]** | Exact finite computational evidence | Identified program, a recorded rerun and the finite cases covered |
| **[L]** | Lean proof | Exact declaration, source hash and compiler report; an explanation of any connection to the written argument that remains unformalized |
| **[M]** | Measured compression | Exact numerator, complete denominator, metric, source editions and reviewed measurement |
| **[O]** | Previously open conjecture proved | Exact conjecture and version, an independently reviewed proof, and a separate check of later literature and priority |

“Our contribution” can mean a shared organization, explicit proof,
correction or new consequence in this exposition. It does not by itself
mean that the idea or theorem is historically new. Elementary group theory,
standard coset constructions and earlier authors' strategies retain their
attribution even when we use new notation or formalize them.

A paper's final review should state which older results it derives, which
proofs it uses, what the computations and Lean files establish, and what
supports any claim of a saving or new result. An unfinished proof or
priority check remains marked as unfinished. The sign summarizes that
review; it does not replace it.

A measured sign applies only to its exact compared manuscripts and
accounting convention. Historical compilation measurements do not carry
over to the new topic families. See [topic complexity](TOPIC_COMPLEXITY.md)
and the [separate question-results catalogue](CONJECTURE_RESULTS.md).

The earlier [eleven-source](archive/ATTRIBUTION_11.md) and
[twelve-source](archive/ATTRIBUTION_12.md) passes, their tools and frozen
annotated readers remain available for reuse and audit.
