s:=[(1,2),(2,3)(4,5),(3,4)(5,6),(4,5)(6,7)];;
sets:=Combinations([1..4]);;groups:=List(sets,i->Group(s{i}));;
fails:=[];;for a in [1..Length(sets)] do for b in [1..Length(sets)] do c:=Position(sets,Intersection(sets[a],sets[b]));;if Intersection(groups[a],groups[b])<>groups[c] then Add(fails,[sets[a],sets[b],Size(Intersection(groups[a],groups[b])),Size(groups[c])]);fi;od;od;
Print("ALLORDER ",Size(Group(s))," END0 ",Size(Group(s{[2..4]}))," IPFAILS ",fails," PRODUCTORDERS ",List([1..3],i->Order(s[i]*s[i+1])),"\n");
QUIT_GAP(0);
