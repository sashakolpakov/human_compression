
The GAP Character Table Library
===============================


What is it?
-----------

The **GAP Character Table Library** is an add-on package
for the computer algebra system
[**GAP 4**](https://www.gap-system.org/).
It can be used also for the older version
[**GAP 3.4**](https://webusers.imj-prg.fr/~jean.michel/gap3/).

The library consists of

* ordinary and Brauer character tables of many finite groups,
  including those that are shown in the famous **ATLAS of Finite Groups**
  and **ATLAS of Brauer Characters**,

* GAP functions for handling these tables,

* and documentation how these data have been used in research.


Copyright
---------

Copyright 2003-2024 by Thomas Breuer


License
-------

This program is released under license GPL-3.0-or-later.
See the included file `GPL` for more details.


Download and Installation
-------------------------

To get the newest released version,

* download the archive file
  (where `x.y.z` stands for the highest available version number)

  `ctbllib-x.y.z.tar.gz`

  from [the homepage of the package](http://www.math.rwth-aachen.de/~Thomas.Breuer/ctbllib),

* move it to the appropriate directory, preferably
  (but not necessarily) into the `pkg` subdirectory of your GAP 4 installation,
  see the sections
  ["Installing a GAP Package"](https://docs.gap-system.org/doc/ref/chap76.html) and
  ["GAP Root Directories"](https://docs.gap-system.org/doc/ref/chap9.html) in
  [the GAP 4 Reference Manual](https://docs.gap-system.org/doc/ref/chap0.html),

* and unpack it using

  `gunzip ctbllib-x.y.z.tar.gz; tar xvf ctbllib-x.y.z.tar`

  Note that if you use a web browser for downloading the archive file the
  `gunzip` step above may already be done by the browser,
  although the name of your file may still have the misleading `.gz` extension.

  Unpacking the archive creates a subdirectory called `ctbllib-x.y.z`.


Loading the library into the GAP session
----------------------------------------

After its installation (see above),
the GAP Character Table Library is by default loaded automatically
when GAP is started.
If the library does not get loaded automatically
then it can be loaded explicitly by typing

  `gap> LoadPackage( "ctbllib" );`

at the GAP prompt.
Afterwards the functions and data of the package are available
in the current GAP session.


Documentation
-------------

The **package manual** is available
[in HTML format](http://www.math.rwth-aachen.de/~Thomas.Breuer/ctbllib/doc/chap0.html)
or [as a PDF file](http://www.math.rwth-aachen.de/~Thomas.Breuer/ctbllib/doc/manual.pdf).

A few **introductory examples** can be found in the
["Tutorial" chapter of the package manual](http://www.math.rwth-aachen.de/~Thomas.Breuer/ctbllib/doc/chap2.html).
You can read this tutorial inside the GAP session
via GAP's interactive help system by entering :

  `gap> ?Tutorial for the GAP Character Table Library`

at the GAP prompt.

More **character theoretic computations in the context of the
GAP Character Table Library** are listed in
[the introduction to the package manual](http://www.math.rwth-aachen.de/~Thomas.Breuer/ctbllib/doc/chap1.html#application_files).


Feedback
--------

If you have found important features missing or if there is a bug,
let us know and we will try to address it in the next version of the
GAP Character Table Library.
Please send a short email to

  Thomas Breuer (<sam@math.rwth-aachen.de>)

This holds also if you have used the GAP Character Table Library
to solve a problem.


License
-------

This package may be distributed under the terms and conditions of the
[**GNU Public License**](http://www.gnu.org/licenses) Version 3 or later.


Acknowledgement
---------------

Thomas Breuer gratefully acknowledges support by
the German Research Foundation (DFG) -- Project-ID 286237555 -- within the
[SFB-TRR 195 *Symbolic Tools in Mathematics and their Applications*](https://www.computeralgebra.de/sfb/).


---------------------------------------------------------------------------


For those who want to use the package with GAP 3.4
--------------------------------------------------

The **installation for GAP 3.4** works like the **installation for GAP 4**,
the package gets installed via unpacking the archive file in the `pkg`
directory of the GAP 3.4 installation.

When one starts GAP 3,
the outdated character table library is available by default.
For replacing it by the new one, one has to type

  `gap> RequirePackage( "ctbllib" );`

at the GAP prompt.

If one wants to use the new character table library as the default,
one can put this `RequirePackage` statement into one's `.gaprc` file
(see [the GAP 3.4 Reference Manual](https://webusers.imj-prg.fr/~jean.michel/gap3/htm/) for details).

Inside the GAP 3.4 session,
the value of the global variable `TBLNAME` allows one to decide
which of the two character table library variants is actually used.
This value ends with `tbl/` if the outdated library is used,
and with `ctbllib/data/` if the new library is used.

The manual of the GAP Character Table Library is intended for GAP 4,
in particular the cross-references refer to the GAP 4 Reference Manual.
So when using the new character table library with GAP 3.4,
one should still consult the documentation of the character table library
contained in the Reference Manual of GAP 3.4.


