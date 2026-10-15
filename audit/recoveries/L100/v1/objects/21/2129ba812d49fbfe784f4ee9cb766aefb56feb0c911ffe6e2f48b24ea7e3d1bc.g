LoadPackage("grape");;LoadPackage("json");;SizeScreen([100000,24]);;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/palette_work/cosets.g");;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/palette_work/palette.g");;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/palette_interface_controls02/function_only.g");;
G:=Group((1,2),(3,4));;a:=Group((1,2));;b:=Group((3,4));;c:=Group((1,2)(3,4));;
data:=rec(group_generators:=GeneratorsOfGroup(G),representatives:=[rec(borel_id:=1,source_index:=1,parabolics:=[a,b]),rec(borel_id:=1,source_index:=2,parabolics:=[a,c]),rec(borel_id:=1,source_index:=3,parabolics:=[b,c])]);;
RunLiteralPaletteCatalogue(G,data,"/Users/sasha/medusa/research/leemans/geometry/psl3_4/palette_interface_controls02/tiny");;
Print("PASS_ACTUAL_TINY_PALETTE_CALLER\n");QUIT_GAP(0);
