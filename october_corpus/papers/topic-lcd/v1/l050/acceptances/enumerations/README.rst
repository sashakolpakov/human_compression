Bounded review of the ternary enumeration method
===============================================

This review accepts the mathematical logic of the five pinned author programs
and supplies a small independent certificate for the 105-coordinate subcode.
It does not accept a complete recovery of either source manuscript. The live
seven-code queue was neither restarted nor changed.

The packed addition formulas implement addition in F3. A base-three counter,
including its carries, therefore enumerates every coefficient vector exactly
once. The basis must first be certified: without independence the program
counts coefficient vectors with multiplicity. The separate exact MacWilliams
transform then gives the dual weight enumerator. The independent small tests
check the actual author C executable and actual dual function, using direct
coordinate enumeration for the expected answers. No author Python computes
an expected answer; oracle.py imports the dual function only as the subject
under test.

The witness
-----------

Let A be the 105 by105 adjacency matrix constructed from projective flags as
specified in check_witness.py. Let D be the span over F3 of the differences
between each row and the first row. The checker reconstructs the field with
an explicit multiplication table, checks all strongly regular parameters,
and obtains exactly the pinned rank19 RREF basis. The19 coefficient vectors
in weight36_witness.json yield19 words of weight36 and rank19. Each uses at
most four of the certified basis vectors. The complete adjacency code has
rank20; both completed enumerators count3360 words of weight36. Since D is
contained in the adjacency code, their weight36 sets coincide. The19 words
therefore prove D is precisely the source's span of all weight36 words.

The computed graph is identified with the source graph through the retained
uniqueness of SRG(105,32,4,12), as cited by the source. We do not identify the
implemented rule with the source's problematic literal flag-adjacency prose.
The complete two weight tables agree coefficient by coefficient. Their dual
minimum weights/multiplicities are6/15680 and5/84, respectively.

Replay
------

Use a fresh output directory for each command::

  python3 -B -O check_witness.py --out /fresh/witness
  python3 -B -O oracle.py --author-root /path/to/topic_LCD_L050_F017_recovery --out /fresh/oracles

The first command uses only the small frozen certificate and finished output
files. The second compiles a fresh private executable and runs only the small
coordinate tests. Neither starts a complete code enumeration.

Limits
------

The120-coordinate N/K socle claims, full automorphism/module assertions and
the other complete enumerations remain separate obligations. Named-graph
uniqueness and classical MacWilliams duality remain retained mathematical
inputs. There is no new source credit, whole-source proof or Lean claim.
