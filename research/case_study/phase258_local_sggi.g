# All string generating triples, without assuming intersection property.
Need258:=function(b,s) if not b then Error(s);fi;end;
IP258:=function(G,rr)
 local ss,hs,i,j;
 ss:=Combinations([1..Length(rr)]);hs:=List(ss,s->Subgroup(G,rr{s}));
 for i in [1..Length(ss)] do for j in [1..Length(ss)] do
 if Intersection(hs[i],hs[j])<>hs[Position(ss,Intersection(ss[i],ss[j]))] then return false;fi;
 od;od;return true;
end;
Run258:=function()
 local pair,G,inv,a,b,c,rr,total,bad,types,t,markings,aut,left,orb,cs,H,z,x,y;
 for pair in [[SymmetricGroup(4),72,[[3,3,4],[3,4,3],[4,3,3]]],
              [AlternatingGroup(5),360,[[3,5,5],[5,3,5],[5,5,3]]]] do
 G:=pair[1];inv:=Filtered(Elements(G),x->Order(x)=2);total:=0;bad:=0;markings:=[];
 for a in inv do for c in inv do if a<>c and a*c=c*a then for b in inv do
 rr:=[a,b,c];if Length(Set(rr))=3 and Subgroup(G,rr)=G then
 total:=total+1;Add(markings,rr);if not IP258(G,rr) then bad:=bad+1;fi;
 Need258(Order(a*b)>2 and Order(b*c)>2,"irreducible local pair");
 fi;od;fi;od;od;
 Need258(total=pair[2] and bad=0,"complete sggi to C local bridge");
 types:=[];aut:=AutomorphismGroup(G);left:=ShallowCopy(markings);
 while Length(left)>0 do rr:=left[1];orb:=Orbit(aut,rr,OnTuples);
 Add(types,[Order(rr[1]*rr[2]),Order(rr[2]*rr[3]),Order(Product(rr))]);
 left:=Filtered(left,x->not x in orb);od;
 Sort(types);Need258(types=pair[3],"all-sggi automorphism orbits");
 Print("SGGI_LOCAL ",Size(G)," TOTAL ",total," BAD_IP ",bad," TYPES ",types,"\n");
 od;
 # Exact counterexample to literal source Lemma3.3 maximality.
 G:=AlternatingGroup(5);z:=(1,2)(3,4);H:=Stabilizer(G,5);cs:=Centralizer(G,z);
 Need258(Size(cs)=4 and Size(H)=12 and IsSubgroup(H,cs) and H<>G,"centralizer maximality counterexample");
 Print("SOURCE_L33_COUNTEREXAMPLE PSL5 CENTRALIZER4 CONTAINED_A4_12\n");
 # Omitting IP in an arbitrary group really enlarges the local class.
 G:=DihedralGroup(IsPermGroup,12);inv:=Filtered(Elements(G),x->Order(x)=2);rr:=fail;
 for a in inv do for b in inv do for c in inv do
 if Length(Set([a,b,c]))=3 and a*c=c*a and Subgroup(G,[a,b,c])=G
 and Order(a*b)>2 and Order(b*c)>2 and not IP258(G,[a,b,c]) then rr:=[a,b,c];break;fi;
 od;if rr<>fail then break;fi;od;if rr<>fail then break;fi;od;
 Need258(rr<>fail,"no blanket sggi implies C assertion");
 Print("DIHEDRAL_NON_C_SGGI_CONTROL TYPE ",List([1,2],i->Order(rr[i]*rr[i+1])),"\n");
 # A centre-free group with the common-centralizer condition can have five
 # distinct involutory generators if the string relations are omitted.
 G:=AlternatingGroup(5);
 rr:=[(1,2)(3,4),(1,3)(2,4),(1,2)(3,5),(1,3)(2,5),(1,4)(2,5)];
 Need258(Length(Set(rr))=5 and Group(rr)=G,"no-string five-generator control");
 inv:=Filtered(Elements(G),x->Order(x)=2);
 for a in inv do for b in inv do if a*b<>b*a then
 Need258(Size(Centralizer(G,Subgroup(G,[a,b])))<=2,"pair-centralizer premise in control");
 fi;od;od;
 Need258(rr[1]*rr[3]<>rr[3]*rr[1],"actual omitted string relation");
 Print("RANK_BOUND_NO_STRING_FALSE_WEAKENING_A5_FIVE_MARKERS_REJECTED\n");
 Print("PHASE258_LOCAL_PASS\n");
end;
Run258();QUIT;
