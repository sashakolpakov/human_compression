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
D:=P177Graph("128_018",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 67], [1, 81], [1, 97], [1, 104], [2, 65], [2, 67], [2, 97], [2, 126], [3, 81], [3, 92], [3, 104], [3, 124], [4, 67], [4, 91], [4, 106], [4, 121], [5, 67], [5, 72], [5, 119], [5, 121], [6, 65], [6, 78], [6, 112], [6, 126], [7, 90], [7, 92], [7, 100], [7, 124], [8, 91], [8, 92], [8, 106], [8, 116], [9, 75], [9, 86], [9, 97], [9, 99], [10, 79], [10, 81], [10, 105], [10, 117], [11, 74], [11, 86], [11, 97], [11, 118], [12, 70], [12, 81], [12, 101], [12, 117], [13, 72], [13, 78], [13, 102], [13, 119], [14, 71], [14, 78], [14, 112], [14, 113], [15, 89], [15, 90], [15, 100], [15, 108], [16, 83], [16, 92], [16, 115], [16, 116], [17, 69], [17, 75], [17, 99], [17, 124], [18, 79], [18, 90], [18, 105], [18, 122], [19, 76], [19, 95], [19, 104], [19, 123], [20, 86], [20, 95], [20, 117], [20, 121], [21, 65], [21, 68], [21, 82], [21, 127], [22, 79], [22, 91], [22, 99], [22, 123], [23, 94], [23, 95], [23, 98], [23, 104], [24, 68], [24, 86], [24, 121], [24, 125], [25, 65], [25, 68], [25, 94], [25, 98], [26, 70], [26, 91], [26, 98], [26, 99], [27, 74], [27, 87], [27, 112], [27, 118], [28, 70], [28, 101], [28, 125], [28, 126], [29, 77], [29, 78], [29, 102], [29, 114], [30, 71], [30, 80], [30, 103], [30, 113], [31, 88], [31, 89], [31, 108], [31, 109], [32, 83], [32, 89], [32, 103], [32, 115], [33, 69], [33, 96], [33, 110], [33, 124], [34, 73], [34, 90], [34, 107], [34, 122], [35, 76], [35, 85], [35, 100], [35, 123], [36, 69], [36, 95], [36, 116], [36, 117], [37, 82], [37, 88], [37, 113], [37, 127], [38, 79], [38, 83], [38, 110], [38, 123], [39, 66], [39, 125], [39, 126], [39, 128], [40, 75], [40, 76], [40, 105], [40, 106], [41, 66], [41, 74], [41, 82], [41, 119], [42, 75], [42, 94], [42, 101], [42, 106], [43, 74], [43, 94], [43, 101], [43, 119], [44, 68], [44, 87], [44, 102], [44, 125], [45, 70], [45, 72], [45, 98], [45, 118], [46, 87], [46, 93], [46, 111], [46, 112], [47, 77], [47, 80], [47, 108], [47, 114], [48, 80], [48, 85], [48, 103], [48, 122], [49, 87], [49, 88], [49, 102], [49, 109], [50, 89], [50, 93], [50, 103], [50, 111], [51, 80], [51, 96], [51, 108], [51, 110], [52, 73], [52, 88], [52, 107], [52, 113], [53, 84], [53, 85], [53, 100], [53, 120], [54, 69], [54, 85], [54, 116], [54, 122], [55, 73], [55, 83], [55, 110], [55, 120], [56, 66], [56, 71], [56, 109], [56, 128], [57, 76], [57, 96], [57, 105], [57, 115], [58, 66], [58, 82], [58, 93], [58, 114], [59, 72], [59, 118], [59, 127], [59, 128], [60, 71], [60, 84], [60, 109], [60, 120], [61, 73], [61, 93], [61, 114], [61, 120], [62, 84], [62, 96], [62, 107], [62, 115], [63, 77], [63, 111], [63, 127], [63, 128], [64, 77], [64, 84], [64, 107], [64, 111]]);;
R:=P177Census(D);;Need(Size(R.F)=1024);;
PrintTo("current_c4_descent/128_018.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_018 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
