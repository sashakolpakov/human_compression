#!/bin/sh
# Sixteen fresh interpreters, one at a time. The first nonzero status stops.
# Each mathematical invocation has its own125s/128MiB checks. No files are made.
set -eu
CDPATH= cd -- "$(dirname -- "$0")"
for census_case in baseline obstructions 15_366 15_515 15_1055 15_1253 15_2252 15_2285 15_2303 15_2988 15_3009 15_3101 15_3126 16_189 16_423 16_483
do
    python3 -I -B -S check.py --case "$census_case"
done
printf '%s\n' '{"status":"PASS_COMPLETE_FIVE_FAMILY_CENSUS","original_indexed_rows":16414,"obstructions":16400,"valid_string_C_group_markings":14,"unresolved":0,"whole_F004_or_manuscript_claim":false,"new_open_conjecture_claim":false,"Lean_claim":false,"compression_measurement_claim":false}'
