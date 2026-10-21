# All source presentations are literal. GAP's exact finitely presented/permutation
# group algorithms are retained; this is not a Lean kernel certificate.
SetInfoLevel(InfoWarning,0);;
check:=function(ok,label) if not ok then Print("FAIL ",label,"\n");QUIT_GAP(1);fi;end;;
F:=FreeGroup("a","b","c");; a:=F.1;; b:=F.2;; c:=F.3;;
base:=[(a*b)^2,(b*c)^2,(a*b*c)^2];;
prs:=rec(P:=Concatenation([a^6,b^9,c^6],base,[b*a^2*(a^2*b^4)^-1,c^2*b*(b^4*c^2)^-1]),T:=Concatenation([a^6,b^9,c^2],base,[(a*b^-2)^2,a*b^2*a*(a*b^-1*a)^2]),Td:=Concatenation([a^2,b^9,c^6],base,[(c^-1*b^2)^2,b*c^2*b*(c^-1*b*c^-1)^2]));;
make:=function(name)
 local fp,iso,g,s;
 fp:=F/prs.(name);iso:=IsomorphismPermGroup(fp);g:=Image(iso);
 check(IsBijective(iso),Concatenation(name," fp isomorphism"));
 s:=List(GeneratorsOfGroup(fp),x->Image(iso,x));
 check(ForAll(prs.(name),w->MappedWord(w,GeneratorsOfGroup(F),s)=One(g)),Concatenation(name," literal relators"));
 return rec(g:=g,s:=s);
end;;
mix:=function(A,B)
 local d,e1,e2,s;
 d:=DirectProduct(A.g,B.g);e1:=Embedding(d,1);e2:=Embedding(d,2);
 s:=List([1..3],i->Image(e1,A.s[i])*Image(e2,B.s[i]));
 return rec(g:=Group(s),s:=s);
end;;
P:=make("P");;T:=make("T");;Td:=make("Td");;
Pm:=rec(g:=P.g,s:=[P.s[1]^-1,P.s[1]^2*P.s[2],P.s[3]]);;
R:=mix(P,Pm);;Q:=mix(R,T);;Qd:=mix(R,Td);;
expected:=rec(P:=[324,[6,9,6],[54,54],9,false],T:=[324,[6,9,2],[162,18],9,true],Td:=[324,[2,9,6],[18,162],9,true],R:=[972,[6,9,6],[162,162],27,true],Q:=[2916,[6,9,6],[162,162],9,true],Qd:=[2916,[6,9,6],[162,162],9,true]);;
A:=P;;
for name in ["P","T","Td","R","Q","Qd"] do
 A:=ValueGlobal(name);f:=Group(A.s{[1,2]});v:=Group(A.s{[2,3]});m:=Group([A.s[2]]);
 reg:=GroupHomomorphismByImages(A.g,A.g,A.s,[A.s[1]^-1,A.s[1]^2*A.s[2],A.s[3]]);
 row:=[Size(A.g),List(A.s,Order),[Size(f),Size(v)],Size(Intersection(f,v)),reg<>fail];
 check(row=expected.(name),Concatenation(name," exact row"));
 check(Size(m)=9,Concatenation(name," medial"));
 check(Intersection(Group([A.s[1]]),m)=TrivialSubgroup(A.g),Concatenation(name," facet IP"));
 check(Intersection(Group([A.s[3]]),m)=TrivialSubgroup(A.g),Concatenation(name," vertex IP"));
 check(ForAll(base,w->MappedWord(w,GeneratorsOfGroup(F),A.s)=One(A.g)),Concatenation(name," rotation relations"));
 if reg<>fail then check(IsBijective(reg),Concatenation(name," mirror automorphism"));fi;
 if name<>"R" then check(Intersection(f,v)=m,Concatenation(name," end IP"));else check(Intersection(f,v)<>m,"R fails IP");fi;
 Print("ROW ",name," ",row,"\n");
od;
for pair in [[R,P],[Q,R],[Qd,R]] do
 cov:=GroupHomomorphismByImages(pair[1].g,pair[2].g,pair[1].s,pair[2].s);
 check(cov<>fail and IsSurjective(cov),"marked cover");
 check(Size(Kernel(cov))=3,"degree three");
od;
p1:=GroupHomomorphismByImages(R.g,P.g,R.s,P.s);;
p2:=GroupHomomorphismByImages(R.g,P.g,R.s,Pm.s);;
check(p1<>fail and p2<>fail,"two mirror projections");
Xf:=Image(p1,Intersection(Group(R.s{[1,2]}),Kernel(p2)));;
Xv:=Image(p1,Intersection(Group(R.s{[2,3]}),Kernel(p2)));;
check(Xf=Group([P.s[2]^3]) and Xv=Xf,"local chirality obstruction b^3");
Print("CHIRALITY facet=vertex=<b^3> ORDER 3\n");
faciso:=GroupHomomorphismByImages(Group(T.s{[1,2]}),Group(R.s{[1,2]}),T.s{[1,2]},R.s{[1,2]});;
check(faciso<>fail and IsBijective(faciso),"T facet is R facet");
dualiso:=GroupHomomorphismByImages(T.g,Td.g,T.s,[Td.s[3]^-1,Td.s[2]^-1,Td.s[1]^-1]);;
check(dualiso<>fail and IsBijective(dualiso),"Td is literal dual of T");
w:=(b*c^-1)^2*a*c^2*a^-1;;
check(List([Q,Qd],A->Order(MappedWord(w,GeneratorsOfGroup(F),A.s)))=[1,3],"nonisomorphism witness");
Print("DISTINGUISH (b*c^-1)^2*a*c^2*a^-1 ORDERS [1,3]\n");
Print("PASS GAP ",GAPInfo.Version," six exact groups, all maps, IP, regularity, duality, witness\n");
QUIT_GAP(0);
