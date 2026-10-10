#!/usr/bin/env python3
"""Compile the actual marked parity-mix fiber, profile and intersection theorem."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

DEPENDENCY_SHA = "4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3"
MODULES = [('CoprimePullback.lean',
  '4eb20ee7eb85943eab4100b565146a8cd938e4f3c2055b66c6fbbdfa3f68987c',
  {'MathCompression.CoprimePullback.closure_paired_generators',
   'MathCompression.CoprimePullback.eq_fiberProduct_of_coprime',
   'MathCompression.CoprimePullback.snd_kernel_mem'},
  False),
 ('LiftCertificate.lean',
  'd8429bd867cbc8ea29c6af9768d93df49c5be027328f2b25fa32102cbc3009d7',
  {'LeemansLift.cyclic_intersection_transfer',
   'LeemansLift.intersection_of_image_and_kernel',
   'LeemansLift.noReverser_of_cyclic_kernel',
   'LeemansLift.reversing_preserves_power_subgroup'},
  False),
 ('CoordinateKernels.lean',
  '168fb88f08a5f7a4bc41d403ac1e288fe8a7641c3714fc23ac80295414fac4d6',
  {'LeemansCoordinates.coordinate_kernel_meet',
   'LeemansCoordinates.intersection_transport_with_coordinates'},
  False),
 ('SupportedKernelGeneration.lean',
  '1fb99082407826a390e975432c5f12d1e665ac66af9d18fbb75532af5a57f10a',
  {'MathCompression.SupportedKernelGeneration.coordinate_mem_marked_inter',
   'MathCompression.SupportedKernelGeneration.generated_eq_fiber',
   'MathCompression.SupportedKernelGeneration.kernel_profile',
   'MathCompression.SupportedKernelGeneration.local_kernel_witness',
   'MathCompression.SupportedKernelGeneration.marked_base_fixed',
   'MathCompression.SupportedKernelGeneration.marked_compatibility',
   'MathCompression.SupportedKernelGeneration.marked_intersection_property',
   'MathCompression.SupportedKernelGeneration.pure_kernel_mem',
   'MathCompression.SupportedKernelGeneration.supported_kernel_construction',
   'MathCompression.SupportedKernelGeneration.triangular_isolation'},
  False),
 ('IntervalOverlapCancellation.lean',
  '7a1072ffb966606b7d0371b7c123220a0498d00a2299b8c76f5ccb7c2f8f4ae5',
  {'MathCompression.IntervalOverlapCancellation.endpoint_mem',
   'MathCompression.IntervalOverlapCancellation.exists_leaf',
   'MathCompression.IntervalOverlapCancellation.weights_eq_zero'},
  False),
 ('FinIntervalOverlapCancellation.lean',
  'a951b853c7a33512a2d0293bdef7f8c101d4f1dcf55d8a87482d38fbb3851417',
  {'MathCompression.IntervalOverlapCancellation.fin_val_disjoint_iff',
   'MathCompression.IntervalOverlapCancellation.fin_val_ordConnected',
   'MathCompression.IntervalOverlapCancellation.fin_weights_eq_zero'},
  False),
 ('ParityMix.lean',
  '99388ddf23fe27c684ab2ca238e9953a9bda9b31b11a5b1301427f15cb03c852',
  {'MathCompression.ParityMix.binary_companion',
   'MathCompression.ParityMix.connected_parity_fiber',
   'MathCompression.ParityMix.isolate_odd_second',
   'MathCompression.ParityMix.mix_le_fiber',
   'MathCompression.ParityMix.pure_adjacent',
   'MathCompression.ParityMix.pure_path'},
  True),
 ('ParityMixComponents.lean',
  'd76a62d2064ba4833c9edae7989b3bb443bba0f5a23aade3fc61b1519310eba9',
  {'MathCompression.ParityMix.componentAssembly_injective',
   'MathCompression.ParityMix.componentAssembly_map',
   'MathCompression.ParityMix.componentAssembly_range',
   'MathCompression.ParityMix.marked_commute',
   'MathCompression.ParityMix.marked_component_sup',
   'MathCompression.ParityMix.marked_components_independent'},
  True),
 ('ParityMixLocal.lean',
  '869f91e13478d51775129327b27b553d8362f02c0dd976ddd5073f297b94c633',
  {'MathCompression.ParityMix.connected_support_profile',
   'MathCompression.ParityMix.localMarker_generation',
   'MathCompression.ParityMix.local_mix_map'},
  True),
 ('ParityMixProfile.lean',
  '04b65e4c8f032ee58181a72d0f13c2b4e160a1c68ecf1be95b884db2ee53ad74',
  {'MathCompression.ParityMix.mixed_component_profile'},
  True),
 ('ParitySupportIntervals.lean',
  '9dca720c5209f3e3bc3874af480e878c146d524356ad5730cf73e3ce96607400',
  {'MathCompression.ParityMix.component_index_nonempty',
   'MathCompression.ParityMix.component_index_ordConnected',
   'MathCompression.ParityMix.components_separated',
   'MathCompression.ParityMix.interval_forward_path',
   'MathCompression.ParityMix.interval_path',
   'MathCompression.ParityMix.supportComponent_eq_component',
   'MathCompression.ParityMix.supportComponent_eq_of_overlap',
   'MathCompression.ParityMix.supportComponents_cover',
   'MathCompression.ParityMix.supportComponents_disjoint'},
  True),
 ('ParityMixFiniteProfile.lean',
  '3195bfd88411ecfeefa4f9e341f12ce96aa118d2566d2c9695cd0b883f1ede66',
  {'MathCompression.ParityMix.canonical_mixed_parity_profile',
   'MathCompression.ParityMix.component_string_comm',
   'MathCompression.ParityMix.component_subtype_cover',
   'MathCompression.ParityMix.interval_support_profile',
   'MathCompression.ParityMix.path_adjacent_odd'},
  True),
 ('ParityComponentCoordinates.lean',
  '21eac58b0a1e41c8bb71dd98b5c93289e63565527f069b4d728e246e53bbcc4c',
  {'MathCompression.ParityMix.componentAssembly_mem_super',
   'MathCompression.ParityMix.componentCoordinate_local',
   'MathCompression.ParityMix.component_coordinate_refinement',
   'MathCompression.ParityMix.hom_pi_product'},
  True),
 ('ParityMixCoordinateProfile.lean',
  '3abb2e2a2d21c78a2a03680b63967995d9597872d304ab9638bb57e2854370d2',
  {'MathCompression.ParityMix.mixed_membership_coordinates'},
  True),
 ('ParityOverlapGrid.lean',
  '54552b16682f4b4fce648d96882549fc0b970b74e061e775cb68839ba463f2e6',
  {'MathCompression.ParityMix.overlapScope_commute',
   'MathCompression.ParityMix.overlapScope_cover',
   'MathCompression.ParityMix.overlapScope_disjoint',
   'MathCompression.ParityMix.overlapScope_ordConnected'},
  True),
 ('ParityRefinementCharacters.lean',
  'a229dcd40c7c0f823f7da888b0ee235d929128a336bcbb596f435728de84da12',
  {'MathCompression.ParityMix.character_defect_sum',
   'MathCompression.ParityMix.column_filtered_product',
   'MathCompression.ParityMix.refined_character_equality',
   'MathCompression.ParityMix.row_filtered_product'},
  True),
 ('ParityMixIntersections.lean',
  'ddd29b0ae7f118c8fa9e4b93e75abc44dbed070cd4b332cac38fab5e6ae09039',
  {'MathCompression.ParityMix.mixed_coordinate_membership',
   'MathCompression.ParityMix.parity_overlap_intersection'},
  True),
 ('ParityMixTheorem.lean',
  '9927c96f935d5b1739f7d21a7685117d18f8217399e7ac06921388d46abd86ed',
  {'MathCompression.ParityMix.intrinsic_parity_mix_intersection',
   'MathCompression.ParityMix.marked_parity_mix_intersection',
   'MathCompression.ParityMix.mixedMarker_generation',
   'MathCompression.ParityMix.mixedMarker_involutions',
   'MathCompression.ParityMix.mixedMarker_string'},
  True)]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packages", type=Path, required=True)
    ap.add_argument("--lean", default="lean")
    ap.add_argument("--source-dir", type=Path,
                    default=Path(__file__).resolve().parent / "formal")
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    output = args.output_dir.absolute()
    require(not output.exists() and not output.is_symlink(), "Fresh output directory required")
    source_dir = args.source_dir.resolve()
    dependency_file = source_dir / "dependency_manifest.json"
    require(sha(dependency_file) == DEPENDENCY_SHA, "Frozen dependency manifest changed")
    for name, expected, _, _ in MODULES:
        source = source_dir / name
        require(sha(source) == expected, "Frozen source changed: " + name)
        require(not re.search(r"\b(sorry|admit|axiom)\b", source.read_text()),
                "Unproved source declaration or placeholder: " + name)
    dependencies = json.loads(dependency_file.read_text())
    lean = shutil.which(args.lean)
    require(lean is not None, "Lean executable not found")
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = dependencies["lean"]
    version = subprocess.check_output([lean, "--version"], env=env, text=True).strip()
    expected_version = dependencies["lean"].split(":")[-1].removeprefix("v")
    require(re.search(r"\bversion " + re.escape(expected_version) + r"(?:,|\s|\))", version),
            "Unexpected Lean version")
    checked, libraries = [], []
    for item in dependencies["packages"]:
        checkout = args.packages.resolve() / item["name"]
        rev = subprocess.check_output(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
        require(rev == item["rev"], "Wrong dependency revision: " + item["name"])
        clean = subprocess.run(["git", "-C", str(checkout), "diff", "--quiet", "HEAD", "--"])
        require(clean.returncode == 0, "Tracked dependency changed: " + item["name"])
        library = checkout / ".lake/build/lib/lean"
        if library.is_dir():
            libraries.append(library)
        checked.append({"name": item["name"], "revision": rev, "tracked_files_clean": True,
                        "compiled_library_present": library.is_dir()})
    output.mkdir(parents=True, exist_ok=False)
    env["LEAN_PATH"] = os.pathsep.join(map(str, [output] + libraries))
    builds = []
    for name, expected_sha, declarations, is_new in MODULES:
        source = source_dir / name
        require(sha(source) == expected_sha, "Frozen source changed during execution: " + name)
        started = time.monotonic()
        obj = output / name.replace(".lean", ".olean")
        run = subprocess.run([lean, "-o", str(obj), str(source)], cwd=source_dir, env=env,
                             capture_output=True, text=True, timeout=300)
        elapsed = time.monotonic() - started
        log = output / name.replace(".lean", ".log")
        log.write_text(run.stdout + run.stderr)
        require(run.returncode == 0 and not run.stderr.strip(), run.stdout + run.stderr)
        require(not re.search(r"sorryAx|native_decide|warning:|error:", run.stdout),
                "Unexpected diagnostic or trust axiom: " + name)
        matches = re.findall(
            r"'([A-Za-z_][A-Za-z_0-9.]*)' depends on axioms: \[([^]]*)\]",
            run.stdout)
        require(len(matches) == len(declarations) and {n for n, _ in matches} == declarations,
                "Missing or duplicate axiom report: " + name)
        reports = {}
        for declaration, text in matches:
            axioms = {a.strip() for a in text.split(",") if a.strip()}
            require(axioms <= {"propext", "Classical.choice", "Quot.sound"},
                    "Unexpected axiom: " + declaration)
            reports[declaration] = sorted(axioms)
        require(obj.is_file() and not obj.is_symlink(), "Fresh compiler object missing: " + name)
        builds.append({"source": name, "source_sha256": expected_sha,
                       "seconds": elapsed, "exit_code": run.returncode,
                       "log_sha256": sha(log), "object_sha256": sha(obj),
                       "axiom_reports": reports, "new_component": is_new,
                       "stdout": run.stdout, "stderr": run.stderr})
    require(sha(dependency_file) == DEPENDENCY_SHA, "Frozen dependency manifest changed during execution")
    for name, expected, _, _ in MODULES:
        require(sha(source_dir / name) == expected, "Frozen source changed during execution: " + name)
    report = {
        "status": "PASS", "date": "2026-10-10", "lean": version,
        "runner_sha256": sha(Path(__file__)),
        "dependency_manifest_sha256": DEPENDENCY_SHA, "dependencies": checked, "builds": builds,
        "new_printed_declarations": 50, "existing_recompiled_declarations": 25,
        "new_local_modules": 12, "retained_local_modules": 6,
        "scope": "Actual generated parity fiber, canonical all-support component profile, proved overlap character equations and intrinsic full marked intersection property from the two-primary, odd-adjacency, genuine-character and factor string/IP hypotheses.",
        "target_mixed_intersection_assumed": False,
        "target_connected_fiber_assumed": False,
        "row_and_column_parity_equations_derived": True,
        "interval_cancellation_proved_in_retained_modules": True,
        "intrinsic_generation_and_nonidentity_involutions_proved": True,
        "unproved_placeholders": False, "native_evaluation_axioms": False,
        "trust_boundary": "All 18 local sources freshly compiled. Pinned package revisions and tracked cleanliness checked; compiled package dependency objects and the installed compiler remain trusted. No private source text or historical monolith is needed to run this replay.",
        "exclusions": ["formal parabolic cardinality formula", "exact adjacent lcm orders",
                       "source-specific finite-field parameter selection", "BFL group construction and intersection inputs",
                       "existence or value of a source-specific Dickson or matrix parity character",
                       "abstract-polytope correspondence", "all-label universal-group conjecture",
                       "full source-paper formalization", "historical priority", "source-level compression ratio"]
    }
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "new_printed_declarations": 50,
                      "retained_printed_declarations": 25, "local_modules_compiled": 18,
                      "seconds": sum(b["seconds"] for b in builds), "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
