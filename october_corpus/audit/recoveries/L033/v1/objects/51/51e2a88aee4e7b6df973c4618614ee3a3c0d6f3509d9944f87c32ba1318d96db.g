hyperbolic_records:=[];;named_direct_records:=[];;named_series_records:=[];;named_dot_record:=rec();;linear_bridge:=rec();;
if GAPInfo.Version<>"4.15.1" then Error("GAP version");fi;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L033_work/hyperbolic_recovery_work/named_stage03/verify.g");;
VerifyNamed("/Users/sasha/medusa/research/leemans/corpus106_L033_hyperbolic_core_v1","/Users/sasha/medusa/research/leemans/reboot_20261013/L033_work/hyperbolic_recovery_work/named_stage03",4);;
QUIT;
