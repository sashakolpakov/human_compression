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
D:=P177Graph("128_019",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 67], [1, 84], [1, 97], [1, 105], [2, 65], [2, 67], [2, 97], [2, 126], [3, 70], [3, 84], [3, 98], [3, 105], [4, 67], [4, 72], [4, 103], [4, 121], [5, 67], [5, 75], [5, 117], [5, 121], [6, 65], [6, 81], [6, 100], [6, 126], [7, 70], [7, 94], [7, 98], [7, 108], [8, 70], [8, 72], [8, 103], [8, 122], [9, 77], [9, 88], [9, 97], [9, 101], [10, 73], [10, 84], [10, 104], [10, 124], [11, 68], [11, 77], [11, 97], [11, 99], [12, 82], [12, 84], [12, 102], [12, 124], [13, 75], [13, 81], [13, 115], [13, 117], [14, 81], [14, 92], [14, 100], [14, 106], [15, 83], [15, 94], [15, 108], [15, 114], [16, 70], [16, 74], [16, 112], [16, 122], [17, 69], [17, 88], [17, 98], [17, 101], [18, 73], [18, 94], [18, 104], [18, 107], [19, 93], [19, 96], [19, 105], [19, 109], [20, 77], [20, 93], [20, 121], [20, 124], [21, 65], [21, 78], [21, 87], [21, 127], [22, 66], [22, 87], [22, 88], [22, 103], [23, 93], [23, 95], [23, 105], [23, 118], [24, 77], [24, 78], [24, 121], [24, 125], [25, 65], [25, 78], [25, 95], [25, 118], [26, 88], [26, 90], [26, 103], [26, 119], [27, 68], [27, 79], [27, 99], [27, 100], [28, 82], [28, 102], [28, 125], [28, 126], [29, 81], [29, 85], [29, 115], [29, 116], [30, 86], [30, 92], [30, 106], [30, 113], [31, 83], [31, 91], [31, 114], [31, 123], [32, 74], [32, 83], [32, 112], [32, 113], [33, 69], [33, 89], [33, 98], [33, 111], [34, 80], [34, 94], [34, 107], [34, 119], [35, 76], [35, 96], [35, 108], [35, 109], [36, 69], [36, 93], [36, 122], [36, 124], [37, 87], [37, 91], [37, 106], [37, 127], [38, 66], [38, 74], [38, 87], [38, 111], [39, 66], [39, 125], [39, 126], [39, 128], [40, 72], [40, 101], [40, 127], [40, 128], [41, 68], [41, 96], [41, 104], [41, 117], [42, 72], [42, 80], [42, 101], [42, 110], [43, 68], [43, 80], [43, 110], [43, 117], [44, 85], [44, 96], [44, 104], [44, 120], [45, 78], [45, 79], [45, 115], [45, 125], [46, 75], [46, 90], [46, 99], [46, 119], [47, 71], [47, 79], [47, 100], [47, 120], [48, 85], [48, 86], [48, 114], [48, 116], [49, 76], [49, 86], [49, 107], [49, 113], [50, 79], [50, 91], [50, 115], [50, 123], [51, 71], [51, 83], [51, 113], [51, 120], [52, 86], [52, 89], [52, 111], [52, 114], [53, 80], [53, 91], [53, 106], [53, 119], [54, 76], [54, 90], [54, 108], [54, 110], [55, 69], [55, 76], [55, 107], [55, 122], [56, 74], [56, 82], [56, 111], [56, 118], [57, 66], [57, 92], [57, 123], [57, 128], [58, 89], [58, 112], [58, 127], [58, 128], [59, 73], [59, 75], [59, 99], [59, 109], [60, 89], [60, 95], [60, 102], [60, 112], [61, 71], [61, 73], [61, 109], [61, 116], [62, 71], [62, 95], [62, 102], [62, 116], [63, 82], [63, 85], [63, 118], [63, 120], [64, 90], [64, 92], [64, 110], [64, 123]]);;
R:=P177Census(D);;Need(Size(R.F)=1024);;
PrintTo("current_c4_descent/128_019.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_019 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
