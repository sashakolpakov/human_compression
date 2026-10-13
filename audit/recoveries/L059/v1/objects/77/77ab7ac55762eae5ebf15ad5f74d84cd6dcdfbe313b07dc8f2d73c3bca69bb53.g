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
D:=P177Graph("128_014",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 65], [1, 66], [1, 101], [1, 102], [2, 65], [2, 66], [2, 93], [2, 94], [3, 93], [3, 94], [3, 121], [3, 122], [4, 85], [4, 86], [4, 121], [4, 122], [5, 85], [5, 86], [5, 113], [5, 114], [6, 77], [6, 78], [6, 113], [6, 114], [7, 77], [7, 78], [7, 105], [7, 106], [8, 69], [8, 70], [8, 105], [8, 106], [9, 69], [9, 70], [9, 97], [9, 98], [10, 97], [10, 98], [10, 125], [10, 126], [11, 89], [11, 90], [11, 125], [11, 126], [12, 89], [12, 90], [12, 117], [12, 118], [13, 81], [13, 82], [13, 117], [13, 118], [14, 81], [14, 82], [14, 109], [14, 110], [15, 73], [15, 74], [15, 109], [15, 110], [16, 73], [16, 74], [16, 101], [16, 102], [17, 66], [17, 67], [17, 126], [17, 127], [18, 66], [18, 67], [18, 70], [18, 71], [19, 70], [19, 71], [19, 74], [19, 75], [20, 74], [20, 75], [20, 78], [20, 79], [21, 78], [21, 79], [21, 82], [21, 83], [22, 82], [22, 83], [22, 86], [22, 87], [23, 86], [23, 87], [23, 90], [23, 91], [24, 90], [24, 91], [24, 94], [24, 95], [25, 94], [25, 95], [25, 98], [25, 99], [26, 98], [26, 99], [26, 102], [26, 103], [27, 102], [27, 103], [27, 106], [27, 107], [28, 106], [28, 107], [28, 110], [28, 111], [29, 110], [29, 111], [29, 114], [29, 115], [30, 114], [30, 115], [30, 118], [30, 119], [31, 118], [31, 119], [31, 122], [31, 123], [32, 122], [32, 123], [32, 126], [32, 127], [33, 67], [33, 68], [33, 103], [33, 104], [34, 67], [34, 68], [34, 95], [34, 96], [35, 95], [35, 96], [35, 123], [35, 124], [36, 87], [36, 88], [36, 123], [36, 124], [37, 87], [37, 88], [37, 115], [37, 116], [38, 79], [38, 80], [38, 115], [38, 116], [39, 79], [39, 80], [39, 107], [39, 108], [40, 71], [40, 72], [40, 107], [40, 108], [41, 71], [41, 72], [41, 99], [41, 100], [42, 99], [42, 100], [42, 127], [42, 128], [43, 91], [43, 92], [43, 127], [43, 128], [44, 91], [44, 92], [44, 119], [44, 120], [45, 83], [45, 84], [45, 119], [45, 120], [46, 83], [46, 84], [46, 111], [46, 112], [47, 75], [47, 76], [47, 111], [47, 112], [48, 75], [48, 76], [48, 103], [48, 104], [49, 65], [49, 68], [49, 125], [49, 128], [50, 65], [50, 68], [50, 69], [50, 72], [51, 69], [51, 72], [51, 73], [51, 76], [52, 73], [52, 76], [52, 77], [52, 80], [53, 77], [53, 80], [53, 81], [53, 84], [54, 81], [54, 84], [54, 85], [54, 88], [55, 85], [55, 88], [55, 89], [55, 92], [56, 89], [56, 92], [56, 93], [56, 96], [57, 93], [57, 96], [57, 97], [57, 100], [58, 97], [58, 100], [58, 101], [58, 104], [59, 101], [59, 104], [59, 105], [59, 108], [60, 105], [60, 108], [60, 109], [60, 112], [61, 109], [61, 112], [61, 113], [61, 116], [62, 113], [62, 116], [62, 117], [62, 120], [63, 117], [63, 120], [63, 121], [63, 124], [64, 121], [64, 124], [64, 125], [64, 128]]);;
R:=P177Census(D);;Need(Size(R.F)=256);;
PrintTo("current_c4_descent/128_014.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_014 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
