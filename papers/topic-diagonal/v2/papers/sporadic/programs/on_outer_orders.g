# The character table is retained named data, not reconstructed from the permutation model.
Read("programs/finite_tools.g");;
tab:=CharacterTable("ON.2");;
Need(tab<>fail and Size(tab)=921631011840,"named ON.2 character table");;
linear:=Filtered(Irr(tab),chi->chi[1]=1);;
Need(Length(linear)=2,"unique index-two character");;
eps:=First(linear,chi->not ForAll(chi,x->x=1));;
Need(ForAll(eps,x->x in [-1,1]),"real sign character");;
orders:=OrdersClassRepresentatives(tab);;
outside:=Filtered([1..Length(orders)],i->eps[i]=-1);;
outerorders:=Set(orders{outside});;
Need(outerorders=[2,6,8,10,14,22,24,30,38,56] and not 4 in outerorders,"no outer order four");;
Print("ON.2 character-table provenance ",InfoText(tab),"\n");;
Print("ON.2 outer orders ",outerorders," NO_OUTER_ORDER4 PASS\n");;
QUIT;
