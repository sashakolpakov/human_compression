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
D:=P177Graph("VT3_98_6",98,[1, 3, 4, 5, 8, 9, 10, 11, 12, 15, 18, 19, 22, 23, 27, 28, 29, 30, 32, 33, 34, 36, 39, 45, 47, 49, 50, 51, 52, 53, 56, 57, 60, 61, 64, 66, 68, 69, 71, 73, 74, 81, 86, 90, 91, 93, 94, 97, 98],[[1, 6], [1, 88], [1, 96], [2, 8], [2, 47], [2, 91], [3, 24], [3, 54], [3, 63], [4, 7], [4, 25], [4, 80], [5, 16], [5, 17], [5, 38], [6, 12], [6, 34], [7, 45], [7, 53], [8, 35], [8, 96], [9, 48], [9, 82], [9, 87], [10, 40], [10, 58], [10, 65], [11, 21], [11, 40], [11, 55], [12, 72], [12, 75], [13, 27], [13, 51], [13, 81], [14, 36], [14, 52], [14, 97], [15, 41], [15, 76], [15, 84], [16, 18], [16, 45], [17, 50], [17, 93], [18, 25], [18, 48], [19, 46], [19, 65], [19, 82], [20, 57], [20, 66], [20, 69], [21, 28], [21, 73], [22, 62], [22, 76], [22, 80], [23, 37], [23, 75], [23, 88], [24, 49], [24, 93], [25, 64], [26, 28], [26, 86], [26, 94], [27, 70], [27, 78], [28, 59], [29, 38], [29, 75], [29, 85], [30, 44], [30, 92], [30, 96], [31, 32], [31, 66], [31, 68], [32, 65], [32, 79], [33, 54], [33, 77], [33, 78], [34, 35], [34, 79], [35, 68], [36, 77], [36, 92], [37, 71], [37, 86], [38, 98], [39, 72], [39, 79], [39, 82], [40, 66], [41, 86], [41, 90], [42, 47], [42, 57], [42, 68], [43, 45], [43, 61], [43, 93], [44, 52], [44, 90], [46, 60], [46, 81], [47, 63], [48, 98], [49, 78], [49, 89], [50, 85], [50, 89], [51, 77], [51, 95], [52, 84], [53, 62], [53, 67], [54, 91], [55, 69], [55, 94], [56, 59], [56, 70], [56, 89], [57, 67], [58, 73], [58, 81], [59, 71], [60, 87], [60, 95], [61, 63], [61, 67], [62, 69], [64, 83], [64, 87], [70, 73], [71, 85], [72, 98], [74, 80], [74, 83], [74, 84], [76, 94], [83, 97], [88, 90], [91, 92], [95, 97]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_98_6.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_98_6 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
