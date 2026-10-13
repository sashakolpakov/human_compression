SizeScreen([100000,100000]);;
Read("literal_rows.g");;
L044Templates:=function()
 local restrict,row,rev,gs,n,d,H,K,fixed,c,u,v,w,z,Y,R,C,cr,cy,
       a,b,ar,br,aux,expectedA,expectedB,positive,negative;
 restrict:=function(g,S,n)
  local images,i;images:=[1..n];
  for i in S do images[i]:=i^g;od;
  return PermList(images);
 end;
 positive:=0;negative:=0;
 for row in L044SourceRows do
  if row.id>=4 then
   for rev in [false,true] do
    gs:=List(row.gens,PermList);if rev then gs:=Reversed(gs);fi;
    n:=row.n;d:=Length(gs);H:=Group(gs);K:=Group(gs{[1..d-1]});
    if H<>AlternatingGroup(n) then Error("literal alternating support");fi;
    fixed:=Filtered([1..n],i->ForAll(GeneratorsOfGroup(K),g->i^g=i));
    if Length(fixed)=0 then
     negative:=negative+1;Print("NO_ENDPOINT|",row.id,"|",rev,"\n");
    else
     if Length(fixed)<>1 then Error("nonunique endpoint");fi;
     c:=fixed[1];a:=gs[d];b:=gs[d-1];
     u:=c^a;v:=u^b;w:=v^a;z:=w^b;Y:=[u,v,w,z];
     if Length(Set(Concatenation([c],Y)))<>5 then Error("five distinct vertices");fi;
     R:=Difference([1..n],Concatenation([c],Y));
     if OnSets(Set(Y),a)<>Set(Concatenation([c],[v,w,z])) then Error("a support");fi;
     if OnSets(R,a)<>R or OnSets(R,b)<>R then Error("auxiliary support");fi;
     expectedA:=(c,u)*(v,w);expectedB:=(u,v)*(w,z);
     if restrict(a,Concatenation([c],Y),n)<>expectedA or
        restrict(b,Concatenation([c],Y),n)<>expectedB then Error("attachment words");fi;
     C:=Centralizer(SymmetricGroup(Difference([1..n],[c])),K);
     if not ForAll(GeneratorsOfGroup(C),g->OnSets(Set(Y),g)=Set(Y) and OnSets(R,g)=R) then Error("centralizer support");fi;
     cy:=Group(Concatenation([()],List(GeneratorsOfGroup(C),g->restrict(g,Y,n))));
     cr:=List(GeneratorsOfGroup(C),g->restrict(g,R,n));
     ar:=restrict(a,R,n);br:=restrict(b,R,n);
     aux:=Group(Concatenation([ar,br],cr));
     if Size(C)>2 or Size(cy)>2 or Size(aux)>2 then Error("two-element bound");fi;
     if n=11 and Size(cy)<>1 then Error("degree-eleven kernel orbit bound");fi;
     if not ForAll(cr,g->g*ar=ar*g) then Error("decoration centralization");fi;
     if not ForAll(GeneratorsOfGroup(aux),g->SignPerm(g)=1) then Error("even decoration");fi;
     if Size(Group(a,b))>=60 then Error("dihedral intersection obstruction");fi;
     positive:=positive+1;
     Print("TEMPLATE|",row.id,"|",rev,"|",n,"|",c,"|",Y,"|",R,"|",Size(C),"|",Size(cy),"|",Size(aux),"|",Size(Group(a,b)),"|",List(Elements(C),g->List([1..n],i->i^g)),"\n");
    fi;
   od;
  fi;
 od;
 Print("COMPLETE_TEMPLATES|",positive,"|",negative,"\n");
end;;
L044Templates();;
QUIT;
