# Unfrozen exact finite census for the fixed L023 v2 Table 1.
# Enumerate every nonscalar solution to equations (1) and (3):
# In even characteristic I is the sole further solution; I*J has order 2
# and never contributes to the primitive-order columns.
# odd q, one free PGL(2,q) orbit; even q, one fixed point and trace-zero parameter.
SetInfoLevel(InfoWarning,0);;
SizeScreen([200,1000]);;
PrintTo("polynomial_table_rows.json","[\n");;
qs := [3,4,5,7,8,9,11,13,16,17,19,23];;
EncodeElt := function(x,z) if IsZero(x) then return -1; fi; return LogFFE(x,z); end;;
RunQ := function(q)
 local tm,K,ee,base,one,zero,Q,z,J,seed,a,b,c,R,Rq,found,sols,g,d,det,counts,n,o,t,P,pts,rr,seen,code,exception;
 tm:=Runtime(); Q:=q^3; K:=GF(Q); ee:=Elements(K); z:=Z(Q); one:=One(K);zero:=Zero(K);
 base:=Filtered(ee,x->x^q=x); J:=[[zero,one],[-one,zero]];
 sols:=[];
 if IsOddInt(q) then
  found:=false;
  for a in ee do
   for b in ee do
    if b=zero then continue;fi;
    c:=(-one-a*a)/b;R:=[[a,b],[c,-a]];Rq:=List(R,row->List(row,x->x^q));
    if List(R,row->List(row,x->x^(q*q)))=R*Rq then seed:=R;found:=true;break;fi;
   od;
   if found then break;fi;
  od;
  if not found then Error("No seed");fi;
  for a in base do if a=zero then continue;fi; for b in base do
   g:=[[a,b],[zero,one]];Add(sols,seed^g);
  od;od;
  for a in base do for d in base do for b in base do
   if a*d=b then continue;fi;
   g:=[[a,b],[one,d]];Add(sols,seed^g);
  od;od;od;
 else
  pts:=[[[one,zero],[zero,one]]];
  # infinity followed by all finite fixed points; conjugation by inverse g
  # carries infinity to x when g=[[x,1],[1,0]].
  for a in base do Add(pts,[[a,one],[one,zero]]);od;
  for t in ee do
   if t=zero or t+t^q+t^(q*q)<>zero then continue;fi;
   R:=[[one,t],[zero,one]];
   for g in pts do Add(sols,g*R*g^-1);od;
  od;
  seed:=sols[1];
 fi;
 n:=Length(sols);if Length(Set(sols))<>n then Error("Duplicate matrix");fi;
 if IsOddInt(q) and n<>q*(q*q-1) then Error("Odd orbit size");fi;
 if IsEvenInt(q) and n<>(q+1)*(q*q-1) then Error("Even size");fi;
 counts:=[0,0]; exception:=[0,0];
 for R in sols do
  if DeterminantMat(R)<>one or TraceMat(R)<>zero then Error("Eq1");fi;
  if List(R,row->List(row,x->x^(q*q)))<>R*List(R,row->List(row,x->x^q)) then Error("Eq3");fi;
  o:=Order(R*J);
  if o=Q-1 then counts[1]:=counts[1]+1;if IsZero(R[1][2]*R[2][1]) then exception[1]:=exception[1]+1;fi;fi;
  if o=Q+1 then counts[2]:=counts[2]+1;if IsZero(R[1][2]*R[2][1]) then exception[2]:=exception[2]+1;fi;fi;
 od;
 code:=List(seed,row->List(row,x->EncodeElt(x,z)));
 if q<>3 then AppendTo("polynomial_table_rows.json",",\n");fi;
 AppendTo("polynomial_table_rows.json","{\"q\":",q,",\"nonscalar_total\":",n,",\"primitive_counts\":",counts,",\"bc_zero_counts\":",exception,",\"seed_log_encoding\":",code,"}");
 Print("ROW q=",q," total=",n," minus=",counts[1]," plus=",counts[2]," bc0=",exception," seed=",code," ms=",Runtime()-tm,"\n");
end;;
for q in qs do RunQ(q);od;
AppendTo("polynomial_table_rows.json","\n]\n");
QUIT;
