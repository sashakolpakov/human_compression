# Finite diagnostics of the uniform written construction, not proof premises.
Need := function(ok,msg) if not ok then Error(Concatenation("L007_REJECT: ",msg)); fi; end;
CarryModel := function(p,n,even)
 local e,r,mods,aa,ag,ss,i,T,ims,zz,m,s,z,tm,dd,ea,ec,cc,cs,ts,dm,
       cp,cpgen,act,E,beta0,em,eb,N,q,P,beta,sp,zp,sig,G,ep,es,a,b,gens,xx;
 e:=QuoInt(n-1,p-1)+1; r:=(n-1) mod (p-1)+1;
 Need(n mod 2=0 and n>=4,"even module length >=4");
 if even then Need(e>=2,"source even extension e>=2");fi;
 mods:=Concatenation(List([1..r],i->p^e),List([r+1..p-1],i->p^(e-1)));
 aa:=AbelianGroup(IsPcGroup,Filtered(mods,k->k>1));ag:=GeneratorsOfGroup(aa);
 ss:=List([1..p-1],i->One(aa));
 for i in [1..Length(ag)] do ss[i]:=ag[i];od;
 ims:=[];
 for i in [1..p-2] do Add(ims,ss[i]*ss[i+1]);od;
 Add(ims,ss[p-1]*Product([1..p-1],j->ss[j]^(-Binomial(p,j))));
 T:=GroupHomomorphismByImages(aa,aa,ss,ims);
 Need(T<>fail and IsBijective(T) and Order(T)=p,"actual cyclotomic automorphism");
 zz:=ss[r]^(p^(e-1));
 if not even then
  m:=aa;s:=ss[1];z:=zz;tm:=T;
 else
  cc:=CyclicGroup(IsPcGroup,p^2);dd:=DirectProduct(aa,cc);
  ea:=Embedding(dd,1);ec:=Embedding(dd,2);cs:=Image(ec,GeneratorsOfGroup(cc)[1]);
  s:=Image(ea,ss[1])*cs;z:=Image(ea,zz);
  dm:=GroupHomomorphismByImages(dd,dd,
      Concatenation(List(ag,g->Image(ea,g)),[cs]),
      Concatenation(List(ag,g->Image(ea,Image(T,g))),[cs]));
  Need(dm<>fail and IsBijective(dm),"product automorphism");
  m:=Group(List([0..p-1],i->Image(dm^i,s)));
  Need(Size(m)=p^(n+1) and z in m,"complete module fibre");
  tm:=GroupHomomorphismByImages(m,m,GeneratorsOfGroup(m),
     List(GeneratorsOfGroup(m),g->Image(dm,g)));
 fi;
 Need(Order(z)=p and Image(tm,z)=z,"nonzero fixed carry");
 cp:=CyclicGroup(IsPcGroup,p^2);cpgen:=GeneratorsOfGroup(cp)[1];
 act:=GroupHomomorphismByImages(cp,Group(tm),[cpgen],[tm]);
 E:=SemidirectProduct(cp,act,m);em:=Embedding(E,2);eb:=Embedding(E,1);
 beta0:=Image(eb,cpgen);
 # GAP's action convention is verified by the exact generator equation.
 Need(ForAll(GeneratorsOfGroup(m),g->Image(em,g)^beta0=Image(em,Image(tm,g))),"right conjugation convention");
 N:=Group(beta0^p*Image(em,z)^-1);Need(Size(N)=p and IsNormal(E,N),"central relation kernel");
 q:=NaturalHomomorphismByNormalSubgroup(E,N);P:=Image(q);
 beta:=Image(q,beta0);sp:=Image(q,Image(em,s));zp:=Image(q,Image(em,z));
 Need(Size(P)=p*Size(m) and beta^p=zp and Order(zp)=p,"extension order/injection/carry");
 Need(Size(Group(beta,sp))=Size(P),"two generators of kernel");
 sig:=GroupHomomorphismByImages(P,P,[beta,sp],[beta^-1,sp]);
 Need(sig<>fail and IsBijective(sig) and Order(sig)=2,"reflection involution");
 G:=SemidirectProduct(Group(sig),P);ep:=Embedding(G,2);es:=Embedding(G,1);
 a:=Image(ep,beta*sp);b:=Image(ep,sp^-1)*Image(es,sig);
 Need(Size(Group(a,b))=Size(G),"marked generation");
 Need([Order(a),Order(b),Order(a*b)]=[p^2,2*p^e,2],"exact marker orders");
 Need(Size(Intersection(Group(a),Group(b)))=1,"cyclic intersection");
 Need(GroupHomomorphismByImages(G,G,[a,b],[a^-1,b^-1])=fail,"no simultaneous inversion");
 Need(Order(a)*Order(b)<Size(G),"non-tightness");
 Print("CARRY ",rec(p:=p,n:=n,even_extension:=even,order:=Size(G),type:=[Order(a),Order(b)],intersection:=1,reversal:=false),"\n");
 return true;
end;
for par in [[3,4,false],[3,6,false],[5,4,false],[7,4,false],[5,6,false],
 [3,4,true],[3,6,true],[5,6,true],[7,8,true]] do
 CarryModel(par[1],par[2],par[3]);
od;
QUIT_GAP(0);
