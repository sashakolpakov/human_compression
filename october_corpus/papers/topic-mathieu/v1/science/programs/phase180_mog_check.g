# Check all compatible source Golay completions, not an assumed QR labelling.
# Set INPUT_FILE, WITNESS_FILE and OUTPUT_FILE before reading this program.
LoadPackage("design");;
SizeScreen([100000,24]);;
if not IsBound(INPUT_FILE) or not IsBound(WITNESS_FILE) or not IsBound(OUTPUT_FILE) then
 Error("three explicit file parameters required");
fi;
Read(INPUT_FILE);;
Read(WITNESS_FILE);;
Phase180Check:=function(test,msg) if not test then Error(msg);fi;end;;
Phase180Signature:=function(t)
 return [SortedList(List(t,Size)),SortedList(List(Combinations(t,2),p->Size(Intersection(p)))),Size(Intersection(t))];
end;;
Phase180Run:=function()
 local full, allM, AP, wsets, wsigs, tdesign, tgraph, c, sgraph, iso, p,
       case, pts, t, B, pairorders, res, helly, k, other, j, l, P, Q,
       one, two, flagtransitive, ids, tset, signature, i, first, maps,
       expectedOrders, actualSizes, memberships, sourceWords, sourceDodecads,
       octad, octad2;
 tdesign:=BlockDesign(24,targetBlocks);
 full:=AutGroupBlockDesign(tdesign);
 Phase180Check(Size(full)=244823040,"wrong full Steiner automorphism group");
 Phase180Check(Stabilizer(Stabilizer(full,targetFixed[1]),targetFixed[2])=G,"named M22 is not the pointwise two-point stabilizer");
 allM:=Concatenation(List(maximalClassRepresentatives,H->Orbit(G,H,OnPoints)));
 AP:=Action(A,allM,OnPoints);
 Phase180Check(Size(AP)=887040,"incomplete automorphism action");
 wsets:=List(M22Triples,t->Set(List(t,H->Position(allM,H))));
 wsigs:=List(M22Triples,Phase180Signature);
 tgraph:=IncidenceGraphSupportBlockDesign(tdesign);
 PrintTo(OUTPUT_FILE,"{\"status\":\"COMPLETE_EXACT_SOURCE_DIAGNOSTIC\",\"full_Steiner_automorphism_order\":",Size(full),",\"M22_order\":",Size(G),",\"completion_cases\":[\n");
 first:=true;maps:=[];
 for c in [1..Length(sourceCodeBlocks)] do
  sgraph:=IncidenceGraphSupportBlockDesign(BlockDesign(24,sourceCodeBlocks[c]));
  iso:=GraphIsomorphism(
   rec(graph:=sgraph,colourClasses:=[[24],[15],Difference([1..24],[24,15]),[25..783]]),
   rec(graph:=tgraph,colourClasses:=[[targetFixed[2]],[targetFixed[1]],Difference([1..24],targetFixed),[25..783]]));
  Phase180Check(iso<>fail,"source completion not isomorphic with distinguished points");
  p:=PermList(List([1..24],i->i^iso));
  Add(maps,p);
  Phase180Check(Set(List(sourceCodeBlocks[c],s->OnSets(s,p)))=Set(targetBlocks),"block isomorphism validation failed");
  for case in [1..Length(sourceTriples)] do
   pts:=List(sourceTriples[case],s->OnSets(Set(s),p));
   t:=List(pts,s->Stabilizer(G,s,OnSets));
   B:=Intersection(t);
   pairorders:=List([[1,2],[1,3],[2,3]],q->Size(Intersection(t[q[1]],t[q[2]])));
   res:=[];helly:=[];
   for k in [1..3] do
    other:=Difference([1..3],[k]);j:=other[1];l:=other[2];
    P:=Intersection(t[k],t[j]);Q:=Intersection(t[k],t[l]);
    Add(res,Size(Group(Concatenation(GeneratorsOfGroup(P),GeneratorsOfGroup(Q)))));
    one:=Set(List(RightTransversal(t[j],P),g->RightCoset(t[k],g)));
    two:=Set(List(RightTransversal(t[l],Q),g->RightCoset(t[k],g)));
    Add(helly,[Length(Intersection(one,two)),Index(Intersection(t[j],t[l]),B)]);
   od;
   flagtransitive:=ForAll(helly,x->x[1]=x[2]);
   ids:=[];
   if flagtransitive then
    tset:=Set(List(t,H->Position(allM,H)));
    Phase180Check(not fail in tset,"nonmaximal displayed object stabilizer");
    signature:=Phase180Signature(t);
    for i in [1..Length(M22Triples)] do
     if signature=wsigs[i] and RepresentativeAction(AP,tset,wsets[i],OnSets)<>fail then Add(ids,i);fi;
    od;
   fi;
   if not first then AppendTo(OUTPUT_FILE,",\n");fi;first:=false;
   AppendTo(OUTPUT_FILE,"{\"completion\":",c,",\"case\":",case,",\"label\":\"",sourceLabels[case],"\",\"point_map\":",List([1..24],i->i^p),",\"target_objects\":",pts,",\"stabilizer_orders\":",List(t,Size),",\"pair_orders\":",pairorders,",\"borel_id\":",IdGroup(B),",\"residue_generated_orders\":",res,",\"Helly_actual_expected\":",helly,",\"flag_transitive\":",flagtransitive,",\"census_witnesses\":",ids,"}");
   Print("SOURCE_COMPLETION ",c," CASE ",case," HELLY ",helly," WITNESSES ",ids,"\n");
  od;
 od;
 AppendTo(OUTPUT_FILE,"\n],\"explicit_pair_cases\":[\n");first:=true;
 expectedOrders:=[20160,5760,2520,2520,1344,1920,720,660];
 for c in [1..Length(sourceCodeBlocks)] do
  p:=maps[c];
  sourceWords:=[[]];
  # Binary span of the octads, represented as supports.
  for octad in sourceCodeBlocks[c] do
   if not octad in sourceWords then
    sourceWords:=Set(Concatenation(sourceWords,List(sourceWords,w->Union(Difference(w,octad),Difference(octad,w)))));
   fi;
  od;
  Phase180Check(Length(sourceWords)=4096,"source octad span size");
  sourceDodecads:=Filtered(sourceWords,w->Length(w)=12);
  for case in [1..Length(sourcePairs)] do
   pts:=List(sourcePairs[case],s->OnSets(Set(s),p));
   t:=List(pts,s->Stabilizer(G,s,OnSets));
   actualSizes:=List(t,Size);
   memberships:=[];
   for i in [1,2] do
    if sourcePairTypes[case][i]=8 then
     Add(memberships,Union(sourcePairs[case][i],[24]) in sourceDodecads);
    elif sourcePairTypes[case][i]=7 then
     Add(memberships,Set(sourcePairs[case][i]) in sourceDodecads);
    elif sourcePairTypes[case][i]=5 then
     Add(memberships,Set(sourcePairs[case][i]) in Set(sourceCodeBlocks[c]));
    else Add(memberships,true);fi;
   od;
   if not first then AppendTo(OUTPUT_FILE,",\n");fi;first:=false;
   AppendTo(OUTPUT_FILE,"{\"completion\":",c,",\"pair\":",case,",\"label\":\"",sourcePairLabels[case],"\",\"canonical_object_membership\":",memberships,",\"stabilizer_orders\":",actualSizes,",\"expected_stabilizer_orders\":",expectedOrders{sourcePairTypes[case]},",\"actual_intersection_size\":",Length(Intersection(sourcePairs[case])),",\"actual_pair_id\":",IdGroup(Intersection(t)),",\"printed_pair_order\":",sourcePairOrders[case],"}");
   if not ForAll(memberships,x->x) or actualSizes<>expectedOrders{sourcePairTypes[case]} or Size(Intersection(t))<>sourcePairOrders[case] then
    Print("SOURCE_PAIR_DISCREPANCY ",c," ",sourcePairLabels[case]," membership=",memberships," actual=",actualSizes," pair=",IdGroup(Intersection(t))," printed=",sourcePairOrders[case],"\n");
   fi;
  od;
 od;
 AppendTo(OUTPUT_FILE,"\n]}\n");
 Print("PHASE180_ALL_SOURCE_COMPLETIONS_CHECKED ",Length(sourceCodeBlocks),"\n");
end;;
Phase180Run();;
QUIT;
