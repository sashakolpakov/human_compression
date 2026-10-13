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
D:=P177Graph("VT3_162_22",162,[1, 4, 6, 10, 12, 13, 14, 17, 18, 20, 23, 24, 27, 28, 29, 32, 34, 35, 36, 40, 42, 43, 45, 46, 47, 48, 49, 51, 52, 54, 55, 56, 60, 61, 64, 65, 68, 70, 73, 77, 78, 79, 80, 82, 89, 91, 92, 94, 95, 97, 99, 100, 101, 106, 107, 109, 110, 112, 116, 121, 123, 124, 125, 127, 128, 129, 130, 131, 134, 135, 136, 138, 139, 140, 145, 153, 154, 155, 159, 160, 162],[[1, 21], [1, 67], [1, 146], [2, 95], [2, 97], [2, 100], [3, 13], [3, 28], [3, 123], [4, 26], [4, 144], [4, 157], [5, 12], [5, 47], [5, 160], [6, 22], [6, 37], [6, 83], [7, 13], [7, 73], [7, 95], [8, 13], [8, 17], [8, 68], [9, 51], [9, 116], [9, 136], [10, 38], [10, 53], [10, 156], [11, 24], [11, 47], [11, 128], [12, 74], [12, 76], [14, 53], [14, 103], [14, 120], [15, 89], [15, 130], [15, 139], [16, 42], [16, 61], [16, 79], [17, 39], [17, 72], [18, 44], [18, 113], [18, 142], [19, 45], [19, 46], [19, 60], [20, 71], [20, 75], [20, 132], [21, 24], [21, 32], [22, 35], [22, 134], [23, 102], [23, 142], [23, 161], [24, 98], [25, 28], [25, 46], [25, 127], [26, 70], [26, 136], [27, 96], [27, 104], [27, 119], [28, 71], [29, 37], [29, 90], [29, 108], [30, 54], [30, 78], [30, 139], [31, 61], [31, 65], [31, 145], [32, 66], [32, 72], [33, 129], [33, 145], [33, 159], [34, 39], [34, 104], [34, 113], [35, 120], [35, 150], [36, 66], [36, 143], [36, 156], [37, 107], [38, 77], [38, 80], [39, 65], [40, 50], [40, 93], [40, 122], [41, 52], [41, 70], [41, 123], [42, 132], [42, 133], [43, 72], [43, 84], [43, 90], [44, 97], [44, 110], [45, 76], [45, 118], [46, 111], [47, 62], [48, 63], [48, 86], [48, 119], [49, 102], [49, 114], [49, 146], [50, 101], [50, 154], [51, 69], [51, 114], [52, 53], [52, 86], [54, 119], [54, 141], [55, 67], [55, 118], [55, 133], [56, 81], [56, 86], [56, 133], [57, 82], [57, 121], [57, 138], [58, 92], [58, 159], [58, 160], [59, 91], [59, 134], [59, 140], [60, 69], [60, 120], [61, 157], [62, 135], [62, 138], [63, 64], [63, 154], [64, 152], [64, 161], [65, 103], [66, 94], [67, 140], [68, 74], [68, 152], [69, 101], [70, 98], [71, 82], [73, 114], [73, 117], [74, 131], [75, 109], [75, 125], [76, 139], [77, 142], [77, 158], [78, 90], [78, 144], [79, 83], [79, 117], [80, 88], [80, 148], [81, 100], [81, 162], [82, 87], [83, 128], [84, 101], [84, 155], [85, 92], [85, 94], [85, 100], [87, 91], [87, 130], [88, 106], [88, 140], [89, 117], [89, 156], [91, 147], [92, 147], [93, 110], [93, 130], [94, 111], [95, 105], [96, 127], [96, 128], [97, 150], [98, 110], [99, 115], [99, 122], [99, 148], [102, 121], [103, 138], [104, 116], [105, 106], [105, 135], [106, 144], [107, 126], [107, 151], [108, 121], [108, 162], [109, 143], [109, 149], [111, 112], [112, 157], [112, 161], [113, 153], [115, 131], [115, 162], [116, 147], [118, 153], [122, 145], [123, 151], [124, 126], [124, 137], [124, 143], [125, 141], [125, 150], [126, 153], [127, 148], [129, 141], [129, 146], [131, 149], [132, 155], [134, 152], [135, 137], [136, 149], [137, 154], [151, 159], [155, 158], [158, 160]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_162_22.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_162_22 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
