# Required conjugation-convention correction

For `phase83_nonabelian_cover_theorem.md`, SHA-256
`ba1744144b1206b09c4e1b271516340b3715d3d5af0a52c50faa63d23cee0a35`,
Section 5: replace “Conjugating (8) by t_16⁻¹t_32” with “Conjugating (8)
by t_32⁻¹t_16.” With the declared convention x^g=g⁻¹xg, this means
left-multiplication by t_16⁻¹t_32 and right-multiplication by t_32⁻¹t_16.
The displayed equation (8) and the Lean proof already use the correct
products; no certificate or theorem statement changes. The independent
reviewer identified this wording error on 10 October 2026.
