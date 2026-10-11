# Independent transcription of the two hemi-map universal amalgam.
Need:=function(b,s)if not b then Error(s);fi;end;
F:=FreeGroup("a","b","c","d");s:=GeneratorsOfGroup(F);
M:=[[1,4,2,2],[4,1,3,2],[2,3,1,4],[2,2,4,1]];
rel:=List(s,x->x*x);
for i in [1..4]do for j in [i+1..4]do
 if j<=4 then Add(rel,(s[i]*s[j])^M[i][j]);fi;
od;od;
Add(rel,(s[1]*s[2]*s[3])^3);Add(rel,(s[2]*s[3]*s[4])^3);
U:=F/rel;u:=GeneratorsOfGroup(U);
A:=Subgroup(U,u{[1,2,3]});B:=Subgroup(U,u{[2,3,4]});
Need(Size(A)=24 and Size(B)=24,"both source hemi-map orders");
Need(Index(U,A)=4 and Index(U,B)=4,"exact source universal index");
Need(Size(U)=96,"source presentation upper bound");
Need(Size(Intersection(A,B))=6,"exact universal middle subgroup");
Need(List([1..3],i->Order(u[i]*u[i+1]))=[4,3,4],"source type");
Print("INDEPENDENT_PRESENTATION_INDEX4_FACET24_UNIVERSAL96_PASS\n");
