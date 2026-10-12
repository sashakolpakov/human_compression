Read("profile_match_v2.g");;
Read("intersection_profiles.g");;
# Partition only the supplied HS roster; no geometric classification census.
Read("archive_data/inputs.g");;SizeScreen([1000000,1000000]);;
G:=Group(Concatenation(L096Inputs[1].parabolic_generators));;
AutG:=AutomorphismGroup(G);;
Print("AUT_ORDER|",Size(AutG),"\n");
OnSub:=function(H,a)return Image(a,H);end;;
class_inputs:=[1, 2, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 20, 22, 24, 26, 28, 29, 30, 31];;class_sizes:=[1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1];;
L096Classes:=List(class_inputs,r->List(L096Inputs[r].parabolic_generators,Group));;
caches:=List(class_inputs,r->rec());;
for row in [32..Length(L096Inputs)] do
 input:=L096Inputs[row];SG:=Group(Concatenation(input.parabolic_generators));
 if SG<>G then Error("literal common ambient changed");fi;
 H:=List(input.parabolic_generators,Group);hit:=fail;
 for j in [1..Length(L096Classes)] do
  if Length(H)=Length(L096Classes[j]) and L096ProfileEquivalent(AutG,H,L096Profiles[row],L096Classes[j],L096Profiles[class_inputs[j]],caches[j]) then hit:=j;break;fi;
 od;
 if hit=fail then Add(L096Classes,H);Add(class_inputs,row);Add(class_sizes,0);Add(caches,rec());hit:=Length(L096Classes);fi;
 class_sizes[hit]:=class_sizes[hit]+1;
 Print("MATCH|",input.member,"|",input.active,"|",input.construction,"|",hit,"|",class_inputs[hit],"\n");
od;
Print("CLASS_INPUT_ROWS|",class_inputs,"\n");
Print("CLASS_SIZES|",class_sizes,"\n");
PrintTo("class_inputs.g","L096ClassInputRows:=",class_inputs,";;\n");
Print("PASS_HS_WHOLE_FAMILY_PARTITION\n");QUIT;
