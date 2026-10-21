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
D:=P177Graph("128_028",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 65], [1, 66], [1, 85], [1, 86], [2, 65], [2, 66], [2, 77], [2, 78], [3, 77], [3, 78], [3, 89], [3, 90], [4, 69], [4, 70], [4, 89], [4, 90], [5, 69], [5, 70], [5, 81], [5, 82], [6, 81], [6, 82], [6, 93], [6, 94], [7, 73], [7, 74], [7, 93], [7, 94], [8, 73], [8, 74], [8, 85], [8, 86], [9, 67], [9, 68], [9, 95], [9, 96], [10, 67], [10, 68], [10, 71], [10, 72], [11, 71], [11, 72], [11, 75], [11, 76], [12, 75], [12, 76], [12, 79], [12, 80], [13, 79], [13, 80], [13, 83], [13, 84], [14, 83], [14, 84], [14, 87], [14, 88], [15, 87], [15, 88], [15, 91], [15, 92], [16, 91], [16, 92], [16, 95], [16, 96], [17, 66], [17, 67], [17, 117], [17, 118], [18, 66], [18, 67], [18, 109], [18, 110], [19, 90], [19, 91], [19, 109], [19, 110], [20, 90], [20, 91], [20, 101], [20, 102], [21, 82], [21, 83], [21, 101], [21, 102], [22, 82], [22, 83], [22, 125], [22, 126], [23, 74], [23, 75], [23, 125], [23, 126], [24, 74], [24, 75], [24, 117], [24, 118], [25, 65], [25, 68], [25, 127], [25, 128], [26, 65], [26, 68], [26, 103], [26, 104], [27, 73], [27, 76], [27, 103], [27, 104], [28, 73], [28, 76], [28, 111], [28, 112], [29, 81], [29, 84], [29, 111], [29, 112], [30, 81], [30, 84], [30, 119], [30, 120], [31, 89], [31, 92], [31, 119], [31, 120], [32, 89], [32, 92], [32, 127], [32, 128], [33, 97], [33, 98], [33, 118], [33, 119], [34, 97], [34, 98], [34, 110], [34, 111], [35, 110], [35, 111], [35, 121], [35, 122], [36, 102], [36, 103], [36, 121], [36, 122], [37, 102], [37, 103], [37, 113], [37, 114], [38, 113], [38, 114], [38, 126], [38, 127], [39, 105], [39, 106], [39, 126], [39, 127], [40, 105], [40, 106], [40, 118], [40, 119], [41, 99], [41, 100], [41, 125], [41, 128], [42, 99], [42, 100], [42, 101], [42, 104], [43, 101], [43, 104], [43, 107], [43, 108], [44, 107], [44, 108], [44, 109], [44, 112], [45, 109], [45, 112], [45, 115], [45, 116], [46, 115], [46, 116], [46, 117], [46, 120], [47, 117], [47, 120], [47, 123], [47, 124], [48, 123], [48, 124], [48, 125], [48, 128], [49, 86], [49, 87], [49, 98], [49, 99], [50, 78], [50, 79], [50, 98], [50, 99], [51, 78], [51, 79], [51, 122], [51, 123], [52, 70], [52, 71], [52, 122], [52, 123], [53, 70], [53, 71], [53, 114], [53, 115], [54, 94], [54, 95], [54, 114], [54, 115], [55, 94], [55, 95], [55, 106], [55, 107], [56, 86], [56, 87], [56, 106], [56, 107], [57, 93], [57, 96], [57, 97], [57, 100], [58, 69], [58, 72], [58, 97], [58, 100], [59, 69], [59, 72], [59, 105], [59, 108], [60, 77], [60, 80], [60, 105], [60, 108], [61, 77], [61, 80], [61, 113], [61, 116], [62, 85], [62, 88], [62, 113], [62, 116], [63, 85], [63, 88], [63, 121], [63, 124], [64, 93], [64, 96], [64, 121], [64, 124]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_028.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_028 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
