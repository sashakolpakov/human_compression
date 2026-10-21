# Exact validation of the corrected four-family regular scope.
Need:=function(ok,msg) if not ok then Error(Concatenation("L007_REJECT: ",msg));fi;end;
IP:=function(rs,target)
 local g,subs,I,J,ij;
 g:=Group(rs);Need(Size(g)=target,"full regular generation/order");
 Need(ForAll(rs,r->Order(r)=2) and rs[1]*rs[3]=rs[3]*rs[1],"string involutions");
 subs:=Combinations([1..3]);
 for I in subs do for J in subs do
  ij:=Intersection(I,J);
  Need(Intersection(Subgroup(g,rs{I}),Subgroup(g,rs{J}))=Subgroup(g,rs{ij}),"full subset IP");
 od;od;
 return [Order(rs[1]*rs[2]),Order(rs[2]*rs[3])];
end;
CyclotomicRegular:=function(p,n)
 local e,r,mods,A,gg,ss,i,ims,T,P,ep,eb,s,beta,sig,tau,K,R,er,ek,sg,tg,bg,sp,rs,a,b,c,ty1,ty2;
 e:=QuoInt(n-1,p-1)+1;r:=(n-1) mod (p-1)+1;
 mods:=Concatenation(List([1..r],i->p^e),List([r+1..p-1],i->p^(e-1)));
 A:=AbelianGroup(IsPcGroup,Filtered(mods,k->k>1));gg:=GeneratorsOfGroup(A);
 ss:=List([1..p-1],i->One(A));for i in [1..Length(gg)] do ss[i]:=gg[i];od;
 ims:=List([1..p-2],i->ss[i]*ss[i+1]);
 Add(ims,ss[p-1]*Product([1..p-1],j->ss[j]^(-Binomial(p,j))));
 T:=GroupHomomorphismByImages(A,A,ss,ims);Need(T<>fail and Order(T)=p,"cyclotomic action");
 P:=SemidirectProduct(Group(T),A);ep:=Embedding(P,2);eb:=Embedding(P,1);
 s:=Image(ep,ss[1]);beta:=Image(eb,T);
 sig:=GroupHomomorphismByImages(P,P,[s,beta],[s,beta^-1]);
 tau:=GroupHomomorphismByImages(P,P,[s,beta],[s^-1,beta]);
 Need(sig<>fail and tau<>fail,"two module involutions");K:=Group(sig,tau);Need(Size(K)=4,"independent complement");
 R:=SemidirectProduct(K,P);er:=Embedding(R,2);ek:=Embedding(R,1);
 sp:=Image(er,s);bg:=Image(er,beta);sg:=Image(ek,sig);tg:=Image(ek,tau);
 rs:=[sp*tg*sg,bg*tg*sg,sg];ty1:=IP(rs,4*p^(n+1));Need(ty1=[p,2*p],"constant type");
 a:=bg*sp;b:=sp^-1*sg;c:=tg*sg*sp;
 Need(a^c=a^-1 and b^c=b^-1,"literal second-mark reversal");
 ty2:=IP([a*c,c,c*b],4*p^(n+1));Need(ty2=[p,2*p^e],"variable type");
 Print("REGULAR_CYC ",rec(p:=p,n:=n,order:=Size(R),types:=[ty1,ty2],IP_pairs_per_marking:=64),"\n");
end;
MixedRegular:=function(p)
 local f,col,H,hs,x,v,c,theta,C,q,a,E,eh,eb,b0,N,proj,G,xg,bg,delta,R,eg,ed,xx,bb,dd,ty;
 f:=FreeGroup(4);col:=SingleCollector(f,[p,p,p,p]);
 SetPower(col,1,f.4);
 SetConjugate(col,2,1,f.2*f.3^-1);UpdatePolycyclicCollector(col);
 H:=GroupByRws(col);hs:=GeneratorsOfGroup(H);x:=hs[1];v:=hs[2];c:=hs[3];
 Need(Size(H)=p^4 and Comm(x,v)=c and Order(x)=p^2,"mixed Heisenberg normal form");
 theta:=GroupHomomorphismByImages(H,H,[x,v],[v^-1*x^-1,v]);
 Need(theta<>fail and Order(theta)=2*p,"mixed action");
 C:=CyclicGroup(IsPcGroup,2*p);a:=GeneratorsOfGroup(C)[1];
 q:=GroupHomomorphismByImages(C,Group(theta),[a],[theta]);E:=SemidirectProduct(C,q,H);
 eh:=Embedding(E,2);eb:=Embedding(E,1);b0:=Image(eb,a);N:=Group(b0^2*Image(eh,v)^-1);
 Need(Size(N)=p and IsNormal(E,N),"square-root central kernel");
 proj:=NaturalHomomorphismByNormalSubgroup(E,N);G:=Image(proj);xg:=Image(proj,Image(eh,x));bg:=Image(proj,b0);
 Need(Size(G)=2*p^4 and Order(xg*bg)=2,"mixed rotation group");
 delta:=GroupHomomorphismByImages(G,G,[xg,bg],[xg^-1,bg^-1]);
 Need(delta<>fail and Order(delta)=2,"mixed reversal");
 R:=SemidirectProduct(Group(delta),G);eg:=Embedding(R,2);ed:=Embedding(R,1);
 xx:=Image(eg,xg);bb:=Image(eg,bg);dd:=Image(ed,delta);
 ty:=IP([xx*dd,dd,dd*bb],4*p^4);Need(ty=[p^2,2*p],"mixed type");
 Print("REGULAR_MIXED ",rec(p:=p,order:=Size(R),type:=ty,IP_pairs:=64),"\n");
end;
for pp in [3,5,7] do
 CyclotomicRegular(pp,2);CyclotomicRegular(pp,3);MixedRegular(pp);
od;
QUIT_GAP(0);
