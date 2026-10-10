# Independent route: start with the degree-15 primitive A7 action,
# recover its Steiner lines, then bind the action explicitly to PG(3,2).
need:=function(b,s) if not b then Error(Concatenation("PHASE271_REJECT ",s));fi;end;
SizeScreen([400,40]);
H:=PrimitiveGroup(15,1);
need(Size(H)=2520 and IsomorphismGroups(H,AlternatingGroup(7))<>fail,"actual A7");
orbits:=OrbitsDomain(H,Combinations([1..15],3),OnSets);
need(Set(List(orbits,Length))=[35,420],"complete triple-set orbits");
lines:=Set(First(orbits,O->Length(O)=35));
need(ForAll(Combinations([1..15],2),P->Number(lines,L->IsSubset(L,P))=1),"Steiner joining lines");
Third:=function(a,b) return First(First(lines,L->a in L and b in L),x->x<>a and x<>b);end;
coord:=List([1..16],x->fail);coord[1]:=0;used:=[];
for k in [0..3] do
 bit:=2^k;
 used:=Filtered(coord,x->x<>fail and x<>0);
 point:=First([1..15],x->not x in used);
 coord[bit+1]:=point;
 for v in [1..bit-1] do coord[bit+v+1]:=Third(coord[v+1],point);od;
 need(Length(Set(coord{[2..2*bit]}))=2*bit-1,"independent basis construction");
od;
need(Set(coord{[2..16]})=[1..15],"full binary coordinate bijection");
Xor:=function(a,b)
 local r,bit;
 r:=0;bit:=1;
 while a>0 or b>0 do
  r:=r+bit*((a mod 2+b mod 2) mod 2);
  a:=QuoInt(a,2);b:=QuoInt(b,2);bit:=2*bit;
 od;
 return r;
end;
for a in [1..15] do for b in [a+1..15] do
 need(Third(coord[a+1],coord[b+1])=coord[Xor(a,b)+1],"literal PG(3,2) lines");
od;od;
triples:=Filtered(Tuples([1..15],3),t->Length(Set(t))=3 and not Set(t) in lines);
need(Length(triples)=2520 and Set(Orbit(H,triples[1],OnTuples))=Set(triples),"single noncollinear ordered orbit");
need(Length(Orbit(H,[1,2],OnTuples))=210,"binary affine pair transitivity");
need(Length(Tuples([1..15],3))>2520 and 15*14*13>Size(H),"three-transitive circle excluded");
Print("PHASE271_A7_PASS primitive_degree15 binary_coordinates",coord{[2..16]},
 " all35lines ordered_noncollinear2520 ordered_distinct_pairs210 circle_excluded\n");
QUIT;
