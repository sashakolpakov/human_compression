# Required fixed setup already loaded: G,reps, INPUT_ROWS=[id,done-path,levels,ranks].
# Reads only exact hash-bound completed anchors, not an augmentation engine.
RunPartialFusion:=function(G,reps,rows,out)
 local all,row,t,B,r,par,panels,i,j,A,ag,a,images,phi,rank,candidates,classes,orbits,
      members,w,hit,counts,representatives,comparisons,c,gs,autdata,logfile;
 all:=[];gs:=GeneratorsOfGroup(G);comparisons:=0;
 for row in rows do
  Read(row[2]);
  if borelResult.id<>row[1] or borelResult.order<>Size(reps[row[1]])
   or borelResult.levels<>row[3] or List(borelResult.geometries,Length)<>row[4] then
   Error("completed anchor does not match audited row");fi;
  B:=reps[row[1]];
  for i in [1..Length(borelResult.geometries)] do
   t:=borelResult.geometries[i];r:=Length(t);
   if r<2 then continue;fi;
   if not ForAll(t,H->IsSubgroup(G,H) and IsSubgroup(H,B))
    or Group(Concatenation(List(t,GeneratorsOfGroup)))<>G then Error("wrong panel family");fi;
   par:=List([1..r],j->Group(Concatenation(List(t{Difference([1..r],[j])},GeneratorsOfGroup))));
   if Intersection(par)<>B or ForAny(par,H->H=G) then Error("wrong parabolic/Borel reconstruction");fi;
   panels:=List([1..r],j->Intersection(par{Difference([1..r],[j])}));
   if panels<>t then Error("panel/parabolic inverse failure");fi;
   Add(all,rec(borel_id:=row[1],borel_order:=Size(B),source_index:=i,panels:=t,parabolics:=par));
  od;
 od;
 Print("PARTIAL_INPUT anchors=",List(rows,x->x[1])," rank_families=",Collected(List(all,e->Length(e.panels))),"\n");
 # This is the complete GAP algorithm, not a normalizer in the 21-point action.
 A:=AutomorphismGroup(G);ag:=GeneratorsOfGroup(A);
 images:=List(ag,a->List(gs,g->Image(a,g)));
 for i in [1..Length(ag)] do
  phi:=GroupHomomorphismByImages(G,G,gs,images[i]);
  if phi=fail or not IsBijective(phi) or not ForAll(gs,g->Image(phi,g)=Image(ag[i],g)) then
   Error("full-Aut generator serialization failure");fi;
 od;
 autdata:=rec(group_generators:=gs,automorphism_generator_images:=images,automorphism_order:=Size(A),
  completeness_premise:="GAP AutomorphismGroup on the exact fixed group; not inferred from saved witness maps");
 PrintTo(Concatenation(out,"/automorphisms.g"),"L100FullAutData:=",autdata,";\n");
 Print("FULL_AUT_SAVED order=",Size(A)," generators=",Length(ag),"\n");
 counts:=[];representatives:=[];members:=[];logfile:=Concatenation(out,"/witness_journal.g");
 PrintTo(logfile,"L100PositiveWitnesses:=[];\n");
 for rank in Set(List(all,e->Length(e.panels))) do
  candidates:=Filtered(all,e->Length(e.panels)=rank);classes:=[];orbits:=[];
  for i in [1..Length(candidates)] do
   hit:=fail;w:=fail;
   for j in [1..Length(classes)] do
    comparisons:=comparisons+1;
    w:=FindFamilyWitness(G,A,candidates[classes[j]].parabolics,candidates[i].parabolics);
    if w<>fail then hit:=j;break;fi;
   od;
   if hit=fail then
    Add(classes,i);Add(orbits,[i]);hit:=Length(classes);
    w:=rec(type_permutation:=(),generator_images:=ShallowCopy(gs));
   else Add(orbits[hit],i);fi;
   if not CheckFamilyWitness(G,candidates[classes[hit]].parabolics,candidates[i].parabolics,w) then
    Error("final member witness invalid");fi;
   c:=rec(rank:=rank,source:=[candidates[classes[hit]].borel_id,candidates[classes[hit]].source_index],
    target:=[candidates[i].borel_id,candidates[i].source_index],type_permutation:=w.type_permutation,
    generator_images:=w.generator_images);
   Add(members,c);AppendTo(logfile,"Add(L100PositiveWitnesses,",c,");\n");
  od;
  Add(counts,[rank,Length(candidates),Length(classes)]);Append(representatives,candidates{classes});
  Print("PARTIAL_FUSION rank=",rank," inputs=",Length(candidates)," classes=",Length(classes)," orbits=",orbits,"\n");
 od;
 PrintTo(Concatenation(out,"/result.g"),"L100PartialFusion:=",rec(input_rows:=rows,group_generators:=gs,
  counts:=counts,representatives:=representatives,members:=members,comparison_count:=comparisons,
  automorphism_order:=Size(A),scope:="specified group Aut/type classes of exactly the listed completed anchors; no bare incidence or full catalogue claim"),";\n");
 Print("PASS_PARTIAL_AUT_TYPE_FUSION anchors=",Length(rows)," inputs=",Length(all)," members=",Length(members)," comparisons=",comparisons,"\n");
end;
RunPartialFusion(G,reps,INPUT_ROWS,OUTPUT_DIR);;
