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
D:=P177Graph("128_042",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 65], [1, 71], [1, 99], [1, 119], [2, 88], [2, 99], [2, 113], [2, 119], [3, 69], [3, 77], [3, 97], [3, 106], [4, 77], [4, 82], [4, 84], [4, 97], [5, 69], [5, 95], [5, 106], [5, 114], [6, 79], [6, 117], [6, 127], [6, 128], [7, 68], [7, 89], [7, 96], [7, 101], [8, 65], [8, 71], [8, 121], [8, 123], [9, 82], [9, 84], [9, 95], [9, 114], [10, 75], [10, 115], [10, 127], [10, 128], [11, 67], [11, 68], [11, 85], [11, 96], [12, 79], [12, 102], [12, 117], [12, 118], [13, 89], [13, 100], [13, 101], [13, 107], [14, 88], [14, 113], [14, 121], [14, 123], [15, 75], [15, 110], [15, 111], [15, 124], [16, 87], [16, 105], [16, 108], [16, 118], [17, 70], [17, 76], [17, 104], [17, 122], [18, 70], [18, 94], [18, 104], [18, 126], [19, 75], [19, 102], [19, 115], [19, 118], [20, 67], [20, 85], [20, 100], [20, 107], [21, 75], [21, 93], [21, 110], [21, 120], [22, 66], [22, 72], [22, 105], [22, 118], [23, 76], [23, 80], [23, 103], [23, 122], [24, 74], [24, 79], [24, 111], [24, 124], [25, 87], [25, 108], [25, 116], [25, 127], [26, 80], [26, 94], [26, 103], [26, 126], [27, 73], [27, 82], [27, 86], [27, 122], [28, 82], [28, 83], [28, 86], [28, 126], [29, 66], [29, 90], [29, 92], [29, 93], [30, 66], [30, 78], [30, 92], [30, 111], [31, 80], [31, 98], [31, 114], [31, 125], [32, 74], [32, 79], [32, 93], [32, 120], [33, 66], [33, 72], [33, 116], [33, 127], [34, 90], [34, 93], [34, 108], [34, 112], [35, 70], [35, 98], [35, 109], [35, 114], [36, 78], [36, 108], [36, 111], [36, 112], [37, 73], [37, 91], [37, 106], [37, 122], [38, 83], [38, 91], [38, 106], [38, 126], [39, 77], [39, 80], [39, 81], [39, 125], [40, 67], [40, 73], [40, 121], [40, 125], [41, 67], [41, 73], [41, 109], [41, 119], [42, 83], [42, 101], [42, 109], [42, 119], [43, 71], [43, 91], [43, 98], [43, 100], [44, 68], [44, 81], [44, 86], [44, 113], [45, 70], [45, 77], [45, 81], [45, 109], [46, 81], [46, 91], [46, 100], [46, 113], [47, 83], [47, 101], [47, 121], [47, 125], [48, 68], [48, 71], [48, 86], [48, 98], [49, 87], [49, 89], [49, 123], [49, 124], [50, 85], [50, 87], [50, 120], [50, 123], [51, 72], [51, 89], [51, 99], [51, 124], [52, 72], [52, 85], [52, 99], [52, 120], [53, 65], [53, 74], [53, 105], [53, 107], [54, 88], [54, 96], [54, 110], [54, 116], [55, 74], [55, 88], [55, 107], [55, 116], [56, 65], [56, 96], [56, 105], [56, 110], [57, 92], [57, 95], [57, 102], [57, 104], [58, 78], [58, 84], [58, 94], [58, 115], [59, 95], [59, 102], [59, 103], [59, 112], [60, 76], [60, 84], [60, 90], [60, 115], [61, 92], [61, 97], [61, 104], [61, 128], [62, 69], [62, 78], [62, 94], [62, 117], [63, 97], [63, 103], [63, 112], [63, 128], [64, 69], [64, 76], [64, 90], [64, 117]]);;
R:=P177Census(D);;Need(Size(R.F)=1024);;
PrintTo("current_c4_descent/128_042.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_042 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
