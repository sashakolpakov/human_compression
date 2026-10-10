# Two metadata corrections to the frozen six-source measurement

These corrections leave all frozen phase144 files unchanged and are required when interpreting the reviewed package.

1. In the intake table of `phase144_report.md` (SHA-256 `449b596854953489c07c7cda0ece11618800d29781d98cc0205e3a27a2f0561b`), L035's author-manuscript title is **Existence of regular 3-polytopes of order 2^n**, not “Existence of regular polytopes of order 2^n”. The exact primary PDF, protocol edition and mathematical manuscript already identify the correct source.
2. In `phase144_measurement_protocol.json` (SHA-256 `00bb0c5fe30f1e50d4e29d884501c5be2c7061f0e630db6ddb0a7a4a2b0f21a1`), the final sentence of `render.extensions_to_prior_renderer`, “Literal math/code/table AST nodes unchanged.”, is stale. Its correct final-render meaning is: **Math and Table AST nodes are unchanged; CodeBlock text changes only by reversible display-newline insertion and exactly recovers the original.** This agrees with the same protocol's later `phase144_presentation_note`, the main report, the actual code map and independent recovery checks.

The measurement author confirmed both corrections during independent review. Neither changes a proof, executable program, source body, rendered denominator or numerical result. These are corrections to measurement metadata, so no additional mathematical proof is being omitted from the denominator and no artificial proof-cost charge is added.
