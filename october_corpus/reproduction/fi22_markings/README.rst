Twenty-four Fi22 marking certificates
======================================

This additive package replays the 24 accepted cases with original free
indices 160 through 183. Eighteen have supplied 11- and 13-cycle witnesses
for generation; six have nonempty proper invariant point sets proving
nongeneration. The six excluded indices are 162, 166, 169, 171, 177 and 179.
All earlier public 47 generation and 90 nongeneration certificates remain
in their existing archives.

From the repository root, for example::

    python3 -E -B -S october_corpus/reproduction/fi22_markings/verify.py --controls
    python3 -E -B -S october_corpus/reproduction/fi22_markings/verify.py --index 160
    python3 -E -B -S october_corpus/reproduction/fi22_markings/verify.py --index 166

Run one index per invocation, without -O. Python 3.9 or later on Linux or
macOS and its standard library suffice. The program writes its result to
stdout. It reads the existing immutable proof objects for the encoded
original point frame, the original witness bank and the maximal-order
table. It opens no private file, group library, prior API response or
permission gate. It performs no search or discovery. The verifier passed independent review, all 25 controls and all 24
separate bounded case replays. REPLAY.json records their actual results.

The finite checks
-----------------

The original action has degree 3510. The shared operand body contains five
permutation vectors and the signed ambient spanning tree. The program
checks their framing, permutation properties, endpoint involutions,
distant commutation, signed inverses and tree edge equations. The exact
original 16-byte witness row supplies the three points defining the
virtual middle; its owner and full digest must agree with the certificate.
The actual point-to-involution interpretation is an imported premise.

For generation, every supplied word acts in the two rotations ab and bc,
with the original right-action convention. All edges, including each last
return, of the supplied 11- and 13-cycles are checked directly. No whole
middle permutation or group order is computed. The complete imported
simple-Fi22 maximal-subgroup list contains no proper maximal whose order
has both primes, so the actual rotation group is Fi22.

For exclusion, the program checks every ab and bc image of every listed
point. A nonempty proper invariant set makes the rotation group proper
in the transitive action of Fi22. The ambient tree establishes A
transitivity. The retained normal index-two G in A and the imported
minimum proper G-index 3510 then imply G transitivity. The usual even-word
subgroup has index at most two in <a,b,c>; simplicity therefore turns
properness of the rotations into nongeneration of the original marking.

Generation and the intersection property
----------------------------------------

The point-word kernel supplies generation credit only. The separate
intersection_theorem.tex proves the full rank-three intersection property
for generating triples of nonidentity involutions in a finite nonabelian
simple group when the distinct endpoints commute. The original middle's
membership and involution/class predicates remain explicit imports.
This theorem and its prior review are reused for the same eighteen
markings; the strict kernel is not relabelled as an intersection checker.

The original manuscript is Dimitri Leemans and Jessica Mulpas, The string
C-group representations of the Suzuki, Rudvalis and O'Nan sporadic groups,
The Art of Discrete and Applied Mathematics 5 (2022), #P3.09,
https://doi.org/10.26493/2590-9770.1405.4ce. Its rank-three method also covers
Fi22. The borrowed group classification, original faithful model and
member/Reader/word bridge are described in IMPORTS.rst. The complete
written generation and intersection arguments are retained with their
attribution. Historical preparation wording in generation_theorem.rst
belongs to that earlier edition; the present certificate counts are given
here and in the accepted-delta provenance.

Scope and limits
----------------

The accepted local bank now has 65 generation cases, 65 separately
justified intersection properties for those same cases, 96 nongeneration
cases and 28,747 unpaid rows. These counts concern one candidate bank
inside one endpoint/middle-class selector. The full domain has 105
selectors: 41 have zero contribution proved and 64 remain globally
unclosed. This package closes neither the full bank nor the manuscript,
and adds no conjecture, Lean or compression measurement credit.

Each invocation keeps the existing 128 MiB, 140-second process envelope,
10,000,000 shared work units and 20-second shared-work window, 8 MiB
physical input limit, 32 paths and 50,000-byte Source limit. Each input is
below 2 MiB, and stdout is bounded by 128 KiB. Every opened input is
rehashed at the end. The actual outer runs used the existing 128 MiB,
150-second supervisor. The 24 case processes took 2.601 seconds in total;
the largest sampled process tree was 28,508,160 bytes. Every case read
1,172,638 bytes over seven paths. These are measurements of this replay;
no earlier execution verdict was transferred.
