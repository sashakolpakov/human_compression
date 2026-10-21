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
D:=P177Graph("VT3_114_2",114,[1, 2, 4, 5, 6, 8, 9, 10, 13, 16, 21, 25, 26, 27, 28, 33, 34, 38, 40, 42, 43, 44, 45, 47, 50, 52, 54, 63, 66, 68, 69, 71, 73, 74, 75, 77, 78, 79, 81, 84, 85, 88, 90, 92, 95, 96, 97, 98, 99, 102, 105, 107, 108, 109, 111, 113, 114],[[1, 48], [1, 86], [1, 94], [2, 24], [2, 70], [2, 87], [3, 71], [3, 75], [3, 102], [4, 12], [4, 22], [4, 110], [5, 15], [5, 36], [5, 60], [6, 30], [6, 49], [6, 101], [7, 66], [7, 73], [7, 99], [8, 76], [8, 80], [8, 100], [9, 17], [9, 37], [9, 49], [10, 11], [10, 31], [10, 72], [11, 27], [11, 40], [12, 45], [12, 69], [13, 37], [13, 70], [13, 106], [14, 40], [14, 47], [14, 75], [15, 52], [15, 73], [16, 18], [16, 39], [16, 62], [17, 28], [17, 97], [18, 25], [18, 98], [19, 26], [19, 63], [19, 85], [20, 21], [20, 34], [20, 69], [21, 56], [21, 80], [22, 68], [22, 109], [23, 50], [23, 85], [23, 99], [24, 90], [24, 108], [25, 53], [25, 61], [26, 31], [26, 89], [27, 58], [27, 104], [28, 106], [28, 112], [29, 77], [29, 84], [29, 90], [30, 38], [30, 105], [31, 78], [32, 33], [32, 43], [32, 96], [33, 61], [33, 101], [34, 94], [34, 103], [35, 92], [35, 96], [35, 97], [36, 42], [36, 111], [37, 74], [38, 61], [38, 62], [39, 54], [39, 77], [40, 46], [41, 44], [41, 74], [41, 95], [42, 82], [42, 83], [43, 53], [43, 103], [44, 46], [44, 76], [45, 57], [45, 80], [46, 78], [47, 56], [47, 76], [48, 66], [48, 69], [49, 113], [50, 59], [50, 110], [51, 88], [51, 98], [51, 102], [52, 83], [52, 112], [53, 102], [54, 64], [54, 91], [55, 74], [55, 78], [55, 113], [56, 71], [57, 81], [57, 109], [58, 107], [58, 111], [59, 63], [59, 68], [60, 99], [60, 107], [62, 114], [63, 93], [64, 68], [64, 114], [65, 79], [65, 88], [65, 111], [66, 110], [67, 77], [67, 79], [67, 98], [70, 95], [71, 103], [72, 85], [72, 107], [73, 86], [75, 104], [79, 82], [81, 87], [81, 100], [82, 90], [83, 108], [84, 87], [84, 91], [86, 92], [88, 104], [89, 105], [89, 113], [91, 109], [92, 112], [93, 105], [93, 114], [94, 96], [95, 100], [97, 101], [106, 108]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_114_2.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_114_2 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
