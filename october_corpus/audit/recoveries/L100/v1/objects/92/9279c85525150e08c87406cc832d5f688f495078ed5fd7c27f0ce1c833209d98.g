# Prior complete Aut computation and prior class partition are acquired, not rerun.
RunIncrementalFusion:=function(G,reps,old,autdata,row,out)
 local gs,autgens,images,phi,A,allNew,B,t,r,par,panels,i,j,c,oldIds,newIds,
      allReps,members,newMembers,rank,candidates,classes,w,hit,counts,comparisons,oldCount,nice;
 gs:=GeneratorsOfGroup(G);
 if old.group_generators<>gs or autdata.group_generators<>gs or old.automorphism_order<>autdata.automorphism_order then
  Error("saved full-Aut/fusion model mismatch");fi;
 Print("FIXED_ACQUIRED_MODEL_CONFIRMED\n");
 autgens:=[];
 for images in autdata.automorphism_generator_images do
  Print("MAP_BEGIN ",Length(autgens)+1,"\n");
  phi:=GroupHomomorphismByImages(G,G,gs,images);
  if phi=fail or not IsBijective(phi) then Error("invalid saved automorphism");fi;
  Add(autgens,phi);Print("MAP_VERIFIED ",Length(autgens),"\n");
 od;
 A:=Group(autgens);Print("GENERATOR_GROUP_CONSTRUCTED\n");
 if not IsGroupOfAutomorphismsFiniteGroup(A) then Error("saved automorphism group property");fi;
 # The exact generating maps define the same acquired complete group.
 # Caching its acquired size is not an independent order computation.
 SetSize(A,autdata.automorphism_order);
 Print("EXACT_ACQUIRED_ORDER_SET ",Size(A),"\n");
 nice:=NiceMonomorphism(A);
 PrintTo(Concatenation(out,"/aut_action.g"),"L100ReusedAutAction:=",rec(
  order:=Size(A),degree:=LargestMovedPoint(Image(nice)),
  images:=List(autgens,a->Image(nice,a)),generator_images:=autdata.automorphism_generator_images,
  injectivity_premise:="Retained GAP NiceMonomorphism algorithm; not inferred from cached order"),";\n");
 Print("REUSED_FULL_AUT order=",Size(A)," generators=",Length(autgens),"\n");
 Read(row[2]);
 if borelResult.id<>row[1] or borelResult.order<>Size(reps[row[1]]) or borelResult.levels<>row[3]
  or List(borelResult.geometries,Length)<>row[4] then Error("new done/receipt mismatch");fi;
 B:=reps[row[1]];allNew:=[];
 for i in [1..Length(borelResult.geometries)] do
  t:=borelResult.geometries[i];r:=Length(t);if r<2 then continue;fi;
  if not ForAll(t,H->IsSubgroup(G,H) and IsSubgroup(H,B)) or Group(Concatenation(List(t,GeneratorsOfGroup)))<>G then Error("new panel family");fi;
  par:=List([1..r],j->Group(Concatenation(List(t{Difference([1..r],[j])},GeneratorsOfGroup))));
  if Intersection(par)<>B or ForAny(par,H->H=G) then Error("new parabolic reconstruction");fi;
  panels:=List([1..r],j->Intersection(par{Difference([1..r],[j])}));if panels<>t then Error("new panel inverse");fi;
  Add(allNew,rec(borel_id:=row[1],borel_order:=Size(B),source_index:=i,panels:=t,parabolics:=par));
 od;
 oldIds:=List(old.members,e->e.target);newIds:=List(allNew,e->[e.borel_id,e.source_index]);
 if Length(Set(oldIds))<>Length(oldIds) or Length(Set(newIds))<>Length(newIds) or Intersection(oldIds,newIds)<>[] then Error("duplicate member identities");fi;
 allReps:=ShallowCopy(old.representatives);members:=ShallowCopy(old.members);newMembers:=[];comparisons:=0;
 PrintTo(Concatenation(out,"/new_witnesses.g"),"L100NewWitnesses:=[];\n");
 for rank in Set(List(allNew,e->Length(e.panels))) do
  candidates:=Filtered(allNew,e->Length(e.panels)=rank);classes:=Filtered(allReps,e->Length(e.panels)=rank);
  for c in candidates do
   hit:=fail;w:=fail;
   for j in [1..Length(classes)] do
    comparisons:=comparisons+1;w:=FindFamilyWitness(G,A,classes[j].parabolics,c.parabolics);
    if w<>fail then hit:=j;break;fi;
   od;
   if hit=fail then
    Add(classes,c);Add(allReps,c);hit:=Length(classes);w:=rec(type_permutation:=(),generator_images:=ShallowCopy(gs));
   fi;
   if not CheckFamilyWitness(G,classes[hit].parabolics,c.parabolics,w) then Error("new positive witness invalid");fi;
   t:=rec(rank:=rank,source:=[classes[hit].borel_id,classes[hit].source_index],target:=[c.borel_id,c.source_index],
    type_permutation:=w.type_permutation,generator_images:=w.generator_images);
   Add(newMembers,t);Add(members,t);AppendTo(Concatenation(out,"/new_witnesses.g"),"Add(L100NewWitnesses,",t,");\n");
  od;
 od;
 counts:=[];
 for rank in Set(Concatenation(List(old.counts,e->e[1]),List(allNew,e->Length(e.panels)))) do
  oldCount:=First(old.counts,e->e[1]=rank);if oldCount=fail then oldCount:=0;else oldCount:=oldCount[2];fi;
  Add(counts,[rank,oldCount+Number(allNew,e->Length(e.panels)=rank),Number(allReps,e->Length(e.panels)=rank)]);
 od;
 if Length(members)<>Length(old.members)+Length(allNew) then Error("complete member accumulation");fi;
 PrintTo(Concatenation(out,"/result.g"),"L100CompleteAutFusion:=",rec(group_generators:=gs,
  input_rows:=Concatenation(old.input_rows,[row]),counts:=counts,representatives:=allReps,members:=members,
  automorphism_order:=Size(A),new_comparison_count:=comparisons,new_members:=newMembers,
  old_members_preserved:=true,scope:="Specified-G Aut/type fusion of exactly the acquired old and new complete anchors; bare incidence/source joins remain separate"),";\n");
 Print("PASS_INCREMENTAL_AUT_TYPE_FUSION old_members=",Length(old.members)," new_members=",Length(newMembers)," total_members=",Length(members)," counts=",counts," comparisons=",comparisons,"\n");
end;
