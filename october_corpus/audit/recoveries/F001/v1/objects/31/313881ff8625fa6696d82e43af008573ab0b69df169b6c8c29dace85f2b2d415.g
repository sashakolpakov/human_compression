Read("finite_model.g");;
F001Run:=function()
  local row,q,z,cs,m,delta,d,gs,orders,ip,smallrows,paramrows,t,eta,x,y,det,muorder,rr,sub,i,j,printed;
  smallrows:=[rec(q:=5,cs:=[1,1,2,1],type:=[3,3,5,3]),rec(q:=7,cs:=[1,1,1,2],type:=[3,3,3,7]),rec(q:=9,cs:=fail,type:=[5,3,3,5]),rec(q:=11,cs:=[1,1,1,3],type:=[3,3,3,5])];
  for row in smallrows do
    q:=row.q; z:=Z(q);
    if q=9 then F001Need(z^2=z+One(GF(q)),"F9 basis"); cs:=[z,One(GF(q)),One(GF(q)),z]; else cs:=row.cs*One(GF(q)); fi;
    d:=F001Reflections(q,cs); m:=d.form; delta:=DeterminantMat(m);
    F001Need(delta<>Zero(GF(q)) and delta^((q-1)/2)=One(GF(q)),"spinor determinant square");
    F001Need(Length(d.points)=(q+1)*(q^2+1),"isotropic point count");
    F001ProjectiveFaithfulness(d.points,q); gs:=d.generators;
    F001Need(ForAll(gs,x->Order(x)=2),"five involutions");
    for i in [1..5] do for j in [i+2..5] do F001Need(gs[i]*gs[j]=gs[j]*gs[i],"string commutation"); od; od;
    orders:=List([1..4],i->Order(gs[i]*gs[i+1]));
    F001Need(orders=row.type,"small Schlaefli type");
    F001Need(Size(Group(gs))=q^4*(q^2-1)*(q^4-1)/2,"full Omega5 order");
    ip:=F001AllIP(gs);
    F001Need(ip.logical_pairs=1024,"all subset pairs");
    Print("SMALL ",q," type=",orders," order=",Size(Group(gs))," logical=",ip.logical_pairs," intersections=",ip.actual_intersections," PASS\n");
  od;
  paramrows:=[[13,10,0],[17,9,1],[19,13,2],[23,21,0],[25,11,2],[27,16,4],[29,13,2],[31,6,4]];
  printed:=[[13,10,1],[17,14,3],[19,3,4],[23,14,1],[29,14,4],[31,16,19]];
  for row in paramrows do
    q:=row[1]; z:=Z(q); t:=z^row[2]; eta:=z^row[3]; cs:=[eta,t,t,t];
    if IsPrimeInt(q) then
      rr:=First(printed,x->x[1]=q); F001Need(t=rr[2]*One(GF(q)) and eta=rr[3]*One(GF(q)),"printed prime-field parameters");
    elif q=25 then F001Need(z^2-z+2*One(GF(q))=Zero(GF(q)),"F25 printed basis");
    elif q=27 then F001Need(z^3-z+One(GF(q))=Zero(GF(q)),"F27 printed basis"); fi;
    m:=F001Form(q,cs); delta:=DeterminantMat(m);
    F001Need(delta<>Zero(GF(q)) and delta^((q-1)/2)=One(GF(q)),"boundary spinor square");
    for i in [1..5] do for j in [i..5] do
      sub:=m{[i..j]}{[i..j]}; F001Need(DeterminantMat(sub)<>Zero(GF(q)),"all boundary intervals nonsingular");
    od; od;
    muorder:=(q+1)/2; if q mod 4=3 then muorder:=(q-1)/2; fi;
    F001Need(Order([[t^2-1,t],[-t,-One(GF(q))]])=muorder,"boundary full odd torus order");
    Print("PARAM ",q," t_exponent=",row[2]," eta_exponent=",row[3]," torus_order=",muorder," PASS\n");
  od;
  rr:=F001Q3Exhaust(); Print("Q3 nodes=",rr.nodes," rejected=",rr.rejected," leaves=",rr.leaves," full=",rr.full," PASS\n");
  Print("ALL_F001_ODD_CERTIFICATES_PASS\n");
end;;
F001Run();;
QUIT_GAP(0);
