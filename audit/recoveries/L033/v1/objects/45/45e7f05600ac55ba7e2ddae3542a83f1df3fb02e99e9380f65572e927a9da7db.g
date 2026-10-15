hyperbolic_records:=[];;
DescribeHyperbolic := function(root,output)
  local stream,first,typ,r,H,R,D,Q,item,fn,perms;
  stream:=OutputTextFile(output,false); SetPrintFormattingStatus(stream,false);
  PrintTo(stream,"[\n"); first:=true;
  for typ in ["3434","3334","3335","3534","353","435","535","5333"] do
    fn:=Concatenation(root,"/",typ,"_broad01/records.g"); Read(fn);
    for r in hyperbolic_records do
      perms:=List(r.permutations,PermList); H:=Group(perms);
      Print("DESCRIBE ",typ," NODE ",r.node," ORDER ",r.order,"\n");
      R:=RadicalGroup(H); D:=DerivedSubgroup(H); Q:=FactorGroup(H,R);
      if not first then PrintTo(stream,",\n"); fi; first:=false;
      PrintTo(stream,"{\"type\":\"",typ,"\",\"node\":",r.node,",\"order\":",r.order,",\"degree\":",r.degree,
        ",\"structure\":\"",StructureDescription(H),"\",\"radical_order\":",Size(R),
        ",\"radical_structure\":\"",StructureDescription(R),"\",\"semisimple_quotient\":\"",StructureDescription(Q),
        "\",\"derived_order\":",Size(D),",\"center_order\":",Size(Centre(H)),
        ",\"local_orders\":",r.checks.local_orders,",\"permutations\":",r.permutations,"}");
    od;
  od;
  PrintTo(stream,"\n]\n"); CloseStream(stream); Print("COMPLETE_DESCRIPTIONS\n");
end;;
