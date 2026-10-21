Read("programs/finite_tools.g");;
Need(IsBound(ExternalRoot),"external Atlas data directory required");;
Read(Concatenation(ExternalRoot,"/ONd2G1-p245520B0.g1"));;
Read(Concatenation(ExternalRoot,"/ONd2G1-p245520B0.g2"));;
Read("witnesses/ON_compact.g");;
t:=a11;d:=a21;;
Need(Order(t)=2 and Order(d)=4 and Order(t*d)=22,"Atlas standard-generator orders");;
y:=t*d^2*t*d*t;;z:=(y*(d^2*(d^2)^y)^7)^2;;Need(Comm(d,z)=(),"Atlas ON.2 standard-generator checker");;
EvalWord:=function(w) local x,i;x:=();for i in w do Need(i in [-2,-1,1,2],"word alphabet");if i>0 then x:=x*[t,d][i];else x:=x*([t,d][-i]^-1);fi;od;return x;end;;
centrals:=[];;
for hw in ONBraySeedWords do
 hh:=EvalWord(hw);x:=t*t^hh;k:=Order(x);Need(k mod 2=1,"odd Bray commutator");z:=hh*x^((k-1)/2);Need(Comm(t,z)=(),"exact centralization");Add(centrals,z);
od;
a:=EvalWord(ONaWord);b:=Product(centrals{ONbFactors})^ONbPower;;
Need(Order(a)=2 and Order(b)=2 and Comm(t,b)=(),"saved marking involutions");;
Need([Order(t*a),Order(t*b),Order(a*b)]=[8,2,11],"exact original type");;
g:=CheckTriple("ON.2-polytope",[t,a,b],921631011840);;
# Every saved word is visibly in <t,d>; these two memberships prove the reverse inclusion.
Need(t in g and d in g,"equality with actual Atlas standard group");;
s:=[t,a,a^b];;
Need(GeneratorsOfGroup(g)=[t,a,b] and b=(s[2]*s[3])^5*s[2],"all original generators recovered by literal words");;
Need(Length(Set(s))=3 and ForAll(s,x->Order(x)=2 and x in g),"halved involutions inside original group");;
Need([Order(s[1]*s[2]),Order(s[1]*s[3]),Order(s[2]*s[3])]=[8,8,11],"triangle product orders");;
Print("ON.2-halving order=",Size(g)," pair_orders=[8,8,11] IP=",IPCheckIn(s,g)," panels=",FT3Check(s)," flag_anchors=3 explicit_generation_words PASS\n");;
h:=Group(a,b,a^t);;Need(Size(h)=460815505920 and IsNormal(g,h) and IsSimpleGroup(h),"normal simple index-two socle");;
Need(not t in h and Size(Centralizer(g,h))=1,"faithful noninner outer action");;
Print("COMPLETE ON direct8-11 marking; both64IP and all6flag-product tests; named simple socle PASS\n");;
QUIT;
