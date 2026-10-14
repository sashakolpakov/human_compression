Read("case_input.g");;
F:=GF(289);o:=One(F);z:=Zero(F);beta:=First(Elements(F),x->x*x=3*o);alf:=4*beta;
AB:=Cartesian([-8..8],[-8..8]);SortBy(AB,p->[AbsInt(p[1])+AbsInt(p[2]),AbsInt(p[2]),p[1],p[2]]);
Coeff:=x->First(AB,p->p[1]*o+p[2]*beta=x);
for i in [1..Length(reps)]do
 r:=reps[i];xx:=alf/alpha*r.x;yy:=First(List(AB,p->p[1]*o+p[2]*beta),z->z*z^17=r.y*r.y^17);
 Print(i," ",r.k," x ",Coeff(xx)," y ",Coeff(yy),"\n");
od;
Print("beta ",beta," oldalpha ",alpha," newalpha ",alf,"\n");QUIT;
