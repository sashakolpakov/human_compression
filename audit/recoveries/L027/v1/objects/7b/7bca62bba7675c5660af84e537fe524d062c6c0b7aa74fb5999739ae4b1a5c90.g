Need:=function(ok,message) if not ok then Error(message);fi;end;
CheckFive:=function(q,k,choice)
  local F,p,o,z,w,aa,bb,cc,dd,lines,u,v,gs,a,b,c,d,G,A,B,H,E,C,expectedB,tests,expected,subsets,subgroups,S,T,i,j,idx,gens,g,ipcount,ss,tt,frob;
  F:=GF(q);p:=Characteristic(F);o:=One(F);z:=Zero(F);
  w:=PrimitiveElement(F)^((q-1)/3*choice);
  Need(DegreeOverPrimeField(F)<=2 and (q=p or p mod 3=2),"exact field scope");
  aa:=DiagonalMat([o,w,w^2]);
  bb:=[[-o,z,-k*o],[z,-w^2,-k*w^2],[z,z,w]];
  cc:=[[o,k*o,z],[z,k*o,o],[z,-o,z]];
  dd:=[[z,o,z],[z,z,o],[o,z,z]];
  lines:=[];
  for u in F do for v in F do Add(lines,[o,u,v]);od;od;
  for u in F do Add(lines,[z,o,u]);od;Add(lines,[z,z,o]);
  gs:=List([aa,bb,cc,dd],m->Permutation(m,lines,OnLines));
  Need(ForAll(gs,IsPerm),"actual projective action");
  a:=gs[1];b:=gs[2];c:=gs[3];d:=gs[4];G:=Group(gs);
  A:=Group(a,b,c);B:=Group(b,c,d);H:=Group(a,b);E:=Group(b,c);C:=Group(c,d);
  Need(Size(G)=q^3*(q^3-1)*(q^2-1)/3,"full PSL3");
  Need(Size(A)=2*q^3*(q^2-1),"restricted first parabolic");
  if k=1 then
    expectedB:=Size(A);Need(Size(E)=12*q^2 and Size(C)=6*p^2,"point middle and end pair");
    Need(List(gs,Order)=[3,6,6,3],"positive type");
  else
    expectedB:=q*(q^2-1);
    if (-o)^((q-1)/2)=o then expectedB:=expectedB/2;fi;
    Need(Size(E)=6*q and Size(C)=12,"conic middle and tetrahedron");
    Need(List(gs,Order)=[3,6,3,3],"negative type");
  fi;
  Need(Size(B)=expectedB,"second end order");Need(Size(H)=6*p^2,"first pair translation size");
  tests:=[Size(Intersection(Group(a),Group(b))),Size(Intersection(Group(b),Group(c))),Size(Intersection(H,E)),Size(Intersection(A,B)),Size(Intersection(A,C)),Size(Intersection(A,Group(d)))];
  expected:=[1,1,6,Size(E),Order(c),1];Need(tests=expected,"all recursive actual intersections");
  for i in [1..3] do for j in [i+1..4] do Need(Order(Product(gs{[i..j]}))=2,"nonidentity interval involution");od;od;
  if q<>p then
    frob:=m->List(m,r->List(r,x->x^p));
    Need(frob(aa)=aa^-1,"Frobenius reverses a");
    for g in [aa*bb,aa*bb*cc,aa*bb*cc*dd] do Need(frob(g)=g,"Frobenius fixes prefix");od;
  fi;
  ipcount:=0;
  if q=7 and choice=1 then
    subsets:=Combinations([0..4]);subgroups:=[];
    for S in subsets do
      gens:=[];
      for i in [1..4] do for j in [i..4] do if i-1 in S and j in S then Add(gens,Product(gs{[i..j]}));fi;od;od;
      if Length(gens)=0 then Add(subgroups,Group(()));else Add(subgroups,Group(gens));fi;
    od;
    for ss in [1..Length(subsets)] do for tt in [1..Length(subsets)] do
      idx:=Position(subsets,Intersection(subsets[ss],subsets[tt]));
      Need(Intersection(subgroups[ss],subgroups[tt])=subgroups[idx],"full indexed rotation IP");ipcount:=ipcount+1;
    od;od;
  fi;
  Print("FIELD ",q," SIGN ",k," ROOT ",choice," GROUP ",Size(G)," A ",Size(A)," B ",Size(B)," H ",Size(H)," E ",Size(E)," C ",Size(C)," ALL_IP ",ipcount," PASS\n");
end;
for q in [7,13,19,25] do for k in [1,-1] do for choice in [1,2] do CheckFive(q,k,choice);od;od;od;
Print("PASS_ALL_SIXTEEN_RANK_FIVE_CONTROLS\n");QUIT;
