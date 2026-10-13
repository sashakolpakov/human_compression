# Four exact source families. No search over degree occurs in the certificate.
AddEdge:=function(s,i,a,b) s[i+1]:=s[i+1]*(a,b);end;


LowSix:=function(n)
 local s,m,j,a,b,c,d,e,f,g,h;
 s:=List([1..6],i->());m:=n-6;
 for j in [1..m-5] do AddEdge(s,(j-1) mod 2,j,j+1);od;
 for j in [2..5] do AddEdge(s,j,m-5+j-1,m-5+j);od;
 a:=m-1;b:=m;c:=m+1;d:=m+2;e:=m+3;f:=m+4;g:=m+5;h:=m+6;
 AddEdge(s,3,a,c);AddEdge(s,3,b,d);AddEdge(s,5,c,d);AddEdge(s,4,d,e);
 AddEdge(s,2,c,f);AddEdge(s,4,c,f);AddEdge(s,2,d,g);AddEdge(s,2,e,h);AddEdge(s,3,e,h);AddEdge(s,5,e,h);
 AddEdge(s,5,f,g);AddEdge(s,4,g,h);
 return s;
end;

EvenFive2:=function(n)
 local s,j;
 s:=List([1..5],i->());s[1]:=(1,2)*(3,4);s[2]:=(2,3)*(4,5);s[3]:=(3,4)*(5,6);
 for j in [6..n-1] do AddEdge(s,3+(j mod 2),j,j+1);od;
 return s;
end;

EvenFive0:=function(n)
 local s,j;
 s:=List([1..5],i->());s[1]:=(3,5)*(4,6);s[2]:=(2,3)*(6,7);s[3]:=(1,2)*(3,4)*(5,6)*(7,8);
 for j in [8..n-1] do AddEdge(s,3+(j mod 2),j,j+1);od;
 return s;
end;

EvenFour0:=function(n)
 local s,j;
 # l,n,m,i,b,j,k,f =1..8; g,a,d,h,c,e=9..14. Tail extends f.
 s:=List([1..4],i->());
 s[1]:=(1,2)*(9,12)*(10,13)*(11,14);
 s[2]:=(2,3)*(4,12)*(5,13)*(11,14);
 s[3]:=(3,4)*(5,6)*(7,8)*(10,11)*(13,14);
 s[4]:=(4,5)*(6,7)*(9,10)*(12,13)*(11,14);
 AddEdge(s,3,8,15);
 for j in [15..n-1] do AddEdge(s,2+((j-15) mod 2),j,j+1);od;
 return s;
end;
