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
D:=P177Graph("096_035",96,[1, 5, 6, 8, 9, 10, 13, 14, 15, 16, 19, 23, 24, 28, 33, 34, 39, 41, 42, 43, 46, 47, 48, 50, 51, 55, 56, 59, 60, 62, 63, 65, 66, 67, 68, 72, 76, 77, 78, 79, 82, 84, 87, 88, 89, 90, 95, 96],[[1, 2], [1, 4], [1, 44], [1, 71], [2, 5], [2, 8], [2, 62], [3, 6], [3, 9], [3, 72], [3, 88], [4, 10], [4, 16], [4, 34], [5, 11], [5, 17], [5, 73], [6, 12], [6, 18], [6, 91], [7, 13], [7, 19], [7, 51], [7, 78], [8, 20], [8, 31], [8, 61], [9, 17], [9, 21], [9, 32], [10, 17], [10, 22], [10, 45], [11, 23], [11, 33], [11, 87], [12, 24], [12, 34], [12, 68], [13, 25], [13, 35], [13, 91], [14, 26], [14, 36], [14, 58], [14, 81], [15, 26], [15, 27], [15, 37], [15, 49], [16, 38], [16, 58], [16, 85], [17, 19], [18, 33], [18, 39], [18, 59], [19, 40], [19, 52], [20, 33], [20, 41], [20, 72], [21, 23], [21, 34], [21, 42], [22, 43], [22, 56], [22, 60], [23, 44], [23, 93], [24, 45], [24, 61], [24, 64], [25, 41], [25, 46], [25, 62], [26, 47], [26, 68], [27, 48], [27, 62], [27, 63], [28, 31], [28, 49], [28, 64], [28, 81], [29, 42], [29, 50], [29, 90], [29, 95], [30, 50], [30, 51], [30, 65], [30, 77], [31, 63], [31, 90], [32, 47], [32, 77], [32, 96], [33, 36], [34, 37], [35, 59], [35, 60], [35, 66], [36, 46], [36, 79], [37, 67], [37, 82], [38, 51], [38, 60], [38, 68], [39, 44], [39, 61], [39, 69], [40, 43], [40, 55], [40, 62], [41, 49], [41, 86], [42, 70], [42, 74], [43, 71], [43, 92], [44, 89], [45, 72], [45, 76], [46, 73], [46, 85], [47, 73], [47, 74], [48, 69], [48, 75], [48, 91], [49, 76], [50, 53], [50, 64], [51, 73], [52, 76], [52, 77], [52, 95], [53, 59], [53, 78], [53, 87], [54, 55], [54, 79], [54, 89], [54, 96], [55, 69], [55, 80], [56, 80], [56, 81], [56, 83], [57, 72], [57, 77], [57, 79], [57, 84], [58, 82], [58, 89], [59, 83], [60, 64], [61, 65], [63, 74], [63, 92], [65, 75], [65, 94], [66, 70], [66, 71], [66, 85], [67, 70], [67, 86], [67, 91], [68, 75], [69, 78], [70, 88], [71, 90], [74, 87], [75, 96], [76, 80], [78, 93], [79, 83], [80, 82], [81, 87], [82, 93], [83, 88], [84, 85], [84, 86], [84, 94], [86, 95], [88, 92], [89, 94], [90, 94], [92, 96], [93, 95]]);;
R:=P177Census(D);;Need(Size(R.F)=384);;
PrintTo("current_c4_descent/096_035.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_035 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
