# Compare actual subgroup records, not their chosen printed generating lists.
# Set OLD_DIR and NEW_DIR to directories ending in / before reading this file.
if not IsBound(OLD_DIR) or not IsBound(NEW_DIR) then
 Error("Set OLD_DIR and NEW_DIR before reading the comparator");
fi;
for i in [1..146] do
 Read(Concatenation(OLD_DIR,"phase5_j2_checkpoints/b",String(i),"_done.g"));;
 previous:=borelResult;;
 Read(Concatenation(NEW_DIR,"phase5_j2_checkpoints/b",String(i),"_done.g"));;
 if previous<>borelResult then Error("Subgroup record differs at ",i);fi;
od;
Read(Concatenation(OLD_DIR,"phase5_j2_representatives.g"));;
previous:=J2Representatives;;
Read(Concatenation(NEW_DIR,"phase5_j2_representatives.g"));;
if previous<>J2Representatives then Error("Final actual subgroup families differ");fi;
Print("ACTUAL_SUBGROUP_RECORDS_EQUAL 146 FINAL_REPRESENTATIVES_EQUAL 30\n");
QUIT;
