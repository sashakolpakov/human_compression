SizeScreen([1000000,24]);;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/compare_markings.g");;
Read("/Users/sasha/medusa/research/leemans/algebra/coxeter_quotients/divisor_author01/target/records.g");;
fresh:=divisor_records;;
Read("/Users/sasha/medusa/research/leemans/algebra/coxeter_quotients/divisor_v1/records.g");;

old:=divisor_records;;
if OrderedMarkingBijection(fresh,old)=fail then Error("actual ordered quotient isomorphism");fi;
if OrderedMarkingBijection(fresh,Concatenation(old,old))<>fail then Error("wrong multiplicity accepted");fi;
bad:=StructuralCopy(old[1]);;bad.permutations[1]:=bad.permutations[2];;
if SameOrderedMarking(old[1],bad) then Error("wrong marking accepted");fi;
Print("LITERAL_TARGET ",List(fresh,r->[r.node,r.order,r.permutations]),"\n");;
Print("COMPLETE_MARKED_COMPARISON 1 2\n");;

QUIT_GAP(0);
