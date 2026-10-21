V:=[1..7];; inv:=Filtered(Elements(SymmetricGroup(7)),g->Order(g)=2);;
left:=Filtered(inv,g->1^g<>1 and 7^g=7);; middle:=Filtered(inv,g->1^g=1 and 7^g=7);; right:=Filtered(inv,g->1^g=1 and 7^g<>7);;
pairs:=0;;triples:=0;;transitive:=0;;orbcounts:=[];;
for aa in left do for cc in right do
 if aa*cc<>cc*aa then continue;fi;
 pairs:=pairs+1;;oo:=Orbits(Group(aa,cc),V);;if Length(oo)<4 then Error("four orbit bound");fi;
 for bb in middle do
  if Length(Set([aa,bb,cc]))<>3 then continue;fi;
  triples:=triples+1;; if IsTransitive(Group(aa,bb,cc),V)then transitive:=transitive+1;fi;
 od;
od;od;
Print("EXACT_S7_ANCHORS ",Length(inv)," ",Length(left)," ",Length(middle)," ",Length(right)," ",pairs," ",triples," ",transitive,"\n");
if [Length(inv),Length(left),Length(middle),Length(right),pairs,triples,transitive]<>[231,50,25,50,200,5000,0]then Error("independent count mismatch");fi;
Print("COMPLETE_S7_ANCHOR_CONTROL\n");QUIT;
