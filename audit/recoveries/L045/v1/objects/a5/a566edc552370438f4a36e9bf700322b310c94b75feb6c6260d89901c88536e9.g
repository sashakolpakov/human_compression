SetInfoLevel(InfoWarning,0);;
Check:=function()
 local q,Q,F,els,inf,perm,trans,mul,inv,frob,G,H,cnt,outer,P,W,plus,rows,i,x;
 rows:=[];
 for q in [3,5] do
  Q:=q^2;F:=GF(Q);els:=Elements(F);inf:=Q+1;
  perm:=function(fun)
   local a;return PermList(List([1..Q+1],a->Position(Concatenation(els,[fail]),fun(Concatenation(els,[fail])[a]))));
  end;
  trans:=List(BasisVectors(Basis(F)),x->perm(function(a)if a=fail then return fail;else return a+x;fi;end));
  mul:=perm(function(a)if a=fail then return fail;else return a*Z(Q);fi;end);
  inv:=perm(function(a)if a=fail then return Zero(F);elif IsZero(a)then return fail;else return a^-1;fi;end);
  frob:=perm(function(a)if a=fail then return fail;else return a^q;fi;end);
  G:=Group(Concatenation(trans,[mul,inv]));H:=Group(Concatenation(GeneratorsOfGroup(G),[frob]));
  if Size(G)<>Q*(Q^2-1)or Size(H)<>2*Size(G)then Error("literal projective model");fi;
  cnt:=Sum(Filtered(ConjugacyClasses(H),c->Order(Representative(c))=2),Size);
  outer:=Number(Elements(G),x->Order(x*frob)=2);
  if cnt<>q^4+q^3+q or outer<>q*(q^2+1)then Error("minus involution formula");fi;
  P:=PGL(2,q);W:=WreathProduct(P,Group((1,2)));
  plus:=Sum(Filtered(ConjugacyClasses(W),c->Order(Representative(c))=2),Size);
  if plus<>q^4+q^3+2*q^2-q then Error("plus involution formula");fi;
  Add(rows,[q,Size(G),Size(H),cnt,outer,Size(W),plus]);
 od;
 Print("PASS_INDEPENDENT_PGO4 ",rows,"\n");
end;;
Check();
QUIT;
