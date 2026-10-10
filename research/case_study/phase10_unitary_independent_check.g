# Independent bitmask implementation: exact integer permutation groups only.
Read("phase10_unitary_rank4_witness.g");;
started:=Runtime();;
Assert(0,Length(witness)=4);
G:=Group(witness);;
Assert(0,ForAll(witness,x->x<>One(G) and x*x=One(G)));
Assert(0,Comm(witness[1],witness[3])=One(G));
Assert(0,Comm(witness[1],witness[4])=One(G));
Assert(0,Comm(witness[2],witness[4])=One(G));
masksets:=List([0..15],m->Filtered([1..4],i->RemInt(QuoInt(m,2^(i-1)),2)=1));;
sub:=List(masksets,s->Group(Concatenation([One(G)],witness{s})));;
checks:=0;;
for i in [1..16] do
 for j in [1..16] do
  same:=Intersection(masksets[i],masksets[j]);;
  k:=Position(masksets,same);;
  meet:=Intersection(sub[i],sub[j]);;
  Assert(0,IsSubgroup(meet,sub[k]));
  Assert(0,Size(meet)=Size(sub[k]));
  checks:=checks+1;
 od;
od;
Assert(0,Size(G)=14742000000);
Assert(0,IsSimpleGroup(G));
kind:=IsomorphismTypeInfoFiniteSimpleGroup(G);;
Assert(0,kind.series="2A" and kind.parameter=[3,5]);
Print("GAP ",GAPInfo.Version,"\n");
Print("ORDER ",Size(G)," DEGREE ",LargestMovedPoint(G),"\n");
Print("TYPE ",List([1..3],i->Order(witness[i]*witness[i+1])),"\n");
Print("MASKS ",masksets,"\nORDERS ",List(sub,Size),"\n");
Print("IS_SIMPLE true SIMPLE_TYPE ",kind,"\n");
Print("PASS independent bitmask intersection check ",checks," CPUms=",Runtime()-started,"\n");
QUIT;
