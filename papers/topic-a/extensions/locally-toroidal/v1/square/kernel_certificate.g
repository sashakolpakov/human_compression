Read("root_actions.g");
Check := function(b,s) if not b then Error(s);fi;end;
KernelCertificate := function(name,U,qg,rank,order)
 local Q,phi,K,P,T,rels,letters,pairs,r,indices;
 Q:=Group(qg);Check(Size(Q)=order,"point order");
 phi:=GroupHomomorphismByImages(U,Q,GeneratorsOfGroup(U),qg);
 Check(phi<>fail and IsSurjective(phi),"marked epimorphism");
 K:=Kernel(phi);Check(Index(U,K)=order,"kernel index");
 P:=Image(IsomorphismFpGroup(K));T:=SimplifiedFpGroup(P);
 Check(Length(GeneratorsOfGroup(T))=rank,"actual kernel rank");
 rels:=RelatorsOfFpGroup(T);pairs:=[];
 Check(Length(rels)=rank*(rank-1)/2,"all and only pair commutators");
 for r in rels do
  letters:=LetterRepAssocWord(r);indices:=Set(List(letters,AbsInt));
  Check(Length(letters)=4 and Length(indices)=2,"commutator word length");
  Check(Set(letters)=Set(Concatenation(indices,-indices)),"commutator signs");
  Check(AbsInt(letters[1])=AbsInt(letters[3]) and AbsInt(letters[2])=AbsInt(letters[4]),"alternating commutator");
  AddSet(pairs,indices);
 od;
 Check(pairs=Combinations([1..rank],2),"all kernel pairs");
 Print(name," INDEX ",order," ACTUAL_FREE_ABELIAN_RANK ",rank," RELATORS ",rels,"\n");
end;
Main := function()
 local F,a,b,c,d,U,rels,R,r,i,j,m,T;
 F:=FreeGroup("a","b","c","d");a:=F.1;b:=F.2;c:=F.3;d:=F.4;
 rels:=[a^2,b^2,c^2,d^2,(a*b)^3,(a*c)^2,(a*d)^6,(b*c)^6,(b*d)^2,(c*d)^3,
        (c*(d*a)^2)^2,(b*(a*d)^2*a)^2,(a*(b*c)^2*b)^2];
 U:=F/rels;KernelCertificate("SQUARE",U,List(tau,PermList),4,1152);
 R:=FreeGroup("r0","r1","r2","r3","r4");r:=GeneratorsOfGroup(R);
 rels:=List(r,x->x^2);
 for i in [1..5] do for j in [1..5] do if i<j then
  m:=2;if j=i+1 then m:=[3,3,4,3][i];fi;Add(rels,(r[i]*r[j])^m);
 fi;od;od;
 KernelCertificate("AMBIENT",R/rels,List(rho,PermList),4,1152);
 F:=FreeGroup("A","B","C");a:=F.1;b:=F.2;c:=F.3;
 rels:=[a^2,b^2,c^2,(a*b)^3,(b*c)^6,(a*c)^2];
 KernelCertificate("TRIANGLE",F/rels,List(tau{[4,3,2]},PermList),2,36);
 T:=F/Concatenation(rels,[(a*(b*c)^2)^2]);Check(Size(T)=36,"ordered torus11");
 T:=F/Concatenation(rels,[(a*(b*c)^2*b)^2]);Check(Size(T)=48,"ordered torus20");
 Print("PASS_ALL_THREE_ACTUAL_KERNELS_AND_TWO_FINITE_TORI\n");
end;
Main();
QUIT_GAP(0);
