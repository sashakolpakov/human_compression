SetInfoLevel(InfoWarning,0);;
Control:=function()
 local n,q,F,G,I,t,C,classes,count,rows,i,h,a,els,N,solutions,order,j;
 rows:=[];
 for a in [[4,2],[4,4],[6,2]]do
  n:=a[1];q:=a[2];F:=GF(q);G:=Sp(n,q);I:=IdentityMat(n,F);t:=StructuralCopy(I);
  for i in [1..n/2]do t[i][n+1-i]:=One(F);od;
  if not t in G or RankMat(t-I)<>n/2 then Error("literal nonalternating involution");fi;
  C:=Centralizer(G,t);classes:=ConjugacyClasses(C);count:=Sum(Filtered(classes,c->Order(Representative(c))=2),Size);
  if n=4 then
   if Size(C)<>q^4 or count<>2*q^3-q^2-1 then Error("actual Sp4 centralizer count");fi;
  elif Size(C)<>384 or count>255 then Error("actual Sp6 centralizer bound");fi;
  Add(rows,[n,q,Size(C),count]);
 od;
 F:=GF(3);G:=Sp(4,3);I:=IdentityMat(4,F);els:=Elements(G);
 if Length(els)<>51840 then Error("whole Sp4 order");fi;
 for a in [1,2]do
  if a=1 then h:=DiagonalMat([One(F),One(F),-One(F),-One(F)]);
  else h:=NullMat(4,4,F);for i in [1,2]do h[i][i+2]:=One(F);h[i+2][i]:=-One(F);od;fi;
  N:=Filtered(els,g->g*h=h*g or g*h=-h*g);
  solutions:=Number(N,g->g*g=I or g*g=-I);
  count:=solutions/2-1;
  if (a=1 and (Length(N)<>96 or count<>19))or(a=2 and(Length(N)<>192 or count<>27))then Error("actual odd projective normalizer");fi;
  Add(rows,["actual_projective_normalizer",a,Length(N)/2,count]);
 od;
 Print("PASS_INDEPENDENT_ACTUAL_CENTRALIZERS ",rows,"\n");
end;;
Control();
QUIT;
