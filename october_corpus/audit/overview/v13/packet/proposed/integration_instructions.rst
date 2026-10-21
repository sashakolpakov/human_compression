Private v13 integration proposal
================================

Copy the frozen candidate exports to audit/overview/v13/packet. The embedded
accepted numerical packets stay byte-identical, with their own manifests.
No source primary assets or full corpus catalogues are copied by this packet.
The exact public catalogues are external bindings in programme_binding.json.

Copy proposed/check_projective_covers_overview.py to scripts/. Append the single
function in proposed/verifier_additions.py before main in verify_snapshot.py.
After the existing check_previous_programme46() and check_programme46() calls,
add in main::

    current_fractions, current_bars = check_projective_covers_overview()

All 108 existing non-main function ASTs must remain exact. Root already supplies
the exact four-file historical overlay, so no additional historical wrapper is
proposed. This packet binds that integration baseline separately from the old
104-function public baseline. No broad path exclusions are introduced.

Root creates audit/overview/v13/admission.json after distinct overview review.
The proposed guard expects status ROOT_ADMITTED_EXPANDED_PROJECTIVE_MIXES_OVERVIEW
and artifacts binding the complete packet, evidence, programme and review. Its
software_inclusive_factors and pooled_factor fields remain null. Only the root
admission hash/length remains unresolved in proposed/latest.template.json.
The reader, corpus snapshot and measurement-policy bindings are already exact.

Replace the current root README only after review, using proposed/README.rst and
its exact diff as the candidate. Copy proposed/overview_README.rst to
audit/overview/v13/README.rst. Older admissions and manuscript bytes remain intact.
The proposed reader is neutral about publication lifecycle; admission status is
kept in metadata. Unified A and F007 remain outside this consolidation.
