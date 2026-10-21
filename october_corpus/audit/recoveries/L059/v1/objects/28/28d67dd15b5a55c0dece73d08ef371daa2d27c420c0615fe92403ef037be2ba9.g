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
D:=P177Graph("108_014",108,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54],[[1, 63], [1, 71], [1, 79], [1, 81], [2, 63], [2, 68], [2, 79], [2, 83], [3, 55], [3, 73], [3, 76], [3, 80], [4, 55], [4, 69], [4, 74], [4, 87], [5, 55], [5, 75], [5, 80], [5, 84], [6, 68], [6, 71], [6, 81], [6, 83], [7, 55], [7, 69], [7, 77], [7, 88], [8, 72], [8, 74], [8, 78], [8, 102], [9, 60], [9, 62], [9, 63], [9, 65], [10, 59], [10, 60], [10, 72], [10, 80], [11, 58], [11, 72], [11, 74], [11, 93], [12, 60], [12, 63], [12, 64], [12, 96], [13, 73], [13, 75], [13, 76], [13, 84], [14, 74], [14, 77], [14, 87], [14, 88], [15, 60], [15, 80], [15, 86], [15, 94], [16, 61], [16, 77], [16, 86], [16, 106], [17, 65], [17, 66], [17, 99], [17, 101], [18, 59], [18, 66], [18, 71], [18, 107], [19, 69], [19, 79], [19, 99], [19, 103], [20, 57], [20, 77], [20, 86], [20, 98], [21, 65], [21, 67], [21, 99], [21, 100], [22, 59], [22, 70], [22, 71], [22, 95], [23, 69], [23, 79], [23, 85], [23, 92], [24, 58], [24, 78], [24, 93], [24, 102], [25, 62], [25, 64], [25, 65], [25, 96], [26, 59], [26, 72], [26, 86], [26, 94], [27, 64], [27, 70], [27, 82], [27, 85], [28, 67], [28, 68], [28, 94], [28, 108], [29, 76], [29, 78], [29, 103], [29, 105], [30, 81], [30, 87], [30, 101], [30, 105], [31, 64], [31, 85], [31, 91], [31, 97], [32, 56], [32, 68], [32, 91], [32, 94], [33, 66], [33, 67], [33, 100], [33, 101], [34, 61], [34, 76], [34, 103], [34, 104], [35, 81], [35, 82], [35, 87], [35, 90], [36, 57], [36, 61], [36, 98], [36, 106], [37, 66], [37, 70], [37, 95], [37, 107], [38, 85], [38, 92], [38, 99], [38, 103], [39, 58], [39, 75], [39, 90], [39, 92], [40, 83], [40, 88], [40, 100], [40, 104], [41, 62], [41, 73], [41, 102], [41, 107], [42, 70], [42, 82], [42, 91], [42, 97], [43, 57], [43, 75], [43, 89], [43, 92], [44, 83], [44, 88], [44, 89], [44, 97], [45, 61], [45, 78], [45, 104], [45, 105], [46, 62], [46, 73], [46, 106], [46, 108], [47, 56], [47, 67], [47, 91], [47, 108], [48, 82], [48, 90], [48, 101], [48, 105], [49, 84], [49, 93], [49, 95], [49, 96], [50, 57], [50, 58], [50, 89], [50, 90], [51, 56], [51, 84], [51, 96], [51, 98], [52, 102], [52, 106], [52, 107], [52, 108], [53, 89], [53, 97], [53, 100], [53, 104], [54, 56], [54, 93], [54, 95], [54, 98]]);;
R:=P177Census(D);;Need(Size(R.F)=432);;
PrintTo("current_c4_descent/108_014.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 108_014 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
