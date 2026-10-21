# Direct verification of the retained named witnesses; no census is repeated.
L059Need:=function(ok,msg)
  if not ok then Print("FAIL ",msg,"\n"); QUIT_GAP(1); fi;
end;;
L059Iso:=function(G,H)
  local phi;
  phi:=IsomorphismGroups(G,H);
  return phi<>fail and IsBijective(phi);
end;;
Read("/Users/sasha/medusa/research/leemans/phase177_evidence/phase177_graph_witnesses.g");;
L059Find:=function(label,maxcode,normcode)
  local d,rows;
  d:=First(P177Results,x->x.label=label);
  L059Need(d<>fail,"named graph absent");
  rows:=Filtered(d.witnesses,x->(maxcode=fail or x.maxcode=maxcode)
                   and (normcode=fail or x.normcode=normcode));
  L059Need(Length(rows)=1,"named row is not unique in graph");
  return rows[1];
end;;
r:=L059Find("K3_3",["2T","M","M","2T"],fail);;
L059Need(L059Iso(r.H,DirectProduct(SymmetricGroup(3),CyclicGroup(3))),"K33 S3xC3");;
L059Need(IsCyclic(r.H1) and Size(r.H1)=6 and L059Iso(r.H0,SymmetricGroup(3)) and Size(r.B)=2,"K33 stabilizers");;
r:=L059Find("K3_3",["M","2T","2T","M"],fail);;
L059Need(L059Iso(r.H,DirectProduct(SymmetricGroup(3),CyclicGroup(3))) and IsCyclic(r.H0) and Size(r.H0)=6 and L059Iso(r.H1,SymmetricGroup(3)),"K33 reverse stabilizers");;
r:=L059Find("K3_3",fail,[true,true,true,true]);;
L059Need(IsElementaryAbelian(r.H) and Size(r.H)=9 and Size(r.H0)=3 and Size(r.H1)=3 and Size(r.B)=1,"K33 regular marking");;
r:=L059Find("K3_3",fail,[true,true,false,false]);;
L059Need(L059Iso(r.H,DirectProduct(SymmetricGroup(3),CyclicGroup(3))) and L059Iso(r.H0,SymmetricGroup(3)) and IsCyclic(r.H1) and Size(r.H1)=6,"K33 YYNN");;
r:=L059Find("K3_3",fail,[true,false,true,false]);;
L059Need(L059Iso(r.H,DirectProduct(SymmetricGroup(3),CyclicGroup(3))) and L059Iso(r.H1,SymmetricGroup(3)) and IsCyclic(r.H0) and Size(r.H0)=6,"K33 YNYN");;
r:=L059Find("K4_4",fail,[true,true,true,true]);;
L059Need(IsElementaryAbelian(r.H) and Size(r.H)=16 and IsElementaryAbelian(r.H0) and Size(r.H0)=4 and IsElementaryAbelian(r.H1) and Size(r.H1)=4 and Size(r.B)=1,"K44 regular marking");;
r:=L059Find("cube",["M","M","2T","2T"],fail);;
L059Need(L059Iso(r.H,AlternatingGroup(4)) and Size(r.H0)=3 and Size(r.H1)=3 and Size(r.B)=1,"cube marking");;
r:=L059Find("Heawood",fail,[false,false,false,true]);;
L059Need(Size(r.H)=21 and not IsAbelian(r.H) and Size(r.H0)=3 and Size(r.H1)=3 and Size(r.B)=1,"Heawood marking");;
# The unique nonabelian group of order21 has its normal C7 and a C3 complement.
L059Seven:=SylowSubgroup(r.H,7);;
L059Need(IsNormal(r.H,L059Seven) and Size(ClosureGroup(L059Seven,r.H0))=21,"Heawood semidirect product");;
Read("current_c4_descent/010_002.g");;
rr:=Filtered(L059Result.witnesses,x->x.maxcode=["X","X","2T","2T"]);;
L059Need(Length(rr)=1,"ten-vertex unique code");;
r:=rr[1];;
L059AffineFive:=Group((1,2,3,4,5),(2,3,5,4));;
L059Need(L059Iso(r.H,L059AffineFive) and IsCyclic(r.H0) and Size(r.H0)=4 and IsCyclic(r.H1) and Size(r.H1)=4 and Size(r.B)=1,"ten-vertex groups");;
Read("exception_witnesses.g");;
L059Need(Length(L059Exception.witnesses)=2,"110-vertex markings");;
for r in L059Exception.witnesses do
 if Size(r.H)=1320 then
   L059Need(L059Iso(r.H,PGL(2,11)) and L059Iso(r.H0,SymmetricGroup(4)) and L059Iso(r.H1,DihedralGroup(24)) and L059Iso(r.B,SymmetricGroup(3)),"PGL110 actual groups");
 elif Size(r.H)=660 then
   L059Need(L059Iso(r.H,PSL(2,11)) and L059Iso(r.H0,AlternatingGroup(4)) and L059Iso(r.H1,DihedralGroup(12)) and IsCyclic(r.B) and Size(r.B)=3,"PSL110 actual groups");
 else
   L059Need(false,"110-vertex acting order");
 fi;
od;
Print("PASS_ALL_NAMED_CENSUS_GROUPS\n");

# Retain actual complements instead of repeating their discovery.
Read("mathieu_witness_9.g");;
phi:=GroupHomomorphismByImages(G,G,domain_gens,image_gens);;
L059Need(phi<>fail and IsBijective(phi),"Mathieu automorphism");;
L059Need(G=MathieuGroup(12) and Size(G)=95040,"Mathieu ambient group");;
L059Need(Image(phi,P)=P2 and Image(phi,Q)=Q2 and Q^h=Q2,"Mathieu subgroup images");;
L059Need(SortedList(List(Orbits(P,[1..12]),Length))=[12] and SortedList(List(Orbits(P2,[1..12]),Length))=[3,9],"Mathieu nonconjugacy");;
L059Need(Size(ClosureGroup(P,Q))=95040 and Size(Core(G,Intersection(P,Q)))=1,"Mathieu connected faithful source");;
L059Need(Size(ClosureGroup(P2,Q2))=95040 and Size(Core(G,Intersection(P2,Q2)))=1,"Mathieu connected faithful image");;
Read("mathieu_Q8_complement.g");;
L059Need(IsSubgroup(Q,N) and IsSubgroup(Q,C) and IsNormal(Q,N),"Mathieu192 inclusions");;
L059Need(L059Iso(N,QuaternionGroup(8)) and L059Iso(C,SymmetricGroup(4)),"Mathieu192 factors");;
L059Need(Size(Intersection(N,C))=1 and ClosureGroup(N,C)=Q,"Mathieu192 split");;
Read("mathieu_432_complements.g");;
L059Need(IsSubgroup(P,N) and IsNormal(P,N) and Size(N)=72 and IsSubgroup(N,K) and IsNormal(N,K),"Mathieu432 normal chain");;
L059Need(IsElementaryAbelian(K) and Size(K)=9 and IsSubgroup(N,C8) and L059Iso(C8,QuaternionGroup(8)),"Mathieu72 factors");;
L059Need(Size(Intersection(K,C8))=1 and ClosureGroup(K,C8)=N,"Mathieu72 split");;
L059Need(IsSubgroup(P,C6) and L059Iso(C6,SymmetricGroup(3)) and Size(Intersection(N,C6))=1 and ClosureGroup(N,C6)=P,"Mathieu432 split");;
Print("PASS_MATHIEU_MARKED_ISOMORPHISM_AND_STRUCTURES\n");
QUIT_GAP(0);
