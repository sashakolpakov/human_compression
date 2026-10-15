Read("/Users/sasha/medusa/research/leemans/topic_D_L096_HS_extension/archive_data/inputs.g");;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L091_work/clean_run01/result.g");;
FindPairWitness:=function(G,AutG,p,q)
 local perm,target,places,cur,C,images,k,i,x,phi,good;
 for perm in SymmetricGroup(2) do
  target:=Permuted(q,perm);
  if List(p,Size)<>List(target,Size) then continue;fi;
  places:=[1,2];if Size(target[2])>Size(target[1]) then places:=[2,1];fi;
  cur:=ShallowCopy(p);C:=AutG;images:=ShallowCopy(GeneratorsOfGroup(G));good:=true;
  for k in [1..2] do
   i:=places[k];x:=RepresentativeAction(C,cur[i],target[i],function(H,a)return Image(a,H);end);
   if x=fail then good:=false;break;fi;
   cur:=List(cur,H->Image(x,H));images:=List(images,g->Image(x,g));
   if k=1 then C:=Stabilizer(C,target[i],function(H,a)return Image(a,H);end);fi;
  od;
  if good then
   phi:=GroupHomomorphismByImages(G,G,GeneratorsOfGroup(G),images);
   if phi=fail or not IsBijective(phi) or List(p,H->Image(phi,H))<>target then Error("Invalid explicit automorphism");fi;
   return rec(type_permutation:=perm,generator_images:=images);
  fi;
 od;
 return fail;
end;;
RunWitnesses:=function()
 local G,AutG,witnesses,cls,i,rep,p,q,w;
 G:=Group(Concatenation(L096Inputs[1].parabolic_generators));AutG:=AutomorphismGroup(G);witnesses:=[];
 for cls in HSRankTwoResult.classes do
  rep:=cls[1];q:=List([HSRankTwoResult.pairs[rep].A,HSRankTwoResult.pairs[rep].B],x->Subgroup(G,x));
  for i in cls do
   if i=rep then continue;fi;
   p:=List([HSRankTwoResult.pairs[i].A,HSRankTwoResult.pairs[i].B],x->Subgroup(G,x));
   w:=FindPairWitness(G,AutG,p,q);if w=fail then Error("Missing within-class witness");fi;
   w.source_pair:=i;w.target_pair:=rep;Add(witnesses,w);
   Print("VERIFIED_AUTOMORPHISM ",i," -> ",rep," TYPES ",w.type_permutation,"\n");
  od;
 od;
 PrintTo("/Users/sasha/medusa/research/leemans/reboot_20261013/L091_work/pair_witnesses.g","HSRankTwoWitnesses:=",witnesses,";;\n");
 Print("PASS_EXPLICIT_WITNESSES ",Length(witnesses),"\n");
end;;
RunWitnesses();
QUIT;
