# Literal presentation, no auxiliary relations.  Tables are lower-bound
# certificates until the separate deduction checker has succeeded.
LoadPackage("ace");;
SizeScreen([4096,4096]);;
ExportTable:=function(d,path)
  local n,f,r,rels,i,j,k,ct,stream,row;
  n:=11; f:=FreeGroup(d); r:=GeneratorsOfGroup(f);
  rels:=List(r,x->x^2);
  for i in [1..d-1] do for j in [i+1..d] do
    if j=i+1 then Add(rels,(r[i]*r[j])^n);
    else Add(rels,(r[i]*r[j])^2);fi;
  od;od;
  for i in [1..d-2] do for k in [1..n-1] do
    Add(rels,((r[i+1]*r[i+2])^k*(r[i]*r[i+1])^k)^2);
  od;od;
  Print("START d=",d,"\n");
  if IsExistingFile(path) then
    Print("REFUSING TO OVERWRITE ",path,"\n"); FORCE_QUIT_GAP(1);
  fi;
  ct:=ACECosetTable(r,rels,r{[1..d-1]}:
      hard,workspace:=20000000,time:=120,acenowarnings);
  if ct=fail then Print("ENUMERATION FAILED\n");FORCE_QUIT_GAP(1);fi;
  stream:=OutputTextFile(path,false);
  SetPrintFormattingStatus(stream,false);
  PrintTo(stream,Length(ct[1])," ",d,"\n");
  for i in [1..Length(ct[1])] do
    row:=List([1..d],j->ct[2*j-1][i]);
    for j in [1..d] do PrintTo(stream,row[j]," ");od;
    PrintTo(stream,"\n");
  od;
  CloseStream(stream);
  Print("EXPORTED d=",d," index=",Length(ct[1])," path=",path,"\n");
end;;
P214Output:=GetEnv("PHASE214_OUT");;
if P214Output=fail then P214Output:=DirectoryTemporary();
else P214Output:=Directory(P214Output);fi;
ExportTable(3,Filename(P214Output,"phase214_table3.txt"));
ExportTable(4,Filename(P214Output,"phase214_table4.txt"));
ExportTable(5,Filename(P214Output,"phase214_table5.txt"));
QUIT;
