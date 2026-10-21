Need:=function(b,s)if not b then Error(s);fi;end;
q:=17;F:=GF(q^2);o:=One(F);z:=Zero(F);I:=IdentityMat(3,F);
Bar:=x->x^q;Star:=A->TransposedMat(List(A,row->List(row,Bar)));
HNorm:=x->x*Bar(x);
alpha:=First(Elements(F),x->HNorm(x)=3*o);Need(alpha<>fail,"norm3");
Hom:=function(v)local n; n:=Sum(List(v,HNorm));return -I+2*List(v,x->List(v,y->x*Bar(y)))/n;end;
w:=Hom([z,z,o]);u:=Hom([alpha,z,o]);Need(Order(u*w)=3,"normalized pair");
centres:=[];records:=[];kcount:=[0,0,0];ks:=[7,8,9];
for x in Elements(F)do for y in Elements(F)do if HNorm(x)+HNorm(y)=3*o then
 v:=Hom([x,y,o]);Need(v^2=I and v*Star(v)=I and DeterminantMat(v)=o,"unitary homology");
 Need(Order(w*v)=3,"second normalized pair");Add(centres,[x,y]);
 b:=v*w*u;
 for k in ks do
  pow:=b^k;
  if IsDiagonalMat(pow) and pow[1][1]=pow[2][2] and pow[1][1]=pow[3][3] then
   Need(ForAll(DivisorsInt(k){[1..Length(DivisorsInt(k))-1]},d->not IsDiagonalMat(b^d) or not ((b^d)[1][1]=(b^d)[2][2] and (b^d)[1][1]=(b^d)[3][3])),"exact projective order");
   kcount[Position(ks,k)]:=kcount[Position(ks,k)]+1;
   Add(records,rec(k:=k,x:=x,y:=y,trace:=x/alpha+Bar(x/alpha),u:=u,v:=v,w:=w));
  fi;
 od;
fi;od;od;
Print("CENTRES ",Length(centres)," TYPES ",ks," COUNTS ",kcount,"\n");
Print("TRACE_NONZERO ",List(ks,k->Number(records,r->r.k=k and r.trace<>0*r.trace)),"\n");
PrintTo("centres_records.g","q:=",q,";alpha:=",alpha,";records:=",records,";\n");
Print("PASS_LITERAL_CENTRES_NO_GENERATION_IP_OR_CHIRALITY_CLAIM\n");QUIT;
