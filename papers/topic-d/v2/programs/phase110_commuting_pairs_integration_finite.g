# Full finite exceptional census. No published classification filters the search.
# Run from any directory; this program writes only standard output.
SizeScreen([4096,4096]);;
Need:=function(test,message) if not test then Error(message); fi; end;;
PairAction:=function(pair,phi) return Set(pair,x->Image(phi,x)); end;;
MiddleAction:=function(x,phi) return Image(phi,x); end;;
StringInts:=function(xs) return Concatenation("[",JoinStringsWithSeparator(List(xs,String),","),"]"); end;;
EncodePerm:=function(p) return StringInts(List([1..6],i->i^p)); end;;
EncodeTriple:=function(t) return Concatenation("[",JoinStringsWithSeparator(List(t,EncodePerm),","),"]"); end;;
AllIP:=function(G,triple)
  local subs,groups,i,j,ok,meets;
  subs:=Combinations([1..3]);
  groups:=List(subs,I->Subgroup(G,List(I,i->triple[i])));
  ok:=true;meets:=0;
  for i in [1..8] do for j in [1..8] do
    meets:=meets+1;
    if Intersection(groups[i],groups[j])<>
       groups[Position(subs,Intersection(subs[i],subs[j]))] then ok:=false;fi;
  od;od;
  return rec(ok:=ok,meets:=meets);
end;;
sourcePairs:=[[(1,2),(3,4)],[(1,2),(3,4)(5,6)],
 [(1,2),(1,2)(3,4)],[(1,2),(1,2)(3,4)(5,6)],
 [(1,2)(3,4),(1,3)(2,4)]];;
explicit:=[[(5,6),(2,3)(4,5),(1,2)(3,4)],
 [(5,6),(2,3)(4,5),(1,2)(3,4)(5,6)]];;
orbs:=[];;
for G in [SymmetricGroup(6),AlternatingGroup(6)] do
  inv:=Filtered(Elements(G),x->Order(x)=2);;
  Need(Size(Subgroup(G,inv))=Size(G),"Involutions do not generate ambient group");
  aut:=AutomorphismGroup(G);;
  pairs:=[];;
  for i in [1..Length(inv)] do for j in [i+1..Length(inv)] do
    if inv[i]*inv[j]=inv[j]*inv[i] then Add(pairs,Set([inv[i],inv[j]]));fi;
  od;od;
  orbs:=OrbitsDomain(aut,pairs,PairAction);;
  conjugacy:=OrbitsDomain(SymmetricGroup(6),pairs,OnSets);;
  if Size(G)=720 then reps:=List(sourcePairs,Set);else reps:=[Set(sourcePairs[5])];fi;
  repIndices:=List(reps,p->PositionProperty(orbs,o->p in o));;
  Need(not fail in repIndices,"Primary pair missing");
  Need(Set(repIndices)=[1..Length(orbs)] and Length(Set(repIndices))=Length(reps),
       "Primary representatives are not a complete irredundant orbit list");
  found:=[];;middleCount:=0;;generated:=0;;meetCount:=0;;extendable:=[];;
  for ri in [1..Length(reps)] do
    pair:=reps[ri];;a:=pair[1];;c:=pair[2];;
    stabilizer:=Stabilizer(aut,pair,PairAction);;
    middles:=OrbitsDomain(stabilizer,inv,MiddleAction);;
    localGenerated:=0;;localIP:=0;;
    for mo in middles do
      b:=mo[1];;middleCount:=middleCount+1;;
      if Size(Subgroup(G,[a,b,c]))=Size(G) then
        Need(Length(Set([a,b,c]))=3,"Generating triple has repeated marker");
        generated:=generated+1;;localGenerated:=localGenerated+1;;
        ip:=AllIP(G,[a,b,c]);;meetCount:=meetCount+ip.meets;;
        if ip.ok then
          localIP:=localIP+1;;typ:=SortedList([Order(a*b),Order(b*c)]);;
          Add(found,rec(triple:=[a,b,c],type:=typ,pair_index:=ri));
          Print("SURVIVOR|",Size(G),"|",ri,"|",StringInts(typ),"|",EncodeTriple([a,b,c]),"\n");
        fi;
      fi;
    od;
    if localGenerated>0 then Add(extendable,ri);fi;
    Print("FIBER|",Size(G),"|",ri,"|",Length(orbs[repIndices[ri]]),"|",Size(stabilizer),"|",Length(middles),"|",localGenerated,"|",localIP,"\n");
  od;
  explicitMeets:=0;;
  if Size(G)=720 then
    Need(Length(inv)=75 and Length(pairs)=495 and Length(conjugacy)=9 and
         Length(orbs)=5 and Size(aut)=1440,"Symmetric endpoint census mismatch");
    Need(middleCount=80 and generated=2 and Length(found)=2 and
         SortedList(List(found,r->r.type))=[[5,6],[6,6]] and extendable=[2,4],
         "Symmetric polyhedron census mismatch");
    for triple in explicit do
      Need(Size(Subgroup(G,triple))=Size(G),"Explicit triple does not generate");
      Need(triple[1]*triple[3]=triple[3]*triple[1],"Explicit endpoints fail string relation");
      ip:=AllIP(G,triple);;Need(ip.ok,"Explicit triple IP failure");
      explicitMeets:=explicitMeets+ip.meets;;
      typ:=SortedList([Order(triple[1]*triple[2]),Order(triple[2]*triple[3])]);;
      Need(typ in List(found,r->r.type),"Explicit type not in complete census");
    od;
  else
    Need(Length(inv)=45 and Length(pairs)=90 and Length(conjugacy)=2 and
         Length(orbs)=1 and Size(aut)=1440,"Alternating endpoint census mismatch");
    Need(middleCount=8 and generated=0 and Length(found)=0,
         "Alternating nonexistence census mismatch");
  fi;
  Print("SUMMARY|",Size(G),"|",Size(aut),"|",Length(inv),"|",Length(pairs),"|",Length(conjugacy),"|",Length(orbs),"|",middleCount,"|",generated,"|",Length(found),"|",meetCount,"|",explicitMeets,"\n");
od;
Print("VERSION|",GAPInfo.Version,"\nPASS\n");
QUIT;
