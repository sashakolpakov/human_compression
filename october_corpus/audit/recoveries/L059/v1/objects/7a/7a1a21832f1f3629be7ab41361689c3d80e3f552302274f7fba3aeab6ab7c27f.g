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
D:=P177Graph("128_015",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 65], [1, 66], [1, 77], [1, 78], [2, 65], [2, 66], [2, 121], [2, 122], [3, 117], [3, 118], [3, 121], [3, 122], [4, 105], [4, 106], [4, 117], [4, 118], [5, 101], [5, 102], [5, 105], [5, 106], [6, 89], [6, 90], [6, 101], [6, 102], [7, 85], [7, 86], [7, 89], [7, 90], [8, 73], [8, 74], [8, 85], [8, 86], [9, 69], [9, 70], [9, 73], [9, 74], [10, 69], [10, 70], [10, 125], [10, 126], [11, 113], [11, 114], [11, 125], [11, 126], [12, 109], [12, 110], [12, 113], [12, 114], [13, 97], [13, 98], [13, 109], [13, 110], [14, 93], [14, 94], [14, 97], [14, 98], [15, 81], [15, 82], [15, 93], [15, 94], [16, 77], [16, 78], [16, 81], [16, 82], [17, 66], [17, 67], [17, 126], [17, 127], [18, 66], [18, 67], [18, 74], [18, 75], [19, 74], [19, 75], [19, 82], [19, 83], [20, 82], [20, 83], [20, 90], [20, 91], [21, 90], [21, 91], [21, 98], [21, 99], [22, 98], [22, 99], [22, 106], [22, 107], [23, 106], [23, 107], [23, 114], [23, 115], [24, 114], [24, 115], [24, 122], [24, 123], [25, 70], [25, 71], [25, 122], [25, 123], [26, 70], [26, 71], [26, 78], [26, 79], [27, 78], [27, 79], [27, 86], [27, 87], [28, 86], [28, 87], [28, 94], [28, 95], [29, 94], [29, 95], [29, 102], [29, 103], [30, 102], [30, 103], [30, 110], [30, 111], [31, 110], [31, 111], [31, 118], [31, 119], [32, 118], [32, 119], [32, 126], [32, 127], [33, 67], [33, 68], [33, 79], [33, 80], [34, 67], [34, 68], [34, 123], [34, 124], [35, 119], [35, 120], [35, 123], [35, 124], [36, 107], [36, 108], [36, 119], [36, 120], [37, 103], [37, 104], [37, 107], [37, 108], [38, 91], [38, 92], [38, 103], [38, 104], [39, 87], [39, 88], [39, 91], [39, 92], [40, 75], [40, 76], [40, 87], [40, 88], [41, 71], [41, 72], [41, 75], [41, 76], [42, 71], [42, 72], [42, 127], [42, 128], [43, 115], [43, 116], [43, 127], [43, 128], [44, 111], [44, 112], [44, 115], [44, 116], [45, 99], [45, 100], [45, 111], [45, 112], [46, 95], [46, 96], [46, 99], [46, 100], [47, 83], [47, 84], [47, 95], [47, 96], [48, 79], [48, 80], [48, 83], [48, 84], [49, 65], [49, 72], [49, 124], [49, 125], [50, 65], [50, 72], [50, 73], [50, 80], [51, 73], [51, 80], [51, 81], [51, 88], [52, 81], [52, 88], [52, 89], [52, 96], [53, 89], [53, 96], [53, 97], [53, 104], [54, 97], [54, 104], [54, 105], [54, 112], [55, 105], [55, 112], [55, 113], [55, 120], [56, 113], [56, 120], [56, 121], [56, 128], [57, 68], [57, 69], [57, 121], [57, 128], [58, 68], [58, 69], [58, 76], [58, 77], [59, 76], [59, 77], [59, 84], [59, 85], [60, 84], [60, 85], [60, 92], [60, 93], [61, 92], [61, 93], [61, 100], [61, 101], [62, 100], [62, 101], [62, 108], [62, 109], [63, 108], [63, 109], [63, 116], [63, 117], [64, 116], [64, 117], [64, 124], [64, 125]]);;
R:=P177Census(D);;Need(Size(R.F)=256);;
PrintTo("current_c4_descent/128_015.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_015 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
