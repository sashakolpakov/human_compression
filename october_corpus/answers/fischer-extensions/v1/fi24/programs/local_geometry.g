Need:=function(b,s) if not b then Error(s);fi;end;;
# All proper subset pairs are checked. Pairs with a full subset are identities.
ProperIP:=function(r)
 local ss,ps,i,j;
 Need(Length(r)=3 and Length(Set(r))=3 and ForAll(r,x->Order(x)=2),"distinct nonidentity involutions");
 ss:=Filtered(Combinations([1..3]),s->Length(s)<3);
 ps:=List(ss,s->Group(r{s},()));
 for i in [1..7] do for j in [1..7] do
  Need(Intersection(ps[i],ps[j])=ps[Position(ss,Intersection(ss[i],ss[j]))],"proper intersection property");
 od;od;
 return 49;
end;;
# Exact product-set criterion, never a generated subgroup in its place.
FlagStreaming:=function(r)
 local ps,i,j,k,u,v,rhs,z,count;
 ps:=[Group(r{[2,3]}),Group(r{[1,3]}),Group(r{[1,2]})];
 count:=0;
 for i in [1..3] do
  j:=Difference([1..3],[i])[1];k:=Difference([1..3],[i])[2];
  rhs:=Set(ListX(Elements(Intersection(ps[j],ps[i])),Elements(Intersection(ps[k],ps[i])),function(x,y)return x*y;end));
  for u in Elements(ps[j]) do for v in Elements(ps[k]) do
   z:=u*v;count:=count+1;
   Need(not z in ps[i] or z in rhs,"flag product intersection");
  od;od;
 od;
 return count;
end;;
WordValue:=function(gs,w)
 local z,i;z:=();
 for i in w do Need(i<>0 and AbsInt(i)<=Length(gs),"word letter range");
  if i>0 then z:=z*gs[i];else z:=z*gs[-i]^-1;fi;
 od;return z;
end;;
