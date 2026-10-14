Need:=function(ok,msg)if not ok then Error(msg);fi;end;
RunWitnesses:=function()
 local q,F,o,z,I,Bar,Star,Nm,Homology,beta,alpha,u,w,centres,types,L,x,y,ns,reflectors,ff,r,D,T,ii,v,a,b,c,pp,G,sz,ss,gg,S,intervals,gens,i,j,idx,autcount,reversecount,ng,negative;
 q:=17;F:=GF(q*q);o:=One(F);z:=Zero(F);I:=IdentityMat(3,F);
 Bar:=x->x^q;Star:=A->TransposedMat(List(A,row->List(row,Bar)));Nm:=x->x*Bar(x);
 Homology:=function(v)local n;n:=Sum(List(v,Nm));Need(n<>0*o,"nonisotropic centre");return -I+2*List(v,x->List(v,y->x*Bar(y)))/n;end;
 beta:=First(Elements(F),x->x*x=3*o);Need(beta^17=-beta,"quadratic basis");alpha:=4*beta;
 u:=Homology([alpha,z,o]);w:=Homology([z,z,o]);
 centres:=[[3*o+4*beta,o+3*beta,o],[7*o+beta,o+3*beta,o],[8*o+6*beta,4*o+beta,o]];types:=[7,8,9];
 L:=[];for x in F do for y in F do if o+Nm(x)+Nm(y)=z then Add(L,[o,x,y]);fi;od;od;for x in F do if o+Nm(x)=z then Add(L,[z,o,x]);fi;od;
 Need(Length(L)=4914,"all literal isotropic projective points");
 ns:=Filtered(Elements(F),x->Nm(x)=o);Need(Length(ns)=18,"norm-one group order");
 reflectors:=[];
 for ff in [0,1]do for r in ns do
  if ff=0 then D:=DiagonalMat([o,r,o]);else D:=DiagonalMat([alpha/Bar(alpha),r,o]);fi;
  T:=function(M)if ff=0 then return D*M*D^-1;else return D*List(M,row->List(row,Bar))*D^-1;fi;end;
  Need(T(u)=u and T(w)=w and D*Star(D)=I,"actual centralizer representative");Add(reflectors,rec(field:=ff,D:=D));
 od;od;
 for ii in [1..3]do
  Need(Sum(List(centres[ii],Nm))=4*o,"literal norm-four centre");v:=Homology(centres[ii]);
  a:=w*v;b:=v*w*u;c:=u*w;
  Need(ForAll([u,v,w,a,b,c],M->M*Star(M)=I and DeterminantMat(M)=o),"unitary determinant-one membership");
  Need(u^2=I and v^2=I and w^2=I and a*b=u and b*c=v and a*b*c=w,"literal interval involutions");
  pp:=List([a,b,c],M->Permutation(M,L,OnLines));Need(ForAll(pp,g->g<>fail),"literal projective action");
  Need(List(pp,Order)=[3,types[ii],3],"source Schlaefli type");G:=Group(pp);sz:=Size(G);Need(sz=q^3*(q^3+1)*(q^2-1)/3,"whole PSU generation");
  intervals:=[rec(pair:=[0,1],g:=pp[1]),rec(pair:=[0,2],g:=pp[1]*pp[2]),rec(pair:=[0,3],g:=pp[1]*pp[2]*pp[3]),rec(pair:=[1,2],g:=pp[2]),rec(pair:=[1,3],g:=pp[2]*pp[3]),rec(pair:=[2,3],g:=pp[3])];
  ss:=Combinations([0,1,2,3]);gg:=[];for S in ss do gens:=List(Filtered(intervals,r->IsSubset(S,r.pair)),r->r.g);if IsEmpty(gens)then Add(gg,Group(()));else Add(gg,Group(gens));fi;od;
  for i in [1..16]do for j in [1..16]do idx:=Position(ss,Intersection(ss[i],ss[j]));
   if IsSubset(ss[i],ss[j])then Need(IsSubgroup(gg[i],gg[j]),"actual nested subgroup");
   elif IsSubset(ss[j],ss[i])then Need(IsSubgroup(gg[j],gg[i]),"actual nested subgroup");
   else Need(Intersection(gg[i],gg[j])=gg[idx],"actual nonnested intersection");fi;
  od;od;
  reversecount:=0;
  for r in reflectors do if r.field=0 then T:=r.D*v*r.D^-1;else T:=r.D*List(v,row->List(row,Bar))*r.D^-1;fi;if T=w*v*w then reversecount:=reversecount+1;fi;od;
  Need(reversecount=0 and centres[ii][1]/alpha+Bar(centres[ii][1]/alpha)<>z,"all36 reversers excluded");
  Print("WITNESS ",ii," TYPE 3 ",types[ii]," 3 GROUP ",sz," ENDS ",Size(Group(pp{[1,2]}))," ",Size(Group(pp{[2,3]}))," IP 256 REVERSERS ",reversecount," PASS\n");
 od;
 # Both controls isolate conditions that types/interval relations alone cannot supply.
 v:=Homology([beta,o+2*beta,o]);pp:=List([w*v,v*w*u,u*w],M->Permutation(M,L,OnLines));
 Need(List(pp,Order)=[3,8,3] and Size(Group(pp))=2448,"proper subgroup negative control");
 Print("NEGATIVE_PROPER_GROUP 2448 PASS\n");
 v:=Homology([o,6*o,o]);reversecount:=0;
 for r in reflectors do if r.field=0 then T:=r.D*v*r.D^-1;else T:=r.D*List(v,row->List(row,Bar))*r.D^-1;fi;if T=w*v*w then reversecount:=reversecount+1;fi;od;
 Need(reversecount>0,"actual reflection negative control");Print("NEGATIVE_REFLECTABLE ",reversecount," PASS\n");
 Print("PASS_PSU17_THREE_WITNESSES\n");
end;
RunWitnesses();QUIT;
