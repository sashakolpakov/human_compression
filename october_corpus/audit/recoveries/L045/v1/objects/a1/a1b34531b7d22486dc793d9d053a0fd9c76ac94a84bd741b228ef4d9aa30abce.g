# PacketDirectory, WitnessDirectory and Control are set by the Python driver.
SizeScreen([240,40]);;
Need:=function(b,message)
    if not b then Print("REJECT ",message,"\n");FORCE_QUIT_GAP(1);fi;
end;;
seen:=[];;
CheckPair:=function(name,h,x,t,expectedOrder,orders)
    local actual,u,v;
    if Control="identity" then t:=();fi;
    if Control="wrong_ambient" then h:=SymmetricGroup(LargestMovedPoint(h));fi;
    if Control="wrong_order" then expectedOrder:=expectedOrder+1;fi;
    Need(Order(t)=2,Concatenation(name,": nonidentity involution"));
    Need(x in h and t in h,Concatenation(name,": actual group membership"));
    Need(Size(h)=expectedOrder,Concatenation(name,": named group order"));
    Need(Size(Group(x,t))=Size(h),Concatenation(name,": full generation"));
    u:=x*t*x^2*t*x^3*t;v:=x^-1*t*x^-2*t*x^-3*t;
    actual:=[Order(x),Order(x^-1*t),Order(u),Order(v)];
    if Control="equal_word_orders" then actual[4]:=actual[3];fi;
    Need(actual=orders,Concatenation(name,": exact word orders"));
    Need(actual[1]>2 and actual[2]>2 and actual[3]<>actual[4],Concatenation(name,": chirality criterion"));
    Add(seen,name);
    Print("PASS ",name," ",expectedOrder," ",actual[1]," ",actual[2]," ",actual[3]," ",actual[4],"\n");
end;;

Read(Concatenation(PacketDirectory,"/mathieu_pairs.g"));;
for row in MathieuPairs do
    x:=row.x;;t:=x*row.y;;g:=Group(x,t);;m:=MathieuGroup(row.n);;
    if row.n=23 then
        Need(x in m and t in m,"M23 literal named membership");
        CheckPair("M23",m,x,t,10200960,[11,15,14,6]);
    else
        Need(row.n=24,"only source M23 and M24 pairs");
        iso:=IsomorphismGroups(g,m);;
        Need(iso<>fail,"M24 named isomorphism exists");
        Need(IsBijective(iso) and Image(iso,g)=m,"M24 actual bijective map onto named group");
        CheckPair("M24",g,x,t,244823040,[23,15,15,12]);
    fi;
od;

Read(Concatenation(PacketDirectory,"/rank4_pairs.g"));;
params:=[ ["M12",144,4,95040], ["J2",100,2,604800],
 ["HS",100,4,44352000], ["He",2058,2,4030387200],
 ["Suz",1782,2,448345497600], ["J3",6156,0,50232960] ];;
r:=[];;
for row in SporadicPairs do
    p:=First(params,q->q[1]=row.name);;Need(p<>fail,"known acquired marking");
    Read(Concatenation(WitnessDirectory,"/",row.name,"_rank4_witness.g"));;
    r:=Rank4Witness;;g:=Group(StandardGenerators);;h:=Group(r);;
    if row.name="J3" then
        c:=StandardGenerators[1];;d:=StandardGenerators[2];;
        rels:=[c^2,d^3,(c*d)^24,Comm(c,d)^9,(c*d*(c*d*c*d^-1)^2)^4,
          (c*d*c*d*c*d^-1*(c*d*c*d*c*d^-1*c*d^-1)^2)^2,
          Comm(c,(d*c)^4*(d^-1*c)^2*d)^2,Comm(c,d*(c*d^-1)^2*(c*d)^4)^2];;
        Need(ForAll(rels,z->z=()),"J3 exact retained defining relators");
    else
        Need(g=PrimitiveGroup(p[2],p[3]),"literal named extension");
    fi;
    Need(Size(g)=2*p[4] and Size(h)=p[4],"acquired exact extension and socle orders");
    Need(h=DerivedSubgroup(g) and IsSimpleGroup(h),"actual simple socle");
    Need(Length(row.word)=32 and ForAll(row.word,i->i in [1..4]),"literal word interface");
    x:=Product(List(row.word,i->r[i]));;t:=r[1];;
    CheckPair(row.name,h,x,t,row.order,row.orders);
od;

Read(Concatenation(PacketDirectory,"/small_pairs.g"));;
for row in SmallSporadicPairs do
    if row.name="M11" then h:=MathieuGroup(11);
    elif row.name="M22" then h:=MathieuGroup(22);
    elif row.name="McL" then h:=DerivedSubgroup(PrimitiveGroup(275,2));
    elif row.name="J1" then h:=PrimitiveGroup(266,1);
    else Need(false,"unknown named group");fi;
    CheckPair(row.name,h,row.x,row.t,row.order,row.orders);
od;
Need(Length(seen)=12 and Set(seen)=["HS","He","J1","J2","J3","M11","M12","M22","M23","M24","McL","Suz"],"exact twelve groups once each");
Print("TERMINAL_PASS 12 sporadic chirality certificates\n");
QUIT;
