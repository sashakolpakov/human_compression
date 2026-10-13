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
D:=P177Graph("100_009",100,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50],[[1, 51], [1, 52], [1, 81], [1, 82], [2, 51], [2, 52], [2, 71], [2, 72], [3, 71], [3, 72], [3, 91], [3, 92], [4, 61], [4, 62], [4, 91], [4, 92], [5, 61], [5, 62], [5, 81], [5, 82], [6, 52], [6, 53], [6, 92], [6, 93], [7, 52], [7, 53], [7, 62], [7, 63], [8, 62], [8, 63], [8, 72], [8, 73], [9, 72], [9, 73], [9, 82], [9, 83], [10, 82], [10, 83], [10, 92], [10, 93], [11, 53], [11, 54], [11, 83], [11, 84], [12, 53], [12, 54], [12, 73], [12, 74], [13, 73], [13, 74], [13, 93], [13, 94], [14, 63], [14, 64], [14, 93], [14, 94], [15, 63], [15, 64], [15, 83], [15, 84], [16, 54], [16, 55], [16, 94], [16, 95], [17, 54], [17, 55], [17, 64], [17, 65], [18, 64], [18, 65], [18, 74], [18, 75], [19, 74], [19, 75], [19, 84], [19, 85], [20, 84], [20, 85], [20, 94], [20, 95], [21, 55], [21, 56], [21, 85], [21, 86], [22, 55], [22, 56], [22, 75], [22, 76], [23, 75], [23, 76], [23, 95], [23, 96], [24, 65], [24, 66], [24, 95], [24, 96], [25, 65], [25, 66], [25, 85], [25, 86], [26, 56], [26, 57], [26, 96], [26, 97], [27, 56], [27, 57], [27, 66], [27, 67], [28, 66], [28, 67], [28, 76], [28, 77], [29, 76], [29, 77], [29, 86], [29, 87], [30, 86], [30, 87], [30, 96], [30, 97], [31, 57], [31, 58], [31, 87], [31, 88], [32, 57], [32, 58], [32, 77], [32, 78], [33, 77], [33, 78], [33, 97], [33, 98], [34, 67], [34, 68], [34, 97], [34, 98], [35, 67], [35, 68], [35, 87], [35, 88], [36, 58], [36, 59], [36, 98], [36, 99], [37, 58], [37, 59], [37, 68], [37, 69], [38, 68], [38, 69], [38, 78], [38, 79], [39, 78], [39, 79], [39, 88], [39, 89], [40, 88], [40, 89], [40, 98], [40, 99], [41, 59], [41, 60], [41, 89], [41, 90], [42, 59], [42, 60], [42, 79], [42, 80], [43, 79], [43, 80], [43, 99], [43, 100], [44, 69], [44, 70], [44, 99], [44, 100], [45, 69], [45, 70], [45, 89], [45, 90], [46, 51], [46, 60], [46, 91], [46, 100], [47, 51], [47, 60], [47, 61], [47, 70], [48, 61], [48, 70], [48, 71], [48, 80], [49, 71], [49, 80], [49, 81], [49, 90], [50, 81], [50, 90], [50, 91], [50, 100]]);;
R:=P177Census(D);;Need(Size(R.F)=200);;
PrintTo("current_c4_descent/100_009.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 100_009 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
