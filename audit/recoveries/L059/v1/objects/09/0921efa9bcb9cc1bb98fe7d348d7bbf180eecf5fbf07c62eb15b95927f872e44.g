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
D:=P177Graph("VT3_96_65",96,[1, 2, 4, 5, 10, 11, 12, 15, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 31, 35, 36, 37, 38, 40, 43, 45, 51, 52, 53, 55, 58, 59, 60, 61, 64, 67, 68, 72, 74, 77, 78, 79, 81, 82, 84, 89, 92],[[1, 32], [1, 50], [1, 87], [2, 88], [2, 91], [2, 95], [3, 27], [3, 61], [3, 82], [4, 6], [4, 16], [4, 70], [5, 17], [5, 57], [5, 85], [6, 51], [6, 74], [7, 36], [7, 61], [7, 92], [8, 12], [8, 24], [8, 38], [9, 31], [9, 64], [9, 79], [10, 66], [10, 69], [10, 94], [11, 30], [11, 41], [11, 63], [12, 56], [12, 83], [13, 51], [13, 58], [13, 81], [14, 20], [14, 77], [14, 84], [15, 22], [15, 39], [15, 48], [16, 43], [16, 55], [17, 27], [17, 58], [18, 42], [18, 44], [18, 85], [19, 30], [19, 46], [19, 66], [20, 39], [20, 50], [21, 39], [21, 47], [21, 73], [22, 28], [22, 89], [23, 46], [23, 65], [23, 95], [24, 76], [24, 94], [25, 32], [25, 54], [25, 62], [26, 83], [26, 85], [26, 93], [27, 70], [28, 42], [28, 63], [29, 93], [29, 94], [29, 96], [30, 55], [31, 41], [31, 65], [32, 79], [33, 81], [33, 84], [33, 89], [34, 37], [34, 45], [34, 77], [35, 62], [35, 65], [35, 80], [36, 76], [36, 91], [37, 44], [37, 96], [38, 49], [38, 54], [40, 66], [40, 90], [40, 91], [41, 60], [42, 78], [43, 47], [43, 86], [44, 81], [45, 73], [45, 76], [46, 74], [47, 61], [48, 55], [48, 59], [49, 67], [49, 92], [50, 82], [51, 80], [52, 54], [52, 69], [52, 71], [53, 71], [53, 75], [53, 90], [56, 60], [56, 78], [57, 64], [57, 68], [58, 75], [59, 69], [59, 87], [60, 86], [62, 84], [63, 68], [64, 88], [67, 80], [67, 86], [68, 90], [70, 72], [71, 89], [72, 87], [72, 93], [73, 78], [74, 96], [75, 92], [77, 95], [79, 83], [82, 88]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_96_65.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_96_65 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
