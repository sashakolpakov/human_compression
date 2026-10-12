F011: Diophantine tuples over finite fields
===========================================

This private author edition proposes a complete corrected principal recovery
of Kim–Yip–Yoo, Ramanujan Journal 65 (2024), 163–172. Distinct scientific
review and root adoption remain separate. It supplies no source registration,
compression factor, historical priority, new conjecture answer or Lean claim.

The four-page ``square_patterns.pdf`` contains the full character-filter,
cyclotomic degree, exclusion and parameter arguments. The four-page
``diophantine_tuples.pdf`` proves the exact main +1 and stronger +2 bounds,
the remaining residue-class construction, the maximal-tuple bound, and the
elementary square-field lower bound. The classical multiplicative Weil
estimate is retained explicitly through the exact source Lemma 2.1; its
full proof and the other classical background are not claimed to be proved
or measured here. Cohen's summatory-totient theorem is not a premise of
the repaired argument.

The decisive +2 repair uses centered half-integer powers for even tuple
sizes. With target n, write each entry as z^(2i−(n−1)), z²=y. Products need
only powers y^j+1 with |j| at most n−2, while the filter separately excludes
every order below n. The corrected rounding is T≤B+2+1/p. Small cases have
an exact three-tuple proof. See common Proposition 6/Lemma 7 and application
Proposition 4/Theorem 5. These uniform proofs do not depend on diagnostics.

Source Proposition 3.1 has a false endpoint cardinality, with an explicit
F17 counterexample; a strict-order statement repairs it. The introductory
least-nonresidue example includes a forbidden zero. The printed character
estimate, zero exclusion and rounding used for Theorem 3.5 have errors,
but its final +2 bound is proved here without weakening it. The source
conjecture remains recorded and unanswered. Theorem 3.5 is read with its
Section 3.2 hypothesis q≡7 mod 8, not as an assertion in the other section.

``source_contract.json`` covers all 22 source dispositions, including the
borrowed upper bound and historical material. ``proof_map.json`` binds all
13 current theorem/proof environments plus full native page texts and
identifies the retained inputs. The source's full ten pages have been read
and directly viewed; all eight final own pages have also been viewed. No
primary PDF, source text, glyph, font or raster asset is exported.

``diagnostics.py`` is optional validation only: 196 degree cases, 32
prime-field filter cases, 586 centered constructions, 294 stronger-bound
parameter checks, small exact counts and source-error examples. No
mathematical program is required by a proof. ``check.py`` is the complete
operational binding/render driver. Historical source software is unknown;
no executable listing occurs in the source, and no software-inclusive
factor is supplied. ``program_roles.json`` states the complete boundary.

Current mathematical authorship is enumeration_volume's reworking and
repair of the attributed Kim–Yip–Yoo mechanism. Earlier local
``character_sum_audit.md`` only audited the retained Weil interface for a
different application; it is bound as provenance and is not exported or
used as a substitute for any current proof.

Portable replay, requiring Python with pypdf and the native pdflatex engine::

  /Users/sasha/.venvs/global/bin/python -B -O check.py --out FRESH --render

Add ``--study-root /Users/sasha/medusa/research/leemans`` to check the exact
local source/provenance pins. The replay uses every manifest export, all
proof/page bindings, the optional diagnostics and 15 bounded negative
controls; it does not purport to replace independent mathematical review.

Source IDs and public corpus counts remain unchanged pending review.
