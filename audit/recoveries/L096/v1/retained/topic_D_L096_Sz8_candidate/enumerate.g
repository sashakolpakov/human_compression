Read("ambient.g");;
SizeScreen([100000,100000]);;
cc:=Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2);;
if Length(cc)<>1 or Size(G)<>29120 or not IsSimpleGroup(G) then Error("ambient");fi;
invs:=Set(AsList(cc[1]));; aut:=AutomorphismGroup(G);;
act:=ActionHomomorphism(aut,invs,function(x,f) return Image(f,x);end);;
A:=Image(act);;
if Size(A)<>87360 or Size(Kernel(act))<>1 then Error("autfaithful");fi;
A1:=Stabilizer(A,1);;bs:=List(Orbits(A1,[2..Length(invs)]),Minimum);;Sort(bs);;
firstmaps:=List([1..Length(invs)],x->RepresentativeAction(A,x,1));;
bclass:=[];;bmaps:=[];;cmin:=[];;pairs:=[];;
for b in bs do
 pair:=Stabilizer(A1,b);;Add(pairs,pair);
 for x in Orbit(A1,b) do bclass[x]:=b;bmaps[x]:=RepresentativeAction(A1,x,b);od;
 cmin[b]:=[];
 for o in Orbits(pair,[1..Length(invs)]) do for x in o do cmin[b][x]:=Minimum(o);od;od;
od;
CanonOrdered:=function(t)
 local z,b,c;
 z:=List(t,x->x^firstmaps[t[1]]);b:=bclass[z[2]];
 c:=z[3]^bmaps[z[2]];return [b,cmin[b][c]];
end;;
CanonUnordered:=function(t)
 return Minimum(List(PermutationsList(t),CanonOrdered));
end;;
prodset:=function(H,K) return Set(Concatenation(List(AsList(H),h->List(AsList(K),k->h*k))));end;;
maxes:=MaximalSubgroupClassReps(G);;
Print("MAXIMAL_ORDERS|",List(maxes,Size),"\n");
H:=[];;v:=[];;
seen:=[];;chosen:=[];;nordered:=0;;ngen:=0;;ncgroup:=0;;nft:=0;;nrw:=0;;counts:=[];;
for pos in [1..Length(bs)] do
 b:=bs[pos];pair:=pairs[pos];
 for co in Orbits(pair,Difference([1..Length(invs)],[1,b])) do
  c:=Minimum(co);nordered:=nordered+1;
  key:=CanonUnordered([1,b,c]);
  if key in seen then continue;fi;AddSet(seen,key);
  t:=[1,b,c];v:=invs{t};
  if Size(Group(v))<>Size(G) then continue;fi;ngen:=ngen+1;
  H:=[Group(v{[2,3]}),Group(v{[1,3]}),Group(v{[1,2]})];
  if not ForAll(Combinations([1..3],2),ij->Intersection(H{ij})=Group(v{Difference([1..3],ij)})) then continue;fi;
  ncgroup:=ncgroup+1;
  ft:=ForAll([1..3],i->Length(Intersection(prodset(H[i],H[Difference([1..3],[i])[1]]),prodset(H[i],H[Difference([1..3],[i])[2]])))=2*Size(H[i]));
  if not ft then continue;fi;nft:=nft+1;
  # All rank-two residues are thin polygons. Local weak primitivity is
  # separately checked by prime vertex count; top primitivity by actual
  # conjugacy to a member of the complete GAP maximal-subgroup roster.
  localok:=ForAll(H,h->IsPrimeInt(Size(h)/2));
  topok:=ForAny(H,h->ForAny(maxes,m->Size(m)=Size(h) and IsConjugate(G,h,m)));
  rw:=localok and topok;
  if rw then nrw:=nrw+1;Add(chosen,t);fi;
  Add(counts,[t,List(H,Size),rw]);
 od;
od;
Print("CENSUS|",[nordered,Length(seen),ngen,ncgroup,nft,nrw],"\n");
PrintTo("sz8_rows.g","L096Sz8Involutions:=",invs,";;\nL096Sz8Triples:=",chosen,";;\nL096Sz8AllThin:=",counts,";;\n");
Print("COMPLETE_SZ8_INVOLUTION_CENSUS\n");QUIT;
