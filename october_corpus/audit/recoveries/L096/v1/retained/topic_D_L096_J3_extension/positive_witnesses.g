Read("shadow_residues_sparse.g");;Read("inner_outer_direct.g");;Read("archive_data/inputs.g");;Read("intersection_profiles.g");;
G:=Group(Concatenation(L096Inputs[1].parabolic_generators));;ctx:=L096IOSetup(G);;deg:=LargestMovedPoint(G);;
Witness:=function(pair)
 local p,q,pp,qp,perm,target,indices,places,ai,alpha,cur,C,x,k,i,u,gens;
 p:=List(L096Inputs[pair[1]].parabolic_generators,Group);q:=List(L096Inputs[pair[2]].parabolic_generators,Group);pp:=L096Profiles[pair[1]];qp:=L096Profiles[pair[2]];
 for perm in SymmetricGroup(Length(p)) do
  target:=Permuted(q,perm);indices:=Permuted([1..Length(p)],perm);
  if not ForAll([1..Length(pp.keys)],j->pp.orders[j]=qp.orders[Position(qp.keys,Set(pp.keys[j],i->indices[i]))]) then continue;fi;
  places:=SortedList([1..Length(p)],function(i,j)if Size(target[i])=Size(target[j]) then return i<j;fi;return Size(target[i])>Size(target[j]);end);
  for ai in [1..Length(ctx.outer)] do
   alpha:=ctx.outer[ai];cur:=List(p,H->Image(alpha,H));C:=G;x:=fail;u:=One(G);
   for k in [1..Length(p)] do
    i:=places[k];x:=RepresentativeAction(C,cur[i],target[i]);if x=fail then break;fi;
    cur:=List(cur,H->H^x);u:=u*x;if k<Length(p) then C:=Normalizer(C,target[i]);fi;
   od;
   if x<>fail then
    if cur<>target or not ForAll([1..Length(p)],i->Image(alpha,p[i])^u=target[i]) then Error("explicit witness invalid");fi;
    gens:=GeneratorsOfGroup(G);
    return rec(pair:=pair,type_indices:=indices,outer_index:=ai,inner_conjugator:=ListPerm(u,deg),automorphism_generator_images:=List(gens,g->ListPerm(Image(alpha,g),deg)),ambient_generators:=List(gens,g->ListPerm(g,deg)));
   fi;
  od;
 od;Error("expected positive missing");
end;;
for pair in [[14,13],[17,16]] do Print("WITNESS|",L096JSON(Witness(pair)),"\n");od;
Print("PASS_J3_ACTUAL_POSITIVE_WITNESSES\n");QUIT;
