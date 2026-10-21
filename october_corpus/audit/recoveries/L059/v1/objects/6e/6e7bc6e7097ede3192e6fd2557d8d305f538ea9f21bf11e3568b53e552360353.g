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
D:=P177Graph("VT3_120_64",120,[1, 2, 4, 6, 10, 11, 14, 17, 19, 20, 22, 24, 27, 28, 29, 30, 34, 35, 37, 38, 39, 40, 41, 43, 46, 47, 49, 50, 51, 52, 54, 59, 60, 61, 63, 64, 65, 68, 70, 73, 75, 81, 83, 84, 86, 87, 88, 89, 90, 91, 92, 94, 96, 99, 102, 104, 109, 110, 112, 117],[[1, 33], [1, 56], [1, 116], [2, 45], [2, 56], [2, 115], [3, 24], [3, 27], [3, 102], [4, 44], [4, 48], [4, 53], [5, 83], [5, 96], [5, 110], [6, 48], [6, 78], [6, 98], [7, 19], [7, 49], [7, 61], [8, 22], [8, 39], [8, 87], [9, 20], [9, 24], [9, 104], [10, 12], [10, 97], [10, 113], [11, 31], [11, 45], [11, 119], [12, 35], [12, 73], [13, 14], [13, 91], [13, 104], [14, 26], [14, 82], [15, 46], [15, 88], [15, 117], [16, 29], [16, 83], [16, 109], [17, 25], [17, 66], [17, 118], [18, 46], [18, 64], [18, 73], [19, 25], [19, 82], [20, 95], [20, 103], [21, 49], [21, 59], [21, 90], [22, 36], [22, 82], [23, 39], [23, 63], [23, 92], [24, 45], [25, 29], [26, 65], [26, 89], [27, 79], [27, 97], [28, 62], [28, 85], [28, 120], [29, 119], [30, 32], [30, 78], [30, 79], [31, 68], [31, 81], [32, 40], [32, 75], [33, 40], [33, 70], [34, 36], [34, 107], [34, 114], [35, 62], [35, 118], [36, 110], [37, 95], [37, 98], [37, 107], [38, 42], [38, 69], [38, 108], [39, 58], [40, 57], [41, 76], [41, 111], [41, 118], [42, 75], [42, 110], [43, 72], [43, 74], [43, 76], [44, 70], [44, 104], [46, 103], [47, 58], [47, 77], [47, 113], [48, 51], [49, 120], [50, 74], [50, 85], [50, 101], [51, 55], [51, 108], [52, 78], [52, 101], [52, 115], [53, 63], [53, 64], [54, 56], [54, 71], [54, 111], [55, 87], [55, 99], [57, 89], [57, 99], [58, 60], [59, 100], [59, 114], [60, 66], [60, 69], [61, 77], [61, 103], [62, 99], [63, 120], [64, 105], [65, 100], [65, 111], [66, 102], [67, 86], [67, 92], [67, 112], [68, 80], [68, 107], [69, 91], [70, 114], [71, 83], [71, 94], [72, 87], [72, 90], [73, 115], [74, 109], [75, 76], [77, 81], [79, 94], [80, 91], [80, 94], [81, 106], [84, 93], [84, 98], [84, 116], [85, 88], [86, 101], [86, 106], [88, 116], [89, 105], [90, 93], [92, 95], [93, 96], [96, 106], [97, 112], [100, 117], [102, 105], [108, 112], [109, 113], [117, 119]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_120_64.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_120_64 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
