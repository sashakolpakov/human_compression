# Check printed Borel shapes for the uniquely invariant-matched rows.
# A juxtaposition 2^a H / 3^a H is checked as a normal elementary-abelian
# subgroup with the stated quotient, without inferring an unspecified action.
if not IsBound(INPUT_FILE) or not IsBound(WITNESS_FILE) or not IsBound(OUTPUT_FILE) then Error("explicit files required");fi;
Read(INPUT_FILE);;
Read(WITNESS_FILE);;
SizeScreen([100000,24]);;
Phase180BorelShape:=function(B,label)
 local named, extensions, row, p, rank, qid, N;
 named:=[["1",[1,1]],["2",[2,1]],["3",[3,1]],["4",[4,1]],
 ["22",[4,2]],["23",[8,5]],["24",[16,14]],["S3",[6,1]],
 ["D8",[8,3]],["Q8",[8,4]],["D10",[10,1]],["A4",[12,3]],
 ["D12",[12,4]],["F21",[21,1]],["S4",[24,12]],["A5",[60,5]],
 ["2× D8",IdGroup(DirectProduct(CyclicGroup(2),DihedralGroup(8)))]];
 row:=First(named,r->r[1]=label);
 if row<>fail then return IdGroup(B)=row[2];fi;
 extensions:=[["232",2,3,[2,1]],["322",3,2,[2,1]],["242",2,4,[2,1]],
 ["2222",2,2,[4,2]],["2322",2,3,[4,2]],["324",3,2,[4,1]],
 ["243",2,4,[3,1]],["22A4",2,2,[12,3]],["22D8",2,2,[8,3]],
 ["2422",2,4,[4,2]],["24A4",2,4,[12,3]]];
 row:=First(extensions,r->r[1]=label);
 if row=fail then Error("uninterpreted source Borel shape");fi;
 p:=row[2];rank:=row[3];qid:=row[4];
 if Size(B)<>p^rank*qid[1] then return false;fi;
 for N in NormalSubgroups(B) do
  if Size(N)=p^rank and IsElementaryAbelian(N) and IdGroup(FactorGroup(B,N))=qid then return true;fi;
 od;
 return false;
end;;
Phase180Borels:=function()
 local row,B,ok,first,failures;
 PrintTo(OUTPUT_FILE,"{\"status\":\"COMPLETE_SHAPE_DIAGNOSTIC\",\"extension_interpretation\":\"Normal elementary-abelian kernel with printed quotient; no unspecified action or splitting inferred\",\"rows\":[\n");
 first:=true;failures:=[];
 for row in sourceBorelRows do
  B:=Intersection(M22Triples[row[2]]);ok:=Phase180BorelShape(B,row[3]);
  if not first then AppendTo(OUTPUT_FILE,",\n");fi;first:=false;
  AppendTo(OUTPUT_FILE,"{\"source_row\":",row[1],",\"witness\":",row[2],",\"printed_shape\":\"",row[3],"\",\"actual_small_group_id\":",IdGroup(B),",\"shape_compatible\":",ok,"}");
  if not ok then Add(failures,row[1]);fi;
 od;
 AppendTo(OUTPUT_FILE,"\n],\"incompatible_rows\":",failures,"}\n");
 Print("PHASE180_BOREL_SHAPES_COMPLETE ",Length(sourceBorelRows)," INCOMPATIBLE ",failures,"\n");
end;;
Phase180Borels();;
QUIT;
