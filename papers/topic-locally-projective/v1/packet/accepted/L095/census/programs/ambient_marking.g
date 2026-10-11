# Ambient marking: seed-search algorithm reused from accepted phase40, with reversed order.
# No subgroup or geometry census is an input.
if LoadPackage("tomlib")<>true then Error("TomLib is required");fi;
SizeScreen([100000,24]);;
CheckL084:=function(test,msg) if not test then Error(msg);fi;end;;
G:=UnderlyingGroup(TableOfMarks("J1"));;
CheckL084(Size(G)=175560,"ambient J1 order");;
FindJankoSeed:=function(K)
 local a,b,c,d,iv,bs;
 a:=GeneratorsOfGroup(K)[1];
 CheckL084(Order(a)=2,"ambient first generator");
 iv:=Filtered(Elements(Centralizer(K,a)),x->Order(x)=2);
 for d in iv do
  if d=a then continue;fi;
  bs:=Filtered(Elements(Centralizer(K,d)),x->Order(x)=2 and Order(a*x)=5);
  for c in iv do
   if Order(c*d)<>5 then continue;fi;
   for b in bs do
    if Order(b*c)=3 and (a*b*c)^5=One(K)
      and ((d*c*b)^5*a)^3=One(K) and Group(a,b,c,d)=K then
     return [a,b,c,d];
    fi;
   od;
  od;
 od;
 Error("no source seed");
end;;
s:=FindJankoSeed(G);;
jmarks:=Reversed(s);;
pmarks:=[(1,2)(3,6)(4,7)(5,10)(8,14)(9,15)(11,19)(12,16)(13,17)(18,20),
(1,3)(2,5)(4,8)(6,13)(7,12)(9,17)(10,15)(11,18)(14,19)(16,20),
(1,3)(2,6)(4,9)(5,11)(7,15)(8,16)(10,19)(12,14)(13,18)(17,20),
(1,4)(2,7)(3,8)(5,12)(6,14)(9,18)(10,16)(11,17)(13,19)(15,20)];;
P:=Group(pmarks);; W:=DirectProduct(G,P);; ej:=Embedding(W,1);; ep:=Embedding(W,2);;
marks:=List([1..4],i->Image(ej,jmarks[i])*Image(ep,pmarks[i]));;
CheckL084(Group(marks)=W and Size(W)=600415200,"full product generation");;
H0:=Group(marks{[2,3,4]});;H3:=Group(marks{[1,2,3]});;om:=(marks[1]*marks[2]*marks[3])^5;;
CheckL084(ForAll(marks,x->Order(x)=2),"four involutions");;
CheckL084(List([1..3],i->Order(marks[i]*marks[i+1]))=[5,3,5],"exact adjacent labels");;
CheckL084(ForAll([[1,3],[1,4],[2,4]],ij->Comm(marks[ij[1]],marks[ij[2]])=One(W)),"all string relations");;
CheckL084((marks[2]*marks[3]*marks[4])^5=One(W),"hemi-icosahedral presentation relator");;
CheckL084(Size(P)=3420 and Size(H0)=60 and Size(H3)=120 and Order(om)=2 and ForAll(GeneratorsOfGroup(H3),x->Comm(x,om)=One(W)),"exact local groups and central antipode");;
Print("MODEL ",Size(W)," ENDGROUPS ",Size(H0)," ",Size(H3)," OMEGA ",Order(om),"\n");
