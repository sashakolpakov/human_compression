# Theorem dependencies for the projective-line comparison

Proof dependencies of the matched principal contracts, grouped at named lemmas or closely connected blocks.

Costs are measured at full selected document level. Nodes have no separate numerical weights; node counts are not complexity ratios.

External inputs remain explicit. Arrows point from a premise to its use.

## Source

```mermaid
flowchart TD
  D["retained external input: Dickson and projective subgroup theory"]
  P["retained external input: C-groups, polytopes and local maps"]
  R["retained external input: Earlier PSL2 rank bound"]
  S083["L083: String setup and proper parabolics"]
  L1["L083: Odd characteristic"]
  L2["L083: Odd end labels"]
  L3["L083: Subfield intersection count"]
  L4["L083: Exclude PSL2 facets"]
  L5["L083: Cyclic intersections and normalizers"]
  L6["L083: Exclude PGL2 facets"]
  T["L083: Local maps and ten universal groups"]
  C083["L083: PSL2 classification"]
  G083["L083: Geometric properties and even subgroup"]
  S079["L079: String setup and subgroup alternatives"]
  R079["L079: PGL2 rank bound"]
  O079["L079: Odd end labels"]
  I079["L079: Subfield containment and intersections"]
  A079["L079: Exclude affine facets"]
  F079["L079: Exclude PSL2 and PGL2 facets"]
  C079["L079: PGL2 classification"]
  P --> S083
  D --> L1
  S083 --> L1
  D --> L2
  L1 --> L2
  D --> L3
  L3 --> L4
  S083 --> L4
  L3 --> L5
  L3 --> L6
  L5 --> L6
  L2 --> L6
  D --> C083
  R --> C083
  L1 --> C083
  L4 --> C083
  L6 --> C083
  P --> T
  T --> C083
  C083 --> G083
  P --> G083
  T --> G083
  D --> G083
  P --> S079
  D --> S079
  C083 --> S079
  D --> R079
  S079 --> R079
  D --> O079
  S079 --> O079
  D --> I079
  L3 --> I079
  D --> A079
  S079 --> A079
  I079 --> F079
  O079 --> F079
  S079 --> F079
  R079 --> C079
  A079 --> C079
  F079 --> C079
  T --> C079
  D --> C079
```

## Replacement

```mermaid
flowchart TD
  D["retained external input: Dickson types, embeddings and group facts"]
  P["retained external input: C-groups, polytopes and local maps"]
  S["U_E: Indecomposability and string consequences"]
  N["U_E: Odd-order normalizer lemma"]
  C2["U_E: Characteristic-two centralizer"]
  V["U_E: Four-group centralizer"]
  C["U_E: Dihedral centralizer descent"]
  O["U_E: Odd end labels"]
  R["U_E: Uniform rank restriction"]
  L["U_E: Elementary facet exclusions"]
  F["U_E: Exceptional facets only"]
  Code["required program: Complete exact finite program"]
  Loc["U_E: Six local classes"]
  Tab["U_E: Ten universal presentations"]
  U["U_E: Uniform reduction"]
  A1["A1: PSL2 classification and geometry"]
  A2["A2: PGL2 classification and simplex"]
  D --> S
  C --> O
  C2 --> R
  V --> R
  S --> R
  D --> F
  L --> F
  S --> F
  R --> F
  C --> F
  N --> F
  O --> F
  Code --> Loc
  Loc --> Tab
  Code --> Tab
  P --> Tab
  R --> U
  F --> U
  Loc --> U
  Tab --> U
  U --> A1
  Tab --> A1
  D --> A1
  P --> A1
  U --> A2
  Tab --> A2
  D --> A2
  P --> A2
```

The source graph retains three explicit forms of reuse from L083 in L079:
the characteristic-two exclusion, the subfield counting argument, and Table1.
The replacement graph has no dependency from A1 to A2; both use U_E.
