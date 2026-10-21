hyperbolic_records:=[];;
s:=OutputTextFile("/Users/sasha/medusa/research/leemans/reboot_20261013/L033_hyperbolic_core_distinct/join01/records.json",false);;
SetPrintFormattingStatus(s,false);;
PrintTo(s,"[\n");;
first:=true;;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L033_work/hyperbolic_recovery_work/core_stage02/censuses/3334/records.g");;
for r in hyperbolic_records do
if not first then PrintTo(s,",\n");fi;first:=false;
PrintTo(s,"[\"3334\",",r.node,",",r.order,",",r.permutations,"]");
od;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L033_work/hyperbolic_recovery_work/core_stage02/censuses/3335/records.g");;
for r in hyperbolic_records do
if not first then PrintTo(s,",\n");fi;first:=false;
PrintTo(s,"[\"3335\",",r.node,",",r.order,",",r.permutations,"]");
od;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L033_work/hyperbolic_recovery_work/core_stage02/censuses/3434/records.g");;
for r in hyperbolic_records do
if not first then PrintTo(s,",\n");fi;first:=false;
PrintTo(s,"[\"3434\",",r.node,",",r.order,",",r.permutations,"]");
od;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L033_work/hyperbolic_recovery_work/core_stage02/censuses/3534/records.g");;
for r in hyperbolic_records do
if not first then PrintTo(s,",\n");fi;first:=false;
PrintTo(s,"[\"3534\",",r.node,",",r.order,",",r.permutations,"]");
od;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L033_work/hyperbolic_recovery_work/core_stage02/censuses/353/records.g");;
for r in hyperbolic_records do
if not first then PrintTo(s,",\n");fi;first:=false;
PrintTo(s,"[\"353\",",r.node,",",r.order,",",r.permutations,"]");
od;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L033_work/hyperbolic_recovery_work/core_stage02/censuses/435/records.g");;
for r in hyperbolic_records do
if not first then PrintTo(s,",\n");fi;first:=false;
PrintTo(s,"[\"435\",",r.node,",",r.order,",",r.permutations,"]");
od;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L033_work/hyperbolic_recovery_work/core_stage02/censuses/535/records.g");;
for r in hyperbolic_records do
if not first then PrintTo(s,",\n");fi;first:=false;
PrintTo(s,"[\"535\",",r.node,",",r.order,",",r.permutations,"]");
od;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L033_work/hyperbolic_recovery_work/core_stage02/censuses/5333/records.g");;
for r in hyperbolic_records do
if not first then PrintTo(s,",\n");fi;first:=false;
PrintTo(s,"[\"5333\",",r.node,",",r.order,",",r.permutations,"]");
od;
PrintTo(s,"\n]\n");;
CloseStream(s);;
QUIT;
