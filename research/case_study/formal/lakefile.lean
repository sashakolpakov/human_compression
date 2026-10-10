import Lake
open Lake DSL

package math_compression_certificates

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @
  "905b95818eb32af7874a58b427f50c1711a5e96c"

@[default_target]
lean_lib MathCompressionCertificates where
  roots := #[`LiftCertificate, `FieldIntersection, `TransvectionIntersection,
    `ResidueConnectivity, `ChamberOrbit, `TorsorPartitions,
    `CoordinateKernels, `SuzukiPentagons, `StringIntersection, `BooleanShadow,
    `ConsecutiveShadow, `RankThreeFactorization, `CosetCoordinates,
    `IntertwinerSeparation, `TransvectionForms, `InvolutionCentralizers, `BinaryFrattiniActions, `MarkedSquareDescent,
    `GradedSupport, `BooleanRetractions, `PrincipalKernelIntersections, `NestedKernelIntersections,
    `Phase23TransferAnnihilator, `EndpointDoublingIntersections]
