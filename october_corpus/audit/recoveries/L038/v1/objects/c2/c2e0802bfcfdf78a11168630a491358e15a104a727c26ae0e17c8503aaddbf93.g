Read("a12_witnesses.g");
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L071_A12_full_IP01/records.g");
for j in [1,2] do
 r:=j+2;
 if recordedMarks[r][a12RecordPositions[j]]<>a12RecordIndices[j] or recordedInvolutions{a12RecordIndices[j]}<>a12Tuples[j] then Error("retained record differs");fi;
od;
Print("EXACT_RETAINED_RECORDS_PASS\n");QUIT;
