# Root review: separate coset enumerator and integer-valued cyclic rewriting.
SizeScreen([100000,24]);;
Need:=function(b,s) if not b then Error(s);fi;end;;
f:=FreeGroup("a","b","c","d");;s:=GeneratorsOfGroup(f);;
r:=Concatenation(List(s,x->x^2),[(s[1]*s[2])^5,(s[2]*s[3])^3,(s[3]*s[4])^5,Comm(s[1],s[3]),Comm(s[1],s[4]),Comm(s[2],s[4]),(s[2]*s[3]*s[4])^5]);;
u:=[s[3]*s[2],(s[1]*s[2])^2*s[3]*s[4]*s[1],s[1]*s[2]*s[1]*s[4]*s[3]*s[4]*s[2]];;
# ACE is not loaded. This is the GAP coset enumeration implementation.
tab:=CosetTableFromGensAndRels(s,r,u:max:=100000,silent);;
Need(tab<>fail and Length(tab[1])=20,"independent index20");
w:=f/r;;q:=PresentationSubgroupRrs(w,tab,"q");;
Need(List(PrimaryGeneratorWords(q),v->List(LetterRepAssocWord(v),AbsInt))=List(u,LetterRepAssocWord),"three source words");
TzInitGeneratorImages(q);;TzGoGo(q);;
fr:=List(RelatorsOfFpGroup(FpGroupPresentation(q)),LetterRepAssocWord);;
Need(fr=[[2,2,2],[1,2,1,-2,1,2,-1,2,1]],"same two-generator presentation");
Need(q!.imagesOldGens{[1..3]}=[[-1,-2,1],[-2,-1,2],[-2,-1,2,2,1]],"same marked source generators");
t:=FreeGroup("x","y");;x:=t.1;;y:=t.2;;
l:=t/[y^3,x*y*x*y^-1*x*y*x^-1*y*x];;
a:=NEWTC_CosetEnumerator(FreeGeneratorsOfFpGroup(l),RelatorsOfFpGroup(l),[l.1],true,false:cyclic:=true,limit:=500000,quiet:=true);;
Need(a<>fail and a.isCyclicMtcTable and a.index=175560 and Length(a.subgens)=1,"integer cyclic enumeration");
# Reimplement rewriting from the actual augmented table, including closure.
TraceExponent:=function(start,word,expected)
 local current,total,k;
 current:=start;total:=0;
 for k in word do
  total:=total+a.aug[k+a.offset][current];current:=a.ct[k+a.offset][current];
 od;
 Need(current=expected,"relator path must close");return total;
end;;
# The chosen original subgroup word must rewrite to its own generator.
gcdval:=AbsInt(TraceExponent(1,a.subgword[1],1)-1);;distinct:=[];;
for i in [1..a.n] do
 for rel in a.rels do
  val:=TraceExponent(i,rel,i);gcdval:=Gcd(gcdval,val);
  if val<>0 then AddSet(distinct,AbsInt(val));fi;
 od;
od;
Need(gcdval=171 and 171 in distinct,"independent full cyclic relation gcd");
Need(NEWTC_CyclicSubgroupOrder(a)=171,"official integer routine agrees");
# Local quotient obstruction via Sylow subgroups, rather than element classes.
Read("programs/ambient_marking.g");;
Obstruct:=function(k,markers,allowed)
 local bad,p,sg,subs,z,c,hits,hit,summary;
 bad:=Difference(Set(Concatenation(List(Elements(Group(markers{[2,3,4]})),g->List(Elements(Group(markers{[1,2,3]})),h->g*h)))),allowed);
 summary:=[];
 for p in Set(FactorsInt(Size(k))) do
  sg:=SylowSubgroup(k,p);subs:=[];hits:=0;
  for z in Elements(sg) do
   if Order(z)<>p then continue;fi;
   c:=Group(z);if ForAny(subs,h->IsConjugate(k,c,h)) then continue;fi;Add(subs,c);
   hit:=First(bad,b->Order(b)=p and IsConjugate(k,c,Group(b)));
   Need(hit<>fail,"Sylow prime subgroup obstruction");hits:=hits+1;
  od;
  Need(hits>0,"nonempty prime subgroup test");Add(summary,[p,Length(subs)]);
 od;
 return summary;
end;;
jomega:=(jmarks[1]*jmarks[2]*jmarks[3])^5;;
jtest:=Obstruct(G,jmarks,[One(G),jomega]);;ptest:=Obstruct(P,pmarks,[One(P)]);;
Need(jtest=[[2,1],[3,1],[5,1],[7,1],[11,1],[19,1]] and ptest=[[2,1],[3,1],[5,1],[19,1]],"all prime classes");
PrintTo("distinct.json",[20,a.index,gcdval,20*a.index*gcdval,a.n*Length(a.rels),Length(distinct),jtest,ptest],"\n");
Print("L095_DISTINCT_PASS\n");QUIT;
