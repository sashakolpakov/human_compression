Need:=function(ok,msg)if not ok then Error(msg);fi;end;
CensusCentres:=function(q)
 local F,o,z,I,Bar,Star,HNorm,alpha,Homology,Scalar,w,u,centres,records,kcount,ks,x,y,v,b,k,pow,exact,d;
 F:=GF(q^2);o:=One(F);z:=Zero(F);I:=IdentityMat(3,F);
 Bar:=x->x^q;Star:=A->TransposedMat(List(A,row->List(row,Bar)));HNorm:=x->x*Bar(x);
 alpha:=First(Elements(F),x->HNorm(x)=3*o);Need(alpha<>fail,"norm3");
 Homology:=function(v)local n;n:=Sum(List(v,HNorm));return -I+2*List(v,x->List(v,y->x*Bar(y)))/n;end;
 Scalar:=A->IsDiagonalMat(A) and A[1][1]=A[2][2] and A[1][1]=A[3][3];
 w:=Homology([z,z,o]);u:=Homology([alpha,z,o]);Need(Order(u*w)=3,"normalized pair");
 centres:=[];records:=[];kcount:=[0,0,0];ks:=[7,8,9];
 for x in Elements(F)do for y in Elements(F)do if HNorm(x)+HNorm(y)=3*o then
  v:=Homology([x,y,o]);Need(v^2=I and v*Star(v)=I and DeterminantMat(v)=o,"unitary homology");
  Need(Order(w*v)=3,"second normalized pair");Add(centres,[x,y]);b:=v*w*u;
  for k in ks do
   exact:=Scalar(b^k);
   for d in DivisorsInt(k)do if d<k and Scalar(b^d)then exact:=false;fi;od;
   if exact then
    kcount[Position(ks,k)]:=kcount[Position(ks,k)]+1;
    Add(records,rec(k:=k,x:=x,y:=y,trace:=x/alpha+Bar(x/alpha),u:=u,v:=v,w:=w));
   fi;
  od;
 fi;od;od;
 Print("CENTRES ",Length(centres)," TYPES ",ks," COUNTS ",kcount,"\n");
 Print("TRACE_NONZERO ",List(ks,k->Number(records,r->r.k=k and r.trace<>0*r.trace)),"\n");
 PrintTo("centres_records.g","q:=",q,";alpha:=",alpha,";records:=",records,";\n");
 Print("PASS_LITERAL_CENTRES_NO_GENERATION_IP_OR_CHIRALITY_CLAIM\n");
end;
CensusCentres(17);QUIT;
