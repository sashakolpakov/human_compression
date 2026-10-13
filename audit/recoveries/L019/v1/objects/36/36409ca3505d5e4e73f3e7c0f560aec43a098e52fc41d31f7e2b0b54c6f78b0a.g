SizeScreen([100000,100000]);;
rows:=[[[2, 1, 3, 4, 5, 6, 7, 8], [1, 3, 2, 4, 5, 6, 7, 8], [1, 2, 4, 3, 5, 6, 7, 8], [1, 2, 3, 5, 4, 6, 8, 7], [1, 2, 3, 4, 7, 8, 5, 6]], [[2, 1, 3, 4, 5, 6, 7, 8], [1, 3, 2, 4, 5, 6, 7, 8], [1, 2, 4, 3, 5, 6, 8, 7], [1, 2, 3, 5, 4, 7, 6, 8], [1, 2, 3, 4, 6, 5, 7, 8]], [[2, 1, 3, 4, 5, 6, 7, 8], [1, 3, 2, 4, 5, 6, 7, 8], [1, 2, 4, 3, 5, 6, 8, 7], [1, 2, 3, 5, 4, 7, 6, 8], [1, 2, 3, 4, 6, 5, 8, 7]], [[2, 1, 3, 4, 5, 6, 7, 8], [1, 3, 2, 4, 5, 6, 7, 8], [1, 2, 4, 3, 5, 6, 8, 7], [1, 2, 3, 7, 5, 8, 4, 6], [1, 2, 3, 4, 6, 5, 8, 7]], [[2, 1, 3, 4, 5, 6, 7, 8], [1, 3, 2, 4, 5, 6, 7, 8], [1, 2, 4, 3, 6, 5, 8, 7], [1, 2, 3, 5, 4, 6, 7, 8], [1, 2, 3, 4, 7, 8, 5, 6]], [[2, 1, 3, 4, 5, 6, 7, 8], [1, 3, 2, 4, 5, 6, 7, 8], [1, 2, 4, 3, 6, 5, 8, 7], [1, 2, 3, 5, 4, 6, 8, 7], [1, 2, 3, 4, 7, 8, 5, 6]], [[2, 1, 3, 4, 5, 6, 8, 7], [1, 7, 3, 4, 5, 8, 2, 6], [1, 2, 3, 4, 6, 5, 7, 8], [1, 2, 3, 5, 4, 6, 7, 8], [1, 2, 4, 3, 5, 6, 7, 8]], [[2, 1, 3, 4, 5, 6, 8, 7], [1, 7, 3, 4, 5, 8, 2, 6], [1, 2, 3, 4, 6, 5, 8, 7], [1, 2, 3, 5, 4, 6, 7, 8], [1, 2, 4, 3, 5, 6, 7, 8]], [[2, 1, 4, 3, 6, 5, 8, 7], [1, 3, 2, 4, 5, 6, 7, 8], [1, 2, 5, 6, 3, 4, 7, 8], [1, 2, 3, 4, 7, 8, 5, 6], [1, 2, 3, 4, 5, 6, 8, 7]]];;
safe:=0;;bad:=[];;evenbad:=[];;fractured:=0;;pure:=0;;
for i in [1..Length(rows)] do
 t:=List(rows[i],PermList);;
 if ForAny([1..5],j->IsTransitive(Group(t{Difference([1..5],[j])}),[1..8])) then continue;fi;
 fractured:=fractured+1;;P:=Group([],());;anchorOrbit:=[1];;failures:=[];;
 for j in [1..Length(t)] do Q:=Group(t{[1..j]});K:=Intersection(Q,SymmetricGroup(anchorOrbit));M:=Intersection(K,P);if K<>M then Add(failures,[j,Size(K),Size(M),anchorOrbit]);fi;P:=Q;anchorOrbit:=Orbit(P,1);od;
 if Length(failures)=0 then safe:=safe+1;else Add(bad,[i,failures]);Print("LEAF_BAD|",i,"|",failures,"|",t,"\n");if ForAny(failures,x->x[2]<>2*x[3])then Add(evenbad,i);fi;fi;
 if ForAny(t,h->NrMovedPoints(h)=2)then pure:=pure+1;fi;
od;
Print("COMPLETE_CRITICAL_LEAVES|",Length(rows),"|",fractured,"|",safe,"|",Length(bad),"|",pure,"|",evenbad,"\n");QUIT;
