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
D:=P177Graph("VT3_128_8",128,[1, 2, 4, 5, 6, 7, 9, 13, 14, 16, 17, 18, 20, 21, 22, 23, 25, 26, 28, 33, 34, 35, 38, 43, 49, 50, 51, 52, 53, 54, 55, 56, 59, 60, 64, 65, 69, 71, 73, 75, 76, 78, 80, 81, 83, 84, 88, 89, 90, 94, 95, 97, 99, 101, 106, 107, 109, 110, 113, 115, 116, 118, 124, 126],[[1, 10], [1, 29], [1, 77], [2, 12], [2, 45], [2, 86], [3, 81], [3, 88], [3, 126], [4, 85], [4, 114], [4, 117], [5, 58], [5, 87], [5, 123], [6, 27], [6, 40], [6, 70], [7, 41], [7, 102], [7, 127], [8, 14], [8, 34], [8, 55], [9, 32], [9, 36], [9, 121], [10, 35], [10, 60], [11, 54], [11, 59], [11, 90], [12, 60], [12, 69], [13, 46], [13, 57], [13, 70], [14, 46], [14, 125], [15, 55], [15, 84], [15, 126], [16, 96], [16, 104], [16, 119], [17, 44], [17, 68], [17, 98], [18, 30], [18, 67], [18, 77], [19, 78], [19, 94], [19, 109], [20, 74], [20, 79], [20, 120], [21, 31], [21, 62], [21, 105], [22, 31], [22, 44], [22, 112], [23, 61], [23, 77], [23, 103], [24, 75], [24, 80], [24, 101], [25, 61], [25, 85], [25, 98], [26, 61], [26, 100], [26, 128], [27, 56], [27, 99], [28, 68], [28, 111], [28, 122], [29, 59], [29, 113], [30, 43], [30, 78], [31, 81], [32, 51], [32, 80], [33, 40], [33, 63], [33, 123], [34, 103], [34, 119], [35, 74], [35, 96], [36, 69], [36, 89], [37, 43], [37, 116], [37, 118], [38, 48], [38, 112], [38, 114], [39, 60], [39, 106], [39, 124], [40, 124], [41, 75], [41, 116], [42, 49], [42, 50], [42, 113], [43, 72], [44, 94], [45, 49], [45, 78], [46, 75], [47, 84], [47, 115], [47, 124], [48, 71], [48, 97], [49, 122], [50, 66], [50, 105], [51, 63], [51, 79], [52, 57], [52, 62], [52, 91], [53, 72], [53, 108], [53, 128], [54, 100], [54, 127], [55, 117], [56, 103], [56, 120], [57, 69], [58, 90], [58, 109], [59, 112], [62, 118], [63, 88], [64, 66], [64, 82], [64, 87], [65, 82], [65, 100], [65, 111], [66, 106], [67, 89], [67, 95], [68, 107], [70, 76], [71, 74], [71, 92], [72, 76], [73, 93], [73, 102], [73, 119], [76, 93], [79, 110], [80, 105], [81, 104], [82, 99], [83, 86], [83, 98], [83, 125], [84, 92], [85, 118], [86, 99], [87, 116], [88, 108], [89, 104], [90, 120], [91, 107], [91, 115], [92, 101], [93, 110], [94, 102], [95, 117], [95, 123], [96, 107], [97, 121], [97, 125], [101, 111], [106, 114], [108, 113], [109, 121], [110, 122], [115, 128], [126, 127]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_128_8.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_128_8 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
