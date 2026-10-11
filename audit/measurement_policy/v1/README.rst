Comparing validation costs fairly
================================

This correction withdraws the earlier software-inclusive compression factors.
Those fractions added our programs to the replacement denominator while
leaving the originals' software unmeasured. Correct arithmetic did not make
that a symmetric comparison.

The default comparison excludes optional validation on both sides. If validation
is included, both sides must be inventoried under the same rule and measured
in the same units. Unknown original software costs are not zero.

For a topic with original manuscripts L_i, a whole common paper U and complete
applications A_i, the manuscript comparison is::

    R = sum c(L_i) / (c(U) + sum c(A_i))

Every page of the declared common theory and applications is charged. U is
charged once within the topic; each other topic pays its own common theory
in full. The application comparison, conditional on acquiring the whole
common theory and the declared required dependencies, is::

    r_i = c(L_i) / c(A_i)

An additional comparison that includes validation would be::

    R_validation = (sum c(L_i) + c(original validation))
                   / (c(U) + sum c(A_i) + c(our validation))

It is unavailable until the validation inventory and inclusion rule are
established on both sides. Printed and raw code are alternative representations;
their costs are never added together. Reusing one validation file within a
topic does not require charging it for each application.

Written length and complete proof evidence
-----------------------------------------

Optional validation is different from a program, finite certificate or data
file on which a proof depends. Required evidence keeps its mathematical role.
It cannot be omitted from a complete executable-proof comparison merely by
calling it validation. Program and data inventories remain available, without
an asymmetric ratio.

The existing written figures compare complete manuscript text at the stated
representations. Separate programs are excluded from both manuscript totals.
The nineteen historical topics have not all been screened for validation
listings inside the manuscripts, so this correction does not certify that
every written figure already excludes every embedded listing. A stricter
comparison must check that boundary on both sides. Definitions, group
presentations and written algorithmic arguments are mathematical text.

The figures also retain their original principal-result contracts, corrections
and borrowed inputs. They are neither a measure of the shortest possible proof
nor a comparison of all external dependencies. No pooled factor is formed
across different text representations.

Current published written comparisons
-------------------------------------

The `complete table <written_topics.csv>`_ preserves all nineteen topic rows
from the forty-two-original overview. The strongest published factors are:

.. list-table:: Complete manuscript lengths
   :header-rows: 1

   * - Topic
     - Originals
     - Original characters
     - Common + applications
     - Factor
   * - E: Projective groups
     - 3
     - 71,375
     - 19,790 + 19,513 = 39,303
     - 1.816
   * - A: Supported kernels and finite two-groups
     - 7
     - 213,803
     - 49,059 + 87,019 = 136,078
     - 1.571
   * - Mixes and simultaneous actions
     - 1
     - 57,753
     - 12,615 + 31,077 = 43,692
     - 1.322
   * - C: Chamber operations and binary translations
     - 5
     - 118,433
     - 30,437 + 61,248 = 91,685
     - 1.292

The unit here is NFC characters without whitespace, using each topic's
declared extraction and selection. No published topic currently exceeds
twofold overall written compression. E's written replacement uses about 45%
less text. Its conditional application factors are 6.957, 11.271 and 2.018;
these do not charge the acquired common material a second time.

The two-original expansion of F is not admitted by this correction. The
programme remains at 42 measured originals out of 106 accessible originals,
with 64 awaiting complete recovery.

Record of the correction
------------------------

`policy.json <policy.json>`_ binds the previous overview, the unchanged
written table and the `replacement program cost inventory
<replacement_program_costs.csv>`_. Software-inclusive factors remain unknown
in that inventory. Frozen historical reports retain their original bytes,
including the withdrawn fractions, for an inspectable record. This policy
supersedes those fractions as current claims.

This correction adds no recovered manuscript, conjecture solution or formal
proof. It changes the comparison rule and its presentation.

The inventory retains E's additional 5,173 printed validation characters as
a separate column. Its other printed program costs 7,565 characters and is
required evidence. Empty optional-cost cells do not assert absence of checks;
the historical inventories have different mixtures of required and optional
programs.

The `bounded audit <review/README.rst>`_ identifies the affected fractions and
checks the validation boundary of the pending two-original F comparison.
Its author also contributed earlier numerical packets; that role is disclosed.
This review does not reprove the mathematics or claim that all nineteen topics
have undergone a fresh source-listing audit.
