# Root restores the exact acquired workspace and supplies this literal record
# via an independently authenticated -c. No old rank/cache Sources are Read.
if not IsBound(ONPackedExportConfig)or not IsRecord(ONPackedExportConfig)
 or Set(RecNames(ONPackedExportConfig))<>Set(["endpoint","maps","report"])
 or not IsInt(ONPackedExportConfig.endpoint)or not ONPackedExportConfig.endpoint in [1,2]
 or not IsString(ONPackedExportConfig.maps)or not IsString(ONPackedExportConfig.report)
 or IsExistingFile(ONPackedExportConfig.maps)or IsExistingFile(ONPackedExportConfig.report)
 or IsBound(ONPackedExportReport)or IsBound(ONPackedExportStream)
 or IsBound(ONPackedNeed)or IsBound(ONPackedExport)then
 Error("fresh exact packed export configuration/namespace");
fi;
Read("/Users/sasha/medusa/research/leemans/geometry/onan_regular_maps/permutation_model/middle_partition/packed_conjugacy_keys/portable_io/export_maps.g");;
ONPackedExportReport:=ONPackedExport(ONMiddleBase,ONPackedExportConfig.endpoint,ONPackedExportConfig.maps);;
ONPackedNeed(Length(String(ONPackedExportReport))<=131000,"bounded whole export report");;
ONPackedExportStream:=OutputTextFile(ONPackedExportConfig.report,false);;
ONPackedNeed(ONPackedExportStream<>fail,"fresh export report stream");;
SetPrintFormattingStatus(ONPackedExportStream,false);;
PrintTo(ONPackedExportStream,"return ",String(ONPackedExportReport),";\n");;
CloseStream(ONPackedExportStream);;
Print("COMPLETE_PACKED_BASE_FACTOR_EXPORT\n");
QUIT;
