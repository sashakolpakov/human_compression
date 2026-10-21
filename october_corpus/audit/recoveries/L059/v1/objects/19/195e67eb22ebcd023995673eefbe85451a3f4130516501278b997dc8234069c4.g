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
D:=P177Graph("108_019",108,[1, 2, 3, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 37, 38, 39, 49, 50, 51, 55, 56, 57, 61, 62, 63, 73, 74, 75, 76, 77, 78, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102],[[1, 4], [1, 7], [1, 8], [1, 10], [2, 4], [2, 34], [2, 36], [2, 64], [3, 10], [3, 58], [3, 60], [3, 64], [4, 13], [4, 19], [5, 13], [5, 61], [5, 63], [5, 94], [6, 19], [6, 85], [6, 87], [6, 94], [7, 16], [7, 17], [7, 22], [8, 19], [8, 21], [8, 37], [9, 22], [9, 37], [9, 88], [9, 90], [10, 17], [10, 25], [11, 25], [11, 91], [11, 93], [11, 95], [12, 17], [12, 77], [12, 78], [12, 95], [13, 28], [13, 34], [14, 28], [14, 46], [14, 47], [14, 72], [15, 34], [15, 72], [15, 103], [15, 105], [16, 31], [16, 32], [16, 40], [17, 67], [18, 40], [18, 67], [18, 106], [18, 108], [19, 43], [20, 43], [20, 70], [20, 107], [20, 108], [21, 52], [21, 53], [21, 70], [22, 32], [22, 46], [23, 46], [23, 65], [23, 71], [23, 72], [24, 32], [24, 44], [24, 45], [24, 65], [25, 29], [25, 58], [26, 29], [26, 42], [26, 79], [26, 80], [27, 42], [27, 58], [27, 104], [27, 105], [28, 49], [28, 61], [29, 49], [29, 91], [30, 61], [30, 91], [30, 97], [30, 98], [31, 55], [31, 56], [31, 73], [32, 97], [33, 73], [33, 91], [33, 92], [33, 97], [34, 76], [35, 76], [35, 89], [35, 90], [35, 92], [36, 73], [36, 74], [36, 92], [37, 53], [37, 79], [38, 41], [38, 42], [38, 66], [38, 79], [39, 53], [39, 66], [39, 68], [39, 69], [40, 56], [40, 63], [41, 63], [41, 94], [41, 96], [42, 56], [43, 50], [43, 85], [44, 50], [44, 101], [44, 102], [45, 85], [45, 97], [45, 99], [46, 88], [47, 49], [47, 51], [47, 75], [48, 75], [48, 86], [48, 87], [48, 88], [49, 80], [50, 80], [50, 108], [51, 67], [51, 68], [51, 108], [52, 55], [52, 57], [52, 100], [53, 98], [54, 61], [54, 62], [54, 98], [54, 100], [55, 82], [55, 83], [56, 105], [57, 70], [57, 72], [57, 105], [58, 86], [59, 62], [59, 86], [59, 88], [59, 89], [60, 62], [60, 100], [60, 101], [62, 106], [63, 106], [64, 74], [64, 101], [65, 96], [65, 101], [66, 74], [66, 96], [67, 78], [68, 74], [68, 75], [69, 78], [69, 98], [69, 99], [70, 93], [71, 93], [71, 95], [71, 96], [73, 83], [75, 83], [76, 81], [76, 103], [77, 81], [77, 82], [77, 84], [78, 103], [79, 90], [80, 102], [81, 90], [81, 102], [82, 100], [82, 102], [83, 87], [84, 87], [84, 94], [84, 95], [85, 104], [86, 104], [89, 106], [89, 107], [92, 107], [93, 107], [99, 103], [99, 104]]);;
R:=P177Census(D);;Need(Size(R.F)=432);;
PrintTo("current_c4_descent/108_019.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 108_019 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
