#!/usr/bin/env python3
"""Build and run the two unchanged synthetic harnesses; never run ON production."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shlex
import subprocess
import sys
import tempfile
import time


SOURCE_PATHS = (
    "packed_keys.c", "packed_keys.h", "controls.c",
    "portable_io/portable_cli.c", "portable_io/portable.py",
    "portable_io/controls_io.py", "portable_io/export_maps.g",
    "portable_io/export_driver.g",
)
LOG_LIMIT = 64 * 1024
BINARY_LIMIT = 16 * 1024 * 1024


def digest(path, limit):
    if path.stat().st_size > limit:
        raise ValueError("file exceeds the declared local bound: " + str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(argv, directory, environment, deadline, name):
    """Retain bounded command output in the temporary directory and relay it."""
    outpath, errpath = directory / (name + ".stdout"), directory / (name + ".stderr")
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError("shared 140-second entrypoint deadline")
    with outpath.open("xb") as stdout, errpath.open("xb") as stderr:
        result = subprocess.run(
            argv, cwd=directory, env=environment, stdout=stdout, stderr=stderr,
            timeout=remaining, check=False,
        )
    for path, stream in ((outpath, sys.stdout.buffer), (errpath, sys.stderr.buffer)):
        if path.stat().st_size > LOG_LIMIT:
            raise ValueError("command log exceeds 64 KiB: " + name)
        stream.write(path.read_bytes())
        stream.flush()
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, argv)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--cc", default=os.environ.get("CC", "cc"),
                        help="C compiler command, split as argv without a shell (default: CC or cc)")
    args = parser.parse_args()
    cc = shlex.split(args.cc)
    if not cc:
        raise ValueError("nonempty C compiler command required")
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "SourceManifest.json").read_bytes())
    if manifest["schema"] != "L026_PACKED_KEYS_PUBLIC_SOURCE_MANIFEST_V1":
        raise ValueError("Source manifest schema")
    sources = {item["path"]: item for item in manifest["sources"]}
    if len(manifest["sources"]) != len(SOURCE_PATHS) or set(sources) != set(SOURCE_PATHS):
        raise ValueError("exact eight original Source files required")
    for name in SOURCE_PATHS:
        path, item = root / name, sources[name]
        if path.stat().st_size != item["bytes"] or digest(path, 1024 * 1024) != item["sha256"]:
            raise ValueError("original Source differs from the manifest: " + name)

    # The outer 512 MiB / 150 s family guard is an external execution duty.
    # This local deadline and final byte checks do not replace that guard.
    deadline = time.monotonic() + 140
    with tempfile.TemporaryDirectory(prefix="l026_packed_public_") as directory:
        work = Path(directory)
        environment = dict(os.environ, TMPDIR=str(work))
        core, portable = work / "core_controls", work / "packed_portable"
        flags = ["-std=c11", "-O2", "-Wall", "-Wextra", "-Werror"]
        run(cc + flags + [str(root / "packed_keys.c"), str(root / "controls.c"), "-o", str(core)],
            work, environment, deadline, "build_core")
        # portable_cli.c includes ../packed_keys.c: do not link kernel.o again.
        run(cc + flags + [str(root / "portable_io/portable_cli.c"), "-o", str(portable)],
            work, environment, deadline, "build_portable")
        binary_hashes = {"core_controls": digest(core, BINARY_LIMIT),
                         "portable": digest(portable, BINARY_LIMIT)}
        run([str(core)], work, environment, deadline, "core18")
        run([sys.executable, "-E", "-B", str(root / "portable_io/controls_io.py"),
             "--binary", str(portable), "--binary-sha256", binary_hashes["portable"]],
            work, environment, deadline, "portable_io10")
        # Counts and assertions belong to the unchanged harnesses above.
        print(json.dumps(dict(
            status="COMPLETED_UNCHANGED_SYNTHETIC_PACKED_HARNESSES",
            core_controls=18, portable_controls=10, synthetic_only=True,
            binary_sha256=binary_hashes, compiler_command=cc,
            named_ON_partition_credit=0, generation_credit=0,
            whole_original_credit=0, whole_Lean_claim=False,
        ), sort_keys=True))


if __name__ == "__main__":
    main()
