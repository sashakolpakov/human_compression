# Metacyclic groups satisfy the hereditary powerful-Frattini hypothesis

10 October 2026. Private adapter for review. This derives the earlier
metacyclic 2-group cyclic-TPP result from Theorem B of
phase11_powerful_frattini.md, without a metacyclic classification.

**Lemma.** The Frattini subgroup of every finite metacyclic 2-group is
powerful.

**Proof.** Write H=⟨u,v⟩ with ⟨u⟩ a normal cyclic subgroup and H/⟨u⟩
cyclic. If H is cyclic there is nothing to prove. Otherwise conjugation
has form u^v=u^r for an odd integer r. Put L=⟨u²,v²⟩. This subgroup
is normal: v normalizes ⟨u²⟩, and conjugating v² by u changes it by
an even power of u, since r²−1 is even. The quotient H/L is generated
by two commuting involutions. It follows that Φ(H)≤L. The reverse
inclusion follows because u²,v² are squares, so Φ(H)=L.

The commutator subgroup of L is

    L′=⟨[u²,v²]⟩=⟨u^(2(r²−1))⟩.

Indeed this displayed cyclic subgroup is normal in L, and its quotient
makes the two generators commute. Since every odd r satisfies
8 | (r²−1), the displayed generator is a power of u⁸=(u²)⁴.
Consequently L′≤L⁴, which is exactly powerfulness for a 2-group. ∎

Every subgroup H of a metacyclic group P is metacyclic: if N is a normal
cyclic subgroup with P/N cyclic, then H∩N is cyclic and normal in H,
and H/(H∩N) embeds into the cyclic group P/N. The lemma therefore proves
that Φ(H) is powerful for every H≤P. Theorem B gives cyclic TPP for
every finite metacyclic 2-group.

The odd-prime metacyclic cases are already included in the stronger
phase11_odd_nilpotent.md theorem for all finite odd-p groups. Thus the
combined framework recovers the earlier all-prime metacyclic theorem.
This is an additional derivation, not a second independently counted
resolution of that same result. It does not use the false assertion that
every subgroup of a powerful group is powerful.
