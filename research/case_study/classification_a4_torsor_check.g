# Normalizer-only verification; no global coset-incidence graph is built.
# For q=37,43 (prime), Aut(PSL2(q))=PGL2(q).
CheckA4Torsor:=function(q)
 local G,P,H,T,N,M,C,pa,U,A,k,pair,typ,invfixed,Q,quot,proj;
 G:=PSL(2,q); P:=PGL(2,q);
 H:=First(List(ConjugacyClassesMaximalSubgroups(G),Representative),h->Size(h)=12 and StructureDescription(h)="A4");
 T:=First(List(ConjugacyClassesSubgroups(H),Representative),t->Size(t)=3);
 N:=Normalizer(G,T); M:=Normalizer(H,T);
 C:=Filtered(Orbit(N,H,OnPoints),k->k<>H);
 pa:=function(pair,g) return Set(List(pair,h->h^g)); end;
 U:=[];
 for k in C do
   pair:=Set([H,k]);
   if not ForAny(U,p->RepresentativeAction(N,p,pair,pa)<>fail) then Add(U,pair); fi;
 od;
 A:=[];
 for pair in U do
   if not ForAny(A,p->RepresentativeAction(Normalizer(P,T),p,pair,pa)<>fail) then Add(A,pair); fi;
 od;
 quot:=FactorGroup(N,T);
 invfixed:=Number(Elements(quot),x->x<>One(quot) and x*x=One(quot));
 Print("q=",q," |G|=",Size(G)," |N_G(T)|=",Size(N)," quotient=",StructureDescription(quot)," ordered=",Length(C)," unordered_G=",Length(U)," unordered_Aut=",Length(A)," nonidentity_inverse_fixed=",invfixed,"\n");
 if not ForAll(C,k->Size(Intersection(H,k))=3 and Size(ClosureGroup(H,k))=Size(G)) then Error("intersection/generation failed"); fi;
end;
for q in [13,37,43] do CheckA4Torsor(q); od;
QUIT;
