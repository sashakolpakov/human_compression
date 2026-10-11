# Exact extension-fiber checks for the large Mathieu Steiner systems.
# Named Mathieu actions are retained inputs. This does not reprove their
# classification, uniqueness, or the uniform residue theorem.
P182Require := function(b,msg) if not b then Error(msg); fi; end;
P182Check := function(v,t,k)
  local G,pts,A,H,orbs,small,B,blocks,counts,T,B0,alternatives,K,B1,K1,
        tail,orbit1,orbit2,expected,chambers;
  G:=MathieuGroup(v); pts:=[1..v]; A:=[1..t];
  H:=Stabilizer(G,A,OnTuples);
  orbs:=Orbits(H,Difference(pts,A));
  small:=Filtered(orbs,o->Length(o)=k-t);
  P182Require(Length(small)=1,"ambiguous seed block");
  B:=Union(A,small[1]);
  blocks:=Set(Orbit(G,B,OnSets));
  expected:=Binomial(v,t)/Binomial(k,t);
  P182Require(Length(blocks)=expected,"wrong block orbit size");
  # Verify all t-subsets explicitly, rather than infer a Steiner system
  # from block size and group transitivity alone.
  counts:=List(Combinations(pts,t),X->Number(blocks,C->IsSubset(C,X)));
  P182Require(Set(counts)=[1],"Steiner condition failure");
  T:=[1..t-1];
  B0:=First(blocks,C->IsSubset(C,T));
  alternatives:=Filtered(blocks,C->IsSubset(C,T) and C<>B0);
  K:=Intersection(Stabilizer(G,T,OnTuples),Stabilizer(G,B0,OnSets));
  P182Require(Index(G,K)=Product([0..t-2],i->v-i)*5,
              "base-flag orbit does not exhaust all base flags");
  P182Require(Length(alternatives)=4,"wrong alternative-block count");
  B1:=alternatives[1]; orbit1:=Set(Orbit(K,B1,OnSets));
  P182Require(orbit1=Set(alternatives),"alternative-block orbit incomplete");
  K1:=Stabilizer(K,B1,OnSets); tail:=Difference(B1,T);
  orbit2:=Set(Orbit(K1,tail[1]));
  P182Require(orbit2=Set(tail) and Length(tail)=4,"tail orbit incomplete");
  chambers:=Product([0..t-1],i->v-i)*4;
  P182Require(Size(Stabilizer(K1,tail[1]))=12,"wrong chamber stabilizer");
  P182Require(Size(G)=12*chambers,"wrong chamber orbit count");
  Print("P182_MATHIEU ",rec(v:=v,t:=t,k:=k,group_order:=Size(G),
    block_count:=Length(blocks),tested_subsets:=Length(counts),
    base_stabilizer_order:=Size(K),alternative_orbit:=Length(orbit1),
    tail_stabilizer_order:=Size(K1),tail_orbit:=Length(orbit2),
    chambers:=chambers,chamber_stabilizer:=12),"\n");
end;
P182Check(22,3,6);
P182Check(23,4,7);
P182Check(24,5,8);
Print("P182_MATHIEU_EXTENSION_FIBERS_PASS\n");
QUIT;
