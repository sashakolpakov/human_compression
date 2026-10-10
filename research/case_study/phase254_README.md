# Independent mixed-prime application review

The review in `phase254_review.md` accepts the exact principal L012
contract of frozen phase250. It records both required pre-freeze proof
repairs, the source's auxiliary sign correction, all exclusions and the
retained mathematical inputs. It does not edit the author package or
the public registry.

Run from this directory with a nonexistent output path:

```sh
python3 -B -O phase254_check.py \
  --out /private/tmp/phase254_fresh_review \
  --gap /opt/homebrew/bin/gap \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --packages /Users/sasha/bogachev/formal/.lake/packages
```

The runner requires the bound private primary files and frozen author
dependencies. It replays the complete author interface, then executes
two independent programs: exact finite affine quotient enumeration and
literal source presentation checks. The final review replay took 18.857
seconds in the tested environment; its reports and logs are retained in
`phase254_replay/`. Timings are observations, not guarantees.

The primary source has seventeen pages. The final replacement PDFs have
five and nine pages and were inspected in full. Required earlier proof
components and programs are additional; these page numbers establish no
compression rate. Lean proves three general sign identities, not the
full positive application. No new open question is admitted.
