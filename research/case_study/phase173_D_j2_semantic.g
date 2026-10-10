# Independent comparison of terminal subgroup records, not their generating strings.
if not IsBound(BASELINE_ROOT) or not IsBound(REPLAY_ROOT) then
 Error("Set BASELINE_ROOT and REPLAY_ROOT to the two artifact directories");
fi;
recordChecks:=0;;
for bid in [1..146] do
 Read(Concatenation(BASELINE_ROOT,"/phase5_j2_checkpoints/b",String(bid),"_done.g"));
 before:=borelResult;
 Read(Concatenation(REPLAY_ROOT,"/phase5_j2_checkpoints/b",String(bid),"_done.g"));
 if before<>borelResult then Error("terminal subgroup record differs");fi;
 recordChecks:=recordChecks+1;
od;
Read(Concatenation(BASELINE_ROOT,"/phase5_j2_representatives.g"));;
beforeG:=G;;beforeWitnesses:=J2Representatives;;
Read(Concatenation(REPLAY_ROOT,"/phase5_j2_representatives.g"));;
if beforeG<>G or Length(beforeWitnesses)<>30 or Length(J2Representatives)<>30 then Error("named group or witness count differs");fi;
for i in [1..30] do
 if beforeWitnesses[i]<>J2Representatives[i] then Error("final subgroup record differs");fi;
 recordChecks:=recordChecks+1;
od;
Print("PHASE173_J2_EXACT_SUBGROUP_RECORDS_PASS ",recordChecks,"\n");
QUIT;
