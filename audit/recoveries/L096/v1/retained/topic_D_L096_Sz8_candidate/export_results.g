SizeScreen([100000,100000]);;
Read("sz8_rows.g");;Read("sz8_shadow_results.g");;
J:=function(x)
 if IsBool(x) or IsInt(x) then return String(x);fi;
 if IsString(x) and Length(x)>0 then return Concatenation("\"",x,"\"");fi;
 if IsList(x) then return Concatenation("[",JoinStringsWithSeparator(List(x,J),","),"]");fi;
 if IsRecord(x) then return Concatenation("{",JoinStringsWithSeparator(List(RecNames(x),k->Concatenation(J(k),":",J(x.(k)))),","),"}");fi;
 Error("unhandled JSON object");
end;;
rows:=List([1..Length(L096Sz8ShadowResults)],i->rec(triple:=L096Sz8Triples[i],shadow:=L096Sz8ShadowResults[i]));;
out:=OutputTextFile("results.json",false);;SetPrintFormattingStatus(out,false);;
AppendTo(out,J(rec(group:="Sz(8)",thin:=Length(L096Sz8AllThin),RWPRI:=Length(rows),rank3_counts:=[Number(rows,r->r.shadow.IP3),Number(rows,r->r.shadow.WIP3 and not r.shadow.IP3),Number(rows,r->not r.shadow.WIP3)],full_flag_extensions:=Sum(rows,r->r.shadow.full_flag_extensions),type_tests:=3*Length(rows),rows:=rows)),"\n");
CloseStream(out);;
QUIT;
