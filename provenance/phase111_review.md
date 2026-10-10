# Complexity figure

The [complexity page](../COMPLEXITY.md) plots previously admitted data from
the corrected phase138 inventory and phase144 full-package measurement.
The plotting script verifies their exact hashes, extracts the three
corrected checkpoints and independently recomputes the byte deltas and
all five NFC ratios from their recorded numerator and denominator lengths.
It does not rerun source extraction or mathematical proofs.

Root inspected the complete raster preview of the final SVG, including
axes, metric labels, coverage annotations and denominator scope. The
figure's byte axis begins at zero. The horizontal checkpoints are logical
package states, not equally spaced dates. The increase from five to six
source contracts is distinguished from the later fixed-six-source decrease.
The ratio panel includes all five NFC metrics and a reference at one.

The SVG and machine-readable points are in
`research/case_study/phase190_complexity/`; only project-authored material
is distributed. The plotting script requires matplotlib and a fresh output
directory. This publication adds a visualization, not a new measured ratio,
source contract, Lean theorem or established repeating sawtooth.
