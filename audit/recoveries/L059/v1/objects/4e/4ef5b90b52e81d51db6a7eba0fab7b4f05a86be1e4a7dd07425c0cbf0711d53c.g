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
D:=P177Graph("120_033",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 65, 66, 67, 68, 69, 70, 71, 72, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108],[[1, 24], [1, 25], [1, 53], [1, 54], [2, 18], [2, 19], [2, 53], [2, 54], [3, 18], [3, 19], [3, 59], [3, 60], [4, 24], [4, 25], [4, 59], [4, 60], [5, 53], [5, 64], [5, 77], [5, 78], [6, 58], [6, 59], [6, 77], [6, 78], [7, 58], [7, 59], [7, 83], [7, 84], [8, 53], [8, 64], [8, 83], [8, 84], [9, 82], [9, 83], [9, 119], [9, 120], [10, 76], [10, 77], [10, 119], [10, 120], [11, 76], [11, 77], [11, 113], [11, 114], [12, 82], [12, 83], [12, 113], [12, 114], [13, 80], [13, 81], [13, 109], [13, 110], [14, 74], [14, 75], [14, 109], [14, 110], [15, 74], [15, 75], [15, 115], [15, 116], [16, 80], [16, 81], [16, 115], [16, 116], [17, 29], [17, 32], [17, 85], [17, 86], [18, 85], [18, 86], [19, 101], [19, 102], [20, 38], [20, 39], [20, 101], [20, 102], [21, 38], [21, 39], [21, 93], [21, 94], [22, 30], [22, 31], [22, 93], [22, 94], [23, 30], [23, 31], [23, 87], [23, 88], [24, 87], [24, 88], [25, 103], [25, 104], [26, 37], [26, 40], [26, 103], [26, 104], [27, 37], [27, 40], [27, 95], [27, 96], [28, 29], [28, 32], [28, 95], [28, 96], [29, 57], [29, 58], [30, 57], [30, 58], [31, 63], [31, 64], [32, 63], [32, 64], [33, 60], [33, 61], [33, 73], [33, 74], [34, 54], [34, 55], [34, 73], [34, 74], [35, 54], [35, 55], [35, 79], [35, 80], [36, 60], [36, 61], [36, 79], [36, 80], [37, 55], [37, 56], [38, 55], [38, 56], [39, 61], [39, 62], [40, 61], [40, 62], [41, 65], [41, 66], [41, 93], [41, 96], [42, 65], [42, 66], [42, 86], [42, 87], [43, 86], [43, 87], [43, 89], [43, 90], [44, 89], [44, 90], [44, 102], [44, 103], [45, 102], [45, 103], [45, 105], [45, 106], [46, 94], [46, 95], [46, 105], [46, 106], [47, 67], [47, 68], [47, 94], [47, 95], [48, 67], [48, 68], [48, 85], [48, 88], [49, 85], [49, 88], [49, 91], [49, 92], [50, 91], [50, 92], [50, 101], [50, 104], [51, 101], [51, 104], [51, 107], [51, 108], [52, 93], [52, 96], [52, 107], [52, 108], [56, 98], [56, 99], [57, 98], [57, 99], [62, 97], [62, 100], [63, 97], [63, 100], [65, 116], [65, 117], [66, 110], [66, 111], [67, 110], [67, 111], [68, 116], [68, 117], [69, 73], [69, 84], [69, 117], [69, 118], [70, 78], [70, 79], [70, 117], [70, 118], [71, 78], [71, 79], [71, 111], [71, 112], [72, 73], [72, 84], [72, 111], [72, 112], [75, 97], [75, 98], [76, 97], [76, 98], [81, 99], [81, 100], [82, 99], [82, 100], [89, 114], [89, 115], [90, 109], [90, 120], [91, 109], [91, 120], [92, 114], [92, 115], [105, 112], [105, 113], [106, 118], [106, 119], [107, 118], [107, 119], [108, 112], [108, 113]]);;
R:=P177Census(D);;Need(Size(R.F)=1920);;
PrintTo("current_c4_descent/120_033.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_033 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
