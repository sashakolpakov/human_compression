# Independent native-GAP reconstruction of phase211's finite hypotheses.
# It does not import or execute the author's Python surface implementation.
SizeScreen([4096,4096]);;
Need:=function(ok,msg) if not ok then Print("REJECT ",msg,"\n");FORCE_QUIT_GAP(1);fi;end;;
Dmarks:=List([
[1,2,3,7,5,6,4,12,13,10,11,8,9,16,15,14],
[1,4,3,2,9,7,6,8,5,15,13,12,11,16,10,14],
[2,1,6,8,10,3,12,4,14,5,15,7,16,9,11,13],
[3,5,1,9,2,11,13,8,4,15,6,12,7,14,10,16]],PermList);;
Drot:=List([1..3],i->Dmarks[i]*Dmarks[i+1]);;
Da:=Drot[1];;Db:=Drot[2];;Dc:=Drot[3];;
Dwords:=[Db*Da^2/(Da^2*Db), Dc^2*Db/(Db*Dc^2),
 Db^-1*Da/(Da^-1*Db^-3), Db*Da^-1/(Da*Db^3),
 Dc^-1*Db/(Db^3*Dc), Dc*Db^-1/(Db^-3*Dc^-1)];;
Need(Length(Set(Dwords))=1 and Order(Dwords[1])=2,"six common source-relator values");
Need(ForAll(Drot,x->x*Dwords[1]=Dwords[1]*x),"common value central in rotation image");
Need(not Dwords[1] in Group(Dmarks{[2,3]}),"common quotient detects medial defect");
Print("P218_D_SOURCE_BRIDGE six_equal_relators=true defect_outside_middle=true\n");

TomotopeMarks:=function()
 local a,A,els,ids,faces,cs,c,label,flags,tuple,i,j,f,neighbors,marks,p,I,J;
 a:=[(5,10)(6,9)(7,12)(8,11),(1,6)(2,5)(3,8)(4,7),
     (5,9)(6,10)(7,11)(8,12),(5,8)(6,7)(9,12)(10,11)];
 A:=Group(a);Need(Size(A)=96,"source automorphism order");
 Need(List([[1,2],[2,3],[2,4]],ij->Order(a[ij[1]]*a[ij[2]]))=[3,3,4],
      "primary diagram adjacent orders");
 Need(ForAll([[1,3],[1,4],[3,4]],ij->Order(a[ij[1]]*a[ij[2]])=2),
      "primary diagram commuting pairs");
 Need((a[1]*a[2]*a[4])^3=() and (a[3]*a[2]*a[4])^3=(),
      "primary hemioctahedron and hemicuboctahedron relations");
 for I in Combinations([1..4]) do for J in Combinations([1..4]) do
   Need(Intersection(Subgroup(A,a{I}),Subgroup(A,a{J}))=
        Subgroup(A,a{Intersection(I,J)}),"primary diagram all-subset intersection");
 od;od;
 els:=AsSSortedList(A);faces:=[];
 for ids in [[2,3,4],[1,3,4],[1,2],[1,2,3],[1,2,4]] do
   cs:=RightCosets(A,Subgroup(A,a{ids}));
   Add(faces,List(cs,c->Set(AsList(c),x->PositionSorted(els,x))));
 od;
 Need(List(faces,Length)=[4,12,16,4,4],"source face counts");
 faces[4]:=Concatenation(faces[4],faces[5]);Unbind(faces[5]);
 # Enumerate every pairwise-incident tuple, rather than just the group orbits.
 flags:=[];
 for tuple in Cartesian(List(faces,f->[1..Length(f)])) do
   if ForAll(Combinations([1..4],2),ij->
       not IsEmpty(Intersection(faces[ij[1]][tuple[ij[1]]],
                                faces[ij[2]][tuple[ij[2]]]))) then Add(flags,tuple);fi;
 od;
 Need(Length(flags)=192,"complete incidence flag enumeration");
 marks:=[];
 for i in [1..4] do
   p:=[];
   for f in flags do
     neighbors:=Filtered([1..192],j->flags[j][i]<>f[i] and
       ForAll(Difference([1..4],[i]),k->flags[j][k]=f[k]));
     Need(Length(neighbors)=1,"literal diamond flag adjacency");Add(p,neighbors[1]);
   od;
   Add(marks,PermList(p));
 od;
 Need(Size(Group(marks))=18432,"monodromy order");
 Print("P218_TOMOTOPE_BRIDGE aut=96 faces=[4,12,16,4,4] allflags=192 monodromy=18432\n");
 return marks;
end;;

Surface:=function(name,s)
 local G,els,n,cols,reg,edges,eid,v,i,w,colors,faces,ef,es,pair,orb,
       f,vs,start,step,edge,sgn,q,chi,dsu,lookup,solve,whole,pairs,ans,
       ij,A,B,C,selectedE,selectedF,comp,expected,localrows,ids,H,localE,
       localF,bdy,bdyverts,bdygroup,bdyadj,todo,unseen,bb,x,y,e;
 G:=Group(s);els:=AsSSortedList(G);n:=Length(els);
 Need(els[1]=One(G),"identity is initial Cayley vertex");
 Need(Length(s)=4 and ForAll(s,x->Order(x)=2) and Length(Set(s))=4,"distinct involutions");
 for pair in [[1,3],[1,4],[2,4]] do
   Need(Size(Group(s{pair}))=4,"nonadjacent Klein pair");
 od;
 cols:=List(s,x->List(els,g->PositionSorted(els,g*x)));
 reg:=List(cols,PermList);edges:=[];eid:=List([1..n],x->[0,0,0,0]);
 for v in [1..n] do for i in [1..4] do
   w:=cols[i][v];
   if v<w then Add(edges,[v,w,i]);eid[v][i]:=Length(edges);eid[w][i]:=Length(edges);fi;
 od;od;
 faces:=[];ef:=List(edges,e->[]);es:=List(edges,e->[]);
 for pair in [[1,3],[1,4],[2,4],[2,3]] do
   for orb in Orbits(Group(reg{pair}),[1..n]) do
     vs:=Set(orb);Add(faces,rec(colors:=pair,vertices:=vs));f:=Length(faces);
     start:=vs[1];v:=start;step:=0;
     repeat
       i:=pair[1+(step mod 2)];w:=cols[i][v];edge:=eid[v][i];
       if v<w then sgn:=1;else sgn:=-1;fi;
       Add(ef[edge],f);Add(es[edge],sgn);v:=w;step:=step+1;
     until v=start;
     Need(step=Length(vs),"simple two-colored face cycle");
   od;
 od;
 Need(Length(edges)=2*n and ForAll(ef,x->Length(x)=2),"closed surface edge counts");
 q:=Order(s[2]*s[3]);chi:=n-Length(edges)+Length(faces);
 Need(chi=n/(2*q)-n/4,"Euler formula");
 # Independent signed union-find, instead of the author's dual BFS algorithm.
 solve:=function(se,sf)
   local par,sign,bad,sz,find,e,a,b,ra,rb,sa,sb,z,roots,out,j,k;
   par:=[1..Length(faces)];sign:=List(par,x->1);bad:=List(par,x->false);
   find:=function(a)
     local r,p;
     r:=a;p:=1;
     while par[r]<>r do p:=p*sign[r];r:=par[r];od;
     return [r,p];
   end;
   for e in Difference([1..Length(edges)],se) do
     a:=ef[e][1];b:=ef[e][2];Need(not a in sf and not b in sf,"complement edge boundary");
     ra:=find(a);rb:=find(b);z:=-es[e][1]*es[e][2];
     if ra[1]=rb[1] then
       if rb[2]<>z*ra[2] then bad[ra[1]]:=true;fi;
     else
       par[rb[1]]:=ra[1];sign[rb[1]]:=z*ra[2]*rb[2];
       bad[ra[1]]:=bad[ra[1]] or bad[rb[1]];
     fi;
   od;
   out:=Difference([1..Length(faces)],sf);roots:=List(out,j->find(j)[1]);
   return List(Set(roots),r->[Number(roots,x->x=r),not bad[r]]);
 end;
 whole:=solve([],[]);Need(Length(whole)=1,"connected closed surface");
 pairs:=[[[1,2,3],[2,3,4]],[[1,2],[2,3]],[[2,3],[3,4]]];ans:=[];
 for ij in pairs do
   A:=Set(Orbit(Group(reg{ij[1]}),1));B:=Set(Orbit(Group(reg{ij[2]}),1));
   C:=Set(Orbit(Group(reg{Intersection(ij[1],ij[2])}),1));
   selectedE:=Filtered([1..Length(edges)],e->
       (edges[e][1] in A and edges[e][3] in ij[1]) or
       (edges[e][1] in B and edges[e][3] in ij[2]));
   selectedF:=Filtered([1..Length(faces)],f->
       (IsSubset(ij[1],faces[f].colors) and IsSubset(A,faces[f].vertices)) or
       (IsSubset(ij[2],faces[f].colors) and IsSubset(B,faces[f].vertices)));
   comp:=solve(selectedE,selectedF);
   Add(ans,rec(selected:=Length(selectedF),components:=comp,
     intersection:=Length(Intersection(A,B)),middle:=Length(C)));
 od;
 Print("P218_SURFACE ",name," cells=",[n,Length(edges),Length(faces)],
       " chi=",chi," orientable=",whole[1][2]," middle=",q," tests=",ans,"\n");
 if name="D256" then
   Need([n,Length(edges),Length(faces)]=[256,512,224] and whole[1][2],"D closed surface");
   Need(List(ans,x->x.components)=[[[178,true]],[[223,true]],[[223,true]]],"D complements");
   localrows:=[];
   for ids in [[1,2,3],[2,3,4]] do
     H:=Set(Orbit(Group(reg{ids}),1));
     localE:=Filtered([1..Length(edges)],e->edges[e][1] in H and edges[e][3] in ids);
     localF:=Filtered([1..Length(faces)],f->IsSubset(ids,faces[f].colors) and IsSubset(H,faces[f].vertices));
     bdy:=Filtered(localE,e->Length(Intersection(ef[e],localF))=1);
     bdyverts:=Set(Concatenation(List(bdy,e->edges[e]{[1,2]})));
     unseen:=ShallowCopy(bdyverts);bb:=[];
     while not IsEmpty(unseen) do
       todo:=[unseen[1]];RemoveSet(unseen,todo[1]);
       for x in todo do for e in bdy do
         if x=edges[e][1] then y:=edges[e][2];
         elif x=edges[e][2] then y:=edges[e][1];else y:=0;fi;
         if y in unseen then Add(todo,y);RemoveSet(unseen,y);fi;
       od;od;
       Add(bb,Length(todo));
     od;
     Add(localrows,[Length(H),Length(localE),Length(localF),SortedList(bb)]);
   od;
   Need(ForAll(localrows,x->x=[64,96,24,[8,8,8,8,8,8,8,8]]),"D end surfaces and boundaries");
   Print("P218_D_ENDS ",localrows,"\n");
 elif name="Tomotope" then
   Need([n,Length(edges),Length(faces)]=[18432,36864,14592] and not whole[1][2],"Tomotope closed surface");
   Need(List(ans,x->x.components)=[[[14090,false]],[[14591,false]],[[14591,false]]],"Tomotope complements");
 fi;
 return ans;
end;;
Dmarks[1]:=();; Surface("D256",Dmarks);;
Surface("Tomotope",TomotopeMarks());;
Print("P218_INDEPENDENT_PASS\n");
QUIT_GAP(0);
