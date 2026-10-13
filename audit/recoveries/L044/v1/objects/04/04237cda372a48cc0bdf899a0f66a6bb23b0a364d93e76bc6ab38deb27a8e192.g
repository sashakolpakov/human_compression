Read("census.g");;
L044TableRun:=function()
 local n,id,G,inv,whole,iso,R,actions,retained,solutions;
 actions:=0;retained:=0;solutions:=0;
 for n in [2..11] do
  for id in [1..NrPrimitiveGroups(n)] do
   G:=PrimitiveGroup(n,id);actions:=actions+1;
   if not ForAll(GeneratorsOfGroup(G),g->SignPerm(g)=1) then
    Print("ROSTER|",n,"|",id,"|",Size(G),"|ODD\n");
   else
    inv:=Concatenation(List(Filtered(ConjugacyClasses(G),c->Order(Representative(c))=2),Elements));
    whole:=Length(inv)>0 and Subgroup(G,inv)=G;
    if not whole then
     Print("ROSTER|",n,"|",id,"|",Size(G),"|NOT_INVOLUTION_GENERATED\n");
    else
     Print("ROSTER|",n,"|",id,"|",Size(G),"|CENSUS\n");retained:=retained+1;
     R:=L044TableCensus(n,id,QuoInt(n,2),n-2);
     solutions:=solutions+Length(R.solutions);
     if Length(R.solutions)>0 then
      if n=5 then
       if Size(G)<>10 then Error("degree-five named group");fi;
       Print("NAMED|5|",id,"|DIHEDRAL10\n");
      elif n=6 then
       iso:=IsomorphismGroups(G,AlternatingGroup(5));
       if iso=fail then Error("degree-six named group");fi;
       Print("NAMED|6|",id,"|A5|",List(GeneratorsOfGroup(G),g->List([1..5],i->i^Image(iso,g))),"\n");
      elif not G=AlternatingGroup(n) then Error("higher named group");
      else Print("NAMED|",n,"|",id,"|ALTERNATING\n");fi;
     fi;
    fi;
   fi;
  od;
 od;
 Print("COMPLETE|",actions,"|",retained,"|",solutions,"\n");
end;;
L044TableRun();;
QUIT;
