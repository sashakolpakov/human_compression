# Exact source-marked rank-three residue adapters, not just order comparisons.
L003LocalResidues:=function(table,params,a,pars)
 local x,y,z,defs,i,J,im,kind,uv,r,p,q,t,pp,Q,pi,order,expected,ans,settor,U,V,Ui,Vi,L,mn,bn,an,j,found,Qexact,exiso,hnf;
 x:=a[2];y:=a[3];z:=a[4];defs:=[];
 for i in [1..4] do
  J:=Difference([1..4],[i]);
  Add(defs,rec(kind:="spherical",images:=[a[J[1]]^-1*a[J[2]],a[J[1]]^-1*a[J[3]]],parameters:=[]));
 od;
 settor:=function(i,kind,images,param)defs[i]:=rec(kind:=kind,images:=images,parameters:=param);end;
 if table=3 then
  settor(4,"hex63",[x,y],params[1]);settor(2,"hex36",[y^-1,y^-1*z],params[2]);
 elif table=4 then
  settor(4,"hex36",[x,y],params[1]);settor(2,"hex63",[y^-1,y^-1*z],params[2]);
 elif table=5 then
  settor(4,"hyper333",[y,x],params[1]);settor(2,"hex36",[y,z],params[2]);settor(3,"hex36",[x,z],params[3]);
 elif table=6 then
  settor(2,"hex36",[y,z],params[1]);settor(3,"hex36",[x,z],params[2]);
 elif table=7 then
  settor(4,"hex63",[x,y],params[2]);settor(3,"hex63",[x^-1,x^-1*z],params[3]);
 elif table=8 then
  settor(4,"hex63",[x,y],params[1]);settor(3,"hex63",[x^-1,x^-1*z],params[2]);
  settor(1,"hex63",[z*y,z*x],params[3]);settor(2,"hex36",[y^-1,y^-1*z],params[4]);
 fi;
 ans:=[];
 for i in [1..4] do
  im:=defs[i].images;kind:=defs[i].kind;pp:=defs[i].parameters;
  uv:=FreeGroup("u","v");
  if kind="spherical" then
   p:=Order(im[1]);q:=Order(im[2]);t:=Order(im[1]^-1*im[2]);
   Assert(0,1/p+1/q+1/t>1);
   r:=[uv.1^p,uv.2^q,(uv.1^-1*uv.2)^t];expected:=2/(1/p+1/q+1/t-1);
  else
   if kind="hex63" then
    r:=[uv.1^6,uv.2^3,(uv.1^-1*uv.2)^2,(uv.2^-1*uv.1^-2)^pp[1]*(uv.2*uv.1^2)^pp[2]];
    expected:=6*(pp[1]^2+pp[1]*pp[2]+pp[2]^2);U:=uv.2^-1*uv.1^-2;V:=uv.2*uv.1^2;
   elif kind="hex36" then
    r:=[uv.1^3,uv.2^6,(uv.1^-1*uv.2)^2,(uv.1^-1*uv.2^-2)^pp[1]*(uv.1*uv.2^2)^pp[2]];
    expected:=6*(pp[1]^2+pp[1]*pp[2]+pp[2]^2);U:=uv.1^-1*uv.2^-2;V:=uv.1*uv.2^2;
   else
    Assert(0,kind="hyper333");
    r:=[uv.1^3,uv.2^3,(uv.1^-1*uv.2)^3,(uv.1*uv.2^-1*uv.1)^pp[1]*(uv.1*uv.2)^pp[2]];
    expected:=3*(pp[1]^2+pp[1]*pp[2]+pp[2]^2);U:=uv.1*uv.2^-1*uv.1;V:=uv.1*uv.2;
   fi;
  fi;
  Print("LOCAL_START ",[i,kind,pp,List(im,Order),expected],"\n");
  if table=8 and i=2 and pp=[0,3] then
   # The printed h-word reduces to z*y*z. Its cube is already a base relator.
   # Do not silently use the different standard torus word.
   r:=r{[1..3]};expected:="no finite bound from the printed local period";
  fi;
  Assert(0,ForAll(r,w->MappedWord(w,GeneratorsOfGroup(uv),im)=One(pars[i])));
  Assert(0,Group(im)=pars[i]);
  if IsInt(expected) then
   Q:=uv/r;pi:=IsomorphismPermGroup(Q);Assert(0,pi<>fail and IsBijective(pi));order:=Size(Image(pi));
  else order:=expected;fi;
  Print("LOCAL_ORDERS ",[i,order,Size(pars[i]),expected],"\n");
  if IsInt(expected) then Assert(0,order=expected and order mod Size(pars[i])=0);fi;
  if kind="spherical" then
   Assert(0,order=Size(pars[i]));hnf:=[];
  else
   Ui:=MappedWord(U,GeneratorsOfGroup(uv),im);Vi:=MappedWord(V,GeneratorsOfGroup(uv),im);
   Assert(0,Comm(Ui,Vi)=One(pars[i]));L:=Group([Ui,Vi]);
   Assert(0,IsNormal(pars[i],L));
   if kind="hyper333" then Assert(0,Index(pars[i],L)=3);else Assert(0,Index(pars[i],L)=6);fi;
   mn:=Order(Ui);found:=false;
   for bn in [1..Order(Vi)] do
    for an in [0..mn-1] do
     if Ui^an*Vi^bn=One(L) then found:=true;break;fi;
    od;
    if found then break;fi;
   od;
   Assert(0,found and mn*bn=Size(L));hnf:=[[mn,0],[an,bn]];
   Qexact:=uv/Concatenation(r,[U^mn,U^an*V^bn]);exiso:=IsomorphismPermGroup(Qexact);
   Assert(0,exiso<>fail and IsBijective(exiso) and Size(Image(exiso))=Size(pars[i]));
  fi;
  Add(ans,[i,kind,pp,order,Size(pars[i]),hnf,r]);
 od;
 return ans;
end;;
