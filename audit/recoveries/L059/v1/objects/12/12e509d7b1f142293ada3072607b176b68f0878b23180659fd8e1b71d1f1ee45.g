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
D:=P177Graph("128_050",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 76], [1, 82], [1, 83], [1, 103], [2, 81], [2, 82], [2, 85], [2, 115], [3, 79], [3, 80], [3, 84], [3, 85], [4, 71], [4, 84], [4, 123], [4, 125], [5, 91], [5, 105], [5, 112], [5, 125], [6, 91], [6, 99], [6, 109], [6, 126], [7, 68], [7, 93], [7, 99], [7, 116], [8, 68], [8, 76], [8, 78], [8, 86], [9, 67], [9, 77], [9, 83], [9, 125], [10, 77], [10, 99], [10, 101], [10, 115], [11, 80], [11, 87], [11, 99], [11, 111], [12, 76], [12, 87], [12, 94], [12, 123], [13, 73], [13, 76], [13, 89], [13, 105], [14, 73], [14, 85], [14, 97], [14, 109], [15, 85], [15, 116], [15, 117], [15, 119], [16, 78], [16, 90], [16, 119], [16, 125], [17, 67], [17, 73], [17, 107], [17, 120], [18, 73], [18, 96], [18, 101], [18, 113], [19, 104], [19, 111], [19, 113], [19, 119], [20, 94], [20, 119], [20, 124], [20, 128], [21, 77], [21, 89], [21, 124], [21, 127], [22, 77], [22, 92], [22, 97], [22, 108], [23, 87], [23, 92], [23, 102], [23, 117], [24, 87], [24, 90], [24, 100], [24, 120], [25, 75], [25, 81], [25, 107], [25, 124], [26, 75], [26, 92], [26, 96], [26, 103], [27, 71], [27, 88], [27, 92], [27, 104], [28, 79], [28, 88], [28, 120], [28, 128], [29, 98], [29, 120], [29, 126], [29, 127], [30, 98], [30, 108], [30, 112], [30, 113], [31, 74], [31, 86], [31, 102], [31, 113], [32, 74], [32, 93], [32, 100], [32, 124], [33, 78], [33, 81], [33, 98], [33, 118], [34, 80], [34, 98], [34, 103], [34, 110], [35, 71], [35, 74], [35, 110], [35, 115], [36, 74], [36, 79], [36, 105], [36, 114], [37, 75], [37, 114], [37, 123], [37, 126], [38, 75], [38, 95], [38, 112], [38, 116], [39, 86], [39, 88], [39, 95], [39, 109], [40, 83], [40, 88], [40, 93], [40, 118], [41, 72], [41, 78], [41, 101], [41, 114], [42, 67], [42, 72], [42, 80], [42, 95], [43, 94], [43, 95], [43, 106], [43, 115], [44, 105], [44, 106], [44, 111], [44, 118], [45, 65], [45, 97], [45, 118], [45, 123], [46, 65], [46, 89], [46, 110], [46, 116], [47, 90], [47, 109], [47, 110], [47, 122], [48, 83], [48, 114], [48, 117], [48, 122], [49, 65], [49, 100], [49, 101], [49, 121], [50, 65], [50, 66], [50, 67], [50, 104], [51, 66], [51, 94], [51, 96], [51, 122], [52, 69], [52, 111], [52, 122], [52, 127], [53, 69], [53, 72], [53, 97], [53, 128], [54, 70], [54, 72], [54, 89], [54, 102], [55, 70], [55, 90], [55, 106], [55, 108], [56, 106], [56, 107], [56, 117], [56, 121], [57, 69], [57, 91], [57, 100], [57, 103], [58, 70], [58, 81], [58, 91], [58, 104], [59, 68], [59, 70], [59, 79], [59, 96], [60, 68], [60, 71], [60, 121], [60, 127], [61, 82], [61, 112], [61, 121], [61, 128], [62, 66], [62, 82], [62, 102], [62, 126], [63, 66], [63, 84], [63, 93], [63, 108], [64, 69], [64, 84], [64, 86], [64, 107]]);;
R:=P177Census(D);;Need(Size(R.F)=1024);;
PrintTo("current_c4_descent/128_050.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_050 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
