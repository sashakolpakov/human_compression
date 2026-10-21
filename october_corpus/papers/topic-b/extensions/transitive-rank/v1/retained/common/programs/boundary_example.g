# Exact auxiliary example printed before source Section6, plus branching correction.
# The all-parameter classification and geometry do not depend on this example.
SetInfoLevel(InfoWarning,0);;
Need:=function(b,s) if not b then Error(s); fi; end;;
r:=[(1,2),(1,2)(3,4),(1,2)(7,8),(1,2)(5,6),(1,3)(6,8),(1,8)(3,6)];;
g:=Group(r);;Need(g=SymmetricGroup(8),"literal source example group");;
sets:=Combinations([1..6]);;subs:=List(sets,s->Subgroup(g,r{s}));;
ip:=0;;for i in [1..64] do for j in [1..64] do
 Need(Intersection(subs[i],subs[j])=subs[Position(sets,Intersection(sets[i],sets[j]))],"example full IP");ip:=ip+1;
od;od;
pars:=List([1..6],i->Subgroup(g,r{Difference([1..6],[i])}));;
Need(IsTransitive(pars[1],[1..8]),"source transitive parabolic");;
Need(Size(pars[1])=1344,"source transitive parabolic order");;
checks:=0;;
# Product-set criterion: membership in Ha Hj is represented by the orbit of Ha
# under Hj on right cosets. A common orbit element must be in the orbit under
# the exact intersection of the selected Hj. Check every nonempty anchor choice.
for a in [1..6] do
 cs:=RightCosets(g,pars[a]);;base:=Position(cs,RightCoset(pars[a],()));;
 hom:=ActionHomomorphism(g,cs,OnRight);;
 for js in Combinations(Difference([1..6],[a])) do
  if Length(js)>=2 then
   left:=[1..Length(cs)];;h:=g;;
   for j in js do
    left:=Intersection(left,Set(Orbit(Image(hom,pars[j]),base)));;
    h:=Intersection(h,pars[j]);;
   od;
   right:=Set(Orbit(Image(hom,h),base));;
   Need(left=right,"source example flag transitivity");checks:=checks+1;
  fi;
 od;
od;
Print("BOUNDARY_N8 group40320 IP",ip," flag_products",checks," transitive_parabolic1344 PASS\n");
r9:=[(2,3),(1,2)(3,4),(4,5),(5,6),(5,7),(6,8),(7,9)];;
Need(Group(r9)=SymmetricGroup(9),"branching example generates S9");;
Need(Order(r9[3]*r9[4])=3 and Order(r9[3]*r9[5])=3,"two noncommuting bridge neighbours");;
Need(Order(r9[2]*r9[3])=6,"bridge intrinsic order6");;
Need(Length(Filtered(r9,x->Order(r9[2]*x)=6))=1,"unique order6 neighbour");;
Print("BRANCHING_LITERAL_CORRECTION two_bridge_neighbours_order3 PASS\n");
QUIT;
