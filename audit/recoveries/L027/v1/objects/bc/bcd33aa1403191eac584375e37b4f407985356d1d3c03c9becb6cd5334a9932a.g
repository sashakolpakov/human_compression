Need:=function(ok,message) if not ok then Error(message);fi;end;
Elm:=function(F,i,j,x) local m;m:=IdentityMat(3,F);m[i][j]:=m[i][j]+x;return m;end;
ProjectivelyCommute:=function(F,A,B)
 local c;
 for c in F do if c<>Zero(F) and c^3=One(F) and A*B=c*(B*A) then return true;fi;od;
 return false;
end;
EvenControl:=function(q)
 local F,o,z,a,b,R,u,x,t,f,S2,A,B,count;
 F:=GF(q);o:=One(F);z:=Zero(F);a:=PrimitiveElement(F);b:=a^-1;
 R:=[Elm(F,2,3,o),Elm(F,3,1,a),Elm(F,1,3,b),Elm(F,2,1,o)];u:=[z,o,a];count:=0;
 for x in F do for t in F do
  if x<>z or t<>z then
   f:=[x,a*t,t];S2:=IdentityMat(3,F)+List(u,c->c*f);
   Need(S2^2=IdentityMat(3,F) and DeterminantMat(S2)=o,"even actual involution");
   A:=R[4]*S2;B:=R[3]*R[4];Need(not ProjectivelyCommute(F,A,B),"even actual projective obstruction");count:=count+1;
  fi;
 od;od;
 Print("EVEN ",q," ",count," PASS\n");
end;
OddControl:=function(q)
 local F,o,z,u,v,A,B,count;
 F:=GF(q);o:=One(F);z:=Zero(F);count:=0;B:=Elm(F,3,2,-o);
 for u in F do for v in F do if u<>z or v<>z then
   A:=Elm(F,1,3,-u)*Elm(F,2,3,-v);Need(not ProjectivelyCommute(F,A,B),"odd actual projective obstruction");count:=count+1;
 fi;od;od;
 Print("ODD ",q," ",count," PASS\n");
end;
SmallUnitary:=function()
 local F,G,lines,o,z,x,y,gs,P,inv,a,b,count;
 F:=GF(4);G:=SU(3,2);o:=One(F);z:=Zero(F);lines:=[];
 for x in F do for y in F do Add(lines,[o,x,y]);od;od;
 for x in F do Add(lines,[z,o,x]);od;Add(lines,[z,z,o]);
 gs:=List(GeneratorsOfGroup(G),m->Permutation(m,lines,OnLines));P:=Group(gs);
 Need(Size(G)=216 and Size(P)=72,"actual SU and PSU orders");
 inv:=Filtered(Elements(P),g->Order(g)=2);count:=0;
 for a in inv do for b in inv do if a<>b then Need(a*b<>b*a,"unitary distinct commuting exclusion");count:=count+1;fi;od;od;
 Print("UNITARY 2 ",Size(G)," ",Size(P)," ",Length(inv)," ",count," PASS\n");
end;
for q in [4,8,16] do EvenControl(q);od;
for q in [3,5,7,9] do OddControl(q);od;
SmallUnitary();Print("PASS_RANK_OBSTRUCTION_CONTROLS\n");QUIT;
