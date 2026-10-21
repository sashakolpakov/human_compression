# Required exceptional-prime checks for the trace-quadratic classification.
Need:=function(b,m) if not b then Error(m);fi;end;
ProjectivePerm:=function(M,F)
 local pts,n,im,v,w,pos;
 pts:=Elements(F);n:=Length(pts);im:=[];
 for pos in [1..n+1] do
  if pos<=n then v:=[pts[pos],One(F)];else v:=[One(F),Zero(F)];fi;
  w:=v*M;
  if IsZero(w[2]) then Add(im,n+1);else Add(im,Position(pts,w[1]/w[2]));fi;
 od;return PermList(im);
end;
Run:=function()
 local p,F,o,z,root,ts,typ,tr,aa,bb,cc,d,U,V,u,w,A,B,C,J,delta,rt,R,S,rr,H,K,G,rows,one,cs,good,rev,X;
 for p in [11,19] do
  F:=GF(p);o:=One(F);z:=Zero(F);J:=[[z,o],[-o,z]];
  ts:=List(Filtered(Elements(F),v->v^2=5*o),v->(-o+v)/2);
  for typ in [[5,3,5],[3,5,3]] do
   rows:=[];
   for tr in ts do
    if typ=[5,3,5] then aa:=tr;bb:=o;cc:=tr;else aa:=o;bb:=tr;cc:=o;fi;
    d:=aa^2+bb^2-4*o;Need(d<>z,"irreducible seed");
    one:=First(Cartesian(Elements(F),Elements(F)),v->v[1]^2+v[2]^2=d);U:=one[1];V:=one[2];
    u:=(U+aa)/2;w:=(V-bb)/2;A:=[[u,w+bb],[w,aa-u]];B:=A^-1*J;
    delta:=aa^2*cc^2-4*(aa^2+bb^2+cc^2-4*o);
    for rt in Filtered(Elements(F),v->v^2=delta) do
     R:=(-bb*cc*V+rt*U)/d;S:=(bb*cc*U+rt*V)/d;C:=[[(R+cc)/2,S/2],[S/2,(cc-R)/2]];
     Need(List([A,B,C],DeterminantMat)=[o,o,o],"determinants");
     Need(List([A,B,C],TraceMat)=[aa,bb,cc] and ForAll([A*B,B*C,A*B*C],M->TraceMat(M)=z),"all trace equations");
     rr:=List([A,B,C],M->ProjectivePerm(M,F));Need(List(rr,Order)=typ and List([rr[1]*rr[2],rr[2]*rr[3],Product(rr)],Order)=[2,2,2],"exact relations");
     H:=Group(rr{[1,2]});K:=Group(rr{[2,3]});G:=Group(rr);
     Need(Size(H)=60 and Size(K)=60 and Size(G)=p*(p^2-1)/2,"full groups");
     good:=Size(Intersection(H,K))=typ[2];
     Need(Size(Intersection(Group(rr[1]),Group(rr[2])))=1 and Size(Intersection(Group(rr[2]),Group(rr[3])))=1,"cyclic IP");
     if rt<>z then Need(good,"every nonzero discriminant extension is polytopal");fi;
     if rt=z then
      X:=C-(cc/2)*IdentityMat(2,F);rev:=ProjectivePerm(X,F);
      Need(rr[1]^rev=rr[1]^-1 and rr[2]^rev=rr[1]^2*rr[2] and rr[3]^rev=rr[3],"zero discriminant actual reversal");
     fi;
     Add(rows,[Int(tr),Int(rt),Size(Intersection(H,K)),good]);
    od;
   od;
   good:=Length(Filtered(rows,r->r[2]<>0 and r[4]));
   if p=11 and typ=[3,5,3] then Need(good=0,"no chiral PSL11 353");fi;
   if p=19 and typ=[5,3,5] then Need(good=2,"exactly two chiral PSL19 535");fi;
   Print("SMALL ",p," TYPE ",typ," ROWS ",rows," CHIRAL ",good,"\n");
  od;
 od;
 Print("EXCEPTIONAL_SMALL_PASS\n");
end;
Run();QUIT;
