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
D:=P177Graph("108_020",108,[1, 2, 3, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 31, 32, 33, 37, 38, 39, 43, 44, 45, 52, 53, 54, 61, 62, 63, 73, 74, 75, 82, 83, 84, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102],[[1, 4], [1, 7], [1, 8], [1, 10], [2, 4], [2, 55], [2, 56], [2, 76], [3, 10], [3, 76], [3, 85], [3, 86], [4, 13], [4, 19], [5, 13], [5, 82], [5, 83], [5, 94], [6, 19], [6, 91], [6, 92], [6, 94], [7, 16], [7, 17], [7, 22], [8, 31], [8, 32], [8, 43], [9, 22], [9, 43], [9, 94], [9, 95], [10, 25], [10, 37], [11, 25], [11, 95], [11, 98], [11, 99], [12, 37], [12, 73], [12, 74], [12, 95], [13, 28], [13, 40], [14, 28], [14, 49], [14, 50], [14, 85], [15, 40], [15, 85], [15, 106], [15, 107], [16, 34], [16, 35], [16, 46], [17, 58], [17, 59], [17, 72], [18, 46], [18, 72], [18, 76], [18, 77], [19, 48], [19, 64], [20, 48], [20, 86], [20, 104], [20, 105], [21, 59], [21, 60], [21, 64], [21, 86], [22, 49], [22, 67], [23, 49], [23, 77], [23, 80], [23, 81], [24, 40], [24, 41], [24, 67], [24, 77], [25, 29], [25, 70], [26, 29], [26, 34], [26, 36], [26, 55], [27, 55], [27, 70], [27, 106], [27, 108], [28, 52], [28, 73], [29, 52], [29, 91], [30, 73], [30, 91], [30, 100], [30, 102], [31, 50], [31, 51], [31, 79], [32, 42], [32, 68], [32, 69], [33, 42], [33, 76], [33, 78], [33, 79], [34, 61], [34, 62], [35, 73], [35, 75], [35, 90], [36, 43], [36, 44], [36, 90], [37, 66], [37, 81], [38, 56], [38, 81], [38, 103], [38, 105], [39, 56], [39, 66], [39, 67], [39, 69], [40, 62], [41, 89], [41, 90], [41, 92], [42, 62], [42, 92], [43, 60], [44, 47], [44, 48], [44, 78], [45, 60], [45, 70], [45, 71], [45, 78], [46, 53], [46, 82], [47, 82], [47, 101], [47, 102], [48, 53], [49, 88], [50, 61], [50, 63], [51, 88], [51, 91], [51, 93], [52, 59], [52, 69], [53, 69], [53, 106], [54, 59], [54, 79], [54, 81], [54, 106], [55, 97], [56, 75], [57, 75], [57, 94], [57, 96], [57, 97], [58, 83], [58, 84], [58, 100], [60, 100], [61, 64], [61, 66], [62, 105], [63, 70], [63, 72], [63, 105], [64, 99], [65, 83], [65, 88], [65, 90], [65, 99], [66, 83], [67, 102], [68, 97], [68, 99], [68, 102], [71, 74], [71, 88], [71, 89], [72, 74], [74, 107], [75, 107], [77, 96], [78, 96], [79, 98], [80, 98], [80, 100], [80, 101], [82, 103], [84, 85], [84, 87], [84, 103], [86, 93], [87, 93], [87, 95], [87, 96], [89, 103], [89, 104], [92, 108], [93, 108], [97, 104], [98, 104], [101, 107], [101, 108]]);;
R:=P177Census(D);;Need(Size(R.F)=864);;
PrintTo("current_c4_descent/108_020.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 108_020 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
