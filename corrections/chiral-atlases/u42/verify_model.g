# The standard projective symplectic constructor is an attributed input.
# Checked on GAP4.15.1; an alternative labelling requires an explicit transport.
G:=PSp(4,3);;
expected:=[[6, 17, 37, 27, 5, 1, 7, 26, 19, 36, 35, 18, 28, 14, 24, 34, 2, 12, 9, 20, 40, 30, 32, 15, 25, 8, 4, 13, 29, 22, 39, 23, 33, 16, 11, 10, 3, 38, 31, 21], [17, 34, 30, 9, 20, 14, 2, 27, 6, 37, 12, 24, 40, 25, 13, 39, 5, 26, 35, 16, 21, 3, 10, 33, 31, 29, 32, 8, 18, 1, 19, 36, 28, 7, 38, 11, 23, 4, 22, 15]];;
if G<>Group(List(expected,PermList)) or Size(G)<>25920 then
 Error("literal PSp(4,3) subgroup differs from this edition");
fi;
Print("PASS_LITERAL_PSP4_3_MODEL\n");QUIT;
