L024 distinct principal-recovery review
=====================================

Accepted exact author v3 with the limits in review.rst and review.json.
No author files, public files or source credits were changed.

Replay from this directory with a fresh output path::

  /Users/sasha/.venvs/global/bin/python -B -O check.py \
    --author ../corpus106_L024_recovery_v3 --out /private/tmp/L024_review_fresh

Add --replay-author and --render to repeat the fixed GAP premise and two-pass
five-page pdfLaTeX build. The review exports and separately supplied exact author
exports suffice; --study-root optionally checks both primary PDF bindings.
The installed GAP Character Table Library remains required external data.
