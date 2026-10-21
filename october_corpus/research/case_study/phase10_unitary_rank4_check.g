# Deterministic standalone validation of the constructed permutation tuple.
# GAP 4.15.1; no external files beyond the original witness.
Read("phase10_unitary_rank4_witness.g");;
start:=Runtime();;
g:=Group(witness);;
Print("GAP ",GAPInfo.Version,"\n");
Print("DEGREE ",LargestMovedPoint(g),"\n");
Print("GROUP_ORDER ",Size(g),"\n");
Assert(0,Size(g)=14742000000);
Assert(0,ForAll(witness,x->Order(x)=2));
for i in [1..4] do
 for j in [i+2..4] do
  if j<=4 then Assert(0,Comm(witness[i],witness[j])=()); fi;
 od;
od;
Print("SCHLAFLI ",List([1..3],i->Order(witness[i]*witness[i+1])),"\n");
subsets:=Combinations([1..4]);;
groups:=List(subsets,s->Subgroup(g,witness{s}));;
orders:=List(groups,Size);;
Print("SUBSET_ORDER_PAIRS ",List([1..16],i->[subsets[i],orders[i]]),"\n");
checked:=0;;
for i in [1..16] do
 for j in [1..16] do
  wanted:=Position(subsets,Intersection(subsets[i],subsets[j]));;
  Assert(0,Intersection(groups[i],groups[j])=groups[wanted]);
  checked:=checked+1;
 od;
od;
Print("IP_PAIRS ",checked,"\n");
Print("IS_SIMPLE ",IsSimpleGroup(g),"\n");
Assert(0,IsSimpleGroup(g));
info:=IsomorphismTypeInfoFiniteSimpleGroup(g);;
Print("SIMPLE_TYPE ",info,"\n");
Assert(0,info.series="2A" and info.parameter=[3,5]);
Print("PASS exact standalone string C-group certificate CPUms=",Runtime()-start,"\n");
QUIT;
