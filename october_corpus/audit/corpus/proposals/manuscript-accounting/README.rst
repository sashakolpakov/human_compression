Counting manuscripts and correcting catalogue entries
====================================================

This proposed catalogue revision preserves every one of the 161 registered
source IDs. It groups L063 and L064 as one manuscript: the publisher identifies
L064 as the supplementary appendix to L063, under the same article and DOI
10.26493/1855-3974.181.59e. The article itself describes that appendix as proof
material for its results.

The resulting registered counts are:

* 160 manuscript records historically, including 55 without usable full texts;
* 105 accessible manuscripts: 104 mathematical manuscripts and one editorial;
* 101 complete mathematical treatments: 93 recoveries and eight manuscripts
  treated through refutations;
* three pending manuscripts: F004, F009 and L026.

The unavailable L127 may have an earlier-draft relationship to L007. The retained
evidence does not settle that question. Thus 160 counts the corrected registered
manuscripts; it does not certify exhaustive bibliographic deduplication of the
unavailable works. No source component, result or attribution is removed.

``catalogue.json`` also corrects outdated completion fields for L036, L063 and
L064 and the pending target labels for L100, using their existing published
admissions. These edits confer no new proof, refutation or measurement credit.
``patch.json`` records all 51 changes. An independent check applied them to the
entire previous catalogue, compared the complete proposed value and reversed
them to recover every previous value. The identity map retains all 161 IDs in
160 groups; L063/L064 is its only merged pair.

``manuscript_identity.json`` records the evidence, grouping and qualifications.
The publisher's article is available at
https://amc-journal.eu/index.php/amc/article/view/181 .

The earlier catalogue and the current navigation pointers remain unchanged.
This directory publishes the proposed correction for review while computations
that bind the earlier immutable catalogue finish. Existing measurement factors
have not been recalculated here.

From this directory, run ``python3 -E -B check.py`` to verify the complete patch,
its inverse and the grouping of source IDs. This checks the catalogue revision;
it does not replay mathematical proofs or certify the unresolved identity.
