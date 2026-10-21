SizeScreen([1000000,24]);;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/compare_markings.g");;
Read("/Users/sasha/medusa/research/leemans/algebra/coxeter_quotients/small_square_distinct_work/fresh01/census/records.g");;
fresh:=hyperbolic_records;;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L033_work/hyperbolic_recovery_work/3535_composed_accepted01/records.g");;

positive:=Filtered(fresh,r->r.checks.ok);;
if OrderedMarkingBijection(positive,hyperbolic_records)=fail then Error("same acquired positive kernel");fi;
if Length(fresh)<>23 or Length(positive)<>1 then Error("complete marked roster");fi;
Read("/Users/sasha/medusa/research/leemans/algebra/coxeter_quotients/small_square_v1/records.g");;
if OrderedMarkingBijection(fresh,hyperbolic_records)=fail then Error("same entire marked inventory");fi;
Print("LITERAL_QUOTIENTS ",List(fresh,r->[r.node,r.order,r.permutations,r.checks.ok]),"\n");;
Print("COMPLETE_BOUND_MARKED_COMPARISON\n");;
QUIT_GAP(0);
