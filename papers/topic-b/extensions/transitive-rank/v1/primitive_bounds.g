# Complete finite screening for the primitive strict half-degree bound.
# No source-reported C-rank is used. Residual marking searches are separate.
SizeScreen([100000,100000]);;
L047PrimeLength:=n->Length(FactorsInt(n));;
L047E2rank:=function(G)
 local P,cc,ee;
 P:=SylowSubgroup(G,2);cc:=ConjugacyClassesSubgroups(P);
 ee:=Filtered(cc,c->IsElementaryAbelian(Representative(c)));
 return LogInt(Maximum(List(ee,c->Size(Representative(c)))),2);
end;;
L047Screen:=function()
 local n,id,G,ord,r,cl,invgen,cb,disposition,residuals,expected,
 soc,quot,fr,frq,need,A8iso,m24cent,bound;
 residuals:=[];
 expected:=[[6,1],[6,2],[7,5],[8,3],[8,5],[10,4],[10,5],[10,7],[12,2]];
 for n in [2..25] do
  for id in [1..NrPrimitiveGroups(n)] do
   G:=PrimitiveGroup(n,id);ord:=Size(G);r:=QuoInt(n+1,2);
   if ord>=Factorial(n)/2 then continue;fi;
   disposition:="";
   if L047PrimeLength(ord)<r then disposition:="order_chain";
   else
    cl:=Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2);
    invgen:=Subgroup(G,Concatenation(List(cl,Elements)));
    cb:=List(cl,c->1+L047PrimeLength(QuoInt(ord,Size(c))));
    if invgen<>G then disposition:="not_involution_generated";
    elif Maximum(cb)<r then disposition:="involution_centralizer_chain";
    elif n=16 then
     soc:=Socle(G);
     if Size(soc)<>16 or not IsElementaryAbelian(soc) then Error("not affine16");fi;
     # Faithful quotient embeds in GL(4,2)=A8; normal module costs one.
     disposition:="affine16_Whiston_bound7";
    elif n=15 and id=4 then
     if IsomorphismGroups(G,AlternatingGroup(8))=fail then Error("A8 identification");fi;
     disposition:="A8_Whiston_bound6";
    elif n=9 and id=7 then
     soc:=Socle(G);quot:=G/soc;
     if Size(soc)<>9 or not IsElementaryAbelian(soc) then Error("affine9 socle");fi;
     fr:=FrattiniSubgroup(quot);frq:=quot/fr;
     if Size(fr)<>2 or IsomorphismGroups(frq,SymmetricGroup(4))=fail then Error("GL2(3) Frattini quotient");fi;
     disposition:="affine9_normal_module_bound4";
    elif (n=11 and id=6) or (n=12 and id=1) then
     if L047E2rank(G)<>2 then Error("M11 elementary2 rank");fi;
     disposition:="M11_alternate_labels_bound4";
    elif n=8 and id=4 then
     if IsomorphismGroups(G,PrimitiveGroup(7,5))=fail then Error("PSL2(7) repeated action");fi;
     disposition:="same_abstract_group_as_7_5";
    elif n=24 and id=1 then
     m24cent:=List(cl,c->QuoInt(ord,Size(c)));
     if Set(m24cent)<>[7680,21504] or Maximum(m24cent)>=2^20 then Error("M24 tail bound");fi;
     disposition:="M24_Conder_connected_tail_bound";
    else
     Add(residuals,[n,id]);disposition:="complete_marking_census";
    fi;
   fi;
   Print("SCREEN|",n,"|",id,"|",ord,"|",r,"|",disposition,"\n");
  od;
 od;
 if residuals<>expected then Error("unresolved primitive catalogue entry");fi;
 for need in [[10,4],[10,5],[10,7],[12,2],[8,5]] do
  G:=PrimitiveGroup(need[1],need[2]);bound:=L047E2rank(G);
  if need=[8,5] then
   if bound<>2 then Error("PGL2(7) elementary rank");fi;
  elif bound>3 then Error("residual elementary rank");fi;
  Print("E2RANK|",need[1],"|",need[2],"|",bound,"\n");
 od;
 if IsomorphismGroups(PrimitiveGroup(10,5),SymmetricGroup(6))=fail then Error("degree10 S6");fi;
 # Exact abstract/action identifications used for the residual search limits.
 if IsomorphismGroups(PrimitiveGroup(6,1),AlternatingGroup(5))=fail or IsomorphismGroups(PrimitiveGroup(6,2),SymmetricGroup(5))=fail then Error("degree6 abstract groups");fi;
 if IsomorphismGroups(PrimitiveGroup(7,5),Image(IsomorphismPermGroup(GL(3,2))))=fail then Error("degree7 GL3(2)");fi;
 G:=PrimitiveGroup(8,3);soc:=Socle(G);
 if Size(soc)<>8 or not IsElementaryAbelian(soc) or IsomorphismGroups(G/soc,PrimitiveGroup(7,5))=fail then Error("degree8 affine model");fi;
 # Verify the classical exceptional isomorphism used for affine degree16.
 if IsomorphismGroups(Image(IsomorphismPermGroup(GL(4,2))),AlternatingGroup(8))=fail then Error("GL4(2)=A8");fi;
 for n in [26..63] do
  bound:=n*Product([0..LogInt(n,2)-1],i->n-2^i);
  if bound>=2^(n-1) then Error("Maroti interval bound");fi;
 od;
 Print("PASS_PRIMITIVE_BOUNDS\n");
end;;
L047Screen();QUIT;
