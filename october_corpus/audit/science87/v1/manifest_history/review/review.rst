Science87 publication-manifest correction: distinct operational review
=====================================================================

Decision
--------

ACCEPTED_SCIENCE87_PUBLICATION_MANIFEST_CORRECTION. This is a narrow
post-registration integrity repair. The previous registration review remains
frozen. Its author/reviewer roles, and this reviewer's diagnostic and locator
feedback, are disclosed in review.json. Root authored the implementation.

Failure and preservation proof
------------------------------

The original checker (64a8db65...) includes the publication manifest among
36,504 baseline tree rows but not among the nine archived HISTORY paths.
Consequently its unchanged bind(root,row) requires 7,886,143 bytes with
SHA394f890a... at the current path. Root's successful --write-manifest run
wrote 8,106,309 bytes with SHA17f6cf96.... The direct original bind throws
ValueError, exactly as recorded in finding01.json. Thus a second full run
would fail before reaching its final regeneration. The prior success is not
invalidated: it checked the old manifest, then generated the successor.

The final correction adds precisely three lines to the old-tree loop. It
recognizes only that one literal manifest path, substitutes its immutable
archive locator, and passes the unchanged baseline bytes/SHA to bind. It also
checks the literal locator is not a symlink and preserves executable-mode
status. Every other tree row follows exactly its prior code path. The nine
HISTORY paths, history adapter, verifier, and entire predecessor tree are
byte-identical. The original checker and seven original gate files remain
exact archived bytes, as independently compared with pre-correction snapshots.

Every gate has precisely the new checker pin plus the explicit three archive
bindings/provenance. The shared gate additionally refreshes the six changed
individual gate pins. All other fields, credits, source decisions and old
bindings are unchanged. The root's installer is retained as actual historical
execution; it produced the first correction, not the later locator precision.
Both correction records and the exact final one-line delta are retained.

Current versus historical integrity
-----------------------------------

The historical archive is not a replacement for current tracked-file
integrity. Unchanged publication_rows excludes only the live manifest itself
and hashes every other tracked artifact; unchanged main compares its complete
list with the live manifest. Literal extraction of these functions and that
main assertion in a small independent Git fixture confirms both changed live
manifest content and changed tracked artifact content are rejected. A fresh
regeneration can coexist with the exact historical archive check. No circular
self-hash is introduced. Root must regenerate the final current manifest after
adding the review and adoption; this review does not claim that later action.

Execution and controls
----------------------

The fresh corrected check_science87 run46575 terminated PASS: all 36,504
predecessor paths, all 203 old verifier functions and 19 damage controls;
87 recovered, 9 refuted, 9 pending, 53 measured, 34 unmeasured. This was the
3fd7c34e edition. The final 8a3cf3ce edition differs only by checking the
literal archive locator for a symlink rather than its resolved bind result.
The exact final loop passes an independent replay, rejects a same-byte
internal symlink, and passes all other archive/current-manifest controls.
The final seven gate deltas are checked independently. No unchanged expensive
registration or full snapshot was repeated after that single tested change.

Eleven independent controls cover valid archive routing, length and same-length
hash corruption, executable-mode corruption, same-byte and damaged symlinks,
current-manifest equality, current-manifest damage, tracked-file damage,
regeneration compatibility and the original failure. Independent scripts are
historical workspace helpers, not standalone packet drivers. The small
check.py verifies exact frozen exports and public/study bindings. Root's
1294.804-second full snapshot PASS is acquired explicitly, not represented as
a fresh reviewer run. No scientific computation, source disposition, question,
measurement or Lean result was added by this review.

Historical live-path provenance (v2 addition)
-------------------------------------------

A complete literal scan of the 37,463 currently tracked paths (Python code and
exact JSON path/file rows) is retained in historical_reference_audit.json.
Archived verifier editions retain their global MANIFEST and main-time equality;
these are not invoked by the historical check-function adapters. The six other
old review programs mentioning this path include it in their explicit allowed
later-regeneration sets, not a hash binding. The only pre-science87 JSON row is
Topic C's publication_manifest_at_invocation, a recorded historical invocation
whose obsolete bytes are not treated as the current manifest by any Python
field reference. That record itself remains hash-protected. The full frozen
history adapter and current verifier were read. This is a bounded static
interface audit, not an invented runtime trace. It supports the conclusion
that no older history check adds a second live-manifest equality; the current
main remains responsible for that equality after all historical checks.

V1 is preserved, including its acceptance and controls. V2 adds this explicit
provenance clarification only, with no change to the corrected checker, gates,
scientific results or actual replay claims. An inefficient preliminary AST
report-preparation loop was interrupted before writing its report; the final
classification uses the same source line positions and completed normally.
