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
D:=P177Graph("VT3_98_12",98,[1, 3, 5, 6, 7, 8, 11, 12, 15, 16, 19, 20, 21, 27, 29, 31, 32, 33, 34, 35, 37, 39, 47, 50, 51, 52, 54, 55, 58, 59, 62, 65, 66, 68, 69, 72, 74, 77, 79, 80, 81, 82, 83, 85, 88, 92, 95, 96, 98],[[1, 10], [1, 45], [1, 61], [2, 12], [2, 54], [2, 68], [3, 4], [3, 25], [3, 87], [4, 55], [4, 92], [5, 57], [5, 86], [5, 94], [6, 36], [6, 76], [6, 87], [7, 23], [7, 24], [7, 90], [8, 44], [8, 56], [8, 91], [9, 69], [9, 80], [9, 85], [10, 34], [10, 47], [11, 45], [11, 73], [11, 86], [12, 36], [12, 93], [13, 32], [13, 72], [13, 85], [14, 19], [14, 51], [14, 65], [15, 38], [15, 78], [15, 89], [16, 42], [16, 71], [16, 78], [17, 32], [17, 55], [17, 59], [18, 31], [18, 52], [18, 81], [19, 41], [19, 46], [20, 60], [20, 89], [20, 94], [21, 43], [21, 44], [21, 70], [22, 47], [22, 58], [22, 96], [23, 77], [23, 82], [24, 88], [24, 96], [25, 52], [25, 59], [26, 66], [26, 72], [26, 80], [27, 45], [27, 48], [27, 94], [28, 68], [28, 74], [28, 80], [29, 46], [29, 63], [29, 97], [30, 59], [30, 72], [30, 81], [31, 70], [31, 75], [32, 71], [33, 73], [33, 76], [33, 93], [34, 48], [34, 63], [35, 63], [35, 67], [35, 75], [36, 98], [37, 43], [37, 87], [37, 91], [38, 65], [38, 79], [39, 44], [39, 49], [39, 90], [40, 69], [40, 82], [40, 88], [41, 54], [41, 74], [42, 82], [42, 85], [43, 52], [46, 83], [47, 75], [48, 83], [49, 77], [49, 79], [50, 64], [50, 84], [50, 93], [51, 53], [51, 56], [53, 54], [53, 98], [55, 57], [56, 79], [57, 62], [58, 70], [58, 90], [60, 65], [60, 83], [61, 95], [61, 96], [62, 71], [62, 89], [64, 88], [64, 95], [66, 67], [66, 97], [67, 81], [68, 84], [69, 84], [73, 95], [74, 97], [76, 92], [77, 78], [86, 92], [91, 98]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_98_12.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_98_12 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
