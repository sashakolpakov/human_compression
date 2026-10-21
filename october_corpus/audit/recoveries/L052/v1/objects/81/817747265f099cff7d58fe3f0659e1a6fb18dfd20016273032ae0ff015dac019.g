# Exact C+ presentation / coset-geometry certificate. Input L003Input supplied by runner.
# No assumed source order is assigned to a GAP group.
Need:=function(b) if not b then Error("certificate condition failed");fi;end;;
SizeScreen([100000,100000]);;
CosetTableDefaultMaxLimit:=L003Input.coset_limit;;
L003Stage:=function(s) Print("STAGE ",s,"\n");end;;
L003Meet:=function(m,n)
 return Sum(Filtered([0..3],k->QuoInt(m,2^k) mod 2=1 and QuoInt(n,2^k) mod 2=1),k->2^k);
end;;
L003InProduct:=function(g,H,K)
 return ForAny(Elements(H),h->h^-1*g in K);
end;;
L003FlagChecks:=function(pars,chamber_count)
 local ans,i,J,trs,c,B,want;
 ans:=[];
 for i in [1..4] do
  for J in Filtered(Combinations(Difference([1..4],[i])),j->Length(j)>=2) do
   trs:=RightTransversal(pars[J[1]],Intersection(pars[i],pars[J[1]]));
   c:=Number(trs,g->ForAll(J,j->L003InProduct(g,pars[i],pars[j])));
   B:=Intersection(List(J,j->pars[j]));
   want:=Index(B,Intersection(B,pars[i]));
   if Length(J)=3 then want:=chamber_count;fi;
   if c<>want then Print("FLAG_FAILURE ",[i,J,c,want],"\n");fi;
   Need(c=want);Add(ans,[i,J,c,want]);
  od;
 od;
 return ans;
end;;
L003Stage("presentation");;
F:=FreeGroup("x","y","z");;x:=F.1;;y:=F.2;;z:=F.3;;
pres:=rec(free:=F,relators:=[x^6,y^2,z^2,(x^-1*z)^2,(y^-1*z)^L003Input.p,(x^-1*y)^3,((x^-1*y)*x^-2)^L003Input.a*((y^-1*x)*x^2)^L003Input.b]);;
P:=pres.free/pres.relators;;
iso:=IsomorphismPermGroup(P);;Need(iso<>fail and IsBijective(iso));;
G:=Image(iso);;gg:=List(GeneratorsOfGroup(P),g->Image(iso,g));;
Print("ROTATION_ORDER ",Size(G),"\nPERMUTATION_DEGREE ",LargestMovedPoint(G),"\n");;
Print("SOURCE_ROTATION_ORDER_MATCH ",Size(G)=L003Input.expected_rotation_order,"\n");;Need(Size(G)=L003Input.expected_rotation_order);;
Need(ForAll(pres.relators,w->MappedWord(w,GeneratorsOfGroup(pres.free),gg)=One(G)));;
L003Stage("ICplus");;
a:=Concatenation([One(G)],gg);;subs:=[];;
for m in [0..15] do
 I:=Filtered([1..4],i->QuoInt(m,2^(i-1)) mod 2=1);;
 Add(subs,Group(List(Combinations(I,2),ij->a[ij[1]]^-1*a[ij[2]]),One(G)));
od;
for m in [0..15] do for n in [0..15] do
 Need(Intersection(subs[m+1],subs[n+1])=subs[L003Meet(m,n)+1]);
od;od;
Print("ICPLUS_SUBGROUP_ORDERS ",List(subs,Size),"\nICPLUS_PAIRS 256\n");;
pars:=List([14,13,11,7],m->subs[m+1]);;
Print("ROTATION_PARABOLIC_ORDERS ",List(pars,Size),"\nPAIR_ORDERS ",List(Combinations([1..4],2),ij->Order(a[ij[1]]^-1*a[ij[2]])),"\n");;
L003Stage("marked_local_presentations");;
LF:=FreeGroup("u","v");;u:=LF.1;;v:=LF.2;;
localpres:=LF/[u^6,v^3,(u*v)^2,(v*u^-2)^L003Input.a*(v^-1*u^2)^L003Input.b];;
localiso:=IsomorphismPermGroup(localpres);;Need(localiso<>fail and IsBijective(localiso));;
localmap:=GroupHomomorphismByImages(localpres,pars[4],GeneratorsOfGroup(localpres),[gg[1],gg[1]^-1*gg[2]]);;
Need(localmap<>fail and IsSurjective(localmap) and Size(Image(localiso))=Size(pars[4]));;
Need(Size(pars[4])=6*(L003Input.a^2+L003Input.a*L003Input.b+L003Input.b^2));;
localpres:=LF/[u^3,v^L003Input.p,(u*v)^2];;
localiso:=IsomorphismPermGroup(localpres);;Need(localiso<>fail and IsBijective(localiso));;
localmap:=GroupHomomorphismByImages(localpres,pars[1],GeneratorsOfGroup(localpres),[gg[1]^-1*gg[2],gg[2]^-1*gg[3]]);;
Need(localmap<>fail and IsSurjective(localmap) and Size(Image(localiso))=Size(pars[1]));;
Print("MARKED_LOCAL_PRESENTATIONS ",[Size(pars[4]),Size(pars[1])],"\n");;
L003Stage("rotation_flags");;
flags:=L003FlagChecks(pars,2);;Print("ROTATION_FLAGS ",flags,"\n");;
Need(Group(Concatenation(List(pars,GeneratorsOfGroup)),One(G))=G);;
for i in [1..4] do
 Need(Group(Concatenation(List(Difference([1..4],[i]),j->GeneratorsOfGroup(Intersection(pars[i],pars[j])))),One(G))=pars[i]);
od;
residues:=[];;
for I in Combinations([1..4],2) do
 K:=Intersection(List(I,i->pars[i]));;elts:=Elements(K);;m:=Length(elts);;J:=Difference([1..4],I);;
 adj:=List([1..2*m],i->[]);;
 for h in [1..m] do for k in [1..m] do
  if L003InProduct(elts[h]*elts[k]^-1,pars[J[1]],pars[J[2]]) then Add(adj[h],m+k);Add(adj[m+k],h);fi;
 od;od;
 seen:=[1];;for h in seen do for k in adj[h] do if not k in seen then Add(seen,k);fi;od;od;
 Need(Length(seen)=2*m);;Add(residues,[I,m,Length(seen),List(adj,Length)]);
od;
Print("RANK2_RESIDUES ",residues,"\nRANK3_GENERATION 4\n");;
L003Stage("inversion");;
failed:=Filtered([1..Length(pres.relators)],i->MappedWord(pres.relators[i],GeneratorsOfGroup(pres.free),List(gg,Inverse))<>One(G));;
Print("INVERTED_RELATOR_FAILURES ",failed,"\n");;
Print("SOURCE_REGULARITY_MATCH ",L003Input.regular=(Length(failed)=0),"\n");;Need(L003Input.regular=(Length(failed)=0));;
if Length(failed)=0 then
 Need(Length(failed)=0);;
 aut:=GroupHomomorphismByImages(G,G,gg,List(gg,Inverse));;
 Need(aut<>fail and IsBijective(aut) and aut^2=IdentityMapping(G));;
 L003Stage("regular_completion");;
 # Faithful degree 2d action: g maps to diag(g,aut(g)), t interchanges copies.
 deg:=LargestMovedPoint(G);;
 diag:=g->PermList(Concatenation(List([1..deg],i->i^g),List([1..deg],i->deg+i^Image(aut,g))));;
 t:=PermList(Concatenation([deg+1..2*deg],[1..deg]));;
 rr:=Concatenation([t],List(gg,g->t*diag(g)));;H:=Group(rr);;
 Need(ForAll(rr,r->Order(r)=2) and Size(H)=2*Size(G));;
 hsubs:=List([0..15],m->Group(List(Filtered([1..4],i->QuoInt(m,2^(i-1)) mod 2=1),i->rr[i]),One(H)));;
 for m in [0..15] do for n in [0..15] do
  Need(Intersection(hsubs[m+1],hsubs[n+1])=hsubs[L003Meet(m,n)+1]);
 od;od;
 hpars:=List([14,13,11,7],m->hsubs[m+1]);;
 hflags:=L003FlagChecks(hpars,2);;
 Print("FULL_ORDER ",Size(H),"\nFULL_PARABOLIC_ORDERS ",List(hpars,Size),"\nFULL_IP_PAIRS 256\nFULL_FLAGS ",hflags,"\n");;
else
 Need(Length(failed)>0);;H:=G;;
 Print("FULL_ORDER ",Size(G),"\nCHIRALITY_WITNESS_RELATOR ",failed[1],"\n");;
fi;
# All presentation/parabolic generators retained as concrete permutations for independent inspection.
Print("ROTATION_GENERATORS ",List(gg,g->List([1..LargestMovedPoint(G)],i->i^g)),"\n");;Print("FULL_GENERATORS ",List(GeneratorsOfGroup(H),g->List([1..LargestMovedPoint(H)],i->i^g)),"\n");;
Print("LITERAL_RELATORS ",pres.relators,"\n");;
Print("PASS_L052_ROW ",L003Input.id,"\n");;
QUIT;
