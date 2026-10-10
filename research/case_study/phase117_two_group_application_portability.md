# Additive portability correction to the frozen Module A checkpoint

The original author manifest and all mathematical bytes remain unchanged. Two infrastructure paths in that checkpoint assumed a public `research/case_study/studies` directory. The repository actually stores these artifacts directly in `research/case_study`.

Use the additive `phase117_two_group_application_verify_v2.py`. It checks the original frozen manifest and its complete bindings, plus this additive manifest. Its formal-file resolver checks `ROOT/formal`, which is the actual public location, before the historical fallback locations. The correct public command is:

```sh
python3 -B -O research/case_study/phase117_two_group_application_verify_v2.py --output /private/tmp/NEW-A-integrity.json --rebuild
```

The private command adds `--primary-check --private-visual` and uses the `research/leemans` directory. The original checkpoint generator is a historical private author tool: it verifies private primary PDFs and addresses the public-tree Lean directory from the private research directory. It is not a portable public entry point. The builder itself remains portable because its proof-material dependencies are sibling files.

The earlier successful temporary `/studies/` reconstruction verified the wrong deployment layout. The additive author checks reconstruct the actual `research/case_study` layout with `formal` below it. Only that replay is evidence of public-layout portability. Neither this correction nor either integrity checker is a mathematical proof or an independent admission of U+A. No manuscript, source contract, rendered page or proof-cost count changes.
