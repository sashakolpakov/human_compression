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
D:=P177Graph("VT3_112_36",112,[1, 5, 6, 7, 8, 9, 10, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107],[[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7], [3, 9], [4, 8], [4, 10], [5, 11], [5, 13], [6, 12], [6, 14], [7, 15], [7, 19], [8, 16], [8, 20], [9, 17], [9, 21], [10, 18], [10, 22], [11, 23], [11, 27], [12, 24], [12, 28], [13, 25], [13, 29], [14, 26], [14, 30], [15, 31], [15, 38], [16, 32], [16, 39], [17, 25], [17, 33], [18, 34], [18, 35], [19, 35], [19, 40], [20, 28], [20, 41], [21, 36], [21, 42], [22, 37], [22, 43], [23, 44], [23, 51], [24, 45], [24, 52], [25, 46], [26, 47], [26, 48], [27, 48], [27, 53], [28, 54], [29, 49], [29, 55], [30, 50], [30, 56], [31, 57], [31, 70], [32, 58], [32, 71], [33, 59], [33, 72], [34, 60], [34, 73], [35, 61], [36, 62], [36, 64], [37, 63], [37, 65], [38, 64], [38, 74], [39, 65], [39, 75], [40, 66], [40, 76], [41, 67], [41, 77], [42, 68], [42, 78], [43, 69], [43, 79], [44, 80], [44, 93], [45, 81], [45, 94], [46, 82], [46, 95], [47, 83], [47, 96], [48, 84], [49, 85], [49, 87], [50, 86], [50, 88], [51, 87], [51, 97], [52, 88], [52, 98], [53, 89], [53, 99], [54, 90], [54, 100], [55, 91], [55, 101], [56, 92], [56, 102], [57, 101], [57, 103], [58, 102], [58, 107], [59, 92], [59, 96], [60, 98], [60, 104], [61, 87], [61, 88], [62, 98], [62, 99], [63, 94], [63, 105], [64, 84], [65, 84], [66, 89], [66, 100], [67, 91], [67, 95], [68, 90], [68, 97], [69, 82], [69, 106], [70, 100], [70, 106], [71, 86], [71, 95], [72, 90], [72, 94], [73, 82], [73, 96], [74, 91], [74, 105], [75, 83], [75, 85], [76, 85], [76, 107], [77, 89], [77, 93], [78, 80], [78, 104], [79, 81], [79, 103], [80, 108], [81, 112], [83, 109], [86, 110], [92, 111], [93, 111], [97, 110], [99, 112], [101, 109], [102, 108], [103, 108], [104, 109], [105, 111], [106, 110], [107, 112]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_112_36.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_112_36 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
