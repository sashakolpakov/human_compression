Need:=function(ok) if not ok then Error("L059 cubic census invalid"); fi; end;;
Read("maximal_descent.g");;

# Exact rank-two marked-geometry census for explicitly constructed graphs.
# This is a new bounded census, not a replay of the unrecovered historical lists.
LoadPackage("grape");;
SetAssertionLevel(1);;

P177Graph := function(label, n, black, edges)
  local E, graph, white;
  E := Set(List(edges, Set));
  white := Difference([1..n], black);
  Need( ForAll(E,e->Length(e)=2 and Length(Intersection(e,black))=1));
  graph := Graph(Group(()), [1..n], OnPoints, function(a,b) return Set([a,b]) in E; end, true);
  Need( IsConnectedGraph(graph));
  return rec(label:=label,n:=n,black:=Set(black),white:=white,edges:=E,graph:=graph);
end;;

P177Max := function(upper,lower)
  local degree, action;
  degree := Index(upper,lower);
  Need(degree>1);
  action := Action(upper,RightCosets(upper,lower),OnRight);
  if Transitivity(action,[1..degree])>=2 then return "2T"; fi;
  if IsPrimitive(action,[1..degree]) then return "M"; fi;
  return "X";
end;;

P177Census := function(data)
  local A, F, classes, edge, b, w, witnesses, H, H0, H1, B, D, duals,
        row, cls, maxcode, normcode, maxorder, dualorder, suborders;
  A := AutGroupGraph(data.graph,[data.black,data.white]);
  F := AutGroupGraph(data.graph);
  Need(IsTransitive(A,data.edges,OnSets));
  edge := data.edges[1];
  b := Intersection(edge,data.black)[1]; w := Intersection(edge,data.white)[1];
  classes := L059Descent(A,data.edges);
  witnesses := [];
  for cls in classes do
    H := Representative(cls);
    if IsTransitive(H,data.edges,OnSets) then
      H0 := Stabilizer(H,b); H1 := Stabilizer(H,w); B := Intersection(H0,H1);
      Need(Size(ClosureGroup(H0,H1))=Size(H));
      Need(Size(Core(H,B))=1);
      Need(Index(H,B)=Length(data.edges));
      maxcode := List([[H0,B],[H1,B],[H,H0],[H,H1]],p->P177Max(p[1],p[2]));
      normcode := List([H,H0,H1,B],K->IsNormal(A,K));
      D := Stabilizer(Normalizer(F,H),edge,OnSets);
      duals := Filtered(Elements(D),g->b^g=w);
      if IsEmpty(duals) then dualorder:=0; else dualorder:=Minimum(List(duals,Order)); fi;
      maxorder := Maximum(List(ConjugacyClasses(H),c->Order(Representative(c))));
      row := rec(H:=H,H0:=H0,H1:=H1,B:=B,maxcode:=maxcode,normcode:=normcode,
                 dualorder:=dualorder,maxorder:=maxorder,
                 group_order:=Size(H),subgroup_orders:=List([H0,H1,B],Size),
                 structure:=List([H,H0,H1,B],StructureDescription));
      Add(witnesses,row);
    fi;
  od;
  Print(data.label," vertices=",data.n," edges=",Length(data.edges)," Aut+=",Size(A),
        " Aut=",Size(F)," subgroup_classes=",Length(classes)," geometries=",Length(witnesses),"\n");
  Print("MAX ",Collected(List(witnesses,r->r.maxcode)),"\n");
  Print("NORM ",Collected(List(witnesses,r->r.normcode)),"\n");
  return rec(label:=data.label,n:=data.n,black:=data.black,white:=data.white,edges:=data.edges,
             A:=A,F:=F,base_edge:=edge,b:=b,w:=w,retained_edge_transitive_classes:=Length(classes),search:=L059Search,witnesses:=witnesses);
end;;


t:=Runtime();;
D:=P177Graph("VT3_86_8",86,[1, 3, 4, 6, 8, 9, 12, 13, 15, 18, 19, 21, 22, 25, 26, 27, 29, 34, 36, 38, 39, 41, 45, 47, 53, 55, 56, 58, 59, 60, 62, 64, 66, 68, 71, 72, 74, 75, 76, 78, 79, 81, 86],[[1, 16], [1, 65], [1, 67], [2, 29], [2, 45], [2, 55], [3, 16], [3, 33], [3, 46], [4, 5], [4, 51], [4, 83], [5, 15], [5, 64], [6, 33], [6, 35], [6, 51], [7, 15], [7, 19], [7, 66], [8, 31], [8, 32], [8, 57], [9, 24], [9, 51], [9, 82], [10, 45], [10, 47], [10, 59], [11, 41], [11, 56], [11, 86], [12, 54], [12, 61], [12, 85], [13, 23], [13, 30], [13, 63], [14, 21], [14, 34], [14, 55], [15, 30], [16, 22], [17, 39], [17, 72], [17, 75], [18, 37], [18, 61], [18, 70], [19, 23], [19, 54], [20, 55], [20, 58], [20, 74], [21, 32], [21, 49], [22, 35], [22, 43], [23, 79], [24, 36], [24, 64], [25, 43], [25, 67], [25, 85], [26, 54], [26, 70], [26, 80], [27, 40], [27, 52], [27, 63], [28, 41], [28, 47], [28, 62], [29, 46], [29, 69], [30, 81], [31, 36], [31, 76], [32, 53], [33, 78], [34, 46], [34, 65], [35, 72], [36, 50], [37, 39], [37, 62], [38, 50], [38, 82], [38, 84], [39, 84], [40, 59], [40, 81], [41, 84], [42, 56], [42, 60], [42, 71], [43, 75], [44, 60], [44, 68], [44, 79], [45, 77], [47, 52], [48, 53], [48, 68], [48, 71], [49, 74], [49, 76], [50, 86], [52, 56], [53, 65], [57, 71], [57, 86], [58, 70], [58, 77], [59, 69], [60, 63], [61, 75], [62, 77], [64, 73], [66, 73], [66, 80], [67, 68], [69, 78], [72, 82], [73, 76], [74, 80], [78, 83], [79, 85], [81, 83]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_86_8.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_86_8 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
