Ball packing across singleton-free sections
===========================================

Proposed further necessary restriction for F009. Let G be connected,
simple, four-regular and of girth at least five, with root eccentricity
22 and order at most 94. Reuse singleton_pattern_review.json and its
proof singleton_pattern_bound.rst (SHA256
96dce96a87e04f0b062a2cce34ff059f4824b5329d645600e7cb9e256af846ca).
Thus internal singleton indices lie in [4,19], are separated by at least
four, and number at most three. No old scalar solver or graph enumeration
is used below.

The added observation is that a long section between consecutive singleton
layers contains disjoint radius-three balls at both boundaries, each of
size at least fifteen. Original layers between the two balls are not
singletons. This improves the old constant bound of 22 interior vertices
for every gap of at least six to distance-dependent bounds. Applied to all
first/last caps and consecutive sections, it leaves 66 possible nonempty
singleton-index sets from the 214 permitted by positions and spacing alone.
This is a necessary position reduction, not 148 newly excluded enumerator
roots, not feasibility of the remaining sets, and not a global N94 exclusion.

Singleton-free interval mass
----------------------------

For r consecutive original layers, none a singleton, define

  P(r) = 17*floor(r/5) + 2*(r mod 5),   P(0)=0.

Their total size is at least P(r). Partition into floor(r/5) disjoint
five-layer intervals and the remaining layers. Each five-layer interval
has mass at least 17 by the acquired Moore interval bound recorded in
layer_profile_inequalities.tex; each remaining layer has at least two.
Only a fixed interval partition is used. No existence or sharpness of
these bounds is asserted.

The two-boundary section bound
------------------------------

Let singleton indices i<j be consecutive, and put h=j-i. The induced
section has two boundary vertices u,v of degree two and all other vertices
of degree four. Their distance in the section is h. Distances from u
are the original layer indices minus i: every original root-shortest path
to a section vertex passes through the unique vertex u. Its first four
layers have total mass at least 1+2+6+6=15, by the accepted parent-matching
argument. The same lower bound holds for the radius-three ball about v
when h>=7; all vertices encountered before u have full degree four.
The reverse ball need not equal a union of whole reversed original layers.

For h>=6, the first four original layers have mass at least 15 and the
radius-two v-ball has nine vertices. The latter lies in original layers
j-2,...,j, and these two sets are disjoint. The intervening whole original
layers number h-6 and have mass at least P(h-6). Hence the number of
vertices strictly between u and v is at least

  22 + P(h-6).                                                   (1)

For h>=7, both radius-three boundary balls have at least 15 vertices and
are disjoint. The u-ball is in layers i,...,i+3 and the v-ball lies in
layers j-3,...,j. The intervening whole original layers number h-7.
This gives the further interior bound

  28 + P(h-7).                                                   (2)

Containment follows from the original distance difference: a vertex at
distance at most k from v has original index at least j-k. Thus the
counting uses disjoint vertex sets and retains all whole middle layers;
it does not assume reverse BFS symmetry. Consecutiveness makes every
middle layer singleton-free.

Use the following valid combined lower bound F for the interior:

  F(4)=17, F(5)=18,
  F(6)=22,
  F(h)=max(22+P(h-6), 28+P(h-7)) for h>=7.                      (3)

The first two values are the accepted gap-four and gap-five theorems.
For h=4,...,11 the values are

  h:     4   5   6   7   8   9  10  11
  F(h): 17  18  22  28  30  32  34  39.

In particular the new gap-seven bound is 28 interior vertices, rather
than the old gap-at-least-six constant 22.

First and last caps
-------------------

Let h be the index of the first internal singleton, or 22 minus the
index of the last internal singleton. The corresponding end cap has
boundary degree two and all other degrees four. A vertex at its other
end is an original root or a distance-22 vertex. Its radius-two ball
has 17 vertices and is contained in the three original end layers.

For h>=5 this regular radius-two ball is disjoint from the nine-vertex
radius-two boundary ball. Their original layer supports leave h-5 whole
middle layers, none singletons. For h>=6 it is disjoint from the
at-least-15-vertex radius-three boundary ball, leaving h-6 such middle
layers. Consequently the cap order is at least the maximum of

  19;  20 if h>=4;  26+P(h-5) if h>=5;  32+P(h-6) if h>=6.       (4)

Call this maximum E(h), for h>=3. The first two entries are the accepted
cap theorem and its distance-four consequence. The other two are the new
singleton-free middle contributions. In the first cap the boundary-ball
supports are at the high-index end; in the last cap they are at the
low-index end. In either case the intervening original layers are disjoint
from both balls. No reverse-layer identification is used.

For h=3,...,11 the values are

  h:     3   4   5   6   7   8   9  10  11
  E(h): 19  20  26  32  34  36  38  43  49.

Exact position reduction
-------------------------

For exactly k>=1 internal singleton indices s_1<...<s_k, the disjoint
cap/interior partition gives

  |G| >= E(s_1) + E(22-s_k)
           + sum(F(s_(r+1)-s_r), r=1,...,k-1) + k-2.             (5)

The two end caps include their respective boundary singletons. For k=1
that is the same vertex, requiring subtraction of one; for k>=2 the
k-2 other singletons are added explicitly. There is no overlap of the
strict section interiors or the caps. These are bounds for consecutive
singletons and must not be applied while silently omitting intervening ones.

Substitution in (5), over the index range [4,19] and gaps at least four,
gives the following complete necessary lists. Only values at most 94 are
listed. The original finite sets had respectively 16,78,120 choices;
13,36,17 remain. These numbers count index sets, not graphs or admitted
search roots.

Exactly one singleton may occur only at

  4,5,7,8,9,10,12,13,14,15,17,18,19.

For exactly two, the allowed second indices for each first index are

   4: 8,9,10,12,13,14,15,17,18,19
   5: 13,14,15,18,19
   7: 13,17,18
   8: 13,14,17,18,19
   9: 13,14,15,17,18,19
  10: 18,19
  12: 18
  13: 18,19
  14: 18,19.

For exactly three, the complete list with the lower bound in (5) is

  (4,8,13):94     (4,8,18):92     (4,9,13):94
  (4,9,14):93     (4,9,18):91     (4,9,19):92
  (4,10,18):93    (4,10,19):94    (4,12,18):93
  (4,13,18):91    (4,13,19):94    (4,14,18):92
  (4,14,19):92    (8,13,18):93    (9,13,18):94
  (9,14,18):94    (9,14,19):94.

All table entries were checked by direct substitution of (3)--(5) into
214 integer sums. No degree variables, graph states, parent matrices or
solver models were generated. The omitted choices have a proved lower
bound greater than 94. A reviewer can reproduce the finite arithmetic by
the following literal loops, using the E,F just defined:

  one = [(a,E(a)+E(22-a)-1) for a in range(4,20)]
  two = [((a,b),E(a)+F(b-a)+E(22-b))
         for a in range(4,16) for b in range(a+4,20)]
  three = [((a,b,c),E(a)+F(b-a)+F(c-b)+E(22-c)+1)
           for a in range(4,12) for b in range(a+4,16)
           for c in range(b+4,20)]

Remaining obstruction and limits
--------------------------------

The no-internal-singleton case remains a separate stratum. Its first and
last three layers each have at least 17 vertices; its 17 intervening layers
are singleton-free. The present interval packing gives only

  |G| >= 17+P(17)+17 = 89.

Likewise (4,9,18) receives only the lower bound 91 from (5). These gaps
are limitations of this deduction, not constructed graphs or feasible
assignments to every retained scalar inequality. They pinpoint the needed
additional input: stronger local compatibility for sections with only
layers of sizes at least two, or stronger end/section bounds at one of
the explicit surviving position patterns. Nothing here proves that such
graphs exist or that the old simultaneous pair inequalities permit them.

The mathematical improvement is the two radius-three boundary packing
and its exact whole-layer budget application. The ball sizes and Moore
interval bounds are reused, with no historical novelty claim. This is not
an integration into the frozen enumeration. The accepted prefix, program
files, CURRENT, source status and existing proofs are unchanged. No solver,
frontier replay, graph construction, compilation or material output was run.
