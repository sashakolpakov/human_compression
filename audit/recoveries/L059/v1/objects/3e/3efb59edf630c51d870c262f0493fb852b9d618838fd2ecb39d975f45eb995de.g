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
D:=P177Graph("128_021",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 65], [1, 81], [1, 95], [1, 113], [2, 78], [2, 81], [2, 95], [2, 106], [3, 67], [3, 81], [3, 109], [3, 112], [4, 65], [4, 84], [4, 113], [4, 123], [5, 67], [5, 88], [5, 112], [5, 125], [6, 71], [6, 87], [6, 95], [6, 96], [7, 69], [7, 87], [7, 95], [7, 119], [8, 67], [8, 89], [8, 100], [8, 107], [9, 65], [9, 89], [9, 108], [9, 122], [10, 78], [10, 88], [10, 106], [10, 115], [11, 80], [11, 81], [11, 109], [11, 124], [12, 79], [12, 84], [12, 114], [12, 123], [13, 71], [13, 83], [13, 96], [13, 123], [14, 69], [14, 82], [14, 115], [14, 119], [15, 77], [15, 89], [15, 96], [15, 100], [16, 78], [16, 89], [16, 104], [16, 108], [17, 74], [17, 94], [17, 112], [17, 121], [18, 66], [18, 94], [18, 111], [18, 113], [19, 74], [19, 92], [19, 98], [19, 112], [20, 66], [20, 92], [20, 105], [20, 113], [21, 75], [21, 90], [21, 105], [21, 119], [22, 77], [22, 88], [22, 117], [22, 125], [23, 67], [23, 107], [23, 116], [23, 126], [24, 65], [24, 122], [24, 126], [24, 127], [25, 76], [25, 88], [25, 103], [25, 115], [26, 80], [26, 84], [26, 120], [26, 124], [27, 79], [27, 86], [27, 101], [27, 114], [28, 68], [28, 94], [28, 121], [28, 124], [29, 70], [29, 94], [29, 111], [29, 114], [30, 71], [30, 92], [30, 98], [30, 117], [31, 73], [31, 92], [31, 105], [31, 106], [32, 80], [32, 90], [32, 102], [32, 105], [33, 78], [33, 93], [33, 104], [33, 121], [34, 77], [34, 93], [34, 96], [34, 111], [35, 71], [35, 117], [35, 127], [35, 128], [36, 69], [36, 99], [36, 127], [36, 128], [37, 72], [37, 91], [37, 100], [37, 103], [38, 69], [38, 91], [38, 99], [38, 108], [39, 73], [39, 106], [39, 116], [39, 128], [40, 72], [40, 87], [40, 97], [40, 109], [41, 75], [41, 84], [41, 99], [41, 120], [42, 70], [42, 91], [42, 100], [42, 114], [43, 68], [43, 91], [43, 108], [43, 124], [44, 70], [44, 87], [44, 109], [44, 118], [45, 79], [45, 90], [45, 98], [45, 118], [46, 74], [46, 83], [46, 107], [46, 123], [47, 68], [47, 82], [47, 102], [47, 115], [48, 75], [48, 93], [48, 111], [48, 119], [49, 77], [49, 86], [49, 110], [49, 117], [50, 80], [50, 102], [50, 116], [50, 126], [51, 79], [51, 118], [51, 126], [51, 127], [52, 76], [52, 86], [52, 101], [52, 103], [53, 72], [53, 103], [53, 116], [53, 128], [54, 72], [54, 83], [54, 97], [54, 120], [55, 75], [55, 86], [55, 99], [55, 110], [56, 70], [56, 82], [56, 118], [56, 125], [57, 76], [57, 93], [57, 97], [57, 121], [58, 76], [58, 90], [58, 97], [58, 98], [59, 73], [59, 85], [59, 104], [59, 110], [60, 66], [60, 82], [60, 122], [60, 125], [61, 74], [61, 85], [61, 101], [61, 107], [62, 73], [62, 83], [62, 104], [62, 120], [63, 66], [63, 85], [63, 110], [63, 122], [64, 68], [64, 85], [64, 101], [64, 102]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_021.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_021 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
