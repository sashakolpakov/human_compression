# Coordinates i^+=i, i^-=t+i. These are the two displayed signed caps.
Cap:=function(t,e)
 local s,f;
 s:=List([1..t-1],i->(i,i+1)*(t+i,t+i+1));
 if e=2 then
  f:=(t-1,2*t-1)*(t,2*t);s[t-3]:=s[t-3]*f;
 elif e=4 then
  f:=Product([t-3..t],i->(i,t+i));
  s[t-5]:=s[t-5]*f;s[t-3]:=s[t-3]*s[t-1];Remove(s,t-1);
 else Error("two or four flips required");fi;
 return s;
end;
