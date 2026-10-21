# Paths are relative to the standalone packet root.
Read("programs/finite_tools.g");;
params:=[ ["M12",144,4,95040,[6,3,6]], ["J2",100,2,604800,[6,3,6]],
 ["HS",100,4,44352000,[8,3,8]], ["He",2058,2,4030387200,[6,6,6]],
 ["Suz",1782,2,448345497600,[6,5,6]], ["J3",6156,0,50232960,[5,9,5]] ];;
r:=[];;t:=();;
for row in params do
 Read(Concatenation("witnesses/",row[1],"_rank4_witness.g"));;
 r:=Rank4Witness;t:=OuterWitness;g:=Group(StandardGenerators);h:=Group(r);;
 if row[1]="J3" then
  c:=StandardGenerators[1];d:=StandardGenerators[2];
  rels:=[c^2,d^3,(c*d)^24,Comm(c,d)^9,(c*d*(c*d*c*d^-1)^2)^4,
   (c*d*c*d*c*d^-1*(c*d*c*d*c*d^-1*c*d^-1)^2)^2,
   Comm(c,(d*c)^4*(d^-1*c)^2*d)^2,Comm(c,d*(c*d^-1)^2*(c*d)^4)^2];
  Need(ForAll(rels,x->x=()),"all eight literal ATLAS J3:2 defining relators");
 else Need(g=PrimitiveGroup(row[2],row[3]),"exact named catalogue representation");fi;;
 Need(Size(h)=row[4] and Size(g)=2*row[4],"exact group orders");;
 Need(DerivedSubgroup(g)=h and IsSimpleGroup(h),"simple socle");;
 Need(Size(Centralizer(g,h))=1,"faithful conjugation into Aut(H)");;
 Need(Length(Set(r))=4 and ForAll(r,x->Order(x)=2),"four distinct involutions");;
 Need(ForAll(Combinations([1..4],2),z->z[2]-z[1]=1 or Order(r[z[1]]*r[z[2]])=2),"string commuting relations");;
 Need(List([1..3],i->Order(r[i]*r[i+1]))=row[5],"exact rank-four type");;
 Need(Order(t)=2 and not t in h and Group(Concatenation(r,[t]))=g,"noninner involutory outer action");;
 Need(ForAll([1..4],i->r[i]^t=r[5-i]),"exact duality reversal");;
 Print(row[1]," simple rank4 order=",Size(h)," type=",row[5]," IP=",IPCheck(r)," outer=true PASS\n");;
 CheckTriple(Concatenation(row[1],".2-polytope"),[r[1],t,r[3]],Size(g));;
 CheckTriple(Concatenation(row[1],".2-hypertope"),[r[1],r[2],t],Size(g));;
od;
Read("witnesses/m22_witness.g");;r:=M22Witness;;g:=CheckTriple("M22.2-polytope",r,887040);;
h:=DerivedSubgroup(g);;Need(Size(h)=443520 and IsSimpleGroup(h),"M22 simple socle");;
Need(IsomorphismGroups(h,MathieuGroup(22))<>fail,"M22 named identification");;
Need(Size(Centralizer(g,h))=1,"M22 faithful automorphism action");;
CheckTriple("M22.2-halving",[r[1],r[2],r[2]^r[3]],887040);;
Read("witnesses/mcl_witness.g");;r:=McLWitness;;g:=CheckTriple("McL.2-polytope",r,1796256000);;
Need(g=PrimitiveGroup(275,2),"McL exact named catalogue representation");;
h:=DerivedSubgroup(g);;Need(Size(h)=898128000 and IsSimpleGroup(h),"McL simple socle");;
Need(Size(Centralizer(g,h))=1 and not r[1] in h,"McL faithful outer action");;
CheckTriple("McL.2-halving",[r[1],r[2],r[2]^r[3]],1796256000);;
Print("COMPLETE 8 sporadic full outer extensions; 6 rank-four IP certificates; 16 rank-three IP and flag certificates PASS\n");;
QUIT;
