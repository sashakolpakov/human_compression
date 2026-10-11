# Finite diagnostics, never premises of the quantified written theorems.
SizeScreen([240,60]);;
Require:=function(b,m)if not b then Error(m);fi;end;;
Par:=function(xs,I)return Group(Concatenation([()],xs{I}));end;;
IsC:=function(xs)local sets,groups,j,k;
 if Length(Set(xs))<>Length(xs) or not ForAll(xs,x->Order(x)=2) then return false;fi;
 sets:=Combinations([1..Length(xs)]);groups:=List(sets,I->Par(xs,I));
 for j in [1..Length(sets)] do for k in [j..Length(sets)] do
  if Intersection(groups[j],groups[k])<>Par(xs,Intersection(sets[j],sets[k])) then return false;fi;
 od;od;return true;end;;
StringMarking:=function(xs)local j,k;for j in [1..Length(xs)] do for k in [1..Length(xs)] do
 if AbsInt(j-k)>1 and xs[j]*xs[k]<>xs[k]*xs[j] then return false;fi;
 od;od;return true;end;;
KernelRows:=function(xs,a,domain)local prev,next,j,rootOrbit,C,K,Kprev,rows;
 prev:=Group(());rows:=[];
 for j in [1..Length(xs)] do
  next:=Par(xs,[1..j]);rootOrbit:=Orbit(prev,a);C:=Difference(domain,rootOrbit);
  K:=Stabilizer(next,C,OnTuples);Kprev:=Stabilizer(prev,C,OnTuples);
  Add(rows,[j,Size(K),Size(Kprev),IsSubgroup(prev,K)]);prev:=next;
 od;return rows;end;;
KernelTest:=function(xs,a,domain)return ForAll(KernelRows(xs,a,domain),r->r[4]);end;;
Swap:=function(a,b)return (a,b);end;;

# All subgroups P<=Q of S4, all four roots: exact kernel/intersection lemma.
subgroups:=AllSubgroups(SymmetricGroup(4));kernelcases:=0;;
for Q in subgroups do for P in subgroups do if IsSubgroup(Q,P) then
 for a in [1..4] do
  rootOrbit:=Orbit(P,a);K:=Stabilizer(Q,Difference([1..4],rootOrbit),OnTuples);
  Require((Intersection(Q,Group(Concatenation(GeneratorsOfGroup(P),[Swap(a,5)])))=P)=IsSubgroup(P,K),"kernel equivalence");
  kernelcases:=kernelcases+1;
 od;
fi;od;od;

# Exhaust all string C families through rank3 in degree4; all valid root choices.
inv:=Filtered(Elements(SymmetricGroup(4)),g->Order(g)=2);leafcases:=0;leafpositive:=0;leafnegative:=0;splitcases:=0;splitpositive:=0;splitnegative:=0;;
right:=[];z:=();;
for rank in [1..3] do for xs in Tuples(inv,rank) do
 if StringMarking(xs) and IsC(xs) then
  for a in [1..4] do
   if ForAll([2..rank],j->a^xs[j]=a) then
    ok:=KernelTest(xs,a,[1..4]);actual:=IsC(Concatenation([Swap(a,5)],xs));
    Require(ok=actual and StringMarking(Concatenation([Swap(a,5)],xs)),"leaf equivalence");
    leafcases:=leafcases+1;if ok then leafpositive:=leafpositive+1;else leafnegative:=leafnegative+1;fi;
   fi;
  od;
  # Every literal split partition with alpha=1, including boundary positions.
  for i in [1..rank] do for left in Combinations([1..4]) do
   right:=Difference([1..4],left);
   for a in left do b:=a^xs[i];
    if b in right and ForAll(Difference(left,[a]),z->z^xs[i]=z)
      and ForAll([1..i-1],j->ForAll(right,z->z^xs[j]=z))
      and ForAll([i+1..rank],j->ForAll(left,z->z^xs[j]=z)) then
     beta:=Swap(a,b)*xs[i];new:=Concatenation(xs{[1..i-1]},[Swap(a,5),Swap(5,b)*beta],xs{[i+1..rank]});
     l:=Reversed(xs{[1..i-1]});r:=xs{[i..rank]};
     ok:=KernelTest(l,a,[1..4]) and KernelTest(r,a,[1..4]);actual:=IsC(new);
     Require(StringMarking(new) and ok=actual,"two-wing equivalence");
     splitcases:=splitcases+1;if ok then splitpositive:=splitpositive+1;else splitnegative:=splitnegative+1;fi;
    fi;
   od;
  od;od;
 fi;
od;od;
Require(leafnegative>0 and leafpositive>0 and splitnegative>0 and splitpositive>0,"both outcomes exercised");

# Uniform parity-graph example, checked only at these five finite parameters.
for k in [1..5] do
 z:=Swap(k+2,k+3);xs:=List([1..k],j->Swap(j,j+1)*z);
 Require(IsC(xs) and StringMarking(xs) and KernelTest(xs,1,[1..k+3]),"parity graph family");
 Require(IsC(Concatenation([Swap(1,k+4)],xs)),"impure leaf positive");
od;

# Explicit obstruction in the independently written S11 example's old suffix.
q:=(1,2)(3,4);r:=(2,6)(3,5)(4,7);s:=(3,4)(6,7);
rows:=KernelRows([q,r,s],1,[1..7]);
Require(rows=[[1,1,1,true],[2,1,1,true],[3,6,3,false]],"S3 versus A3 obstruction");
x:=(8,9)(10,11);y:=(1,8)(9,10);
Require(KernelTest([y,x],1,[1..11]),"left wing is not the obstruction");

# Two assumptions cannot be erased.
dependent:=[(1,2)(3,4),(1,3)(2,4),(1,4)(2,3)];
Require(KernelTest(dependent,5,[1..5]) and not IsC(dependent)
 and not IsC(Concatenation([(5,6)],dependent)),"old C assumption is necessary");
Require(IsC([(1,2),(2,3)]) and not StringMarking([(2,4),(1,2),(2,3)]),"root-fixing assumption ensures string commutations");

# A supported image cannot replace its actual kernel: the diagnostic example
# has root image S3 already at P2, but only A3 supported independently.
P:=Group(q,r);rootOrbit:=[1,2,6];
Require(Size(Action(P,rootOrbit))=6 and Size(Stabilizer(P,Difference([1..7],rootOrbit),OnTuples))=3,"image differs from supported kernel");
P:=Group((1,2));Q:=Group(());f:=GroupHomomorphismByFunction(SymmetricGroup(3),Group(()),g->());
Require(IsSubgroup(P,Intersection(Q,Kernel(f))) and Intersection(Q,PreImage(f,Image(f,P)))<>P,"P containment cannot be dropped");

# Two independently supported sides, each with every nested S3 subgroup pair.
Krectangle:=function(L,T)return Group(Concatenation(GeneratorsOfGroup(L),GeneratorsOfGroup(T),[(1,7),(4,7)]));end;;
leftsubs:=AllSubgroups(Group((1,2),(2,3)));rightsubs:=AllSubgroups(Group((4,5),(5,6)));rectanglecases:=0;;
for L1 in leftsubs do for L0 in leftsubs do if IsSubgroup(L1,L0) then
 for T1 in rightsubs do for T0 in rightsubs do if IsSubgroup(T1,T0) then
  Require(Intersection(Krectangle(L0,T1),Krectangle(L1,T0))=Krectangle(L0,T0),"nested rectangle");
  rectanglecases:=rectanglecases+1;
 fi;od;od;
fi;od;od;
Print("PASS kernel_cases=",kernelcases," leaf_cases=",leafcases," leaf_positive=",leafpositive," leaf_negative=",leafnegative," split_cases=",splitcases," split_positive=",splitpositive," split_negative=",splitnegative," rectangle_cases=",rectanglecases," parity_parameters=5 assumption_controls=4\n");
QUIT_GAP(0);
