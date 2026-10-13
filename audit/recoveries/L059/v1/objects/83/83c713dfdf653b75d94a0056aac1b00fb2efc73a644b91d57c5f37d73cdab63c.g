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
D:=P177Graph("128_052",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 68], [1, 69], [1, 93], [1, 102], [2, 75], [2, 100], [2, 102], [2, 121], [3, 65], [3, 74], [3, 121], [3, 126], [4, 74], [4, 94], [4, 98], [4, 110], [5, 85], [5, 100], [5, 110], [5, 111], [6, 82], [6, 85], [6, 87], [6, 90], [7, 75], [7, 87], [7, 94], [7, 96], [8, 78], [8, 80], [8, 96], [8, 108], [9, 82], [9, 98], [9, 108], [9, 127], [10, 70], [10, 79], [10, 83], [10, 127], [11, 78], [11, 79], [11, 90], [11, 101], [12, 93], [12, 95], [12, 101], [12, 114], [13, 70], [13, 80], [13, 95], [13, 122], [14, 68], [14, 105], [14, 122], [14, 126], [15, 83], [15, 89], [15, 105], [15, 114], [16, 65], [16, 69], [16, 89], [16, 111], [17, 71], [17, 80], [17, 109], [17, 110], [18, 82], [18, 122], [18, 123], [18, 125], [19, 83], [19, 87], [19, 113], [19, 120], [20, 78], [20, 89], [20, 118], [20, 128], [21, 73], [21, 93], [21, 99], [21, 108], [22, 70], [22, 81], [22, 102], [22, 106], [23, 79], [23, 107], [23, 119], [23, 126], [24, 66], [24, 74], [24, 91], [24, 114], [25, 72], [25, 95], [25, 111], [25, 115], [26, 68], [26, 77], [26, 84], [26, 85], [27, 75], [27, 105], [27, 116], [27, 124], [28, 65], [28, 67], [28, 76], [28, 96], [29, 69], [29, 88], [29, 92], [29, 98], [30, 100], [30, 103], [30, 104], [30, 127], [31, 86], [31, 90], [31, 97], [31, 121], [32, 94], [32, 101], [32, 112], [32, 117], [33, 93], [33, 97], [33, 110], [33, 120], [34, 76], [34, 100], [34, 117], [34, 122], [35, 71], [35, 87], [35, 99], [35, 126], [36, 89], [36, 94], [36, 104], [36, 125], [37, 107], [37, 108], [37, 111], [37, 113], [38, 82], [38, 102], [38, 112], [38, 118], [39, 72], [39, 73], [39, 75], [39, 79], [40, 74], [40, 78], [40, 81], [40, 123], [41, 95], [41, 98], [41, 119], [41, 124], [42, 70], [42, 85], [42, 91], [42, 128], [43, 90], [43, 92], [43, 105], [43, 115], [44, 77], [44, 96], [44, 106], [44, 114], [45, 69], [45, 80], [45, 86], [45, 116], [46, 66], [46, 67], [46, 68], [46, 127], [47, 83], [47, 88], [47, 109], [47, 121], [48, 65], [48, 84], [48, 101], [48, 103], [49, 106], [49, 116], [49, 120], [49, 125], [50, 76], [50, 107], [50, 116], [50, 118], [51, 66], [51, 88], [51, 99], [51, 118], [52, 72], [52, 81], [52, 88], [52, 104], [53, 81], [53, 84], [53, 97], [53, 107], [54, 91], [54, 97], [54, 112], [54, 124], [55, 71], [55, 72], [55, 76], [55, 91], [56, 71], [56, 77], [56, 92], [56, 123], [57, 77], [57, 104], [57, 113], [57, 124], [58, 67], [58, 86], [58, 113], [58, 128], [59, 67], [59, 73], [59, 92], [59, 112], [60, 73], [60, 103], [60, 106], [60, 109], [61, 86], [61, 103], [61, 119], [61, 123], [62, 66], [62, 117], [62, 119], [62, 120], [63, 109], [63, 115], [63, 117], [63, 128], [64, 84], [64, 99], [64, 115], [64, 125]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_052.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_052 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
