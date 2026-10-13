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
D:=P177Graph("VT3_110_1",110,[1, 4, 5, 6, 8, 9, 10, 12, 13, 16, 17, 18, 25, 27, 31, 37, 38, 42, 43, 44, 45, 46, 47, 48, 49, 50, 52, 54, 56, 59, 60, 62, 65, 68, 69, 72, 77, 78, 82, 83, 84, 86, 88, 89, 90, 92, 94, 96, 97, 99, 103, 104, 105, 106, 110],[[1, 19], [1, 24], [1, 57], [2, 16], [2, 44], [2, 104], [3, 44], [3, 45], [3, 47], [4, 7], [4, 79], [4, 102], [5, 53], [5, 71], [5, 74], [6, 35], [6, 58], [6, 91], [7, 47], [7, 105], [8, 11], [8, 14], [8, 57], [9, 36], [9, 66], [9, 91], [10, 26], [10, 64], [10, 85], [11, 86], [11, 89], [12, 28], [12, 34], [12, 40], [13, 73], [13, 85], [13, 87], [14, 82], [14, 110], [15, 60], [15, 96], [15, 99], [16, 29], [16, 98], [17, 34], [17, 67], [17, 95], [18, 34], [18, 74], [18, 107], [19, 78], [19, 88], [20, 68], [20, 72], [20, 92], [21, 49], [21, 60], [21, 92], [22, 46], [22, 52], [22, 83], [23, 31], [23, 83], [23, 103], [24, 72], [24, 84], [25, 35], [25, 67], [25, 108], [26, 38], [26, 42], [27, 55], [27, 73], [27, 100], [28, 90], [28, 99], [29, 31], [29, 94], [30, 68], [30, 77], [30, 106], [31, 100], [32, 59], [32, 78], [32, 104], [33, 38], [33, 47], [33, 96], [35, 94], [36, 48], [36, 110], [37, 73], [37, 74], [37, 80], [38, 61], [39, 49], [39, 78], [39, 83], [40, 97], [40, 106], [41, 43], [41, 88], [41, 105], [42, 71], [42, 81], [43, 95], [43, 98], [44, 76], [45, 57], [45, 58], [46, 87], [46, 95], [48, 71], [48, 109], [49, 81], [50, 67], [50, 102], [50, 109], [51, 65], [51, 86], [51, 94], [52, 61], [52, 91], [53, 62], [53, 105], [54, 63], [54, 75], [54, 108], [55, 88], [55, 99], [56, 63], [56, 70], [56, 87], [58, 90], [59, 75], [59, 79], [60, 66], [61, 97], [62, 70], [62, 93], [63, 89], [64, 65], [64, 77], [65, 93], [66, 69], [68, 100], [69, 76], [69, 80], [70, 90], [72, 108], [75, 97], [76, 106], [77, 102], [79, 82], [80, 86], [81, 89], [82, 107], [84, 93], [84, 101], [85, 104], [92, 107], [96, 101], [98, 110], [101, 103], [103, 109]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_110_1.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_110_1 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
