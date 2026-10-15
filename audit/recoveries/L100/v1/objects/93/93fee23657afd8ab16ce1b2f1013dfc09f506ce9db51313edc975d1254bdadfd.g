maxorders:=rec();;maxinclusions:=[];;local2T:=[];;
for K in reps do
 k:=Size(K);
 if not IsBound(maxorders.(String(k))) then maxorders.(String(k)):=[];fi;
 if k>1 then
  mm:=List(ConjugacyClassesMaximalSubgroups(K),Representative);
  UniteSet(maxorders.(String(k)),Set(List(mm,Size)));
  for H in mm do
   Add(maxinclusions,[K,H]);
   if Length(DoubleCosets(K,H,H))=2 then Add(local2T,[K,H]);fi;
  od;
 fi;
od;
