# Original exact verification of N009 Theorem 5.5 raw presentations.
# No nilpotent-class or finite-order relations are added.
SizeScreen([4096,100000]);;
CheckN009:=function(caseNumber)
 local F,f,a,b,c,d,rels,G,ct,perms,H,hom,ss,par,i,j,pos,fac;
 F:=FreeGroup("a","b","c","d");f:=GeneratorsOfGroup(F);a:=f[1];b:=f[2];c:=f[3];d:=f[4];
 rels:=Concatenation(List(f,x->x^2),[(a*c)^2,(a*d)^2,(b*d)^2,(a*b)^4,(b*c)^4,(c*d)^4,(a*b*c*b)^4,(b*c*d)^4]);
 if caseNumber=1 then Add(rels,(d*c*b*a*b*d*c)^2);
 else Append(rels,[(b*d*c*d*b*a)^2*(c*b*a*b)^2,(a*b*c*b)^2*(b*a*b*d*c*d)^2]);fi;
 G:=F/rels;
 # A completed Todd-Coxeter enumeration over the trivial subgroup bounds
 # the raw presented group, unlike NQ truncation or a found finite image.
 ct:=CosetTable(G,TrivialSubgroup(G));
 if Length(ct)<>8 or not ForAll(ct,row->Length(row)=1024) then Error("Raw coset count");fi;
 perms:=List([1..4],i->PermList(ct[2*i-1]));H:=Group(perms);
 hom:=GroupHomomorphismByImages(G,H,GeneratorsOfGroup(G),perms);
 if hom=fail or Size(H)<>1024 or not IsSurjective(hom) then Error("Regular quotient order");fi;
 if not ForAll(perms,x->Order(x)=2) or List([1..3],i->Order(perms[i]*perms[i+1]))<>[4,4,4] then Error("Marking/type");fi;
 ss:=Combinations([1..4]);par:=List(ss,S->Subgroup(H,perms{S}));
 for i in [1..16] do for j in [1..16] do
  pos:=Position(ss,Intersection(ss[i],ss[j]));
  if Intersection(par[i],par[j])<>par[pos] then Error("Actual IP");fi;
 od;od;
 fac:=[Size(Group(perms{[1,2,3]})),Size(Group(perms{[2,3,4]}))];
 if fac<>[128,64] then Error("Oriented facets");fi;
 Print("CASE ",caseNumber," raw_cosets=",Length(ct[1])," faithful_image=",Size(H)," type=[4,4,4] oriented_facets=",fac," actual_meets=256 PASS\n");
 return rec(group:=H,marking:=perms);
end;;
Print("GAP_VERSION ",GAPInfo.Version,"\n");;
firstN009:=CheckN009(1);;
secondN009:=CheckN009(2);;
comparisonN009:=GroupHomomorphismByImages(firstN009.group,secondN009.group,firstN009.marking,secondN009.marking);;
if comparisonN009<>fail and IsBijective(comparisonN009) then Error("The two ordered markings coincide");fi;
Print("PASS two distinct ordered raw presentations; total 32 subgroup closures, 512 actual meets. No NQ input.\n");
QUIT;
