# Numerical scope of the Hermitian Figure2 in L092

This audit uses the retained Hermitian-unital proof without repeating it.
The original Figure2, printed p.570, has been read visually from
sources/older_L092_gwdg.pdf, SHA256
f76a72aeec658ace5d821519a686c3041e455d3a1c5c4276988bd711ba830403.
The discrepancies below are present in the PDF image, not only its text
extraction.

For the literal Construction3 on the classical unital UH(q), the design
parameters are 2-(q³+1,q+1,1), and each point is on q² blocks. Therefore:

* point objects: q³+1;
* marked flag objects: q²(q³+1);
* block objects: q²(q²−q+1);
* panel sizes, in Figure2's point/marked/block order: q, q+1, q²−1;
* local orders printed under those nodes should be q−1, q, q²−2.

These are direct counts of the actual source incidences. They do not
depend on the claimed all-q connectivity or on a choice of acting group.

## Panel discrepancies

Three printed rows have smaller marked/block panel sizes:

| q | Printed local orders | Literal local orders |
|---:|---|---|
| 5 | 4,1,7 | 4,5,23 |
| 8 | 7,2,20 | 7,8,62 |
| 11 | 10,3,39 | 10,11,119 |

In each of these rows, the printed marked panel size is (q+1)/3 and the
printed block panel size is (q²−1)/3. Thus the diagram cannot describe
the full literal Construction3 with the printed object set.

This factor three agrees with [PGU(3,q):PSU(3,q)]=gcd(3,q+1) in precisely
these rows. A selected chamber orbit under the smaller group can retain
the transitive object sets while omitting incidences of the complete
construction. That is a possible explanation of the table, not a
verified reconstruction of the source's computational procedure.
No claim that the author used a particular algorithm is made here.

## The q=16 object counts

The printed row gives 1,028 point objects, 263,206 marked objects and
15,482 block objects. Literal unital parameters instead give:

| Object type | Printed | Literal Construction3 |
|---|---:|---:|
| Points | 1,028 | 4,097 |
| Marked flags | 263,206 | 1,048,832 |
| Blocks | 15,482 | 61,696 |

The printed row is internally incompatible with its own q=16 flag
valencies: 1,028·256=263,168 and 15,482·17=263,194, neither equal to
263,206. This is a numerical correction independent of any interpretation
of the group-index issue above.

All other printed object counts for q=3,4,5,7,8,9,11,13 agree with the
literal formulas. The local orders in rows q=3,4,7,9,13,16 agree with
q−1,q,q²−2.

## Admission boundary

The existing all-q Hermitian proof concerns the literal source
construction and is retained as a separate conjecture record. It must
not be forced to reproduce incompatible diagram entries. The complementary
phase186_hermitian_residue_diameters.md now proves all the literal
diameter/gonality labels uniformly, using the root-coset Cayley graph of
SL(2,q). Together the two notes give a complete numerical audit of Figure2.
These new all-q diameter arguments remain written proofs pending review;
they are not covered by the finite Lean certificates.
