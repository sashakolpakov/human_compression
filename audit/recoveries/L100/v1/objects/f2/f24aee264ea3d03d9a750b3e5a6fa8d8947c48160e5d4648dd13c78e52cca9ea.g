# Positive-certificate companion to the byte-identical legacy Boolean test.
# Sequential images avoid relying on an implicit automorphism multiplication convention.
FindFamilyWitness:=function(G,A,p,q)
 local perm,ord,cur,C,x,i,images,phi,good;
 if Length(p)<>Length(q) or Signature(p)<>Signature(q) then return fail;fi;
 for perm in SymmetricGroup(Length(p)) do
  ord:=Permuted(q,perm);
  if List(p,Size)<>List(ord,Size) then continue;fi;
  cur:=ShallowCopy(p);C:=A;images:=ShallowCopy(GeneratorsOfGroup(G));good:=true;
  for i in [1..Length(p)] do
   x:=RepresentativeAction(C,cur[i],ord[i],AutoSub);
   if x=fail then good:=false;break;fi;
   cur:=List(cur,H->Image(x,H));images:=List(images,g->Image(x,g));
   C:=Stabilizer(C,ord[i],AutoSub);
  od;
  if good then
   phi:=GroupHomomorphismByImages(G,G,GeneratorsOfGroup(G),images);
   if phi=fail or not IsBijective(phi) or List(p,H->Image(phi,H))<>ord then
    Error("invalid simultaneous family witness");fi;
   return rec(type_permutation:=perm,generator_images:=images);
  fi;
 od;
 return fail;
end;
CheckFamilyWitness:=function(G,p,q,w)
 local phi;
 if not IsRecord(w) or not IsBound(w.type_permutation) or not IsBound(w.generator_images)
  or not w.type_permutation in SymmetricGroup(Length(p)) then return false;fi;
 phi:=GroupHomomorphismByImages(G,G,GeneratorsOfGroup(G),w.generator_images);
 return phi<>fail and IsBijective(phi) and List(p,H->Image(phi,H))=Permuted(q,w.type_permutation);
end;
