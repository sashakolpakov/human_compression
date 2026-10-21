t:=[(3,5)(4,6),(2,3)(4,5),(1,2)(3,5),(1,7),(7,8)(9,11),(8,9)(10,11),(9,11)(10,12)];;
ss:=Combinations([1..7]);;gg:=List(ss,I->Group(t{I},()));;cnt:=0;;bad:=false;;
for i in [1..Length(ss)] do for j in [1..i] do
cnt:=cnt+1;
if Intersection(gg[i],gg[j])<>Group(t{Intersection(ss[i],ss[j])},()) then Print("FAIL ",ss[i]," ",ss[j],"\n");bad:=true;break;fi;
od;if bad then break;fi;od;
Print("SUMMARY group=",Size(Group(t))," IP=",not bad," pairs=",cnt," signs=",List(t,SignPerm),"\n");
Print("omission_orbits=",List([1..7],j->List(Orbits(Group(t{Difference([1..7],[j])}),[1..12]),Length)),"\n");
Print("anchors=",Filtered([1..12],a->a^t[1]<>a and ForAll(t{[2..7]},h->a^h=a))," ",Filtered([1..12],a->a^t[7]<>a and ForAll(t{[1..6]},h->a^h=a)),"\n");QUIT;
