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
D:=P177Graph("104_010",104,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52],[[1, 53], [1, 54], [1, 85], [1, 86], [2, 53], [2, 54], [2, 73], [2, 74], [3, 73], [3, 74], [3, 93], [3, 94], [4, 61], [4, 62], [4, 93], [4, 94], [5, 61], [5, 62], [5, 81], [5, 82], [6, 81], [6, 82], [6, 101], [6, 102], [7, 69], [7, 70], [7, 101], [7, 102], [8, 69], [8, 70], [8, 89], [8, 90], [9, 57], [9, 58], [9, 89], [9, 90], [10, 57], [10, 58], [10, 77], [10, 78], [11, 77], [11, 78], [11, 97], [11, 98], [12, 65], [12, 66], [12, 97], [12, 98], [13, 65], [13, 66], [13, 85], [13, 86], [14, 54], [14, 55], [14, 102], [14, 103], [15, 54], [15, 55], [15, 58], [15, 59], [16, 58], [16, 59], [16, 62], [16, 63], [17, 62], [17, 63], [17, 66], [17, 67], [18, 66], [18, 67], [18, 70], [18, 71], [19, 70], [19, 71], [19, 74], [19, 75], [20, 74], [20, 75], [20, 78], [20, 79], [21, 78], [21, 79], [21, 82], [21, 83], [22, 82], [22, 83], [22, 86], [22, 87], [23, 86], [23, 87], [23, 90], [23, 91], [24, 90], [24, 91], [24, 94], [24, 95], [25, 94], [25, 95], [25, 98], [25, 99], [26, 98], [26, 99], [26, 102], [26, 103], [27, 55], [27, 56], [27, 87], [27, 88], [28, 55], [28, 56], [28, 75], [28, 76], [29, 75], [29, 76], [29, 95], [29, 96], [30, 63], [30, 64], [30, 95], [30, 96], [31, 63], [31, 64], [31, 83], [31, 84], [32, 83], [32, 84], [32, 103], [32, 104], [33, 71], [33, 72], [33, 103], [33, 104], [34, 71], [34, 72], [34, 91], [34, 92], [35, 59], [35, 60], [35, 91], [35, 92], [36, 59], [36, 60], [36, 79], [36, 80], [37, 79], [37, 80], [37, 99], [37, 100], [38, 67], [38, 68], [38, 99], [38, 100], [39, 67], [39, 68], [39, 87], [39, 88], [40, 53], [40, 56], [40, 101], [40, 104], [41, 53], [41, 56], [41, 57], [41, 60], [42, 57], [42, 60], [42, 61], [42, 64], [43, 61], [43, 64], [43, 65], [43, 68], [44, 65], [44, 68], [44, 69], [44, 72], [45, 69], [45, 72], [45, 73], [45, 76], [46, 73], [46, 76], [46, 77], [46, 80], [47, 77], [47, 80], [47, 81], [47, 84], [48, 81], [48, 84], [48, 85], [48, 88], [49, 85], [49, 88], [49, 89], [49, 92], [50, 89], [50, 92], [50, 93], [50, 96], [51, 93], [51, 96], [51, 97], [51, 100], [52, 97], [52, 100], [52, 101], [52, 104]]);;
R:=P177Census(D);;Need(Size(R.F)=208);;
PrintTo("current_c4_descent/104_010.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 104_010 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
