# Root review of the compact splitting supplement

Date: 2026-10-10. PASS after complete proof/code read and a fresh run.

The four literal offsets after origin change are twice the displayed
integer vectors. Thus a=t+2c gives an integral affine group whose full
translation kernel is Z6. Every linear image has an integral-offset lift;
canceling that offset with an existing translation gives its pure linear
lift. This proves the split extension with the actual integral group Q.
The established reduction kernel becomes mZ6, so the same splitting
descends at every modulus.

The m=1 boundary is handled correctly: Q is retained as an abstract group,
not replaced by its possibly nonfaithful matrix action modulo m. No integral
decomposition into smaller lattice blocks is needed or claimed. The
standalone fresh checker reproduced all24 coordinate equalities and the
saved report byte-for-byte. It does not repeat the retained kernel census.
No universal-group splitting or new priority follows.
