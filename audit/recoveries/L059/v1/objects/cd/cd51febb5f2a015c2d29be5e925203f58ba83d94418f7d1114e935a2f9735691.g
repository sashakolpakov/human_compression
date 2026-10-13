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
D:=P177Graph("128_043",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 85], [1, 88], [1, 89], [1, 95], [2, 66], [2, 88], [2, 89], [2, 124], [3, 93], [3, 102], [3, 109], [3, 112], [4, 81], [4, 82], [4, 99], [4, 116], [5, 65], [5, 96], [5, 117], [5, 123], [6, 80], [6, 93], [6, 98], [6, 102], [7, 76], [7, 77], [7, 81], [7, 116], [8, 88], [8, 96], [8, 107], [8, 123], [9, 68], [9, 75], [9, 122], [9, 125], [10, 91], [10, 97], [10, 109], [10, 122], [11, 78], [11, 87], [11, 101], [11, 119], [12, 67], [12, 123], [12, 126], [12, 127], [13, 67], [13, 83], [13, 103], [13, 114], [14, 71], [14, 98], [14, 106], [14, 110], [15, 84], [15, 95], [15, 127], [15, 128], [16, 78], [16, 79], [16, 99], [16, 113], [17, 111], [17, 115], [17, 121], [17, 124], [18, 68], [18, 78], [18, 93], [18, 101], [19, 68], [19, 71], [19, 75], [19, 86], [20, 65], [20, 69], [20, 105], [20, 117], [21, 73], [21, 79], [21, 109], [21, 122], [22, 70], [22, 72], [22, 87], [22, 119], [23, 105], [23, 120], [23, 126], [23, 127], [24, 83], [24, 94], [24, 103], [24, 120], [25, 106], [25, 110], [25, 112], [25, 125], [26, 74], [26, 84], [26, 90], [26, 95], [27, 67], [27, 89], [27, 104], [27, 114], [28, 78], [28, 88], [28, 99], [28, 107], [29, 81], [29, 115], [29, 119], [29, 124], [30, 68], [30, 93], [30, 96], [30, 114], [31, 84], [31, 92], [31, 104], [31, 107], [32, 80], [32, 86], [32, 91], [32, 97], [33, 85], [33, 92], [33, 111], [33, 121], [34, 72], [34, 76], [34, 97], [34, 106], [35, 96], [35, 114], [35, 118], [35, 128], [36, 85], [36, 92], [36, 118], [36, 126], [37, 73], [37, 82], [37, 101], [37, 108], [38, 100], [38, 104], [38, 107], [38, 115], [39, 66], [39, 74], [39, 90], [39, 100], [40, 75], [40, 82], [40, 99], [40, 102], [41, 69], [41, 94], [41, 118], [41, 128], [42, 70], [42, 73], [42, 77], [42, 108], [43, 66], [43, 87], [43, 100], [43, 116], [44, 108], [44, 112], [44, 113], [44, 125], [45, 82], [45, 89], [45, 101], [45, 104], [46, 71], [46, 98], [46, 103], [46, 117], [47, 72], [47, 76], [47, 79], [47, 113], [48, 65], [48, 80], [48, 83], [48, 86], [49, 109], [49, 112], [49, 118], [49, 126], [50, 67], [50, 75], [50, 102], [50, 123], [51, 69], [51, 97], [51, 105], [51, 106], [52, 71], [52, 86], [52, 87], [52, 116], [53, 70], [53, 77], [53, 91], [53, 110], [54, 100], [54, 103], [54, 115], [54, 117], [55, 80], [55, 81], [55, 98], [55, 119], [56, 65], [56, 66], [56, 83], [56, 124], [57, 69], [57, 90], [57, 94], [57, 111], [58, 70], [58, 72], [58, 90], [58, 111], [59, 122], [59, 125], [59, 127], [59, 128], [60, 74], [60, 105], [60, 120], [60, 121], [61, 91], [61, 94], [61, 110], [61, 120], [62, 73], [62, 79], [62, 85], [62, 95], [63, 84], [63, 92], [63, 108], [63, 113], [64, 74], [64, 76], [64, 77], [64, 121]]);;
R:=P177Census(D);;Need(Size(R.F)=1024);;
PrintTo("current_c4_descent/128_043.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_043 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
