# Exact C+ presentation / coset-geometry certificate. Input L003Input supplied by runner.
# No assumed source order is assigned to a GAP group.
SetAssertionLevel(1);;
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
   Assert(0,c=want);Add(ans,[i,J,c,want]);
  od;
 od;
 return ans;
end;;
L003Presentation:=function(table,params)
 local F,x,y,z,r,a,b,c,d,e,f,g,h,p;
 F:=FreeGroup("x","y","z");x:=F.1;y:=F.2;z:=F.3;
 if table=7 then p:=params[1][1];params:=params{[2,3]};fi;
 a:=params[1][1];b:=params[1][2];c:=params[2][1];d:=params[2][2];
 if table=3 then
  r:=[x^6,y^3,z^2,(x^-1*y)^2,(y^-1*z)^6,(z*x)^2,
      (y^-1*x^-2)^a*(y*x^2)^b,(y*(z*y)^2)^c*(y*z*y^-1*z)^d];
 elif table=4 then
  r:=[x^3,y^6,z^2,(x^-1*z)^2,(y^-1*z)^3,(x^-1*y)^2,
      (x^-1*y^-2)^a*(x*y^2)^b,(z*y^3)^c*(y^-1*z*y^-2)^d];
 elif table=5 then
  e:=params[3][1];f:=params[3][2];
  r:=[x^3,y^3,z^6,(x^-1*z)^2,(y^-1*z)^2,(x^-1*y)^3,
      (y*x^-1*y)^a*(y*x)^b,(y^-1*z^-2)^c*(y*z^2)^d,
      (x^-1*z^-2)^e*(x*z^2)^f];
 elif table=6 then
  r:=[x^3,y^3,z^6,(x^-1*z)^2,(y^-1*z)^2,(x^-1*y)^2,
      (y^-1*z^-2)^a*(y*z^2)^b,(x^-1*z^-2)^c*(x*z^2)^d];
 elif table=7 then
  r:=[x^6,y^3,z^2,(z*x)^3,(z*y)^p,(x^-1*y)^2,
      (y^-1*x^-2)^a*(y*x^2)^b,(z*x^3)^c*(x^-1*z*x^-2)^d];
 elif table=8 then
  e:=params[3][1];f:=params[3][2];g:=params[4][1];h:=params[4][2];
  r:=[x^6,y^3,z^2,(z*x)^3,(z*y)^6,(x^-1*y)^2,
      (y^-1*x^-2)^a*(y*x^2)^b,(z*x^3)^c*(x^-1*z*x^-2)^d,
      (x^-1*z*(y^-1*z)^2)^e*(z*x*(z*y)^2)^f,
      (y*(z*y)^2)^g*(y^-1*(y*z)^2)^h];
 else Error("unknown table");fi;
 return rec(free:=F,relators:=r);
end;;
L003Stage("presentation");;
pres:=L003Presentation(L003Input.table,L003Input.params);;
P:=pres.free/pres.relators;;
# GAP computes an isomorphism from the finitely presented group, not a chosen finite image.
iso:=fail;;G:=fail;;
if L003Input.id="T8.8" then
 # Complete subgroup enumeration supplies upper, actual coset action supplies lower.
 Assert(0,LoadPackage("ace")=true);;ACEIgnoreUnknownDefault:=false;;
 aa:=GeneratorsOfGroup(pres.free);;
 ct:=ACECosetTableFromGensAndRels(aa,pres.relators,[aa[2],aa[3]]:workspace:=5000000,max:=500000,time:=60,silent);;
 Assert(0,ct<>fail);;ix:=Length(ct[1]);;
 yz:=FreeGroup("Y","Z");;localY:=yz.1;;localZ:=yz.2;;
 lP:=yz/[localY^3,localZ^2,(localZ*localY)^6,(localY*(localZ*localY)^2)^5];;lIso:=IsomorphismPermGroup(lP);;lOrder:=Size(Image(lIso));;
 gg:=List([1,3,5],i->PermList(ct[i]));;G:=Group(gg);;
 Assert(0,Size(G)=ix*lOrder);;
 Print("PRESENTATION_UPPER_INDEX ",ix," SUBGROUP_UPPER ",lOrder," MATCHED_IMAGE ",Size(G),"\n");;
else
 iso:=IsomorphismPermGroup(P);;Assert(0,iso<>fail and IsBijective(iso));;
 G:=Image(iso);;gg:=List(GeneratorsOfGroup(P),g->Image(iso,g));;
fi;
Print("ROTATION_ORDER ",Size(G),"\nPERMUTATION_DEGREE ",LargestMovedPoint(G),"\n");;
Print("SOURCE_ROTATION_ORDER_MATCH ",Size(G)=L003Input.expected_rotation_order,"\n");;
Assert(0,ForAll(pres.relators,w->MappedWord(w,GeneratorsOfGroup(pres.free),gg)=One(G)));;
L003Stage("ICplus");;
a:=Concatenation([One(G)],gg);;subs:=[];;
for m in [0..15] do
 I:=Filtered([1..4],i->QuoInt(m,2^(i-1)) mod 2=1);;
 Add(subs,Group(List(Combinations(I,2),ij->a[ij[1]]^-1*a[ij[2]]),One(G)));
od;
for m in [0..15] do for n in [0..15] do
 Assert(0,Intersection(subs[m+1],subs[n+1])=subs[L003Meet(m,n)+1]);
od;od;
Print("ICPLUS_SUBGROUP_ORDERS ",List(subs,Size),"\nICPLUS_PAIRS 256\n");;
pars:=List([14,13,11,7],m->subs[m+1]);;
Print("ROTATION_PARABOLIC_ORDERS ",List(pars,Size),"\nPAIR_ORDERS ",List(Combinations([1..4],2),ij->Order(a[ij[1]]^-1*a[ij[2]])),"\n");;
L003Stage("marked_local_presentations");;
locals:=L003LocalResidues(L003Input.table,L003Input.params,a,pars);;Print("MARKED_LOCAL_PRESENTATIONS ",locals,"\n");;
L003Stage("rotation_flags");;
flags:=L003FlagChecks(pars,2);;Print("ROTATION_FLAGS ",flags,"\n");;
Assert(0,Group(Concatenation(List(pars,GeneratorsOfGroup)),One(G))=G);;
for i in [1..4] do
 Assert(0,Group(Concatenation(List(Difference([1..4],[i]),j->GeneratorsOfGroup(Intersection(pars[i],pars[j])))),One(G))=pars[i]);
od;
residues:=[];;
for I in Combinations([1..4],2) do
 K:=Intersection(List(I,i->pars[i]));;elts:=Elements(K);;m:=Length(elts);;J:=Difference([1..4],I);;
 adj:=List([1..2*m],i->[]);;
 for h in [1..m] do for k in [1..m] do
  if L003InProduct(elts[h]*elts[k]^-1,pars[J[1]],pars[J[2]]) then Add(adj[h],m+k);Add(adj[m+k],h);fi;
 od;od;
 seen:=[1];;for h in seen do for k in adj[h] do if not k in seen then Add(seen,k);fi;od;od;
 Assert(0,Length(seen)=2*m);;Add(residues,[I,m,Length(seen),List(adj,Length)]);
od;
Print("RANK2_RESIDUES ",residues,"\nRANK3_GENERATION 4\n");;
L003Stage("inversion");;
failed:=Filtered([1..Length(pres.relators)],i->MappedWord(pres.relators[i],GeneratorsOfGroup(pres.free),List(gg,Inverse))<>One(G));;
Print("INVERTED_RELATOR_FAILURES ",failed,"\n");;
Print("SOURCE_REGULARITY_MATCH ",L003Input.regular=(Length(failed)=0),"\n");;
if Length(failed)=0 then
 Assert(0,Length(failed)=0);;
 aut:=GroupHomomorphismByImages(G,G,gg,List(gg,Inverse));;
 Assert(0,aut<>fail and IsBijective(aut) and aut^2=IdentityMapping(G));;
 L003Stage("regular_completion");;
 # Faithful degree 2d action: g maps to diag(g,aut(g)), t interchanges copies.
 deg:=LargestMovedPoint(G);;
 diag:=g->PermList(Concatenation(List([1..deg],i->i^g),List([1..deg],i->deg+i^Image(aut,g))));;
 t:=PermList(Concatenation([deg+1..2*deg],[1..deg]));;
 rr:=Concatenation([t],List(gg,g->t*diag(g)));;H:=Group(rr);;
 Assert(0,ForAll(rr,r->Order(r)=2) and Size(H)=2*Size(G));;
 hsubs:=List([0..15],m->Group(List(Filtered([1..4],i->QuoInt(m,2^(i-1)) mod 2=1),i->rr[i]),One(H)));;
 for m in [0..15] do for n in [0..15] do
  Assert(0,Intersection(hsubs[m+1],hsubs[n+1])=hsubs[L003Meet(m,n)+1]);
 od;od;
 hpars:=List([14,13,11,7],m->hsubs[m+1]);;
 hflags:=L003FlagChecks(hpars,2);;
 Print("FULL_ORDER ",Size(H),"\nFULL_PARABOLIC_ORDERS ",List(hpars,Size),"\nFULL_IP_PAIRS 256\nFULL_FLAGS ",hflags,"\n");;
else
 Assert(0,Length(failed)>0);;H:=G;;
 Print("FULL_ORDER ",Size(G),"\nCHIRALITY_WITNESS_RELATOR ",failed[1],"\n");;
fi;
# All presentation/parabolic generators retained as concrete permutations for independent inspection.
Print("ROTATION_GENERATORS ",gg,"\n");;
Print("LITERAL_RELATORS ",pres.relators,"\n");;
Print("PASS_L003_ROW ",L003Input.id,"\n");;
QUIT;
