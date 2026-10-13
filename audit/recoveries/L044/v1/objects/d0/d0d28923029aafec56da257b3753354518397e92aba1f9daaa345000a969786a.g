Read("/Users/sasha/medusa/research/leemans/corpus106_F004_ends_enumeration_v1/q3_model.g");;Read("/Users/sasha/medusa/research/leemans/corpus106_F004_ends_enumeration_v1/q3_ends_records.g");;retained:=recordedMarks;;
    for file in ["/Users/sasha/medusa/research/leemans/reboot_20261013/F004_ends_distinct/replay01/prefix_records.g","/Users/sasha/medusa/research/leemans/reboot_20261013/F004_ends_distinct/replay01/ends_records.g"] do
      Read(file);;
      for r in [4..6] do
        if Length(freshMarks[r])<>Length(retained[r]) then Error("orbit count");fi;
        for t in retained[r] do
          if Number(freshMarks[r],u->RepresentativeAction(A,t,u,OnTuples)<>fail)<>1 then Error("orbit equality");fi;
        od;
      od;
    od;
    Print("EXACT_ORBIT_COMPARISON_COMPLETE\n");QUIT;
    