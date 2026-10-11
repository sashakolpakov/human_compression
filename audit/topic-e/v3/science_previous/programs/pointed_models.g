# Validation of the uniform pointed-triple proof; not a finite proof premise.
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
CheckModel:=function(prm)
 local q,k,F,o,z,t,a,b,c,r,pp,G,endA,endB,mid,p,d,sq,target,invfields,e,img,aut;
 q:=prm[1];k:=prm[2];F:=GF(q);o:=One(F);z:=Zero(F);t:=Z(q)^((q-1)/k);
 a:=[[-t^-1,o],[z,o]];b:=[[t,z],[z,o]];c:=[[o,z],[o+t,-t]];r:=[[-o,o],[z,o]];
 pp:=List([a,b,c],M->ProjectivePerm(M,F));G:=Group(pp);endA:=Group(pp{[1,2]});endB:=Group(pp{[2,3]});mid:=Group(pp[2]);
 Need(Order(pp[1]*pp[2])=2 and Order(pp[2]*pp[3])=2 and Order(Product(pp))=2,"relations");
 Need(Intersection(endA,endB)=mid and Size(Intersection(Group(pp[1]),mid))=1 and Size(Intersection(Group(pp[3]),mid))=1,"intersection");
 p:=Characteristic(F);d:=DegreeOverPrimeField(F);sq:=p=2 or t^((q-1)/2)=o;
 if sq and p<>2 then target:=q*(q^2-1)/2;else target:=q*(q^2-1);fi;
 Need(Size(G)=target and Size(endA)=q*k and Size(endB)=q*k,"orders");
 invfields:=Filtered([1..d-1],e->t^(p^e)=t^-1);
 if Length(invfields)>0 then
  e:=invfields[1];img:=List([a,b,c],M->ProjectivePerm(r*List(M,row->List(row,x->x^(p^e)))*r,F));
  Need(img=[pp[1]^-1,pp[1]^2*pp[2],pp[3]],"semilinear images");
  aut:=GroupHomomorphismByImages(G,G,pp,img);Need(aut<>fail and IsBijective(aut),"actual reversing automorphism");
 fi;
 Print("POINTED ",rec(q:=q,k:=k,group_order:=Size(G),end_order:=Size(endA),intersection:=Size(Intersection(endA,endB)),field_reversal:=invfields),"\n");
end;
for prm in [[4,3],[5,4],[8,7],[9,4],[13,6],[16,15],[25,6],[25,12],[27,26],[49,24]] do CheckModel(prm); od;
Print("POINTED_PASS\n");QUIT;
