# Diagnostic finite models for the written all-subset gluing theorem.
# No finite model list is asserted to prove the theorem for all finite sets.
SetInfoLevel(InfoWarning,0);;
Need:=function(b,s) if not b then Error(s); fi; end;;
OnSubset:=function(marks,S) local x;x:=List(S,i->marks[i]);if IsEmpty(x) then return Group(());fi;return Group(x);end;;
AllIP:=function(marks) local subs,gs,S,T,i,j,k;subs:=Combinations([1..Length(marks)]);gs:=List(subs,S->OnSubset(marks,S));for i in [1..Length(subs)] do for j in [i..Length(subs)] do k:=Position(subs,Intersection(subs[i],subs[j]));if Intersection(gs[i],gs[j])<>gs[k] then return false;fi;od;od;return true;end;;
RootChecks:=function(marks,a) local subs,gs,orbs,i,j,k,O,K,H,Sym,comp,S,rest;subs:=Combinations([1..Length(marks)]);gs:=List(subs,S->OnSubset(marks,S));orbs:=List(gs,g->Set(Orbit(g,a)));for i in [1..Length(subs)] do H:=gs[i];O:=orbs[i];if Length(O)<2 then Sym:=Group(());else Sym:=SymmetricGroup(O);fi;Need(IsSubgroup(H,Sym),"supported root symmetric group");for j in [i..Length(subs)] do k:=Position(subs,Intersection(subs[i],subs[j]));Need(Intersection(orbs[i],orbs[j])=orbs[k],"root orbit meet");od;od;return true;end;;
ExtendAtRoot:=function(g,imgs,n) local out,x;out:=[1..n];for x in [1..Length(imgs)] do out[imgs[x]]:=imgs[x^g];od;return PermList(out);end;;
models:=[
 rec(name:="path",n:=4,marks:=[(1,2),(2,3),(3,4)]),
 rec(name:="branch",n:=4,marks:=[(1,2),(2,3),(2,4)]),
 rec(name:="coupled-tail",n:=5,marks:=[(1,2),(2,3)(4,5)]),
 rec(name:="diagonal-tail",n:=7,marks:=[(1,2),(2,3)(5,6),(3,4)(6,7)]),
 rec(name:="fixed-root",n:=3,marks:=[(2,3)]),
 rec(name:="interior-root",n:=4,marks:=[(1,2),(1,3),(3,4)])
];;
for M in models do Need(AllIP(M.marks),Concatenation("input IP ",M.name));RootChecks(M.marks,1);od;
pairs:=[[1,1],[1,2],[2,3],[3,3],[3,4],[4,4],[4,5],[5,5],[1,6],[3,6],[4,6],[6,6]];;
for pair in pairs do
 L:=models[pair[1]];R:=models[pair[2]];n:=L.n+R.n-1;
 # Conjugate the second input so point 1 is common and every other point is new.
 imgs:=[1];for i in [2..R.n] do Add(imgs,L.n+i-1);od;
 right:=[];for gg in R.marks do Add(right,ExtendAtRoot(gg,imgs,n));od;joined:=Concatenation(L.marks,right);
 Need(AllIP(joined),"glued full IP");RootChecks(joined,1);
 Print("PAIR ",L.name," / ",R.name," rank ",Length(joined)," degree ",n," order ",Size(Group(joined))," PASS\n");
od;
# Iterated attachment, including a central piece with a coupled remote component.
central:=[(1,2),(1,3),(3,4)(5,6)];;
Need(AllIP(central),"central two-port marking");RootChecks(central,1);RootChecks(central,2);
chain:=Concatenation([(2,7)],central,[(1,8)]);;
Need(AllIP(chain),"two-port iterated gluing");RootChecks(chain,7);RootChecks(chain,8);
Print("ITERATED_CHAIN rank5 degree8 order ",Size(Group(chain))," PASS\n");
branch:=[(1,2),(1,3),(1,4),(2,5),(3,6),(4,7)];;
Need(AllIP(branch),"three-port tree gluing");for p in [5,6,7] do RootChecks(branch,p);od;
Print("ITERATED_TREE rank6 degree7 order ",Size(Group(branch))," PASS\n");
# Literal source counterexample to replacing a pure leaf transposition by a
# label that has an additional, disjoint transposition.
old:=[(1,2)(3,4),(2,3),(3,4)];;bad:=[(1,5),(1,2)(3,4),(2,3),(3,4)];;
Need(AllIP(old),"old source C marking");Need(not AllIP(bad),"impure leaf must fail");
A:=Group(bad{[2,3,4]});;B:=Group(bad{[1,2,3]});;C:=Group(bad{[2,3]});;
Need(Size(A)=24 and Size(B)=120 and Size(C)=8 and Size(Intersection(A,B))=24,"literal witness 24/120/8");
Print("IMPURE_LEAF_COUNTEREXAMPLE intersection24 common8 PASS\n");
# Two-point overlap cannot replace the one-point hypothesis, even for trees.
left:=[(1,3),(2,3)];;right:=[(1,4),(2,4)];;
Need(AllIP(left) and AllIP(right),"two trees");Need(not AllIP(Concatenation(left,right)),"two-point overlap failure");
Need(Size(Intersection(Group(left),Group(right)))=2,"two-point overlap common transposition");
Print("TWO_POINT_OVERLAP_COUNTEREXAMPLE PASS\n");
# The C-property alone does not force intersections of distinguished orbits.
marks:=[(1,2),(1,2)(3,4)];;
Need(AllIP(marks),"orbit countermodel input C");
Need(Intersection(Set(Orbit(Group(marks{[1]}),1)),Set(Orbit(Group(marks{[2]}),1)))=[1,2],"orbit countermodel larger meet");
Need(Size(Intersection(Group(marks{[1]}),Group(marks{[2]})))=1,"orbit countermodel subgroup meet");
Print("ROOT_SUPPORT_OMISSION_COUNTEREXAMPLE PASS\n");
Need(not AllIP([(1,2),(2,3),(1,3)]),"cyclic attachment failure");
Print("CYCLIC_ATTACHMENT_COUNTEREXAMPLE PASS\n");
Print("PASS 6 inputs, 12 paired plus 2 iterated cases, all subset IP and root-orbit meets, 4 weakening controls\n");
QUIT;
