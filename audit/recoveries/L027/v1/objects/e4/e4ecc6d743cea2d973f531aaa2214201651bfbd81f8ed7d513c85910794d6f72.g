Need:=function(ok,message) if not ok then Error(message); fi; end;
Control:=function(q)
  local F,o,z,n,prims,x,a,b,c,U,V,ex,gr,lam,src,tgt,eq,rr,i,j,k,l,t,coeff,basis,vec,P,count,cases,rows;
  F:=GF(q);o:=One(F);z:=Zero(F);n:=DegreeOverPrimeField(F);
  prims:=Filtered(AsList(F),x->x<>z and Order(x)=q-1);
  cases:=0;rows:=[];
  for x in prims do
    a:=[[x,o,z],[z,o+x^-1,-x^-1],[z,o,z]];
    b:=[[-x^-1,z,z],[z,z,o],[z,x,z]];
    c:=[[x,z,z],[x-x^-1,o,z],[x-x^-1,z,x^-1]];
    U:=a*b;V:=U*c;
    for ex in [0..n-1] do for gr in [0,1] do
      src:=[a,U,V];
      if gr=1 then src:=List(src,g->TransposedMat(g^-1));fi;
      src:=List(src,g->List(g,r->List(r,t->t^(Characteristic(F)^ex))));
      for lam in Filtered(AsList(F),t->t<>z and t^3=o) do
        tgt:=[lam*a^-1,U,V];eq:=[];
        for t in [1..3] do for i in [1..3] do for j in [1..3] do
          rr:=[];
          for k in [1..3] do for l in [1..3] do
            coeff:=z;
            if i=k then coeff:=coeff+src[t][l][j];fi;
            if l=j then coeff:=coeff-tgt[t][i][k];fi;
            Add(rr,coeff);
          od;od;
          Add(eq,rr);
        od;od;od;
        basis:=NullspaceMat(TransposedMat(eq));
        # All vector-space points, including singular matrices, are inspected.
        Need(Length(basis)<=2,"unexpected large intertwiner space");
        count:=0;
        if Length(basis)=0 then
          vec:=List([1..9],i->z);
          Need(Determinant(List([0..2],i->vec{[3*i+1..3*i+3]}))=z,"zero matrix");
          count:=1;
        else
          for coeff in Tuples(AsList(F),Length(basis)) do
            vec:=List([1..9],i->Sum([1..Length(basis)],j->coeff[j]*basis[j][i]));
            P:=List([0..2],i->vec{[3*i+1..3*i+3]});
            Need(ForAll([1..3],j->P*src[j]=tgt[j]*P),"literal equations");
            Need(Determinant(P)=z,"unexpected invertible reversing intertwiner");
            count:=count+1;
          od;
        fi;
        cases:=cases+1;Add(rows,[ex,gr,Length(basis),count]);
      od;
    od;od;
  od;
  Print("FIELD ",q," PRIMITIVES ",Length(prims)," CASES ",cases," NULLITY_MAX ",Maximum(List(rows,r->r[3]))," MATRICES ",Sum(rows,r->r[4])," PASS\n");
end;
for q in [5,7,8,9,13] do Control(q);od;
Print("PASS_ALL_PROJECTIVE_SEMILINEAR_AND_GRAPH_REVERSAL_CONTROLS\n");
QUIT;
