Fi22:2 finite incidence certificate
==================================

The literal saved permutations generate PrimitiveGroup(3510,2) and give a
regular polytope of type {6,13} and a nonlinear rank-three regular hypertope
with triangle labels (6,6,13). The three-page paper gives the complete
incidence and automorphism argument. Distinct review and question admission
remain separate. No historical priority or compression factor is claimed.

Replay with Python 3 and GAP 4.15.1, PrimGrp 4.0.1, CTblLib 1.3.11::

  python3 -B -O check.py --out /fresh/absolute/path

The output must not already exist, including a dangling symlink. Exact
frozen export hashes and installed catalogue inputs are checked first.
No search is rerun. The whole programs, witness and driver are included;
the installed primitive representation remains an external, hash-bound
catalogue input with its full byte size visible in retained_inputs.json.

The full generated permutation group is constructed independently from
the saved triple and proved equal to the named group. Both markings pass
49 proper-subset IP pairs; the remaining fifteen pairs per marking are
elementary full-subset identities. All six flag equalities are tested by
streaming complete finite product sets. The halved marking has both an
explicit generation inverse and directly verified generated-group equality.

The additional 11/13 words and full maximal-subgroup order test provide
validation of a second generation route. That classification is not a
premise of the direct equality proof. Named-group identification, the
classical outer order and the polytope correspondence remain retained.
GAP's exact algorithms are not claimed as Lean proofs. There are no new
Lean declarations here. The six controls include a marking with IP but
without flag transitivity, so those obligations are not conflated.

This answers the Fi22 existence case left as a possible exception in the
literal Theorem 5.3 of arXiv:2605.04646v2, subject to independent acceptance.
The Fi24-prime exception is untouched. The ten affirmative sporadic cases,
including the separately supplied HN case, are separate frozen packets.
The bounded current-literature status audit and any question catalogue
decision are separate from the deterministic mathematical certificate.

Private search files and original source text/PDF are not exported. Their
absence does not remove any input required to replay the saved witness.
