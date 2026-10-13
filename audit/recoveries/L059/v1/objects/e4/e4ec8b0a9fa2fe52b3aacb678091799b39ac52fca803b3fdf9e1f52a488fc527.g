Need:=function(ok) if not ok then Error("L059 cubic census invalid"); fi; end;;
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
D:=P177Graph("VT3_134_9",134,[1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 14, 16, 21, 22, 23, 24, 28, 29, 30, 32, 35, 36, 38, 40, 41, 42, 43, 45, 46, 51, 53, 58, 59, 63, 65, 66, 68, 69, 70, 72, 73, 74, 75, 76, 77, 80, 87, 88, 92, 94, 98, 99, 105, 107, 108, 110, 111, 112, 113, 114, 122, 123, 124, 125, 127, 132, 134],[[1, 25], [1, 60], [1, 103], [2, 85], [2, 119], [2, 133], [3, 37], [3, 86], [3, 89], [4, 101], [4, 109], [4, 119], [5, 47], [5, 85], [5, 109], [6, 10], [6, 34], [6, 126], [7, 21], [7, 77], [7, 98], [8, 15], [8, 54], [8, 82], [9, 15], [9, 95], [9, 130], [10, 42], [10, 43], [11, 19], [11, 81], [11, 117], [12, 27], [12, 71], [12, 128], [13, 32], [13, 66], [13, 123], [14, 44], [14, 90], [14, 100], [15, 98], [16, 25], [16, 54], [16, 78], [17, 38], [17, 108], [17, 127], [18, 63], [18, 74], [18, 125], [19, 38], [19, 43], [20, 46], [20, 70], [20, 112], [21, 71], [21, 130], [22, 48], [22, 67], [22, 84], [23, 90], [23, 93], [23, 119], [24, 47], [24, 86], [24, 129], [25, 51], [26, 36], [26, 66], [26, 111], [27, 45], [27, 92], [28, 85], [28, 97], [28, 116], [29, 48], [29, 104], [29, 118], [30, 34], [30, 57], [30, 79], [31, 68], [31, 80], [31, 107], [32, 106], [32, 117], [33, 69], [33, 76], [33, 122], [34, 53], [35, 47], [35, 60], [35, 116], [36, 100], [36, 118], [37, 80], [37, 92], [38, 83], [39, 40], [39, 74], [39, 76], [40, 115], [40, 126], [41, 93], [41, 106], [41, 133], [42, 83], [42, 121], [43, 115], [44, 110], [44, 132], [45, 62], [45, 89], [46, 55], [46, 84], [48, 77], [49, 65], [49, 99], [49, 107], [50, 72], [50, 108], [50, 124], [51, 82], [51, 116], [52, 111], [52, 124], [52, 127], [53, 64], [53, 121], [54, 112], [55, 105], [55, 132], [56, 75], [56, 108], [56, 114], [57, 65], [57, 73], [58, 78], [58, 103], [58, 121], [59, 97], [59, 102], [59, 133], [60, 114], [61, 94], [61, 99], [61, 132], [62, 113], [62, 124], [63, 96], [63, 130], [64, 70], [64, 105], [65, 120], [66, 81], [67, 98], [67, 112], [68, 86], [68, 109], [69, 115], [69, 117], [70, 78], [71, 125], [72, 89], [72, 129], [73, 126], [73, 131], [74, 131], [75, 83], [75, 103], [76, 96], [77, 128], [79, 99], [79, 105], [80, 120], [81, 127], [82, 87], [84, 110], [87, 95], [87, 97], [88, 95], [88, 96], [88, 102], [90, 94], [91, 92], [91, 125], [91, 134], [93, 123], [94, 101], [100, 123], [101, 107], [102, 122], [104, 111], [104, 113], [106, 122], [110, 118], [113, 128], [114, 129], [120, 134], [131, 134]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_134_9.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_134_9 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
