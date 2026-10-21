Read("../../../topic_B_L044_small_maxima_v1/author_validation/A10/records.g");
for idx in [1..Length(recordedMarks[5])] do
Print("MARKS ",idx," ",List(recordedInvolutions{recordedMarks[5][idx]},p->List([1..10],x->x^p))," END\n");
od;Print("COMPLETE ",Length(recordedMarks[5]),"\n");QUIT;
