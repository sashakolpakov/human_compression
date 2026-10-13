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
D:=P177Graph("VT3_158_4",158,[1, 6, 11, 14, 15, 17, 19, 20, 21, 22, 25, 27, 28, 31, 32, 35, 36, 38, 39, 40, 41, 43, 46, 48, 50, 51, 57, 58, 59, 61, 64, 68, 70, 71, 72, 75, 77, 81, 82, 84, 85, 86, 90, 93, 94, 96, 98, 100, 102, 103, 104, 106, 107, 108, 111, 112, 113, 114, 118, 122, 124, 127, 128, 131, 137, 138, 139, 140, 141, 144, 145, 149, 150, 151, 153, 154, 156, 157, 158],[[1, 80], [1, 116], [1, 119], [2, 25], [2, 58], [2, 85], [3, 107], [3, 112], [3, 141], [4, 14], [4, 36], [4, 96], [5, 41], [5, 59], [5, 77], [6, 99], [6, 105], [6, 146], [7, 15], [7, 46], [7, 108], [8, 103], [8, 111], [8, 158], [9, 35], [9, 50], [9, 128], [10, 68], [10, 82], [10, 139], [11, 24], [11, 92], [11, 132], [12, 31], [12, 85], [12, 153], [13, 14], [13, 19], [13, 93], [14, 148], [15, 18], [15, 115], [16, 19], [16, 40], [16, 106], [17, 23], [17, 79], [17, 142], [18, 43], [18, 82], [19, 78], [20, 53], [20, 69], [20, 88], [21, 88], [21, 130], [21, 135], [22, 24], [22, 52], [22, 123], [23, 41], [23, 140], [24, 27], [25, 55], [25, 132], [26, 32], [26, 61], [26, 149], [27, 74], [27, 143], [28, 91], [28, 110], [28, 126], [29, 43], [29, 84], [29, 139], [30, 96], [30, 128], [30, 131], [31, 54], [31, 130], [32, 116], [32, 120], [33, 102], [33, 107], [33, 156], [34, 102], [34, 122], [34, 124], [35, 78], [35, 135], [36, 66], [36, 115], [37, 70], [37, 94], [37, 122], [38, 65], [38, 79], [38, 155], [39, 49], [39, 95], [39, 142], [40, 109], [40, 121], [41, 152], [42, 50], [42, 118], [42, 149], [43, 66], [44, 68], [44, 86], [44, 114], [45, 90], [45, 127], [45, 139], [46, 60], [46, 146], [47, 98], [47, 122], [47, 145], [48, 63], [48, 95], [48, 134], [49, 51], [49, 71], [50, 88], [51, 79], [51, 109], [52, 108], [52, 144], [53, 70], [53, 118], [54, 58], [54, 106], [55, 71], [55, 138], [56, 82], [56, 108], [56, 114], [57, 87], [57, 97], [57, 117], [58, 121], [59, 76], [59, 136], [60, 112], [60, 144], [61, 83], [61, 126], [62, 64], [62, 111], [62, 138], [63, 72], [63, 111], [64, 74], [64, 132], [65, 137], [65, 140], [66, 131], [67, 113], [67, 141], [67, 158], [68, 87], [69, 94], [69, 100], [70, 91], [71, 121], [72, 120], [72, 133], [73, 124], [73, 137], [73, 156], [74, 158], [75, 133], [75, 134], [75, 136], [76, 90], [76, 151], [77, 134], [77, 142], [78, 96], [80, 128], [80, 149], [81, 99], [81, 148], [81, 155], [83, 103], [83, 113], [84, 119], [84, 147], [85, 92], [86, 89], [86, 117], [87, 90], [89, 104], [89, 153], [91, 102], [92, 104], [93, 109], [93, 155], [94, 129], [95, 138], [97, 98], [97, 151], [98, 129], [99, 137], [100, 125], [100, 130], [101, 124], [101, 140], [101, 145], [103, 120], [104, 123], [105, 112], [105, 156], [106, 135], [107, 110], [110, 113], [114, 123], [115, 157], [116, 154], [117, 150], [118, 126], [119, 131], [125, 150], [125, 153], [127, 136], [127, 147], [129, 150], [133, 154], [141, 143], [143, 144], [145, 152], [146, 157], [147, 154], [148, 157], [151, 152]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_158_4.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_158_4 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
