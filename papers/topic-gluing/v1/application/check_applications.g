# Complete diagnostics for the written uniform theorems; no finite-premise claim.
SetInfoLevel(InfoWarning,0);;
Need:=function(b,s) if not b then Error(s); fi; end;;
OnSubset:=function(marks,S) local x;x:=List(S,i->marks[i]);if IsEmpty(x) then return Group(());fi;return Group(x);end;;
AllIP:=function(marks) local subs,gs,i,j,k;subs:=Combinations([1..Length(marks)]);gs:=List(subs,S->OnSubset(marks,S));for i in [1..Length(subs)] do for j in [i..Length(subs)] do k:=Position(subs,Intersection(subs[i],subs[j]));if Intersection(gs[i],gs[j])<>gs[k] then return false;fi;od;od;return true;end;;
Components:=function(n,edges) local cs,e,a,b;cs:=List([1..n],x->[x]);for e in edges do a:=PositionProperty(cs,c->e[1] in c);b:=PositionProperty(cs,c->e[2] in c);if a<>b then cs[a]:=Union(cs[a],cs[b]);Remove(cs,b);fi;od;return cs;end;;
Marks:=function(n,edges,Removed) local out,e,g;out:=[];for e in edges do g:=(e[1],e[2]);if Intersection(e,Removed)=[] then g:=g*(n+e[1],n+e[2]);fi;Add(out,g);od;return out;end;;
SymSupport:=function(S) if Length(S)<2 then return Group(());fi;return SymmetricGroup(S);end;;
Predicted:=function(n,edges,Removed) local cs,C,gs,D,ed,other,I,x,g;
 cs:=Components(n,edges);gs:=[];
 for C in cs do
  if Intersection(C,Removed)=[] then
   for g in GeneratorsOfGroup(SymSupport(C)) do Add(gs,g*PermList(Concatenation([1..n],List([1..n],x->n+x^g))));od;
  else
   Append(gs,GeneratorsOfGroup(SymSupport(C)));
   ed:=Filtered(edges,e->IsSubset(C,e) and Intersection(e,Removed)=[]);
   for D in Components(n,ed) do if IsSubset(Difference(C,Removed),D) then Append(gs,GeneratorsOfGroup(SymSupport(List(D,x->x+n))));fi;od;
  fi;
 od;
 if IsEmpty(gs) then return Group(());fi;return Group(gs);
end;;

StringCheck:=function(m) local i,j;for i in [1..Length(m)] do for j in [i+2..Length(m)] do if m[i]*m[j]<>m[j]*m[i] then return false;fi;od;od;return true;end;;
folded:=0;; auxiliary:=0;; negative:=0;;
for n in [2..5] do
 m:=Concatenation([(1,n+1)],List([1..n-1],i->(i,i+1)(n+i,n+i+1)),[(n,2*n+1)]);
 Need(StringCheck(m) and AllIP(m) and Size(Group(m))=Factorial(2*n+1),"folded tail theorem");folded:=folded+1;
od;
for r in [2..5] do
 m:=List([1..r-2],i->(i,i+1)(r+2+i,r+3+i));
 Add(m,(r-1,r)(2*r+1,2*r+2)(r+1,r+2));Add(m,(r,r+1));
 Need(StringCheck(m) and AllIP(m),"auxiliary family C");
 if r=2 then expected:=8;else expected:=Factorial(r+2)*Factorial(r);fi;
 Need(Size(Group(m))=expected,"auxiliary full group");auxiliary:=auxiliary+1;
od;
c:=0;;len:=0;;x:=[];;y:=[];;
for h in [1..3] do for r in [h+4..h+6] do
 n:=h+1;len:=r-h-2;c:=2*n+1;x:=List([1..len],j->c+j);y:=List([1..len],j->c+len+j);
 f:=(1,n+1);d:=List([1..h],j->(j,j+1)(n+j,n+j+1));t:=(n,c);tau:=Product([1..len],j->(x[j],y[j]));ss:=t*tau;u:=(c,x[1]);
 e:=List([1..len-1],j->(x[j],x[j+1])(y[j],y[j+1]));
 m:=Concatenation([f],d,[ss,u],e);P:=Group(Concatenation([f],d,[ss]));Q:=Group(Concatenation(d,[ss,u]));K:=Group(Concatenation(d,[ss]));
 Need(tau in P and tau in Q and not tau in K,"literal parity defect");
 Need(StringCheck(m) and Size(Group(m))=Factorial(2*r-1),"negative family full symmetric string group");
 negative:=negative+1;
od;od;
Print("PASS folded ",folded," auxiliary ",auxiliary," uniform negative ",negative," cases; explicit parity defects checked\n");

# Source's second impure-leaf example: diagnostic for the written short proof.
a:=(1,2)(5,6);b:=(2,3)(4,5)(6,7);c:=(3,4);x:=(8,1);;
Need(AllIP([a,b,c]) and Size(Group(a,b,c))=5040,"second source input marking");
Need(Size(Group(b,c))=8 and Set(Orbit(Group(b,c),[2,3],OnSets))=Set([[2,3],[2,4],[3,5],[4,5]]),"second source orbit");
Need(Intersection(Group(a,b),Group(b,c))=Group(b),"second source end intersection");
Need(Intersection(Group(a,b,c),Group(x,a))=Group((1,2),(5,6)) and not (5,6) in Group(a),"second source literal failure");
Print("PASS second source impure-leaf example, exact orbit and intersection\n");
QUIT;

