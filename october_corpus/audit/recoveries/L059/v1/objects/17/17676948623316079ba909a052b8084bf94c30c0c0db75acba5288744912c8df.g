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
D:=P177Graph("VT3_150_25",150,[1, 3, 4, 5, 7, 8, 11, 13, 14, 15, 16, 20, 25, 27, 29, 30, 31, 32, 33, 34, 36, 38, 39, 40, 41, 42, 45, 48, 49, 50, 51, 53, 55, 56, 57, 58, 62, 65, 67, 68, 73, 74, 75, 76, 80, 82, 85, 86, 97, 100, 101, 103, 104, 108, 110, 113, 115, 119, 120, 121, 123, 124, 125, 126, 127, 128, 129, 131, 132, 137, 138, 140, 143, 144, 148],[[1, 91], [1, 112], [1, 149], [2, 41], [2, 104], [2, 132], [3, 21], [3, 59], [3, 135], [4, 69], [4, 83], [4, 145], [5, 46], [5, 106], [5, 150], [6, 15], [6, 140], [6, 143], [7, 93], [7, 95], [7, 114], [8, 26], [8, 28], [8, 93], [9, 30], [9, 104], [9, 126], [10, 53], [10, 76], [10, 143], [11, 26], [11, 47], [11, 122], [12, 20], [12, 31], [12, 123], [13, 37], [13, 83], [13, 118], [14, 66], [14, 81], [14, 135], [15, 109], [15, 136], [16, 61], [16, 66], [16, 94], [17, 51], [17, 74], [17, 148], [18, 49], [18, 56], [18, 76], [19, 34], [19, 67], [19, 80], [20, 95], [20, 142], [21, 124], [21, 127], [22, 40], [22, 57], [22, 86], [23, 45], [23, 67], [23, 75], [24, 76], [24, 108], [24, 120], [25, 43], [25, 46], [25, 116], [26, 73], [27, 35], [27, 89], [27, 112], [28, 120], [28, 128], [29, 89], [29, 99], [29, 111], [30, 71], [30, 88], [31, 43], [31, 114], [32, 61], [32, 81], [32, 98], [33, 79], [33, 135], [33, 146], [34, 105], [34, 111], [35, 85], [35, 110], [36, 37], [36, 59], [36, 66], [37, 97], [38, 59], [38, 83], [38, 117], [39, 60], [39, 64], [39, 146], [40, 116], [40, 122], [41, 88], [41, 122], [42, 44], [42, 87], [42, 96], [43, 144], [44, 50], [44, 57], [45, 61], [45, 72], [46, 57], [47, 128], [47, 132], [48, 71], [48, 96], [48, 141], [49, 60], [49, 70], [50, 106], [50, 107], [51, 92], [51, 107], [52, 82], [52, 100], [52, 115], [53, 70], [53, 109], [54, 58], [54, 75], [54, 80], [55, 64], [55, 87], [55, 141], [56, 84], [56, 133], [58, 92], [58, 106], [60, 113], [62, 87], [62, 107], [62, 134], [63, 65], [63, 125], [63, 137], [64, 121], [65, 98], [65, 105], [67, 98], [68, 69], [68, 118], [68, 147], [69, 110], [70, 121], [71, 127], [72, 123], [72, 144], [73, 114], [73, 116], [74, 109], [74, 134], [75, 150], [77, 131], [77, 138], [77, 140], [78, 82], [78, 119], [78, 128], [79, 113], [79, 137], [80, 99], [81, 137], [82, 91], [84, 113], [84, 125], [85, 145], [85, 149], [86, 88], [86, 96], [89, 129], [90, 103], [90, 110], [90, 129], [91, 132], [92, 101], [93, 108], [94, 97], [94, 123], [95, 131], [97, 142], [99, 101], [100, 111], [100, 112], [101, 102], [102, 129], [102, 148], [103, 136], [103, 147], [104, 149], [105, 115], [108, 139], [115, 130], [117, 126], [117, 127], [118, 138], [119, 130], [119, 133], [120, 133], [121, 134], [124, 141], [124, 146], [125, 130], [126, 145], [131, 139], [136, 148], [138, 142], [139, 143], [140, 147], [144, 150]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_150_25.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_150_25 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
