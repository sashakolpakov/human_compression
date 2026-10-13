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
D:=P177Graph("VT3_126_22",126,[1, 2, 3, 5, 10, 12, 17, 18, 20, 23, 30, 32, 33, 35, 40, 41, 42, 43, 44, 45, 47, 50, 51, 54, 55, 56, 59, 63, 64, 65, 68, 70, 71, 73, 76, 77, 79, 80, 81, 83, 86, 90, 93, 94, 95, 96, 97, 99, 100, 102, 103, 104, 107, 108, 110, 111, 114, 116, 118, 121, 122, 123, 124],[[1, 25], [1, 37], [1, 113], [2, 9], [2, 16], [2, 22], [3, 11], [3, 49], [3, 66], [4, 17], [4, 81], [4, 122], [5, 21], [5, 75], [5, 125], [6, 54], [6, 90], [6, 104], [7, 95], [7, 97], [7, 108], [8, 20], [8, 70], [8, 86], [9, 43], [9, 68], [10, 11], [10, 26], [10, 105], [11, 51], [12, 34], [12, 52], [12, 61], [13, 18], [13, 96], [13, 102], [14, 20], [14, 50], [14, 71], [15, 40], [15, 64], [15, 123], [16, 64], [16, 108], [17, 37], [17, 126], [18, 34], [18, 98], [19, 59], [19, 76], [19, 100], [20, 25], [21, 65], [21, 104], [22, 83], [22, 97], [23, 27], [23, 52], [23, 98], [24, 50], [24, 93], [24, 110], [25, 73], [26, 77], [26, 111], [27, 42], [27, 63], [28, 45], [28, 93], [28, 111], [29, 76], [29, 77], [29, 79], [30, 36], [30, 82], [30, 119], [31, 95], [31, 99], [31, 122], [32, 58], [32, 84], [32, 89], [33, 36], [33, 38], [33, 98], [34, 116], [35, 58], [35, 60], [35, 78], [36, 102], [37, 123], [38, 47], [38, 63], [39, 96], [39, 107], [39, 124], [40, 113], [40, 125], [41, 74], [41, 88], [41, 120], [42, 101], [42, 120], [43, 74], [43, 101], [44, 85], [44, 92], [44, 106], [45, 57], [45, 105], [46, 70], [46, 94], [46, 116], [47, 66], [47, 82], [48, 99], [48, 102], [48, 124], [49, 54], [49, 77], [50, 57], [51, 82], [51, 91], [52, 114], [53, 55], [53, 79], [53, 100], [54, 62], [55, 67], [55, 92], [56, 67], [56, 72], [56, 125], [57, 73], [58, 97], [59, 60], [59, 84], [60, 103], [61, 70], [61, 71], [62, 65], [62, 79], [63, 117], [64, 75], [65, 67], [66, 90], [68, 75], [68, 109], [69, 76], [69, 103], [69, 111], [71, 115], [72, 86], [72, 94], [73, 126], [74, 83], [78, 83], [78, 121], [80, 91], [80, 105], [80, 126], [81, 91], [81, 119], [84, 107], [85, 96], [85, 116], [86, 113], [87, 108], [87, 122], [87, 123], [88, 110], [88, 121], [89, 95], [89, 124], [90, 117], [92, 94], [93, 112], [99, 119], [100, 106], [101, 118], [103, 112], [104, 109], [106, 107], [109, 118], [110, 115], [112, 121], [114, 115], [114, 120], [117, 118]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_126_22.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_126_22 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
