# Independent route through an actual D10 character table and table induction.
LoadPackage("ctbllib");;
if Z(9)^2<>Z(9)+One(GF(9)) then Error("paper/GAP field generator mismatch");fi;
tab:=CharacterTable("U5(3)");;ch:=Irr(tab);;
htab:=CharacterTable(DihedralGroup(IsPermGroup,10));;
cp:=SizesCentralizers(tab);;oc:=OrdersClassRepresentatives(tab);;
invol:=Filtered([1..Length(cp)],i->oc[i]=2);;
if List(invol,i->cp[i])<>[52254720,580608] then Error("involution table data");fi;
pos2:=First(invol,i->cp[i]=580608);;
pos5:=Filtered([1..Length(cp)],i->oc[i]=5);;
if Length(pos5)<>1 or cp[pos5[1]]<>80 then Error("rotation fusion");fi;
fusion:=List(OrdersClassRepresentatives(htab),function(o)
 if o=1 then return 1;elif o=2 then return pos2;elif o=5 then return pos5[1];else Error("D10 classes");fi;
end);;
ind:=InducedClassFunctionsByFusionMap(htab,tab,[TrivialCharacter(htab)],fusion)[1];;
mm:=List(ch,c->ScalarProduct(tab,c,ind));;
if not ForAll(mm,x->IsInt(x) and x>0) then Error("positive multiplicities");fi;
fs:=Indicator(tab,2);;negpos:=Filtered([1..Length(ch)],i->fs[i]=-1);;
lowpos:=Filtered([1..Length(ch)],i->ch[i][1]<=3846);;
if Length(lowpos)<>24 or Minimum(List(Difference([1..Length(ch)],lowpos),i->ch[i][1]))<>4270 then Error("degree partition");fi;
rows:=List(lowpos,i->[ch[i][1],ch[i][pos2],ch[i][pos5[1]],mm[i]]);;
Print("{\"status\":\"PASS\",\"class_fusion\":",fusion,",\"subgroup_class_sizes\":",SizesConjugacyClasses(htab),",\"multiplicities\":",mm,",\"low_rows\":",rows,",\"negative_FS\":",List(negpos,i->[ch[i][1],mm[i]]),",\"gap\":\"",GAPInfo.Version,"\",\"ctbllib\":\"",PackageInfo("ctbllib")[1].Version,"\"}\n");
QUIT;
