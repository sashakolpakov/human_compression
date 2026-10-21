"""Exclusive semantic cuts in the exact accepted calibrated PDF extraction.

Line numbers are extraction coordinates, not source theorem numbers. Repeated
printed statements retain every occurrence. Shared interfaces unite owner IDs;
they never duplicate a passage's cost. Historical ownership is documentary and
does not endorse an overbroad or corrected printed assertion.
"""
F='front_matter'; C='context'; D='definitions'; R='retained_statement'
N='named_statement_and_proof'; P='unnumbered_proof'; S='statement'
REF='references'; Q='qualified_or_excluded_assertion'; DATA='presentation_or_table_data'

def boundaries():
 return {
 'U_D':[(1,'UD.front',F),(10,'UD.intro',C),(28,'UD.Conventions',D),
 ((38,'The applications'),'UD.PolytopeInterface',R),(43,'UD.actions_heading',C),
 (46,'UD.OrbitData.statement',S),(53,'UD.Centralizer.statement',S),(57,'UD.Normalizer.statement',S),
 (60,'UD.OrbitData.proof',P),(63,'UD.Centralizer.proof',P),(70,'UD.Normalizer.proof',P),
 (80,'UD.ExtensionOrbits',N),(90,'UD.support_heading',C),(92,'UD.SupportSetup',D),
 (98,'UD.AdmissibleExtensions',N),(124,'UD.ExactSupport',N),(133,'UD.Reversal',P),
 (136,'UD.OddOrbits',N),(140,'UD.FieldSupport',P),(150,'UD.coset_heading',C),
 (152,'UD.HellySetup',D),(157,'UD.Helly',N),(168,'UD.realization_heading',C),
 (169,'UD.CosetRealization',N),(185,'UD.PanelSetup',D),(188,'UD.PanelRecognition',N),
 (207,'UD.LocalTests',P),(219,'UD.augmentation_heading',C),(220,'UD.Transport',N),
 (229,'UD.AugmentationSetup',D),(234,'UD.MaximalAugmentation',N),(247,'UD.Termination',P),
 (252,'UD.attribution',C)],
 'D1':[(1,'D1.front',F),(9,'D1.intro',C),(18,'D1.multiplicity_heading',C),
 (19,'D1.Multiplicities',P),(32,'D1.Centralizers',P),(39,'D1.formula_heading',C),
 (41,'D1.Ordered',P),((62,'Swapping'),'D1.Reversal',P),
 ((77,'The order-two case'),'D1.Symmetric',P),(91,'D1.EvenOrdered',P),
 (112,'D1.Alternating',P),(128,'D1.ordinary_automorphisms',R),
 ((131,'All nontrivial'),'D1.DegreeParity',P),(134,'D1.Series',P),
 (154,'D1.exceptional_heading',C),(155,'D1.Exceptional.method',P),
 (171,'D1.Exceptional.table',DATA),(179,'D1.Polyhedra.representatives',DATA),
 (182,'D1.Exceptional.endpoints',DATA),(192,'D1.Exceptional.conclusions',P),
 (197,'D1.Exceptional.exhaustion',P),(205,'D1.table_heading',C),
 (206,'D1.Table',DATA),(231,'D1.Qualifications',Q),(241,'D1.verification_context',C),
 (253,'D1.references',REF)],
 'D2':[(1,'D2.front',F),(9,'D2.intro',C),(20,'D2.RetainedBoundary.structure',R),
 (63,'D2.Normalization',N),(81,'D2.generation_heading',C),
 (82,'D2.SubfieldPosition',N),(93,'D2.Generation',N),(103,'D2.intersection_heading',C),
 (104,'D2.IP',P),(119,'D2.Rank',P),(128,'D2.counting_heading',C),
 (129,'D2.Support',P),(139,'D2.Pairs',P),(154,'D2.Polyhedra.setup',D),
 (157,'D2.Duality',P),(161,'D2.Polyhedra.formula',P),
 ((167,'For prime'),'D2.PrimeExamples.prime',P),(169,'D2.fiber_heading',C),
 (170,'D2.Fibers',P),(189,'D2.Nested',P),(200,'D2.inventory_heading',C),
 (201,'D2.source_inventory',C),((204,'Remark 1'),'D2.PrimeExamples.examples',P),
 (209,'D2.RetainedBoundary.attribution',C),((211,'Source Lemma 1'),'D2.FrobeniusRoot',P),
 ((213,'The finite'),'D2.RetainedBoundary.general',Q),
 ((218,'Lemma 5’s involution count'),'D2.InvolutionCount',P),
 ((220,'Lemma 6'),'D2.RetainedBoundary.classical',R),(224,'D2.verification_context',C),
 (229,'D2.references',REF)],
 'D3':[(1,'D3.front',F),(11,'D3.intro',C),(14,'D3.axioms',D),(21,'D3.method_context',C),
 (26,'D3.census_heading',C),(27,'D3.Interfaces.catalogue',R),
 ((29,'The complete search'),'D3.Candidates',P),(32,'D3.census_table',DATA),
 (39,'D3.Fusion',P),((40,'All 30'),'D3.Verified',P),(47,'D3.census_statement',S),
 (50,'D3.census_proof',P),(54,'D3.interface_heading',C),(55,'D3.Interfaces.actions',P),
 (61,'D3.Faithfulness',P),(64,'D3.program_boundary',P),(74,'D3.exclusion_heading',C),
 (75,'D3.Exclusions',Q),(80,'D3.references',REF)],
 'L066':[(1,'h.L066.front',F),(10,'h.L066.intro',C),(28,'h.L066.1.statement',S),
 (67,'h.L066.2.statement',S),(123,'h.L066.14',DATA),(143,'h.L066.organization',C),
 (149,'h.L066.definitions',D),(167,'h.L066.polytope_correspondence',R),
 (173,'h.L066.centralizer_context',C),(178,'h.L066.3',R),(182,'h.L066.16',P),
 (186,'h.L066.ordered_setup',D),(201,'h.L066.4',N),(267,'h.L066.reversal_setup',D),
 (273,'h.L066.5',Q),(324,'h.L066.averaging_setup',D),(332,'h.L066.6',Q),
 (337,'h.L066.diagonal',P),(430,'h.L066.1.proof',P),(436,'h.L066.15',DATA),
 (448,'h.L066.7',D),(456,'h.L066.8',N),(466,'h.L066.9',R),
 (468,'h.L066.alternating_context',C),(474,'h.L066.10',N),
 (484,'h.L066.even_setup',D),(496,'h.L066.11',N),(534,'h.L066.2.proof',P),
 (538,'h.L066.12',N),(546,'h.L066.13',N),(555,'h.L066.acknowledgments',C),
 (558,'h.L066.references',REF),(589,'h.L066.addresses',C)],
 'L074':[(1,'h.L074.front',F),(16,'h.L074.intro',C),(35,'h.L074.1.statement',S),
 (50,'h.L074.main_heading',C),(51,'h.L074.2.statement',S),(79,'h.L074.context',C),
 (88,'h.L074.acknowledgments',C),(93,'h.L074.coordinates.first',D),(112,'h.L074.5',R),
 (117,'h.L074.structure_context',C),(122,'h.L074.17.ovoid',D),
 (128,'h.L074.coordinates.second',D),(138,'h.L074.16.table',DATA),(152,'h.L074.6',R),
 (159,'h.L074.ovoid_setup',D),(163,'h.L074.7',R),(165,'h.L074.coprime_setup',D),
 (169,'h.L074.8',R),(170,'h.L074.16.context',R),(177,'h.L074.marking',D),
 (188,'h.L074.rank_heading',C),(190,'h.L074.3',R),(198,'h.L074.counting_setup',D),
 (209,'h.L074.first_step',C),(211,'h.L074.9',N),(216,'h.L074.normalization',P),
 (240,'h.L074.prime_pair_count',P),(246,'h.L074.10',R),(247,'h.L074.prime_pair_count',P),
 (252,'h.L074.middle',P),(266,'h.L074.prime_triples',P),(270,'h.L074.duality',P),
 ((275,'All these triples'),'h.L074.IP.prime',P),(279,'h.L074.4.statement',S),
 (283,'h.L074.composite_setup',D),(293,'h.L074.11',R),(317,'h.L074.12',N),
 (336,'h.L074.1.proof',P),(349,'h.L074.fiber_setup',D),(354,'h.L074.15.first_example',P),
 (366,'h.L074.fiber_setup',D),(377,'h.L074.13',N),(435,'h.L074.Q',P),
 ((449,'However'),'h.L074.subfields.setup',P),(454,'h.L074.15.second_example',P),
 (473,'h.L074.17.orbit_definition',D),(481,'h.L074.15.second_example',P),
 (495,'h.L074.subfields.context',C),(499,'h.L074.14',S),(508,'h.L074.4.remark',P),
 (510,'h.L074.subfields.inversion',P),((564,'They all satisfy'),'h.L074.IP.final',P),
 (567,'h.L074.references',REF)],
 'L104':[(1,'h.L104.front',F),(15,'h.L104.intro_heading',C),(16,'h.L104.oldsearch',P),
 (25,'h.L104.organization',C),(31,'h.L104.axioms',D),(60,'h.L104.extension',P),
 (67,'h.L104.ranktest',P),(73,'h.L104.census_heading',C),(74,'h.L104.census',S),
 (80,'h.L104.4',Q),(172,'h.L104.supplement',Q),(180,'h.L104.references',REF)],
 'CODE':[(1,'CODE.wrapper',C),(9,'program.exceptional.printed',DATA),
 (110,'diagnostic.pairs.printed',DATA),(216,'diagnostic.fields.printed',DATA),
 (371,'diagnostic.q8.printed',DATA),(423,'program.search.printed',DATA),
 (638,'program.fusion.printed',DATA),(698,'program.verify.printed',DATA),
 (722,'program.predicates.printed',DATA)]}

def supplements():
 s={
 'UD.AdmissibleExtensions':['UD.SupportSetup'], 'UD.ExactSupport':['UD.SupportSetup'],
 'UD.Helly':['UD.HellySetup'], 'UD.PanelRecognition':['UD.PanelSetup'],
 'UD.MaximalAugmentation':['UD.AugmentationSetup'],
 'D1.Symmetric':['D1.ordinary_automorphisms'], 'D1.Alternating':['D1.ordinary_automorphisms'],
 'D1.Polyhedra':['D1.Exceptional.method','D1.Exceptional.table','D1.Exceptional.endpoints','D1.Exceptional.conclusions','D1.Exceptional.exhaustion'],
 'D3.Interfaces':['D3.axioms','D3.program_boundary'],
 'D3.NoHigher':['D3.census_statement','D3.census_proof','D3.census_table','D3.program_boundary'],
 'h.L066.4':['h.L066.ordered_setup'], 'h.L066.5':['h.L066.reversal_setup'],
 'h.L066.diagonal':['h.L066.averaging_setup'], 'h.L066.7':['h.L066.definitions','h.L066.polytope_correspondence'],
 'h.L066.11':['h.L066.even_setup'],
 'h.L074.1':['h.L074.prime_pair_count'], 'h.L074.2':['h.L074.prime_triples','h.L074.subfields.inversion'],
 'h.L074.4':['h.L074.prime_triples'], 'h.L074.7':['h.L074.ovoid_setup'],
 'h.L074.8':['h.L074.coprime_setup'], 'h.L074.13':['h.L074.fiber_setup'],
 'h.L074.normalization':['h.L074.counting_setup','h.L074.marking'],
 'h.L074.IP':['h.L074.marking']}
 for n in ['D3.Candidates','D3.Fusion','D3.Verified']:
  s[n]=['D3.census_statement','D3.census_proof','D3.census_table']
 for n in ['h.L104.1','h.L104.2','h.L104.3']:s[n]=['h.L104.census']
 s['h.L104.3'].append('h.L104.supplement')
 for n in ['program.exceptional','diagnostic.pairs','diagnostic.fields','diagnostic.q8','program.search','program.fusion','program.verify','program.predicates']:
  s[n]=['CODE.wrapper',n+'.printed']
 return s
