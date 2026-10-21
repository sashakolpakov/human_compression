#!/usr/bin/env python3
"""Rework the reviewed common proof without repeating its mathematical work."""
import argparse, hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
BASE='7f33595f3013cb04392c80835fb4b6f45f9af7d2d06834db87cf72751023eb66'
def digest(s): return hashlib.sha256(s.encode()).hexdigest()
def build():
 source=(ROOT/'phase230_rank_one_classification.md').read_text()
 if digest(source)!=BASE: raise RuntimeError('changed frozen common source')
 definition=source[source.index('Let $q$ be a prime power.'):source.index('We prove the following classification')]
 start=source.index('## 2. Retained inputs and elementary string consequences')
 end=source.index('## 6. Proof of the two classifications')
 block=source[start:end]
 old='This is the standard correspondence used in both sources and in the existing proof library.'
 new=old+' A group epimorphism preserving the ordered distinguished generators between two string C-groups induces a covering of their regular polytopes. We retain this covering part of the correspondence as well.'
 if block.count(old)!=1: raise RuntimeError('ambiguous Input P amendment')
 block=block.replace(old,new)
 prefix=r'''# Centralizers, facets and finite amalgams on the projective line

## Abstract

We give a common reduction for string C-groups of projective linear degree
two. A nonabelian dihedral subgroup defined over an odd-characteristic
subfield acquires no new centralizing projectivity under field extension.
Combined with an odd-order normalizer argument, this excludes subfield
facets without counting their mutual intersections. The remaining local
markings form six classes; their fourteen compatible ordered pairs give
ten universal presentations up to reversal. We retain Dickson's subgroup
types and the group–polytope correspondence. The finite part is supplied
by one exact computation. Separate applications derive the complete
projective special and general linear principal classifications.

## 1. The common theorem

'''+definition+r'''**Theorem 1 (uniform reduction).** Suppose that a string C-group is
isomorphic to $L(q)$ or $P(q)$ and has rank at least four. Then $q$ is odd,
the rank is four, and both end parabolics are proper and isomorphic to
$S_4$ or $A_5$. Their ordered markings are among the six classes of
Lemma 10. Up to reversal, the full marked group is a quotient of one of
the ten literal presentations of Lemma 11.

The assertion is a reduction, not yet a classification of all quotients
of those presentations. That last step belongs to the two application
papers. The common theorem includes small fields and arbitrary subfield
extension degrees. Its proof is completed in §6 after the general
centralizer argument and the finite table have been established.

The six local classes and the ten-row table are earlier results from
L083. The common proof below reworks their use in the two classifications.
The centralizer calculation and the normalizer assembly replace the
source's subfield-incidence counts. No claim of historical priority for
this proof method is needed for the applications.

'''
 suffix=r'''## 6. Proof of the reduction and verification

**Proof of Theorem 1.** Section 2 excludes consecutive labels two, including
in the small groups. Proposition 7 then gives rank four in odd
characteristic. Theorem 9 identifies both proper end parabolics as $S_4$
or $A_5$. Lemma 10 exhausts their ordered markings and supplies an exact
presentation for each local group. The consecutive pairs share their
middle product order. Substituting their two presentations into the
four-generator string relations gives the marked epimorphism from (7).
All compatible pairs, with their reversals, occur in Lemma 11. This proves
every assertion. $\square$

The common mathematical proof consists of this paper and the single
program `phase230_finite_check.g`. The finite-presentation computations
use GAP's exact algorithms to obtain the order of each *presented group*,
and then an isomorphism with a permutation group. Checking a chosen
permutation image alone would give only a lower bound and would not
justify the table. Here the exact computation also verifies all marked
subgroup intersections, group identifications, self-dualities and the
listed coset incidences. The same program is used by both applications;
it is not rerun as an additional mathematical hypothesis for either.

The inherited formal file `phase230_formal/DihedralFacetObstruction.lean`
proves five abstract steps: an involution with an odd vanishing power is
trivial; the corresponding homomorphism assertion; membership in a normal
facet; derivation of this conclusion from the normalizer condition and
generation; and contradiction with an independent generator. These are
parts of Lemma 2 and its use. They do not formalize the matrix centralizers,
Dickson's theorem, the finite presentations, or Theorem 1 as a whole.
The finite program and those remaining written proofs retain their stated
verification status.

A portable replay verifies the six local classes and all ten universals.
Changing a Petrie relator is rejected by the universal-order check;
duplicating a distinguished generator is rejected by the full intersection
test. The formal replay reports only the usual Lean axioms. The accompanying
contract gives the exact files, versions and retained source editions.

## 7. Attribution and the application interface

Dickson's subgroup classification, the ordinary projective group structure
facts and the string C-group/regular-polytope correspondence are retained
inputs, not new results. The six exceptional rank-three maps and the
amalgam table are recovered from L083 with an explicit replay. The
classifications derived in the application papers belong to Leemans and
Schulte; the 11-cell and 57-cell themselves are the earlier constructions
of Grünbaum and Coxeter.

Relative to the existing proof bank, the work here is the explicit
projective-line centralizer descent and its common assembly with the
odd-order normalizer argument. An analogous centralizer strategy already
appears in the retained Suzuki discussion; it is not a substitute for
the matrix proof in §3. The present paper preserves the complete common
proof from the independently reviewed combined manuscript, while the
two applications carry their separate quotient and geometric obligations.

The applications use Theorem 1 and the exact marking data of Lemma 11.
Neither application is a premise of the other. Together they recover two
principal classification contracts; they do not reprove every secondary
statement in the historical sources. In particular the almost-simple
seventeen-case census and the separate conjecture in L079 are not
consequences asserted here. The topic's cost includes this entire common
paper and its required finite program once, followed by each complete
application. A common lemma used in another topic is charged again as
part of that other topic's full chosen umbrella.

## References

[L083] D. Leemans and E. Schulte, *Groups of type $L_2(q)$ acting on
polytopes*, retained arXiv:math/0606660v1 author edition, 14 physical pages;
*Advances in Geometry* 7 (2007), 529–539. Theorem 2 prints the retained
subgroup classification; §5 prints the exceptional amalgam table.

[L079] D. Leemans and E. Schulte, *Polytopes with groups of type
$PGL_2(q)$*, retained arXiv:0909.1991v1, 9 physical pages. Propositions 1–2
print the projective subgroup inputs; Theorem 10 is the principal
projective general linear classification.

[MS] P. McMullen and E. Schulte, *Abstract Regular Polytopes*, Cambridge
University Press, 2002. The marked-group correspondence, face cosets,
duality and marked epimorphism/covering theorem are retained.
'''
 output=prefix+block+suffix
 provenance={'source':'phase230_rank_one_classification.md','source_sha256':BASE,
 'copied_definition':{'sha256':digest(definition),'characters':len(definition)},
 'copied_common_block':{'source_character_start':start,'source_character_end':end,
 'source_sha256':digest(source[start:end]),'sections':'2–5, complete',
 'single_addition_to_Input_P':{'before':old,'after':new}},
 'output':'phase238_topic_E_umbrella.md','output_sha256':digest(output),
 'new_material':'Common reduction theorem/assembly; separate application interface; retained covering input made explicit.',
 'frozen_source_mutated':False}
 return output,provenance
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
 output,p=build()
 for name,data in [('phase238_topic_E_umbrella.md',output),('phase238_provenance.json',json.dumps(p,indent=2,ensure_ascii=False)+'\n')]:
  path=ROOT/name
  if a.check:
   if not path.exists() or path.read_text()!=data: raise RuntimeError('nonreproducible '+name)
  else:path.write_text(data)
 print('PHASE238_COMMON_BUILD_PASS')
