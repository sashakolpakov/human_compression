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
D:=P177Graph("128_051",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 68], [1, 71], [1, 87], [1, 93], [2, 85], [2, 87], [2, 89], [2, 94], [3, 94], [3, 97], [3, 121], [3, 125], [4, 66], [4, 68], [4, 97], [4, 114], [5, 66], [5, 80], [5, 89], [5, 116], [6, 84], [6, 93], [6, 116], [6, 121], [7, 84], [7, 85], [7, 108], [7, 114], [8, 71], [8, 80], [8, 108], [8, 125], [9, 68], [9, 72], [9, 122], [9, 128], [10, 85], [10, 95], [10, 100], [10, 128], [11, 95], [11, 102], [11, 109], [11, 121], [12, 68], [12, 99], [12, 109], [12, 110], [13, 77], [13, 80], [13, 100], [13, 110], [14, 72], [14, 77], [14, 96], [14, 121], [15, 85], [15, 96], [15, 99], [15, 126], [16, 80], [16, 102], [16, 122], [16, 126], [17, 72], [17, 73], [17, 82], [17, 92], [18, 73], [18, 81], [18, 100], [18, 107], [19, 83], [19, 91], [19, 102], [19, 107], [20, 82], [20, 83], [20, 99], [20, 118], [21, 65], [21, 75], [21, 100], [21, 118], [22, 65], [22, 72], [22, 91], [22, 117], [23, 81], [23, 99], [23, 112], [23, 117], [24, 75], [24, 92], [24, 102], [24, 112], [25, 70], [25, 82], [25, 87], [25, 124], [26, 67], [26, 81], [26, 87], [26, 104], [27, 67], [27, 91], [27, 97], [27, 111], [28, 82], [28, 97], [28, 115], [28, 123], [29, 75], [29, 104], [29, 116], [29, 123], [30, 90], [30, 91], [30, 116], [30, 124], [31, 81], [31, 90], [31, 108], [31, 115], [32, 70], [32, 75], [32, 108], [32, 111], [33, 69], [33, 74], [33, 122], [33, 124], [34, 74], [34, 95], [34, 98], [34, 104], [35, 79], [35, 86], [35, 95], [35, 111], [36, 69], [36, 86], [36, 110], [36, 115], [37, 104], [37, 105], [37, 110], [37, 113], [38, 79], [38, 96], [38, 113], [38, 124], [39, 96], [39, 98], [39, 115], [39, 127], [40, 105], [40, 111], [40, 122], [40, 127], [41, 69], [41, 71], [41, 73], [41, 78], [42, 73], [42, 94], [42, 98], [42, 101], [43, 79], [43, 83], [43, 94], [43, 119], [44, 66], [44, 69], [44, 83], [44, 106], [45, 65], [45, 66], [45, 101], [45, 105], [46, 65], [46, 78], [46, 79], [46, 84], [47, 84], [47, 98], [47, 106], [47, 112], [48, 71], [48, 105], [48, 112], [48, 119], [49, 70], [49, 78], [49, 120], [49, 128], [50, 67], [50, 76], [50, 101], [50, 128], [51, 67], [51, 88], [51, 109], [51, 119], [52, 106], [52, 109], [52, 120], [52, 123], [53, 77], [53, 101], [53, 103], [53, 123], [54, 77], [54, 78], [54, 88], [54, 90], [55, 76], [55, 90], [55, 106], [55, 126], [56, 70], [56, 103], [56, 119], [56, 126], [57, 74], [57, 92], [57, 93], [57, 120], [58, 74], [58, 76], [58, 89], [58, 107], [59, 86], [59, 88], [59, 107], [59, 125], [60, 86], [60, 114], [60, 118], [60, 120], [61, 89], [61, 103], [61, 113], [61, 118], [62, 88], [62, 93], [62, 113], [62, 117], [63, 76], [63, 114], [63, 117], [63, 127], [64, 92], [64, 103], [64, 125], [64, 127]]);;
R:=P177Census(D);;Need(Size(R.F)=3072);;
PrintTo("current_c4_descent/128_051.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_051 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
