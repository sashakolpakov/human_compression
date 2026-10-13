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
D:=P177Graph("128_016",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 65], [1, 66], [1, 105], [1, 106], [2, 65], [2, 66], [2, 89], [2, 90], [3, 89], [3, 90], [3, 113], [3, 114], [4, 73], [4, 74], [4, 113], [4, 114], [5, 73], [5, 74], [5, 97], [5, 98], [6, 97], [6, 98], [6, 121], [6, 122], [7, 81], [7, 82], [7, 121], [7, 122], [8, 81], [8, 82], [8, 105], [8, 106], [9, 66], [9, 67], [9, 122], [9, 123], [10, 66], [10, 67], [10, 74], [10, 75], [11, 74], [11, 75], [11, 82], [11, 83], [12, 82], [12, 83], [12, 90], [12, 91], [13, 90], [13, 91], [13, 98], [13, 99], [14, 98], [14, 99], [14, 106], [14, 107], [15, 106], [15, 107], [15, 114], [15, 115], [16, 114], [16, 115], [16, 122], [16, 123], [17, 67], [17, 68], [17, 107], [17, 108], [18, 67], [18, 68], [18, 91], [18, 92], [19, 91], [19, 92], [19, 115], [19, 116], [20, 75], [20, 76], [20, 115], [20, 116], [21, 75], [21, 76], [21, 99], [21, 100], [22, 99], [22, 100], [22, 123], [22, 124], [23, 83], [23, 84], [23, 123], [23, 124], [24, 83], [24, 84], [24, 107], [24, 108], [25, 68], [25, 69], [25, 124], [25, 125], [26, 68], [26, 69], [26, 76], [26, 77], [27, 76], [27, 77], [27, 84], [27, 85], [28, 84], [28, 85], [28, 92], [28, 93], [29, 92], [29, 93], [29, 100], [29, 101], [30, 100], [30, 101], [30, 108], [30, 109], [31, 108], [31, 109], [31, 116], [31, 117], [32, 116], [32, 117], [32, 124], [32, 125], [33, 69], [33, 70], [33, 109], [33, 110], [34, 69], [34, 70], [34, 93], [34, 94], [35, 93], [35, 94], [35, 117], [35, 118], [36, 77], [36, 78], [36, 117], [36, 118], [37, 77], [37, 78], [37, 101], [37, 102], [38, 101], [38, 102], [38, 125], [38, 126], [39, 85], [39, 86], [39, 125], [39, 126], [40, 85], [40, 86], [40, 109], [40, 110], [41, 70], [41, 71], [41, 126], [41, 127], [42, 70], [42, 71], [42, 78], [42, 79], [43, 78], [43, 79], [43, 86], [43, 87], [44, 86], [44, 87], [44, 94], [44, 95], [45, 94], [45, 95], [45, 102], [45, 103], [46, 102], [46, 103], [46, 110], [46, 111], [47, 110], [47, 111], [47, 118], [47, 119], [48, 118], [48, 119], [48, 126], [48, 127], [49, 71], [49, 72], [49, 111], [49, 112], [50, 71], [50, 72], [50, 95], [50, 96], [51, 95], [51, 96], [51, 119], [51, 120], [52, 79], [52, 80], [52, 119], [52, 120], [53, 79], [53, 80], [53, 103], [53, 104], [54, 103], [54, 104], [54, 127], [54, 128], [55, 87], [55, 88], [55, 127], [55, 128], [56, 87], [56, 88], [56, 111], [56, 112], [57, 65], [57, 72], [57, 121], [57, 128], [58, 65], [58, 72], [58, 73], [58, 80], [59, 73], [59, 80], [59, 81], [59, 88], [60, 81], [60, 88], [60, 89], [60, 96], [61, 89], [61, 96], [61, 97], [61, 104], [62, 97], [62, 104], [62, 105], [62, 112], [63, 105], [63, 112], [63, 113], [63, 120], [64, 113], [64, 120], [64, 121], [64, 128]]);;
R:=P177Census(D);;Need(Size(R.F)=256);;
PrintTo("current_c4_descent/128_016.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_016 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
