# Exhaustive inner-conjugacy reduction of string C-group prefixes.
# Required finite proof component; distinct review and admission are separate.
Need:=function(x,m) if not x then Error(m);fi;end;;
Need(DefaultStabChainOptions.random=1000,"guaranteed permutation verification option");;
# Compute from permutations alone, with no cached chain/order or ambient bound.
FreshPermutationOrder:=function(g,tag)
 local fresh,options,chain,n;
 fresh:=Group(ShallowCopy(GeneratorsOfGroup(g)),());
 Need(not IsIdenticalObj(fresh,g),"fresh independent group object");
 Need(not HasSize(fresh),"fresh group has no cached size");
 Need(not HasStabChainMutable(fresh),"fresh group has no cached chain");
 Need(IsIdenticalObj(Parent(fresh),fresh),"fresh group has no ambient parent");
 Need(not IsBound(StabChainOptions(fresh).size) and not IsBound(StabChainOptions(fresh).limit),"no supplied size or upper bound");
 options:=rec(random:=1000,tryPcgs:=false);
 chain:=StabChain(fresh,options);
 Need(not IsBound(options.size) and not IsBound(options.limit),"chain used no cached size or upper bound");
 n:=SizeStabChain(chain);
 Print("FRESH_ORDER|",tag,"|",n,"|NO_CACHED_SIZE_OR_CHAIN\n");
 return n;
end;;
Invs:=function(g) return Concatenation(List(Filtered(ConjugacyClasses(g),c->Order(Representative(c))=2),AsList));end;;
FullIP:=function(p)
 local subsets,subs,i,j,k;
 subsets:=Combinations([1..Length(p)]);;
 subs:=List(subsets,s->Group(List(s,i->p[i]),()));;
 for i in [1..Length(subsets)] do for j in [i..Length(subsets)] do
  k:=Position(subsets,Intersection(subsets[i],subsets[j]));
  if Intersection(subs[i],subs[j])<>subs[k] then return false;fi;
 od;od;return true;
end;;
SearchStrings:=function(g)
 local stats,allinvs,first,walk,a,t0;
 stats:=rec(nodes:=[],candidates:=[],orbit_representatives:=[],independence_rejections:=[],ip_rejections:=[],full_groups:=[],witnesses:=[],group_order:=Size(g),complete:=false);;
 allinvs:=Invs(g);;first:=List(Filtered(ConjugacyClasses(g),c->Order(Representative(c))=2),Representative);;
 walk:=function(p,h,z,eligible)
  local r,pool,orb,reps,t,q,hq,zq,eligibleq,i,s,ind;
  r:=Length(p);
  if not IsBound(stats.nodes[r]) then stats.nodes[r]:=0;stats.candidates[r]:=0;stats.orbit_representatives[r]:=0;stats.independence_rejections[r]:=0;stats.ip_rejections[r]:=0;stats.full_groups[r]:=0;fi;
  stats.nodes[r]:=stats.nodes[r]+1;
  # eligible = all involutions of C_G(p[1],...,p[r-1]); z=C_G(p).
  pool:=Filtered(eligible,t->not t in h and Order(p[r]*t)>2);
  stats.candidates[r]:=stats.candidates[r]+Length(pool);
  orb:=OrbitsDomain(z,pool,OnPoints);
  Need(Set(Concatenation(orb))=Set(pool),"complete candidate orbit coverage");
  Need(Sum(List(orb,Length))=Length(pool),"disjoint candidate orbits");
  reps:=List(orb,x->x[1]);
  stats.orbit_representatives[r]:=stats.orbit_representatives[r]+Length(reps);
  # next pool is independent of t, namely involutions centralizing all of p.
  eligibleq:=Filtered(eligible,t->Comm(t,p[r])=());
  for t in reps do
   q:=Concatenation(p,[t]);
   # Necessary intersection with the newly added adjacent dihedral subgroup.
   if Intersection(h,Group(p[r],t))<>Group(p[r]) then stats.ip_rejections[r]:=stats.ip_rejections[r]+1;continue;fi;
   ind:=true;
   for i in [1..r] do
    s:=Group(q{Difference([1..r+1],[i])});
    if q[i] in s then ind:=false;break;fi;
   od;
   if not ind then stats.independence_rejections[r]:=stats.independence_rejections[r]+1;continue;fi;
   if not FullIP(q) then stats.ip_rejections[r]:=stats.ip_rejections[r]+1;continue;fi;
   hq:=Group(q);
   if Size(hq)=Size(g) then stats.full_groups[r]:=stats.full_groups[r]+1;Add(stats.witnesses,q);continue;fi;
   zq:=Centralizer(z,t);
   walk(q,hq,zq,eligibleq);
  od;
 end;
 t0:=Runtime();
 for a in first do walk([a],Group(a),Centralizer(g,a),allinvs);od;
 stats.complete:=true;stats.runtime_ms:=Runtime()-t0;
 stats.involution_classes:=Length(first);stats.involutions:=Length(allinvs);
 return stats;
end;;
