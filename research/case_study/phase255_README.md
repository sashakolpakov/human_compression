# Independent review of the locally faithful cover criterion

`phase255_locally_faithful_review.md` gives the accepted mathematical scope.
The review covers the complete frozen phase246 argument, including its
topological interpretation, finite classification and source attribution.
The older phase245 integer review alone did not cover those matters.

The review adds two independent computations:

1. Native GAP right cosets and a complete square orbit reconstruct the
   Tomotope complex without importing phase246 geometry code. A differently
   numbered matrix gives the same integral homology and surviving defect.
2. The actual voltage cover acts by conjugation on the three nonidentity
   kernel elements. This verifies its unique invariant kernel line and the
   surviving discrepancy without using the author's normal-subgroup census.

The complete author replay freshly passed, including the three scoped Lean
declarations. Its report is retained as `phase255_author_report.json`.
No primary publication text or page image is exported by this packet.

To reproduce the independent complex and integer calculation, use fresh
absolute output paths:

```sh
python3 -B -O phase255_native_complex.py --gap /path/to/gap \
  --out /tmp/NEW-native-complex
python3 -B -O phase245_tomotope_integral.py \
  --input /tmp/NEW-native-complex/complex.json \
  --out /tmp/NEW-native-integral.json
```

After running the author `phase246_check.py` with its explicit GAP, Lean and
package paths, use the actual generated voltage permutations:

```sh
python3 -B -O phase255_run_kernel.py --gap /path/to/gap \
  --voltage /tmp/NEW-author-replay/Tomotope_voltage.json \
  --out /tmp/NEW-kernel-check
```

The supplied wrapper records the same independent GAP check that was run
directly during review. Generated matrices, large literal permutation files
and private page rasters are recorded by hashes, not required as public
source artifacts. The small reconstruction programs regenerate the matrices;
the author replay regenerates the literal voltage action.

The accepted result is a general criterion under locally faithful end-group
hypotheses and an exact restricted Tomotope classification. It does not settle
the general finite minimal-cover question or add a principal-source count.
