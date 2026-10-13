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
D:=P177Graph("VT3_122_9",122,[1, 3, 6, 7, 8, 9, 10, 11, 14, 15, 17, 19, 20, 21, 24, 28, 30, 34, 35, 36, 37, 39, 41, 43, 44, 45, 47, 49, 50, 53, 54, 57, 59, 61, 62, 64, 65, 66, 69, 70, 78, 79, 80, 82, 87, 88, 91, 95, 96, 100, 102, 103, 108, 109, 111, 112, 113, 114, 115, 117, 121],[[1, 71], [1, 74], [1, 75], [2, 28], [2, 102], [2, 109], [3, 25], [3, 38], [3, 89], [4, 88], [4, 91], [4, 102], [5, 7], [5, 15], [5, 39], [6, 13], [6, 23], [6, 60], [7, 89], [7, 97], [8, 31], [8, 55], [8, 110], [9, 12], [9, 55], [9, 77], [10, 26], [10, 85], [10, 99], [11, 31], [11, 77], [11, 94], [12, 95], [12, 96], [13, 43], [13, 53], [14, 52], [14, 76], [14, 104], [15, 75], [15, 106], [16, 47], [16, 65], [16, 112], [17, 18], [17, 32], [17, 119], [18, 49], [18, 113], [19, 40], [19, 73], [19, 92], [20, 73], [20, 107], [20, 120], [21, 92], [21, 98], [21, 105], [22, 36], [22, 88], [22, 103], [23, 54], [23, 59], [24, 94], [24, 104], [24, 116], [25, 54], [25, 79], [26, 49], [26, 57], [27, 36], [27, 102], [27, 114], [28, 51], [28, 110], [29, 79], [29, 82], [29, 109], [30, 76], [30, 120], [30, 122], [31, 87], [32, 39], [32, 70], [33, 47], [33, 69], [33, 95], [34, 81], [34, 104], [34, 119], [35, 48], [35, 89], [35, 106], [36, 86], [37, 72], [37, 107], [37, 122], [38, 59], [38, 121], [39, 71], [40, 44], [40, 66], [41, 42], [41, 52], [41, 94], [42, 69], [42, 111], [43, 101], [43, 118], [44, 46], [44, 58], [45, 67], [45, 75], [45, 84], [46, 108], [46, 117], [47, 118], [48, 108], [48, 121], [49, 81], [50, 52], [50, 68], [50, 122], [51, 82], [51, 87], [53, 68], [53, 72], [54, 63], [55, 62], [56, 65], [56, 80], [56, 100], [57, 93], [57, 105], [58, 62], [58, 96], [59, 72], [60, 61], [60, 114], [61, 86], [61, 101], [62, 83], [63, 109], [63, 114], [64, 90], [64, 116], [64, 119], [65, 101], [66, 83], [66, 98], [67, 96], [67, 117], [68, 111], [69, 77], [70, 90], [70, 97], [71, 113], [73, 108], [74, 100], [74, 112], [76, 115], [78, 92], [78, 93], [78, 120], [79, 97], [80, 85], [80, 86], [81, 115], [82, 90], [83, 91], [84, 95], [84, 112], [85, 103], [87, 116], [88, 98], [91, 110], [93, 115], [99, 100], [99, 113], [103, 105], [106, 117], [107, 121], [111, 118]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_122_9.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_122_9 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
