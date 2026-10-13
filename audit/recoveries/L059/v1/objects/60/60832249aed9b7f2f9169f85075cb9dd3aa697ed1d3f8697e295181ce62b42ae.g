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
D:=P177Graph("128_053",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 92], [1, 104], [1, 110], [1, 112], [2, 79], [2, 83], [2, 101], [2, 110], [3, 83], [3, 96], [3, 114], [3, 121], [4, 88], [4, 118], [4, 119], [4, 121], [5, 88], [5, 102], [5, 120], [5, 123], [6, 94], [6, 95], [6, 102], [6, 124], [7, 68], [7, 78], [7, 86], [7, 95], [8, 70], [8, 78], [8, 111], [8, 117], [9, 72], [9, 93], [9, 111], [9, 127], [10, 72], [10, 97], [10, 99], [10, 113], [11, 81], [11, 84], [11, 97], [11, 116], [12, 81], [12, 87], [12, 90], [12, 91], [13, 77], [13, 89], [13, 90], [13, 128], [14, 73], [14, 85], [14, 89], [14, 115], [15, 71], [15, 73], [15, 75], [15, 98], [16, 74], [16, 75], [16, 106], [16, 112], [17, 65], [17, 70], [17, 89], [17, 120], [18, 66], [18, 73], [18, 94], [18, 127], [19, 68], [19, 75], [19, 108], [19, 113], [20, 70], [20, 84], [20, 112], [20, 122], [21, 91], [21, 105], [21, 110], [21, 127], [22, 77], [22, 83], [22, 113], [22, 125], [23, 69], [23, 84], [23, 115], [23, 121], [24, 71], [24, 88], [24, 91], [24, 109], [25, 74], [25, 77], [25, 102], [25, 107], [26, 82], [26, 92], [26, 95], [26, 115], [27, 71], [27, 78], [27, 79], [27, 80], [28, 74], [28, 96], [28, 100], [28, 111], [29, 72], [29, 76], [29, 92], [29, 119], [30, 79], [30, 97], [30, 120], [30, 126], [31, 81], [31, 94], [31, 96], [31, 103], [32, 67], [32, 68], [32, 90], [32, 119], [33, 65], [33, 81], [33, 104], [33, 118], [34, 66], [34, 90], [34, 101], [34, 123], [35, 89], [35, 108], [35, 114], [35, 124], [36, 73], [36, 86], [36, 118], [36, 122], [37, 75], [37, 105], [37, 117], [37, 123], [38, 93], [38, 112], [38, 124], [38, 125], [39, 69], [39, 86], [39, 99], [39, 110], [40, 83], [40, 109], [40, 116], [40, 117], [41, 87], [41, 93], [41, 107], [41, 121], [42, 82], [42, 88], [42, 99], [42, 128], [43, 80], [43, 85], [43, 102], [43, 116], [44, 87], [44, 95], [44, 98], [44, 100], [45, 76], [45, 78], [45, 106], [45, 128], [46, 85], [46, 104], [46, 111], [46, 126], [47, 72], [47, 98], [47, 101], [47, 103], [48, 67], [48, 97], [48, 106], [48, 114], [49, 80], [49, 100], [49, 113], [49, 118], [50, 76], [50, 84], [50, 100], [50, 123], [51, 76], [51, 91], [51, 124], [51, 126], [52, 77], [52, 86], [52, 103], [52, 126], [53, 67], [53, 103], [53, 115], [53, 117], [54, 65], [54, 67], [54, 71], [54, 93], [55, 65], [55, 66], [55, 74], [55, 99], [56, 66], [56, 92], [56, 108], [56, 116], [57, 79], [57, 87], [57, 108], [57, 122], [58, 96], [58, 105], [58, 122], [58, 128], [59, 85], [59, 105], [59, 119], [59, 125], [60, 69], [60, 98], [60, 120], [60, 125], [61, 69], [61, 94], [61, 106], [61, 109], [62, 68], [62, 104], [62, 107], [62, 109], [63, 70], [63, 82], [63, 101], [63, 107], [64, 80], [64, 82], [64, 114], [64, 127]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_053.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_053 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
