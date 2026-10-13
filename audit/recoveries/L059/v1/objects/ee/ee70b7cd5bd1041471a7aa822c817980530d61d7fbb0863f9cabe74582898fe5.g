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
D:=P177Graph("128_049",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],[[1, 79], [1, 82], [1, 83], [1, 84], [2, 74], [2, 83], [2, 90], [2, 108], [3, 88], [3, 90], [3, 106], [3, 115], [4, 65], [4, 88], [4, 112], [4, 126], [5, 93], [5, 96], [5, 117], [5, 126], [6, 68], [6, 71], [6, 93], [6, 105], [7, 69], [7, 89], [7, 105], [7, 127], [8, 69], [8, 78], [8, 79], [8, 111], [9, 81], [9, 82], [9, 87], [9, 126], [10, 74], [10, 81], [10, 105], [10, 118], [11, 91], [11, 97], [11, 105], [11, 106], [12, 65], [12, 79], [12, 91], [12, 103], [13, 76], [13, 79], [13, 96], [13, 128], [14, 68], [14, 76], [14, 90], [14, 101], [15, 86], [15, 90], [15, 120], [15, 127], [16, 104], [16, 111], [16, 120], [16, 126], [17, 76], [17, 87], [17, 99], [17, 121], [18, 76], [18, 85], [18, 113], [18, 118], [19, 97], [19, 98], [19, 113], [19, 120], [20, 103], [20, 120], [20, 124], [20, 125], [21, 81], [21, 95], [21, 125], [21, 128], [22, 81], [22, 94], [22, 101], [22, 119], [23, 73], [23, 86], [23, 91], [23, 94], [24, 91], [24, 104], [24, 109], [24, 121], [25, 78], [25, 80], [25, 99], [25, 125], [26, 80], [26, 85], [26, 94], [26, 115], [27, 92], [27, 94], [27, 98], [27, 108], [28, 92], [28, 117], [28, 121], [28, 124], [29, 95], [29, 102], [29, 112], [29, 121], [30, 89], [30, 102], [30, 113], [30, 119], [31, 71], [31, 73], [31, 77], [31, 113], [32, 77], [32, 84], [32, 109], [32, 125], [33, 74], [33, 78], [33, 102], [33, 116], [34, 82], [34, 102], [34, 110], [34, 115], [35, 65], [35, 77], [35, 108], [35, 110], [36, 77], [36, 106], [36, 114], [36, 117], [37, 68], [37, 80], [37, 112], [37, 114], [38, 80], [38, 89], [38, 96], [38, 100], [39, 71], [39, 92], [39, 100], [39, 111], [40, 84], [40, 92], [40, 116], [40, 127], [41, 74], [41, 75], [41, 104], [41, 114], [42, 75], [42, 82], [42, 97], [42, 100], [43, 65], [43, 100], [43, 107], [43, 118], [44, 106], [44, 107], [44, 116], [44, 128], [45, 66], [45, 68], [45, 103], [45, 116], [46, 66], [46, 86], [46, 96], [46, 110], [47, 101], [47, 110], [47, 111], [47, 123], [48, 87], [48, 114], [48, 123], [48, 127], [49, 66], [49, 85], [49, 104], [49, 122], [50, 66], [50, 67], [50, 97], [50, 99], [51, 67], [51, 118], [51, 123], [51, 124], [52, 70], [52, 98], [52, 123], [52, 128], [53, 70], [53, 75], [53, 103], [53, 119], [54, 72], [54, 75], [54, 86], [54, 95], [55, 72], [55, 101], [55, 107], [55, 109], [56, 73], [56, 87], [56, 107], [56, 122], [57, 70], [57, 84], [57, 85], [57, 93], [58, 72], [58, 93], [58, 99], [58, 108], [59, 69], [59, 72], [59, 115], [59, 124], [60, 69], [60, 98], [60, 112], [60, 122], [61, 83], [61, 117], [61, 119], [61, 122], [62, 67], [62, 71], [62, 83], [62, 95], [63, 67], [63, 88], [63, 89], [63, 109], [64, 70], [64, 73], [64, 78], [64, 88]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_049.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_049 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
