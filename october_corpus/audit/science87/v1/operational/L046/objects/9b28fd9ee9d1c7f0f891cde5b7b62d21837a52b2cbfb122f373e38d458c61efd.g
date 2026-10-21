Need:=function(b,m)if not b then Error(m);fi;end;;
Check:=function(g)
 local cs,reps,subs,maxs,mreps,types,els,p,q,x,e,bound,h,orders,actual,count;
 cs:=ConjugacyClassesSubgroups(g);reps:=List(cs,Representative);subs:=Concatenation(List(cs,Elements));
 maxs:=Filtered(subs,h->Size(h)<Size(g)and not ForAny(subs,k->Size(h)<Size(k)and Size(k)<Size(g)and IsSubgroup(k,h)));
 mreps:=Filtered(reps,h->h in maxs);types:=Filtered(Set(List(Elements(g),Order)),n->n>1);
 els:=Elements(g);count:=0;
 for p in types do for q in Filtered(types,z->z>=p)do
  x:=0;e:=0;
  for h in Cartesian(Filtered(els,z->Order(z)=p),Filtered(els,z->Order(z)=q))do
   if Order(h[1]*h[2])=2 then x:=x+1;if Subgroup(g,h)=g then e:=e+1;fi;fi;
  od;
  bound:=0;
  for h in mreps do
   actual:=Number(Cartesian(Filtered(Elements(h),z->Order(z)=p),Filtered(Elements(h),z->Order(z)=q)),z->Order(z[1]*z[2])=2);
   bound:=bound+Index(g,h)*actual;
  od;
  Need(0<=x-e and x-e<=bound,"union bound failure");Need(e mod Size(AutomorphismGroup(g))=0,"free orbit failure");count:=count+1;
 od;od;
 Print("CONTROL ",Size(g)," MAXCLASSES ",Length(mreps)," TYPES ",count," PASS\n");
end;;
for group in [SymmetricGroup(3),DihedralGroup(IsPermGroup,8),AlternatingGroup(4),SymmetricGroup(4),AlternatingGroup(5)]do Check(group);od;
Print("COMPLETE MAXIMAL UNION CONTROLS\n");QUIT_GAP(0);
