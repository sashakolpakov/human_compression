# Exact upper bound for the literal Hartley--Leemans presentation.
# GAP/ACE coset enumeration and GAP Schreier/Tietze/MTC algorithms are required.
if LoadPackage("ace")<>true then Error("ACE required");fi;
ACEIgnoreUnknownDefault:=false;; SizeScreen([100000,24]);;
Need:=function(b,s) if not b then Error(s);fi;end;;
f:=FreeGroup("s0","s1","s2","s3");;a:=GeneratorsOfGroup(f);;
rels:=Concatenation(List(a,x->x^2),[(a[1]*a[2])^5,(a[2]*a[3])^3,
 (a[3]*a[4])^5,Comm(a[1],a[3]),Comm(a[1],a[4]),Comm(a[2],a[4]),
 (a[2]*a[3]*a[4])^5]);;
sub:=[a[3]*a[2],(a[1]*a[2])^2*a[3]*a[4]*a[1],
 a[1]*a[2]*a[1]*a[4]*a[3]*a[4]*a[2]];;
ct:=ACECosetTableFromGensAndRels(a,rels,sub:
 workspace:=5000000,max:=100000,time:=30,silent);;
Need(ct<>fail and Length(ct[1])=20,"complete index twenty");
PrintTo("index20.json",ct,"\n");
w:=f/rels;;rp:=PresentationSubgroupRrs(w,ct,"h");;
primary:=PrimaryGeneratorWords(rp);;
Need(Length(primary)=3,"three actual primary subgroup words");
# Involutory generators permit erasing the signs in the primary words.
Need(List(primary,x->List(LetterRepAssocWord(x),AbsInt))=
 List(sub,LetterRepAssocWord),"literal subgroup words");
PrintTo("schreier_initial.json",List(RelatorsOfFpGroup(FpGroupPresentation(rp)),LetterRepAssocWord),"\n");
TzInitGeneratorImages(rp);;TzGoGo(rp);;
outgens:=GeneratorsOfPresentation(rp);;
Need(Length(outgens)=2,"two final generators");
final:=List(RelatorsOfFpGroup(FpGroupPresentation(rp)),LetterRepAssocWord);;
# FpGroupPresentation renumbers the two surviving generators.
Need(final=[[2,2,2],[1,2,1,-2,1,2,-1,2,1]],"exact two relators");
images:=rp!.imagesOldGens;;
Need(images{[1..3]}=[[-1,-2,1],[-2,-1,2],[-2,-1,2,2,1]],"tracked images of the three source generators");
PrintTo("schreier_final.json",[final,images,rp!.preImagesNewGens],"\n");
# This is a new presented group; no finite permutation quotient enters here.
t:=FreeGroup("x","y");;x:=t.1;;y:=t.2;;
l:=t/[y^3,x*y*x*y^-1*x*y*x^-1*y*x];;
aug:=NEWTC_CosetEnumerator(FreeGeneratorsOfFpGroup(l),RelatorsOfFpGroup(l),
 [l.1],true,false:abelian:=true,limit:=500000,quiet:=true);;
Need(aug<>fail and aug.index=175560,"complete cyclic subgroup index");
Need(Length(aug.subgens)=1,"one specified cyclic generator");
matrix:=NEWTC_AbelianizedRelatorsSubgroup(aug);;
Need(ForAll(matrix,r->Length(r)=1),"one-column relation matrix");
exponents:=List(matrix,r->r[1]);;
Need(Gcd(exponents)=171,"cyclic subgroup relation gcd");
PrintTo("cyclic_relations.json",matrix,"\n");
PrintTo("presentation_summary.json",[20,175560,Gcd(exponents),20*175560*Gcd(exponents),Length(matrix)],"\n");
Print("L095_PRESENTATION_PASS 20 175560 171 600415200\n");
QUIT;
