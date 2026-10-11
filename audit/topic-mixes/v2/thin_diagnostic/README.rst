A thin base whose two-sheeted cover is not thin
==============================================

This is a distinct finite diagnostic of the example proposed by the cover
manuscript author. It verifies the literal hypotheses and failure of Lemma
3.5 on physical page 5 of arXiv:2305.01372v2. The base has 32 flags and
two faces of every rank; the cover has 64 flags and face counts 2,4,4,2.
All base diamonds have two intermediate faces. Sixteen cover diamonds have
four. The base is unfaithful; the cover is faithful.

The integer-bit implementation imports no author mathematics or code. It
checks every adjacency, nonconsecutive square, component, face projection,
face-order transitivity triple and diamond interval. The written general
repair and the rest of the source remain separate review obligations. This
record creates no whole-source or open-conjecture credit.

Run with Python from any directory::

  python3 -B -O check.py /fresh/result.json

Bit order is v0,v1,v2,v3,z,epsilon, with the last bit used in the cover.
The source PDF and source images are not exported.
