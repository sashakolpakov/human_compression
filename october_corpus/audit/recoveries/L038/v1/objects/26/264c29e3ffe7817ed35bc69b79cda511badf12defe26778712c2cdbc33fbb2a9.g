# Source diagrams, with vertices numbered in the accompanying working notes.
AddEdge:=function(s,i,a,b) s[i+1]:=s[i+1]*(a,b);end;
HighOdd:=function(r,k)
 local s,labels,j,off,L;
 s:=List([1..r],i->()); labels:=[[0],[1],[0,2]];
 for j in [1..2*k] do Append(labels,[[1],[0]]);od;
 Add(labels,[1]); for j in [2..r-1] do Add(labels,[j]);od;
 for j in [1..Length(labels)] do for L in labels[j] do AddEdge(s,L,j,j+1);od;od;
 off:=Length(labels)+1;
 for j in [3..r-1] do AddEdge(s,j,off+j-2,off+j-1);od;
 AddEdge(s,r-3,off-1,off+r-3);AddEdge(s,r-3,off,off+r-2);
 return s;
end;
HighEven:=function(r,k)
 local s,labels,j,off,L;
 s:=List([1..r],i->()); labels:=[[0],[1],[0,2]];
 for j in [1..2*k] do Append(labels,[[1],[0]]);od;
 Add(labels,[1]); for j in [2..r-1] do Add(labels,[j]);od;Add(labels,[r-2]);
 for j in [1..Length(labels)] do for L in labels[j] do AddEdge(s,L,j,j+1);od;od;
 off:=Length(labels)+1;
 for j in [3..r-1] do AddEdge(s,j,off+j-2,off+j-1);od;
 AddEdge(s,r-2,off+r-2,off+r-1);
 for j in [0..3] do AddEdge(s,r-4,off-j,off+r-1-j);od;
 return s;
end;
