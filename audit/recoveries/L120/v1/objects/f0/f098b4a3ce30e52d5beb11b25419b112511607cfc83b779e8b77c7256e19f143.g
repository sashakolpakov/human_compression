# Exact positive validation; no enumeration or inherited prefix state.
IntervalStringIP := function(t)
 local r, a, b, len, H, checks;
 if not IsList(t) or Length(t)=0 then return rec(ok:=false,checks:=0);fi;
 r:=Length(t);checks:=0;
 if not ForAll(t,x->IsPerm(x) and Order(x)=2) then return rec(ok:=false,checks:=0);fi;
 if Length(Set(t))<>r then return rec(ok:=false,checks:=0);fi;
 for a in [1..r] do
  for b in [a+2..r] do
   if Comm(t[a],t[b])<>() then return rec(ok:=false,checks:=0);fi;
  od;
 od;
 H:=List([1..r],a->[]);
 for len in [1..r] do
  for a in [1..r-len+1] do
   b:=a+len-1;H[a][b]:=Group(t{[a..b]});
   if len>=3 then
    checks:=checks+1;
    if Intersection(H[a][b-1],H[a+1][b])<>H[a+1][b-1] then
     return rec(ok:=false,checks:=checks);
    fi;
   fi;
  od;
 od;
 return rec(ok:=true,checks:=checks);
end;;
