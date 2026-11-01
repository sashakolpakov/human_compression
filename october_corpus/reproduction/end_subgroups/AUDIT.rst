Independent review of the finite certificate replay
==================================================

The private and installed replays each passed all 26 controls and all
eleven supplied cases. Their complete results agree byte for byte. An
independent audit checked the actual execution chains, exact installation,
inputs, Source identities and resource records. It found no blockers.

Each complete eleven-case replay used 782 matrix products, four row
images and 12,440 scalar work units, with 211,776 charged input bytes.
Each control run used 98 products, seven row images and 32,882 scalar
units. The installed case replay took about 0.132 seconds; its sampled
peak process-tree RSS was 28,377,088 bytes. These observations retain
the supervisor's sampling and process-tracking qualifications.

The Source review is identified by SHA256
27ed552bc2fbb46a98f971404763fa1a6866638f67846402af9076b4094fd639.
The private actual review is identified by SHA256
79f8f8ed65f7ea82e126ae9667226d3337a8a4d7d69df7c2540cce38d43597c3.
The combined review of export, private replay, installation and installed
replay is identified by SHA256
15f7e471252211df34c58945ae2e4d413c2d079b5b567700cf075c76d629668b.
VALIDATION.json records the execution and input anchors. These two
external records are not consumed by the mathematical checker.

These checks reproduce existing exclusions. Group and module
identification, memberships, source rows and the complete maximal
subgroup classification retain their attribution in proof.tex and
IMPORTS.json. No subgroup search, full census, completed manuscript,
new conjecture solution or Lean proof is claimed by this replay.
