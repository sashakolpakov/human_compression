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
D:=P177Graph("VT3_112_32",112,[1, 2, 4, 8, 9, 11, 12, 13, 14, 16, 17, 18, 21, 23, 24, 27, 28, 29, 33, 34, 35, 36, 37, 38, 39, 42, 43, 48, 50, 54, 55, 57, 58, 64, 66, 68, 71, 72, 74, 75, 78, 79, 82, 84, 87, 89, 90, 91, 94, 95, 96, 97, 98, 109, 110, 112],[[1, 22], [1, 52], [1, 60], [2, 32], [2, 104], [2, 108], [3, 27], [3, 58], [3, 71], [4, 61], [4, 83], [4, 85], [5, 35], [5, 68], [5, 75], [6, 50], [6, 84], [6, 98], [7, 17], [7, 39], [7, 57], [8, 20], [8, 44], [8, 65], [9, 46], [9, 61], [9, 76], [10, 14], [10, 24], [10, 78], [11, 32], [11, 88], [11, 111], [12, 15], [12, 41], [12, 76], [13, 19], [13, 51], [13, 106], [14, 76], [14, 107], [15, 34], [15, 91], [16, 45], [16, 101], [16, 103], [17, 56], [17, 106], [18, 22], [18, 44], [18, 92], [19, 29], [19, 64], [20, 27], [20, 98], [21, 41], [21, 47], [21, 52], [22, 82], [23, 25], [23, 62], [23, 80], [24, 80], [24, 108], [25, 28], [25, 79], [26, 50], [26, 54], [26, 72], [27, 107], [28, 31], [28, 59], [29, 49], [29, 67], [30, 34], [30, 90], [30, 98], [31, 42], [31, 64], [32, 110], [33, 77], [33, 93], [33, 102], [34, 86], [35, 40], [35, 53], [36, 49], [36, 86], [36, 105], [37, 41], [37, 59], [37, 88], [38, 77], [38, 86], [38, 103], [39, 47], [39, 70], [40, 48], [40, 55], [42, 93], [42, 107], [43, 47], [43, 73], [43, 103], [44, 57], [45, 82], [45, 89], [46, 96], [46, 97], [48, 65], [48, 99], [49, 75], [50, 59], [51, 74], [51, 97], [52, 68], [53, 74], [53, 90], [54, 67], [54, 81], [55, 63], [55, 88], [56, 79], [56, 87], [57, 100], [58, 70], [58, 85], [60, 66], [60, 71], [61, 72], [62, 94], [62, 109], [63, 78], [63, 112], [64, 101], [65, 96], [66, 102], [66, 111], [67, 71], [68, 80], [69, 75], [69, 95], [69, 110], [70, 110], [72, 92], [73, 84], [73, 97], [74, 102], [77, 87], [78, 81], [79, 99], [81, 87], [82, 104], [83, 90], [83, 109], [84, 108], [85, 89], [89, 99], [91, 104], [91, 106], [92, 95], [93, 95], [94, 105], [94, 111], [96, 105], [100, 109], [100, 112], [101, 112]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_112_32.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_112_32 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
