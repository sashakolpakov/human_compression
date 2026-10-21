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
D:=P177Graph("VT3_128_16",128,[1, 2, 4, 6, 9, 12, 13, 16, 17, 18, 20, 21, 28, 31, 32, 33, 34, 37, 38, 39, 41, 44, 45, 46, 47, 49, 51, 53, 54, 57, 59, 61, 62, 63, 64, 65, 66, 68, 69, 71, 72, 77, 79, 83, 84, 87, 88, 91, 92, 93, 94, 97, 100, 102, 106, 109, 114, 115, 117, 118, 119, 121, 123, 125],[[1, 23], [1, 48], [1, 95], [2, 5], [2, 8], [2, 58], [3, 87], [3, 93], [3, 102], [4, 8], [4, 10], [4, 52], [5, 32], [5, 68], [6, 24], [6, 67], [6, 81], [7, 39], [7, 49], [7, 79], [8, 12], [9, 29], [9, 70], [9, 103], [10, 51], [10, 63], [11, 44], [11, 45], [11, 83], [12, 19], [12, 99], [13, 19], [13, 22], [13, 52], [14, 31], [14, 65], [14, 77], [15, 39], [15, 44], [15, 92], [16, 26], [16, 35], [16, 112], [17, 25], [17, 112], [17, 116], [18, 70], [18, 86], [18, 89], [19, 93], [20, 55], [20, 60], [20, 80], [21, 56], [21, 67], [21, 78], [22, 84], [22, 102], [23, 69], [23, 117], [24, 83], [24, 119], [25, 34], [25, 68], [26, 31], [26, 41], [27, 44], [27, 72], [27, 79], [28, 81], [28, 86], [28, 96], [29, 88], [29, 97], [30, 33], [30, 118], [30, 123], [31, 116], [32, 99], [32, 104], [33, 43], [33, 124], [34, 58], [34, 95], [35, 97], [35, 106], [36, 46], [36, 87], [36, 88], [37, 40], [37, 78], [37, 110], [38, 95], [38, 112], [38, 128], [39, 73], [40, 65], [40, 91], [41, 90], [41, 120], [42, 61], [42, 84], [42, 123], [43, 65], [43, 121], [45, 98], [45, 108], [46, 73], [46, 75], [47, 80], [47, 111], [47, 122], [48, 63], [48, 114], [49, 75], [49, 99], [50, 59], [50, 121], [50, 123], [51, 60], [51, 122], [52, 109], [53, 81], [53, 89], [53, 105], [54, 104], [54, 110], [54, 126], [55, 100], [55, 118], [56, 72], [56, 83], [57, 74], [57, 98], [57, 111], [58, 63], [59, 67], [59, 96], [60, 109], [61, 96], [61, 127], [62, 86], [62, 103], [62, 127], [64, 74], [64, 82], [64, 113], [66, 85], [66, 113], [66, 120], [68, 126], [69, 89], [69, 128], [70, 106], [71, 73], [71, 76], [71, 82], [72, 110], [74, 125], [75, 93], [76, 88], [76, 115], [77, 120], [77, 124], [78, 121], [79, 104], [80, 125], [82, 92], [84, 107], [85, 100], [85, 125], [87, 103], [90, 97], [90, 115], [91, 116], [91, 126], [92, 98], [94, 101], [94, 108], [94, 111], [100, 124], [101, 114], [101, 117], [102, 127], [105, 117], [105, 119], [106, 128], [107, 109], [107, 118], [108, 119], [113, 115], [114, 122]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_128_16.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_128_16 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
