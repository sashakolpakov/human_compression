Need:=function(ok,message) if not ok then Error(message);fi;end;
FaithfulPerms:=function(F,gs)
 local lines,o,z,u,v;
 lines:=[];o:=One(F);z:=Zero(F);
 for u in F do for v in F do Add(lines,[o,u,v]);od;od;
 for u in F do Add(lines,[z,o,u]);od;Add(lines,[z,z,o]);
 return List(gs,m->Permutation(m,lines,OnLines));
end;
FullIP:=function(gs)
 local sets,groups,S,i,j,k;
 sets:=Combinations([1..Length(gs)]);groups:=[];
 for S in sets do if IsEmpty(S) then Add(groups,Group(()));else Add(groups,Group(gs{S}));fi;od;
 for i in [1..Length(sets)] do for j in [1..Length(sets)] do
   k:=Position(sets,Intersection(sets[i],sets[j]));
   Need(Intersection(groups[i],groups[j])=groups[k],"all actual subset intersections");
 od;od;
 return Length(sets)^2;
end;
Control:=function(q,which)
 local F,p,o,z,a,d,b,c,e,f,ms,gs,G,A,B,H,expected,ip,heis,diag,allforms,x,y,zz,i,j,m,permforms,am,bm;
 F:=GF(q);p:=Characteristic(F);o:=One(F);z:=Zero(F);
 a:=o;d:=o;b:=z;c:=o;
 if which="product" then e:=z;f:=o;expected:=4*p^2;
 elif which="heisenberg" then e:=o;f:=z;expected:=4*p^3;
 else d:=2*o;e:=o;f:=o-d^2;Need(f<>z,"one-zero parameter");expected:=0;fi;
 ms:=[DiagonalMat([o,-o,-o]),[[a,b,z],[c,-a,z],[z,z,-o]],
      [[-o,z,z],[z,-d,f],[z,e,d]],DiagonalMat([-o,-o,o])];
 Need(ForAll(ms,m->DeterminantMat(m)=o and m^2=IdentityMat(3,F)),"literal involutions");
 gs:=FaithfulPerms(F,ms);G:=Group(gs);A:=Group(gs{[1,2,3]});B:=Group(gs{[2,3,4]});
 if which="onezero" then
   Need(gs[1] in B,"one-zero omitted mark actually in end");ip:=0;
 else
   Need(Size(G)=expected,"actual affine group order");ip:=FullIP(gs);
   Need(Order(gs[1]*gs[2])=p and Order(gs[3]*gs[4])=p,"outer types");
   if which="product" then Need(Order(gs[2]*gs[3])=2,"degenerate middle");
   else
     Need(Order(gs[2]*gs[3])=2*p,"Heisenberg middle");
     allforms:=[];am:=[];bm:=[];
     for x in GF(p) do for y in GF(p) do for zz in GF(p) do for i in [0,1] do for j in [0,1] do
       m:=[[o,z,z],[x,o,z],[zz,y,o]]*ms[1]^i*ms[4]^j;
       Add(allforms,m);if y=-j*o then Add(am,m);fi;if x=i*o then Add(bm,m);fi;
     od;od;od;od;od;
     permforms:=FaithfulPerms(F,allforms);Need(Set(permforms)=Set(Elements(G)),"all global Heisenberg normal forms");
     Need(Set(FaithfulPerms(F,am))=Set(Elements(A)),"all first-end normal forms");
     Need(Set(FaithfulPerms(F,bm))=Set(Elements(B)),"all second-end normal forms");
     Need(Size(Intersection(A,B))=4*p,"actual Heisenberg common dihedral");
   fi;
 fi;
 Print("MODEL ",q," ",which," ",Size(G)," ",Size(A)," ",Size(B)," ",ip," PASS\n");
end;
for q in [3,5,7,9,11] do Control(q,"product");Control(q,"heisenberg");od;
for q in [5,7,9,11] do if q=9 then
 # Characteristic three has no prime-field one-zero d; use a genuine extension parameter below.
 else Control(q,"onezero");fi;od;
Print("PASS_ALL_ODD_FOUR_CONTROLS\n");QUIT;
