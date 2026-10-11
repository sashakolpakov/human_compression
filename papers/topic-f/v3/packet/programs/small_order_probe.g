# Exploratory exact scan. The accepted final boundary has not yet been fixed.
Print("GAP ",GAPInfo.Version,"\n");
for sz in [54,162,1250] do
  found:=0; pairs:=0; cnt:=NrSmallGroups(sz);
  Print("ORDER ",sz," catalog ",cnt,"\n");
  for id in [1..cnt] do
    g:=SmallGroup(sz,id);
    xs:=Filtered(List(ConjugacyClasses(g),Representative),x->Order(x)>2 and IsOddInt(Order(x)));
    ts:=Filtered(Elements(g),t->Order(t)=2);
    for x in xs do
      c:=Centralizer(g,x);
      reps:=List(Orbits(c,ts,OnPoints),o->o[1]);
      for t in reps do
        y:=x^-1*t;
        if Order(y)>2 and Size(Intersection(Group(x),Group(y)))=1 and Order(x)*Order(y)<sz and Size(Group(x,t))=sz then
          pairs:=pairs+1;
          h:=GroupHomomorphismByImages(g,g,[x,y],[x^-1,y^-1]);
          if h=fail then Print("CHIRAL ",sz," ",id," ",[Order(x),Order(y)],"\n");found:=found+1;fi;
          if sz=1250 and Order(x)=5 and Order(y)=50 then Print("REMARK TYPE FOUND\n");fi;
        fi;
      od;
    od;
  od;
  Print("RESULT ",sz," non-tight pair orbits ",pairs," chiral ",found,"\n");
od;
QUIT_GAP(0);
