SizeScreen([1000,1000]);;
f:=FreeGroup("u","v","w");;u:=f.1;;v:=f.2;;w:=f.3;;
for st in [[1,3],[3,1]] do
rels:=[u^4,v^4,w^4,(u*v)^2,(v*w)^2,(u*v*w)^2,(u^-1*v)^st[1]*(u*v^-1)^st[2],(v^-1*w)*(v*w^-1)^3];;
g:=f/rels;;iso:=IsomorphismPermGroup(g);;h:=Image(iso);;a:=List(GeneratorsOfGroup(g),x->Image(iso,x));;
Print("CASE ",st," ORDER ",Size(h)," LOCAL ",Size(Group(a{[1,2]}))," ",Size(Group(a{[2,3]})),"\n");
od;
QUIT_GAP(0);
