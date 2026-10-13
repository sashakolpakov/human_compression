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
D:=P177Graph("VT3_104_19",104,[1, 2, 3, 7, 9, 11, 13, 16, 17, 21, 22, 24, 30, 32, 33, 34, 35, 38, 40, 45, 46, 47, 49, 50, 52, 54, 56, 59, 60, 61, 64, 65, 66, 67, 70, 71, 72, 73, 74, 75, 76, 80, 83, 88, 89, 90, 91, 92, 98, 100, 103, 104],[[1, 28], [1, 31], [1, 81], [2, 28], [2, 39], [2, 55], [3, 85], [3, 93], [3, 99], [4, 34], [4, 60], [4, 74], [5, 24], [5, 67], [5, 70], [6, 9], [6, 30], [6, 56], [7, 15], [7, 20], [7, 55], [8, 21], [8, 45], [8, 73], [9, 10], [9, 57], [10, 33], [10, 49], [11, 43], [11, 58], [11, 101], [12, 35], [12, 45], [12, 47], [13, 36], [13, 51], [13, 84], [14, 30], [14, 72], [14, 100], [15, 60], [15, 100], [16, 77], [16, 81], [16, 102], [17, 62], [17, 85], [17, 96], [18, 52], [18, 75], [18, 83], [19, 52], [19, 61], [19, 104], [20, 72], [20, 92], [21, 81], [21, 87], [22, 23], [22, 37], [22, 43], [23, 88], [23, 91], [24, 25], [24, 79], [25, 66], [25, 71], [26, 40], [26, 64], [26, 76], [27, 61], [27, 71], [27, 75], [28, 45], [29, 50], [29, 83], [29, 89], [30, 94], [31, 54], [31, 88], [32, 41], [32, 62], [32, 97], [33, 51], [33, 69], [34, 95], [34, 99], [35, 39], [35, 95], [36, 40], [36, 74], [37, 54], [37, 92], [38, 44], [38, 85], [38, 95], [39, 60], [40, 99], [41, 46], [41, 91], [42, 65], [42, 92], [42, 104], [43, 65], [44, 47], [44, 66], [46, 86], [46, 102], [47, 68], [48, 52], [48, 65], [48, 90], [49, 77], [49, 86], [50, 63], [50, 87], [51, 56], [53, 72], [53, 103], [53, 104], [54, 55], [56, 82], [57, 59], [57, 70], [58, 64], [58, 90], [59, 86], [59, 97], [61, 79], [62, 80], [63, 73], [63, 75], [64, 93], [66, 96], [67, 96], [67, 97], [68, 71], [68, 73], [69, 89], [69, 98], [70, 94], [74, 82], [76, 78], [76, 84], [77, 98], [78, 83], [78, 90], [79, 103], [80, 93], [80, 101], [82, 100], [84, 89], [87, 98], [88, 102], [91, 101], [94, 103]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_104_19.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_104_19 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
