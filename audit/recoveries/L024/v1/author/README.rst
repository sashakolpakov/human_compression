L024 recovery candidate
=======================

Read schur_characters.tex and source_map.json. Run the exact finite premise
with GAP 4.15.1 and Character Table Library 1.3.11:

    gap -q verify_schur_example.g

The ordinary table is a retained input, pinned in dependencies.json. The
script uses fixed matrices and directly enumerated isotropic points; it
does not use the discovery search, an Atlas download, or unspecified class
representatives. Its output begins STATUS=PASS only after all checks finish.
Build schur_characters.tex twice with pdflatex. The five-page written proof
is not a Lean formalization; no numerical comparison has been made.

The intersection property is proved in writing from the product orders and
full generation. The unchanged program also checks it as corroboration;
generation and character computations remain required finite premises.
