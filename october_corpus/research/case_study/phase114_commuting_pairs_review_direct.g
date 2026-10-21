# Independent complete triple census. No source list or stabilizer-orbit reduction
# is used to generate candidates; the full raw extension space is visited first.
SizeScreen([4096,4096]);;
Require114:=function(ok,msg) if not ok then Error(msg);fi;end;;
TripAction114:=function(t,alpha)
  local ends;
  ends:=SortedList([Image(alpha,t[1]),Image(alpha,t[3])]);
  return [ends[1],Image(alpha,t[2]),ends[2]];
end;;
PairAction114:=function(p,alpha) return Set(p,x->Image(alpha,x));end;;
IP114:=function(G,t)
  local indices,subs,i,j;
  indices:=Combinations([1..3]);
  subs:=List(indices,I->Subgroup(G,List(I,k->t[k])));
  for i in [1..8] do for j in [1..8] do
    if Intersection(subs[i],subs[j])<>
       subs[Position(indices,Intersection(indices[i],indices[j]))] then
      return false;
    fi;
  od;od;
  return true;
end;;
endpointOrbs:=[];;pairGenerated:=[];;endpoints:=[];;
for G in [SymmetricGroup(6),AlternatingGroup(6)] do
  invols:=Filtered(Elements(G),g->g<>One(G) and g*g=One(G));;
  endpoints:=Filtered(Combinations(invols,2),p->p[1]*p[2]=p[2]*p[1]);;
  raw:=0;;generating:=[];;types:=[];;pairGenerated:=[];;
  for ends in endpoints do
    localCount:=0;;
    for b in invols do
      raw:=raw+1;;
      t:=[ends[1],b,ends[2]];;
      if Size(Subgroup(G,t))=Size(G) then
        Require114(IP114(G,t),"Raw generating triple fails IP");
        Add(generating,t);;localCount:=localCount+1;;
        Add(types,SortedList([Order(t[1]*t[2]),Order(t[2]*t[3])]));
      fi;
    od;
    Add(pairGenerated,localCount);
  od;
  # Only after generation/IP has been decided for every raw triple do we take
  # full automorphism orbits. Sorting endpoints implements duality explicitly.
  A:=AutomorphismGroup(G);;
  endpointOrbs:=OrbitsDomain(A,endpoints,PairAction114);;
  tripleOrbs:=OrbitsDomain(A,generating,TripAction114);;
  conjugacy:=OrbitsDomain(SymmetricGroup(6),endpoints,OnSets);;
  allCounts:=Collected(types);;
  Print("DIRECT|",Size(G),"|",Size(A),"|",Length(invols),"|",Length(endpoints),"|",raw,"|",Length(generating),"|",Length(generating)*64,"|",Length(tripleOrbs),"|",SortedList(List(tripleOrbs,Length)),"|",allCounts,"\n");
  Print("ENDPOINT|",Size(G),"|",Length(conjugacy),"|",Length(endpointOrbs),"|",SortedList(List(endpointOrbs,Length)),"|",Collected(pairGenerated),"\n");
  primary:=[Set([(1,2),(3,4)]),Set([(1,2),(3,4)(5,6)]),
    Set([(1,2),(1,2)(3,4)]),Set([(1,2),(1,2)(3,4)(5,6)]),
    Set([(1,2)(3,4),(1,3)(2,4)])];;
  if Size(G)=360 then primary:=[primary[5]];fi;
  labels:=List(primary,p->PositionProperty(endpointOrbs,o->p in o));;
  Require114(not fail in labels and Set(labels)=[1..Length(endpointOrbs)] and
    Length(Set(labels))=Length(primary),"Source representative list disagrees");
  Print("PRIMARY|",Size(G),"|",List(primary,p->pairGenerated[Position(endpoints,p)]),"\n");
  if Size(G)=720 then
    Require114(Length(tripleOrbs)=2 and Set(types)=[[5,6],[6,6]],"Symmetric result");
  else Require114(IsEmpty(generating),"Alternating result");fi;
od;
Print("VERSION|",GAPInfo.Version,"\nPASS\n");
QUIT;
