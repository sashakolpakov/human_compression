Products and stabilizers in the Fi22 geometry
============================================

The `argument <ARGUMENT.rst>`_ gives a conditional method for the unfinished
Fi22 part of L026. It derives the three involution classes from vertices,
commuting edges and pairs of triangles in the three-transposition geometry.
It then computes their stabilizers and orbit weights through smaller local
actions. This replaces the proposed flat class enumeration with a precise
geometric problem; its performance has not yet been measured.

The main deductions are:

* Products identify commuting edges with the class 2B. Each element of 2C
  corresponds to exactly two commuting triangles.
* The two triangles are disjoint and form a hexad in a maximal commuting
  clique. This recovers its Witt design and binary relation code from the
  product fibers.
* Successive point stabilizers classify ordered local configurations.
  Quotienting by coordinate permutations and then by the triangle partner
  gives the correct element orbits, stabilizers and weights.
* A point fixed by the full centralizer, together with equality of orders,
  can identify the existing permutation model with the geometric action.
  This identification remains a finite obligation.

The Fischer geometry, unitary action, maximal subgroups and transporter
methods are attributed literature inputs. The note supplies its deductions
and their proposed use in this project; it claims no historical novelty.
The `primary-source record <PRIMARY_SOURCES.rst>`_ gives exact references
and reading scope. The `independent review <REVIEW.rst>`_ checks the written
arguments and distinguishes them from the computations still required.

Status and reproduction
-----------------------

These are exact copies of the reviewed notes. The
`acquisition interface <ACQUISITION_INTERFACE.rst>`_ states the certificates
needed to apply the theory to the current model. The model correspondence,
endpoint stabilizers, complete local orbits, generation results and duality
census have not been acquired by this package. It adds no completed
original, compression measurement or Lean proof.

This package contains mathematical text and review records. It provides no
executable census. Read the argument with its cited premises, then the
review and interface. References to local maintenance paths in the frozen
notes identify earlier evidence; they are not portable replay commands.
The `manifest <SourceManifest.json>`_ records the published bytes and their
originals. `Verification <verification.json>`_ records the scope of the
review. File integrity can be checked from the repository root:

.. code-block:: sh

   python3 -E -B - <<'PY'
   from pathlib import Path
   import hashlib, json
   root = Path('october_corpus/research/fi22/involution_geometry')
   manifest = json.loads((root / 'SourceManifest.json').read_text())
   for row in manifest['files']:
       data = (root / row['path']).read_bytes()
       assert len(data) == row['bytes']
       assert hashlib.sha256(data).hexdigest() == row['sha256']
   print('All published files match the manifest.')
   PY

This checks the files, rather than formalizing the mathematical argument.
