SizeScreen([100000,100000]);;
# Required exact Reidemeister--Schreier certificate for L121 Section 3.
# No finite image alone is used to identify the universal group.
f:=FreeGroup("a","b","d","c");;a:=f.1;;b:=f.2;;d:=f.3;;c:=f.4;;
rels:=[a^2,b^2,d^2,c^2,(a*b)^3,(a*d)^2,(a*c)^2,(b*d)^6,(b*c)^3,(d*c)^2,(c*(b*d)^2*b)^2];;
g:=f/rels;;
q:=[(1,2)(4,5),(2,3)(5,6),(1,5)(2,4)(3,6),(1,5)(2,4)];;
Q:=Group(q);;
if Size(Q)<>48 then Error("linear group order");fi;
h:=GroupHomomorphismByImages(g,Q,GeneratorsOfGroup(g),q);;
if h=fail or Size(Image(h))<>48 then Error("linear epimorphism");fi;
k:=Kernel(h);;is:=IsomorphismFpGroup(k);;p:=Range(is);;
if Length(GeneratorsOfGroup(p))<>3 or Length(RelatorsOfFpGroup(p))<>3 then Error("kernel presentation shape");fi;
pre:=List(GeneratorsOfGroup(p),x->LetterRepAssocWord(UnderlyingElement(PreImagesRepresentative(is,x))));;
rr:=List(RelatorsOfFpGroup(p),LetterRepAssocWord);;
Print("{\"gap_version\":\"",GAPInfo.Version,"\",\"linear_order\":48,\"kernel_generators\":3,\"kernel_relators\":",rr,",\"basis_words\":",pre,"}\n");
QUIT;
