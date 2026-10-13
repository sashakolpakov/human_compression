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
D:=P177Graph("108_002",108,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107],[[1, 38], [1, 72], [1, 74], [1, 108], [2, 37], [2, 39], [2, 73], [2, 75], [3, 38], [3, 40], [3, 74], [3, 76], [4, 39], [4, 41], [4, 75], [4, 77], [5, 40], [5, 42], [5, 76], [5, 78], [6, 41], [6, 43], [6, 77], [6, 79], [7, 42], [7, 44], [7, 78], [7, 80], [8, 43], [8, 45], [8, 79], [8, 81], [9, 44], [9, 46], [9, 80], [9, 82], [10, 45], [10, 47], [10, 81], [10, 83], [11, 46], [11, 48], [11, 82], [11, 84], [12, 47], [12, 49], [12, 83], [12, 85], [13, 48], [13, 50], [13, 84], [13, 86], [14, 49], [14, 51], [14, 85], [14, 87], [15, 50], [15, 52], [15, 86], [15, 88], [16, 51], [16, 53], [16, 87], [16, 89], [17, 52], [17, 54], [17, 88], [17, 90], [18, 53], [18, 55], [18, 89], [18, 91], [19, 54], [19, 56], [19, 90], [19, 92], [20, 55], [20, 57], [20, 91], [20, 93], [21, 56], [21, 58], [21, 92], [21, 94], [22, 57], [22, 59], [22, 93], [22, 95], [23, 58], [23, 60], [23, 94], [23, 96], [24, 59], [24, 61], [24, 95], [24, 97], [25, 60], [25, 62], [25, 96], [25, 98], [26, 61], [26, 63], [26, 97], [26, 99], [27, 62], [27, 64], [27, 98], [27, 100], [28, 63], [28, 65], [28, 99], [28, 101], [29, 64], [29, 66], [29, 100], [29, 102], [30, 65], [30, 67], [30, 101], [30, 103], [31, 66], [31, 68], [31, 102], [31, 104], [32, 67], [32, 69], [32, 103], [32, 105], [33, 68], [33, 70], [33, 104], [33, 106], [34, 69], [34, 71], [34, 105], [34, 107], [35, 70], [35, 72], [35, 106], [35, 108], [36, 37], [36, 71], [36, 73], [36, 107], [37, 74], [37, 108], [38, 73], [38, 75], [39, 74], [39, 76], [40, 75], [40, 77], [41, 76], [41, 78], [42, 77], [42, 79], [43, 78], [43, 80], [44, 79], [44, 81], [45, 80], [45, 82], [46, 81], [46, 83], [47, 82], [47, 84], [48, 83], [48, 85], [49, 84], [49, 86], [50, 85], [50, 87], [51, 86], [51, 88], [52, 87], [52, 89], [53, 88], [53, 90], [54, 89], [54, 91], [55, 90], [55, 92], [56, 91], [56, 93], [57, 92], [57, 94], [58, 93], [58, 95], [59, 94], [59, 96], [60, 95], [60, 97], [61, 96], [61, 98], [62, 97], [62, 99], [63, 98], [63, 100], [64, 99], [64, 101], [65, 100], [65, 102], [66, 101], [66, 103], [67, 102], [67, 104], [68, 103], [68, 105], [69, 104], [69, 106], [70, 105], [70, 107], [71, 106], [71, 108], [72, 73], [72, 107]]);;
R:=P177Census(D);;Need(Size(R.F)=432);;
PrintTo("current_c4_descent/108_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 108_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
