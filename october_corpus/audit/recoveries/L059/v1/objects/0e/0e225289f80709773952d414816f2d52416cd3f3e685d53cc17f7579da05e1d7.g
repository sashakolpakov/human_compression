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
D:=P177Graph("VT3_80_30",80,[1, 5, 6, 7, 8, 9, 10, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 69, 70, 71, 72, 73, 74, 75, 76, 80],[[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7], [3, 9], [4, 8], [4, 10], [5, 11], [5, 13], [6, 12], [6, 14], [7, 15], [7, 19], [8, 16], [8, 20], [9, 17], [9, 21], [10, 18], [10, 22], [11, 23], [11, 27], [12, 24], [12, 28], [13, 25], [13, 29], [14, 26], [14, 30], [15, 31], [15, 39], [16, 32], [16, 40], [17, 33], [17, 41], [18, 34], [18, 42], [19, 35], [19, 43], [20, 36], [20, 44], [21, 37], [21, 45], [22, 38], [22, 46], [23, 47], [23, 55], [24, 48], [24, 56], [25, 49], [25, 57], [26, 50], [26, 58], [27, 51], [27, 59], [28, 52], [28, 60], [29, 53], [29, 61], [30, 54], [30, 62], [31, 47], [31, 48], [32, 47], [32, 63], [33, 53], [33, 63], [34, 55], [34, 67], [35, 57], [35, 64], [36, 57], [36, 58], [37, 49], [37, 65], [38, 59], [38, 64], [39, 50], [39, 66], [40, 60], [40, 65], [41, 51], [41, 52], [42, 52], [42, 66], [43, 54], [43, 67], [44, 56], [44, 68], [45, 62], [45, 68], [46, 61], [46, 62], [48, 69], [49, 69], [50, 73], [51, 70], [53, 71], [54, 70], [55, 72], [56, 71], [58, 72], [59, 73], [60, 74], [61, 74], [63, 75], [64, 75], [65, 73], [66, 76], [67, 71], [68, 76], [69, 77], [70, 77], [72, 78], [74, 78], [75, 79], [76, 79], [77, 80], [78, 80], [79, 80]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_80_30.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_80_30 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
