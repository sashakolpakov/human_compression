# Exploratory fixed-edge construction, pending uniform completeness proof.
SizeScreen([240,1000]);;SetInfoLevel(InfoWarning,0);;
Run:=function(q,seedlog,tag)
 local Q,F,one,zero,z,base,J,Sig,Code,Encode,R,seed,sols,x,y,w,d,g,t,order,R0,S,H0,V,H,rot,rr,i,j,m,sgn,verts,dict,rep,a,b,c,vtx,nbr,edges,fixed,pair,key,ekeys,fkeys,tm,filename,full;
 tm:=Runtime();Q:=q^3;F:=GF(Q);one:=One(F);zero:=Zero(F);z:=Z(Q);
 base:=Filtered(Elements(F),x->x^q=x);J:=[[zero,one],[-one,zero]];
 Sig:=x->List(x,row->List(row,a->a^q));
 Encode:=function(x) return List(x,row->List(row,function(a) if a=zero then return -1;fi;return LogFFE(a,z);end));end;
 Code:=function(x) local code,row,a;code:=0;for row in x do for a in row do code:=code*Q;if a<>zero then code:=code+LogFFE(a,z)+1;fi;od;od;return code;end;
 sols:=[List(seedlog,row->List(row,function(e) if e<0 then return zero;fi;return z^e;end))];
 H:=[];
 for x in base do if x=zero then continue;fi;for y in base do for w in base do Add(H,[[x,y],[w,(one+y*w)/x]]);od;od;od;
 for y in base do if y=zero then continue;fi;for d in base do Add(H,[[zero,y],[-one/y,d]]);od;od;
 for sgn in [1] do
  R0:=sols[1]; order:=Order(R0*J);
  if R0=fail then Print("NO SEED q=",q," sign=",sgn,"\n");continue;fi;
  R:=R0;S:=Sig(R);m:=Order(R*J);if IsOddInt(q) and IsEvenInt(m) then m:=m/2;fi;
  Print("GROUP q=",q," tag=",tag," orderSL=",Size(Group(R,S,J))," m=",m,"\n");
  rot:=R*J;rr:=rot^0;H0:=[];
  for i in [0..order-1] do AddSet(H0,rr);AddSet(H0,R*rr);rr:=rr*rot;od;
  H0:=Elements(Group(R,J));
  V:=Elements(Group(R,S));
  verts:=[];dict:=NewDictionary(0,true);
  for x in H do for g in [x,S*x] do
   if LookupDictionary(dict,Code(g))<>fail then continue;fi;
   Add(verts,g);vtx:=Length(verts);
   for a in H0 do AddDictionary(dict,Code(a*g),vtx);od;
  od;od;
  edges:=[];fixed:=[];ekeys:=[];fkeys:=[];
  for i in [1..Length(verts)] do
   rr:=rot^0;
   for j in [0..m-1] do
    g:=rr*verts[i];rr:=rr*rot;nbr:=LookupDictionary(dict,Code(S*g));
    if nbr=fail then continue;fi;
    if nbr=i then Error("Loop");fi;
    pair:=Set([i,nbr]);key:=Minimum(List(V,a->Code(a*g)));
    if Sig(g)*g^-1 in V then AddSet(fixed,pair);AddSet(fkeys,key);else AddSet(edges,pair);AddSet(ekeys,key);fi;
   od;
  od;
  if Length(edges)<>Length(ekeys) or Length(fixed)<>Length(fkeys) then Error("Multiple edges");fi;
  Print("RESULT q=",q," m=",m," abs=",Length(verts)," moving=",Length(edges)," fixed=",Length(fixed)," deg=",Collected(List([1..Length(verts)],i->Number(edges,e->i in e)))," ms=",Runtime()-tm,"\n");
  filename:=Concatenation("oracle_q",String(q),"_r",String(tag),".json");
  PrintTo(filename,"{\"q\":",q,",\"m\":",m,",\"R_log\":",Encode(R),",\"absolute\":",Length(verts),",\"edges\":",edges,",\"fixed\":",fixed,"}\n");
 od;
end;;
Run(2,[[0,-1],[1,0]],0);
Run(4,[[0,-1],[56,0]],0);
Run(4,[[0,-1],[57,0]],1);
Run(5,[[107,104],[111,45]],3);
Run(5,[[97,80],[28,35]],4);
Run(7,[[57,266],[304,228]],0);
Run(7,[[83,139],[195,254]],1);
Run(7,[[22,313],[339,193]],2);
Run(7,[[129,4],[36,300]],3);
Run(7,[[129,61],[321,300]],4);
Run(7,[[2,321],[54,173]],5);
Run(7,[[2,36],[339,173]],6);
Run(9,[[614,4],[142,250]],0);
QUIT;
