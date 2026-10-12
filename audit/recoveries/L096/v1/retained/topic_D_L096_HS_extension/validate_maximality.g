Read("actual_maximality.g");;
L096ValidateMaximality:=function()
 local groups,G,cl,H,C,phi,a,b,n,pos,neg,one,nf,k;
 groups:=[SymmetricGroup(3),SymmetricGroup(4),DihedralGroup(IsPermGroup,8),CyclicGroup(IsPermGroup,4),ElementaryAbelianGroup(IsPermGroup,4)];
 n:=0;pos:=0;neg:=0;one:=0;nf:=0;
 for G in groups do
  for cl in ConjugacyClassesSubgroups(G) do
   H:=Representative(cl);C:=RightCosets(G,H);phi:=ActionHomomorphism(G,C,OnRight);
   a:=Length(C)>=2 and IsPrimitive(Image(phi),[1..Length(C)]);b:=L096MaximalByDoubleCosets(G,H);
   if a<>b.value then Error("actual primitive action disagrees");fi;
   if IsBound(b.intermediate_generators) then
    k:=Group(List(b.intermediate_generators,PermList));
    if not IsSubgroup(G,k) or not IsSubgroup(k,H) or Size(k)<=Size(H) or Size(k)>=Size(G) then Error("intermediate witness");fi;
   fi;
   n:=n+1;if a then pos:=pos+1;else neg:=neg+1;fi;
   if H=G then one:=one+1;fi;
   if a and Size(Core(G,H))>1 then nf:=nf+1;fi;
  od;
 od;
 Print("VALIDATION|",L096JSON(rec(cases:=n,primitive:=pos,imprimitive:=neg,excluded_degree_one:=one,primitive_nonfaithful:=nf)),"\n");
end;;L096ValidateMaximality();Print("PASS_ACTUAL_MAXIMALITY_VALIDATION\n");QUIT;
