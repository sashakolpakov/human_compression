Need236:=function(ok,msg) if not ok then Error(Concatenation("PHASE236_REJECT ",msg)); fi; end;
IP236:=function(rr)
  local subsets,hs,I,J;
  subsets:=Combinations([1..3]); hs:=List(subsets,I->Group(List(I,i->rr[i]),()));
  for I in [1..8] do for J in [1..8] do
    if Intersection(hs[I],hs[J])<>hs[Position(subsets,Intersection(subsets[I],subsets[J]))] then
      return false;
    fi;
  od;od;return true;
end;
Run236:=function()
local row,p,m,s,beta,sigma,tau,P,A,ss,i,u,v,rr,G,par,a,b,points,x,y,r0,r1,r2;
for row in PHASE236_DATA do
  p:=row.p; m:=row.m; s:=row.s; beta:=row.beta; sigma:=row.sigma; tau:=row.tau;
  P:=Group(s,beta); A:=Subgroup(P,Orbit(Group(beta),s,OnPoints));
  Need236(Size(A)=p^(m-1) and IsAbelian(A),"abelian lattice order");
  Need236(Size(P)=p^m and not IsAbelian(P),"nonabelian kernel order");
  Need236(Order(beta)=p and Order(sigma)=2 and Order(tau)=2 and Comm(sigma,tau)=(),"complement");
  Need236(s^sigma=s and beta^sigma=beta^-1 and s^tau=s^-1 and beta^tau=beta,"source automorphisms");
  ss:=[s]; for i in [2..p-1] do Add(ss,Comm(ss[i-1],beta)); od;
  Need236(List(ss,Order)=row.moduli,"every source generator order");
  for u in ss do for v in ss do Need236(Comm(u,v)=(),"source abelian relators");od;od;
  Need236(Comm(ss[p-1],beta)=Product([1..p-1],i->ss[i]^(-Binomial(p,i))),"last source commutator");
  rr:=[s*tau*sigma,beta*tau*sigma,sigma]; G:=Group(rr);
  Need236(ForAll(rr,x->Order(x)=2),"marked involutions");
  Need236(Comm(rr[1],rr[3])=(),"string relation");
  Need236([Order(rr[1]*rr[2]),Order(rr[2]*rr[3])]=[p,2*p],"type");
  Need236(Size(G)=4*p^m,"full generation and order");
  Need236(IP236(rr),"all 64 intersection equalities");
  Need236(NilpotencyClassOfGroup(P)=m-1,"maximal class");
  Print("CYCLOTOMIC p=",p," m=",m," order=",Size(G)," moduli=",row.moduli," IP=64 PASS\n");
od;
# Independent affine models for the abelian classification, including unequal exponents.
for par in [[3,1,1],[3,1,2],[3,2,2],[5,1,2]] do
  p:=par[1]; a:=par[2]; b:=par[3]; points:=Cartesian([0..p^b-1],[0..p^a-1]);
  x:=PermList(List(points,v->Position(points,[(v[1]+1) mod p^b,v[2]])));
  y:=PermList(List(points,v->Position(points,[v[1],(v[2]+1) mod p^a])));
  r0:=PermList(List(points,v->Position(points,[v[1],(-v[2]) mod p^a])));
  r2:=PermList(List(points,v->Position(points,[(-v[1]) mod p^b,(-v[2]) mod p^a])));
  r1:=x*y*r2;
  rr:=[r0,r1,r2]; G:=Group(rr);
  Need236(ForAll(rr,r->Order(r)=2),"abelian marked involutions");
  Need236(Size(G)=4*p^(a+b),"abelian group order");
  Need236([Order(r0*r1),Order(r1*r2)]=[2*p^a,p^b],"abelian type");
  Need236(IP236(rr),"abelian intersection property");
  Need236((x*y*r0)^2=x^2 and x^2<>(),"literal source marking defect");
  Print("ABELIAN p=",p," a=",a," b=",b," order=",Size(G)," IP=64 BAD_MARKING_REJECTED\n");
od;
Print("PHASE236_FINITE_PASS\n");
end;
Run236();
QUIT;
