Packed conjugacy-key representation core: Source boundary
=========================================================

AuthorC5; distinct reviewerRoot or another independently assigned agent.
All code/controls are UNCOMPILED and UNRUN. The full mathematical statement is
ARGUMENT.rst. This kit changes no accepted caller, workspace, Source proof,
checkpoint or current state. It is one new representation core, not a clone
of the old named per-orbit protocol.

Programs and ABI
----------------

program=packed_keys.c; programs exact{kernel:packed_keys.c,
header:packed_keys.h,controls:controls.c}. All exported signatures are literal
in the header. Codes are typed C integers/arrays; no JSON parser or Python
bool/int equality is involved. A future wire reader must explicitly enforce
exact JSON/binary types, canonical records, full whole-file bounds and stable
ordinary-file authentication before calling this API. Pointer lengths must
match the complete authenticated degree/catalogue and remain immutable for
the context lifetime. The C API cannot authenticate arbitrary pointer storage.

pck_create checks finite dimensions, all full permutation bijections, the
nonidentity a^2=1 relation and actual inverse tables. It does NOT establish
named membership, faithful base, complete class cardinality or full T order.
The future admitted input carries those exact acquired authorities. Zero-based
points are0..degree-1; factors are positive1..factor_count. First root is
parent0/factor0 only. Parent IDs are earlier committed nodes. Node depth is
the literal number of factors, at most8192. The format has no signed-factor
ambiguity; include actual inverse factors as separately authenticated entries
if a caller wants them. No action multiplication convention is implicit.

pck_close accepts one actual endpoint generator catalogue/order and supplies
one complete orbit with every edge, or no new committed nodes on failure.
An existing seed returns PCK_OLD. Callers must distinguish PCK_OLD from a
new closed orbit and all stop/error codes from both. The dictionary is for
ONE T partition. Do not run a different T against the same committed orbit
intervals and interpret its overlaps as an old-orbit certificate.

Saved uses pck_check_append once per supplied node and requires PCK_OK plus
the exact next expected ID. It uses pck_check_orbit on every interval and
requires PCK_OK. No proposing pck_close call belongs in Saved. Complete edge
checks and a traversal of the supplied finite edge graph are verification,
not a replayed search for an unknown orbit. All whole scalar/record/binary
comparisons and literal node-prefix equality are external mandatory duties.

Checkpoint/wrapper transport still owed
---------------------------------------

Use explicit little-endian field writes rather than sizeof(struct) bytes:
node(parent_u32,factor_u8,depth_u16,key[stride]), and orbit(first_u32,
weight_u16,generator_count_u8,edge_target_u32[weight*generator_count]). Node
IDs and orbit member IDs are consecutive and implicit. Bounds are targetN,
stride<=43, weight<=256, generators<=16. All byte counts must be exact. This
describes the next wire contract; no serializer/reader has secretly run here.
At the worst domain node records use142862000 bytes. Orbit records use at
most7N+4*16N=202863969 bytes. Both are finite disk payload, below384MiB
together. A reviewed wrapper may stream bounded chunks; it must not claim
that a prior16MiB output-profile already covers these new components.

Restore requires an exact accepted prefix and full Saved verification; then
ambient queue cursor+generator position continues the connected class graph.
Commit only a closed orbit; output/successor manifest atomically names the
old accepted prefix and new closed suffix. A guard interruption before the
manifest yields no successor. Whole input/final rehashes, aliases, runtime
loader identity, actual guard/CLI and known-scope closure remain Root duties.

The next small actual acquisition needed is the faithful strict base plus
actual maps from the accepted chain/action/endpoint boundary. It must reuse
the old model and endpoint words, not reconstruct or guess them. Production
needs a separate bounded CLI and separate whole-process Saved invocation.
Current512MiB/150s remains the proposed outer profile. The prior shared20s
phase CPU profile is not silently changed by a C callback; the new wrapper
must explicitly enforce any admitted phase budget and report its real scope.

Synthetic compile/control proposal, NOT executed
------------------------------------------------

After independent Source review, Root may authenticate a real C11 toolchain
and issue an explicit bounded compile producing a fresh binary, for example::

  ACTUAL_CC -std=c11 -O2 -Wall -Wextra -Werror \
    /absolute/packed_keys.c /absolute/controls.c -o /fresh/packed_key_controls

Compiler/runtime/link identities and resulting binary hash are runtime roles,
not future hashes embedded in this Source packet. The fresh binary then runs
only the eighteen small synthetic branches and must emit the exact marker
``COMPLETE_PACKED_KEYS_CONTROLS 18`` after all named PASS lines, with exit0 and
empty stderr. This is proposed; neither command nor any function was called
by the author. A compiler/controls failure remains honest failed history.

Proof outputs and finite Source scope
-------------------------------------

Expected D/distinct_source_review.json status
PASS_DISTINCT_L026_PACKED_CONJUGACY_KEYS_SOURCE; canonical
D/distinct_source_execution.json status
COMPLETED_GENUINE_DISTINCT_L026_PACKED_CONJUGACY_KEYS_SOURCE_REVIEW.
Both bind exact current program/programs/source_packet/inverse/argument/checks/
method, authorC5/reviewer distinct, blockers[], and mandatory
late_author_preparation. The canonical execution retains genuine command,
real five-tool return/full raw and literal required_root_admission_inputs
including the late receipt. No future proof pin is invented in the packet.

The packet's current Source rows are freshly hashed. Existing Source/Root
documents are explicit closed authorities, not recursively expanded historical
data/runtime/workspace scopes. The author assembly reads ONLY listed Source
and ordinary proof/resource metadata and writes new Source/assembly artifacts.
It never compiles/imports/invokes the C/GAP/kernel/controls, decodes scientific
payloads or calls guard/state/liveness APIs. Source qualification is not actual
resource fit, census, generation, reversal or Original credit.
