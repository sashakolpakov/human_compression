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
D:=P177Graph("VT3_96_31",96,[1, 2, 3, 4, 8, 13, 17, 20, 21, 23, 24, 25, 28, 29, 31, 32, 34, 36, 40, 41, 43, 45, 48, 51, 52, 54, 55, 56, 61, 62, 63, 64, 65, 67, 70, 72, 75, 76, 77, 78, 81, 85, 88, 89, 90, 91, 94, 95],[[1, 5], [1, 30], [1, 49], [2, 26], [2, 33], [2, 86], [3, 42], [3, 80], [3, 96], [4, 30], [4, 84], [4, 92], [5, 20], [5, 23], [6, 24], [6, 51], [6, 94], [7, 13], [7, 25], [7, 72], [8, 35], [8, 44], [8, 69], [9, 62], [9, 63], [9, 70], [10, 64], [10, 65], [10, 88], [11, 17], [11, 34], [11, 41], [12, 13], [12, 81], [12, 94], [13, 79], [14, 25], [14, 43], [14, 94], [15, 43], [15, 51], [15, 56], [16, 31], [16, 55], [16, 89], [17, 39], [17, 79], [18, 20], [18, 52], [18, 90], [19, 64], [19, 70], [19, 78], [20, 47], [21, 33], [21, 53], [21, 68], [22, 70], [22, 77], [22, 95], [23, 46], [23, 84], [24, 44], [24, 83], [25, 73], [26, 56], [26, 89], [27, 45], [27, 54], [27, 65], [28, 59], [28, 60], [28, 73], [29, 46], [29, 50], [29, 80], [30, 61], [31, 42], [31, 60], [32, 50], [32, 69], [32, 83], [33, 62], [34, 47], [34, 53], [35, 36], [35, 85], [36, 57], [36, 87], [37, 40], [37, 63], [37, 64], [38, 61], [38, 72], [38, 91], [39, 81], [39, 85], [40, 57], [40, 58], [41, 58], [41, 68], [42, 54], [43, 59], [44, 81], [45, 60], [45, 74], [46, 90], [47, 76], [48, 69], [48, 80], [48, 87], [49, 72], [49, 76], [50, 67], [51, 82], [52, 53], [52, 86], [54, 87], [55, 86], [55, 96], [56, 66], [57, 65], [58, 85], [59, 89], [61, 71], [62, 66], [63, 68], [66, 77], [67, 84], [67, 93], [71, 78], [71, 88], [73, 91], [74, 88], [74, 91], [75, 82], [75, 83], [75, 93], [76, 79], [77, 82], [78, 92], [90, 96], [92, 95], [93, 95]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_96_31.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_96_31 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
