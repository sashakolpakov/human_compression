Need:=function(ok) if not ok then Error("L059 descent invalid"); fi; end;;
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
D:=P177Graph("102_003",102,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85],[[1, 19], [1, 34], [1, 90], [1, 99], [2, 18], [2, 20], [2, 91], [2, 100], [3, 19], [3, 21], [3, 92], [3, 101], [4, 20], [4, 22], [4, 93], [4, 102], [5, 21], [5, 23], [5, 86], [5, 94], [6, 22], [6, 24], [6, 87], [6, 95], [7, 23], [7, 25], [7, 88], [7, 96], [8, 24], [8, 26], [8, 89], [8, 97], [9, 25], [9, 27], [9, 90], [9, 98], [10, 26], [10, 28], [10, 91], [10, 99], [11, 27], [11, 29], [11, 92], [11, 100], [12, 28], [12, 30], [12, 93], [12, 101], [13, 29], [13, 31], [13, 94], [13, 102], [14, 30], [14, 32], [14, 86], [14, 95], [15, 31], [15, 33], [15, 87], [15, 96], [16, 32], [16, 34], [16, 88], [16, 97], [17, 18], [17, 33], [17, 89], [17, 98], [18, 39], [18, 48], [19, 40], [19, 49], [20, 41], [20, 50], [21, 42], [21, 51], [22, 35], [22, 43], [23, 36], [23, 44], [24, 37], [24, 45], [25, 38], [25, 46], [26, 39], [26, 47], [27, 40], [27, 48], [28, 41], [28, 49], [29, 42], [29, 50], [30, 43], [30, 51], [31, 35], [31, 44], [32, 36], [32, 45], [33, 37], [33, 46], [34, 38], [34, 47], [35, 53], [35, 68], [36, 52], [36, 54], [37, 53], [37, 55], [38, 54], [38, 56], [39, 55], [39, 57], [40, 56], [40, 58], [41, 57], [41, 59], [42, 58], [42, 60], [43, 59], [43, 61], [44, 60], [44, 62], [45, 61], [45, 63], [46, 62], [46, 64], [47, 63], [47, 65], [48, 64], [48, 66], [49, 65], [49, 67], [50, 66], [50, 68], [51, 52], [51, 67], [52, 73], [52, 82], [53, 74], [53, 83], [54, 75], [54, 84], [55, 76], [55, 85], [56, 69], [56, 77], [57, 70], [57, 78], [58, 71], [58, 79], [59, 72], [59, 80], [60, 73], [60, 81], [61, 74], [61, 82], [62, 75], [62, 83], [63, 76], [63, 84], [64, 77], [64, 85], [65, 69], [65, 78], [66, 70], [66, 79], [67, 71], [67, 80], [68, 72], [68, 81], [69, 87], [69, 102], [70, 86], [70, 88], [71, 87], [71, 89], [72, 88], [72, 90], [73, 89], [73, 91], [74, 90], [74, 92], [75, 91], [75, 93], [76, 92], [76, 94], [77, 93], [77, 95], [78, 94], [78, 96], [79, 95], [79, 97], [80, 96], [80, 98], [81, 97], [81, 99], [82, 98], [82, 100], [83, 99], [83, 101], [84, 100], [84, 102], [85, 86], [85, 101]]);;
R:=P177Census(D);;Need(Size(R.F)=408);;
PrintTo("current_c4_descent/102_003.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 102_003 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
