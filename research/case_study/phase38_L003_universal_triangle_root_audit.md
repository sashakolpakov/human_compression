# Root review: universal infinitude for every parameter at least six

10 October 2026. PASS for the complete written group and spectral proof,
with a fresh exact checker replay. This review supersedes the author's
historical pending-review labels. The separate Lean work is still in
progress and is not part of this certificate.

I read the entire manuscript and checker, and compared the ten defining
words directly with section 8 on page 17 of the cached primary 2018 paper.
The ordered substitution is (3,0), (2,0), (1,1), (s,0). I also read Table 8
and the surrounding discussion and Problem 9.2 on pages 18–19. This is
targeted source verification, not a new whole-paper reading.

The right permutation convention is consistent with the displayed wreath
multiplication. Expanding v=dqd and using only the two finite factors
reduces each of the nine fixed relators to the identity. The tenth word
is exactly (hq,1,qh), whose s-th power is one in the presented triangle
group. The three displayed kernel elements project to d,h,q, so the
coordinate map is surjective from a subgroup of the image. A global
surjection from the original group to the triangle group is not assumed.
The reversing involution supplies a direct quotient of the four-involution
presentation, independently of any previously claimed split extension.

The explicit real reflections satisfy the triangle presentation. On the
invariant two-plane, HQ has distinct eigenvalues exp(±2πi/s), and the
remaining eigenvalue is one. Thus its s-th power is exactly one, including
at s=6. For s>6 the displayed characteristic polynomial of DHQ has a real
root greater than one; at s=6 its square is I+M with M nonzero and M²=0.
Both arguments prove infinite order. Neither depends on triangle-group
classification, a numerical approximation or faithfulness of the model.

I freshly ran the unchanged standard-library checker to a new scratch
report. It passed all abstract word, permutation, subgroup-witness,
involution, Coxeter-pair and integer-polynomial checks; its output is
byte-identical to the author report. I inspected the finite-factor reducer
and the polynomial implementation. They verify the displayed identities;
the all-parameter trigonometric, eigenvalue and surjection arguments remain
written proofs, reviewed above.

The theorem is that the exact P_s and U_s are infinite for every integer
s≥6. The earlier universal-geometry theorem separately identifies U_s as
the desired regular hypertope group. Finite universal groups at s=2,3,4,5
are retained published computations, not freshly established by this
package. Finite quotients with the prescribed local groups still exist at
every s≥2; that assertion is compatible with infinite universal groups.

No additional whole-manuscript coverage, compression factor, historical
priority, end-to-end Lean proof or current-open-problem resolution is
certified here. The unread 2024 covering-paper comparison remains a
material priority boundary.
