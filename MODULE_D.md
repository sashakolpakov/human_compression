# Module D: Marked actions, field orbits and geometry enumeration

The separately reviewed [Recognizable extensions and finite incidence representations](FINITE_INCIDENCE_REPRESENTATIONS.md)
application develops the related restriction-and-extension argument for
F010. Its complete principal-theorem contract, three local corrections
and additional costs are separate from this frozen three-source edition.

Read the complete [18-page manuscript](research/case_study/phase164_enumeration.pdf)
or its [Markdown source](research/case_study/phase164_enumeration_manuscript.md).
The [independent review](research/case_study/phase173_D_independent_review.md)
and [root admission](research/case_study/phase181_D_root_admission.md)
accept the three principal source contracts below, with a qualified
fourth-source component kept separate.

    U + Marked actions, field orbits and geometry enumeration
      + complete required mathematical programs and drivers
        -> principal contracts of L066, L074 and L104.

| Source | Results derived |
|---|---|
| Kiefer–Leemans, *On pairs of commuting involutions in Sym(n) and Alt(n)* (2013), L066 | All-degree symmetric and alternating counting formulas, the exceptional degree-six endpoint classes, and the complete stated S6/A6 regular-polyhedron classification |
| Kiefer–Leemans, *On the number of abstract regular polytopes whose automorphism group is a Suzuki simple group Sz(q)* (2010; declared 2011 author edition), L074 | Both counting formulas for every odd exponent, generation, intersection property, rank restriction and absence of self-duality |
| Leemans, *The residually weakly primitive geometries of J2* (2002), L104 | The fixed principal census: 8, 19 and 3 geometries in ranks two, three and four, and none in higher ranks, with full group-automorphism/type fusion |

The common argument fixes a partial marking and classifies its extensions
under the actual stabilizer. Orbit multiplicities and parity handle
commuting involutions. Two field coordinates turn Suzuki generation into
an exact field-of-definition condition. Panel recognition and exhaustive
maximal augmentation handle geometries with nontrivial chamber stabilizers.
The local generation, intersection and completeness proofs are included.

The [41-row source ledger](research/case_study/phase164_enumeration_ledger.json)
distinguishes original results, classical inputs and repository arguments.
Suzuki structure, the standard polytope correspondence, complete named-group
catalogues and exact GAP algorithms remain attributed inputs. The source
geometry lists are not inputs to either finite census. L104's further
printed diagrams, full geometric automorphism/correlation groups and
doubling relation are not all recovered; these omissions occur in the
main body as well as the supplement. Principal-contract coverage does
not mean whole-paper coverage.

The qualified fourth comparison is Leemans–Rowley, *Rank three residually
connected geometries for M22, revisited* (2010), L073. The module derives
its 81 rank-two and 431 rank-three classes, with explicit witnesses and
geometric shadows. The complete refined correspondence with its printed
table remains open. The recorded 419/431 coarse matching is only a
diagnostic. The [dated admission note](research/case_study/phase181_D_root_admission.md)
records subsequent recovery of the older notation source; frozen earlier
access statements are preserved as historical records.

The required package costs **178,689 UTF-8 bytes**: U 61,576, D 60,471,
eleven mathematical programs 40,997 and three drivers 15,645. Its marginal
cost with U already present is 117,113 bytes. The 18-page rendering
excludes U and the programs. No matched compression ratio, full Lean
certificate or newly solved conjecture is claimed for this assembly.

Independent review read the full manuscript and all four primary text
bodies and inspected all 18 rendered pages. Fresh finite replays checked
every J2 Borel anchor, all final witnesses, the complete M22 census and
shadows, and the degree-six/Suzuki diagnostics. Actual J2 subgroup equality
was checked where generating strings differed between runs. Publication
adds fresh public binding checks and a replay of the small diagnostics;
the unchanged larger runs retain their independent execution records.

```sh
python3 -B -O research/case_study/phase173_D_review_check.py --report /tmp/NEW-D-binding.json
python3 -B -O research/case_study/phase164_enumeration_run.py --part all --output-dir /tmp/NEW-D-census
```

The runner also accepts `--part small`, `--part j2` and `--part m22`.
Exact computation does not certify the uniform written proofs in Lean.
