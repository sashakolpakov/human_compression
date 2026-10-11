Explicit TeX input and paper-selection review
===========================================

Accepted for the current canonical catalogue and forthcoming modular Topic A
edition. The reviewed builder is SHA256
477c1730fb93cc6efe53651efce93150eb0ccb286fede017606f39847772a826;
the reviewed verifier is
844064198480029f18c30f29b3bdd57c60cb8f8e2447958bb17eecfdc6f1fb0d.
This is an infrastructure review, not a mathematical admission or cost result.
No public file or frozen author packet was modified by this reviewer.

The minimal schema is an optional ``tex_inputs`` list of repository-relative
TeX filenames. Its omission means an empty list. Every input must be a regular
file within the main source's parent directory or its descendants. The builder
rejects traversal, aliases, symlink files/directories, malformed lists, duplicate
or self inputs and a collision with the staged main name ``paper.tex``. It reads
all selected source bundles before starting workers, copies only their declared
bytes while preserving relative paths, reports input sizes and SHA256 hashes,
and checks every original source against those captured bytes after compiling.
No directory copy, glob expansion or Markdown reconstruction is introduced.

A modular umbrella declares its shared preamble and all section files. A5 and
A6 each declare only the shared preamble: the common theorems are mathematical
prerequisites, not files read during their separate typesetting. The full code
appendix embeds its four programs verbatim and has no TeX input dependency on
the program files. Their mathematical/program bindings remain in the separate
application and admission records. ``tex_inputs`` is therefore a build-input
boundary, not a replacement for theorem dependencies or cost accounting.

The snapshot verifier uses the same source-bundle validator. Preserved
text-identical migrations must have an empty input list. Every input of a new
edition must also occur in that edition's PASS admission artifact table, whose
bytes and hashes are checked. The current catalogue check passed for ten
preserved papers and eight new editions. No old migration hash or review record
is rewritten to introduce a modular dependency.

``--paper`` is repeatable and accepts exact catalogue IDs, including the audit
protocol. Unknown IDs fail before the output directory is created. Catalogue
IDs are validated globally before filtering; duplicates are rejected. Repeating
a requested ID builds it once, and output follows catalogue order. Omitting the
option preserves the existing full-build behavior. The final success count now
reports selected documents rather than assuming the protocol is always present.

The final candidate passed 30 tests. Four genuine isolated compilations used
the full 17-page umbrella, six-page A5, eleven-page A6 and an existing one-page
standalone PGL application. Every fresh PDF has the same page count and exactly
the same extracted text on every page as its bound original. Input hashes match
the staged declarations. Omitting one actual umbrella section fails even while
that section remains available in the unstaged repository. Absolute repository
input is also rejected by the new recorder check. Other controls cover C0
characters, traversal, symlinks, duplicate and self inputs, missing files,
filename collision, selection errors and backwards compatibility.

Two trust limits remain explicit. Installed TeX packages and fonts are external
build dependencies. The recorder check detects original-checkout reads outside
the staged target; it is not a general TeX sandbox and does not classify every
arbitrary file outside the repository. Output directories must be chosen fresh
and outside canonical source folders, as documented; the current implementation
checks freshness but does not enforce the latter location restriction. The
catalogue currently has no paper ID which is an ancestor of another paper ID;
such a future namespace overlap should be rejected or assigned disjoint build
roots before being supported.

Evidence is in tex_inputs_candidate_final_test.json, with the exact private
test program alongside it. The earlier miniature design experiment is separate
and demonstrates why copying alone would not justify a stronger input-isolation
claim. The original build_A5_A6.py remains an author conversion tool only; its
old Markdown input is neither invoked nor required by the public builder.
