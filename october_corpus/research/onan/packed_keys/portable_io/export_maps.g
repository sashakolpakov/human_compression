# New namespace only; no represented call at load. Restore the exact acquired
# ONMiddleBase workspace, Read this file only, then call ONPackedExport.
ONPackedNeed:=function(ok,message)
 if not ok then Error(message);fi;
end;;

ONPackedExport:=function(base,endpoint,path)
 local e,chain,size,next,points,indices,factors,ng,nt,i,j,p,start,stream,
       buffer,flush,byte,u32,u64,map,oldindex,oldrank,oldunrank,written;
 start:=Runtime();
 ONPackedNeed(IsRecord(base)and base.schema="ONAN_MIDDLE_RANK_BASE_V1"
  and base.named_ON=true and base.model.degree=122760
  and base.index.length=2857239 and IsIdenticalObj(base.index.group,base.G)
  and IsIdenticalObj(base.index.subgroup,base.U),"same acquired named action/index");
 ONPackedNeed(IsInt(endpoint)and endpoint>=1 and endpoint<=2
  and Length(base.endpoints)=2,"one actual endpoint selector");
 e:=base.endpoints[endpoint];
 ONPackedNeed(e.order in [144,256]and e.class_size in [630,1120]
  and e.order*e.class_size=161280 and e.full_aut_order=2*e.order,
  "same acquired pointwise endpoint group, not full-Aut group");
 oldindex:=base.index;oldrank:=base.index.rank;oldunrank:=base.index.unrank;
 chain:=base.index.root.chain;size:=SizeStabChain(chain);
 ONPackedNeed(size=460815505920,"existing complete ambient chain exact order");
 points:=[];indices:=[];
 while size>1 do
  ONPackedNeed(Runtime()-start<20000 and IsBound(chain.stabilizer)
   and IsBound(chain.orbit)and Length(chain.orbit)>=1,"bounded existing chain tier");
  next:=SizeStabChain(chain.stabilizer);
  ONPackedNeed(next>=1 and size mod next=0 and size/next=Length(chain.orbit),
   "actual complete stabilizer-chain index");
  if size>next then
   ONPackedNeed(Length(points)<20 and not chain.orbit[1] in points,
    "at most20 strict tiers, distinct faithful base points");
   Add(points,chain.orbit[1]);Add(indices,size/next);
  fi;
  chain:=chain.stabilizer;size:=next;
 od;
 ONPackedNeed(size=1 and Length(points)>=1 and Length(points)<=20
  and Product(indices)=460815505920,"strict base ends at trivial stabilizer");
 ng:=Length(base.model.generators);nt:=Length(e.generators);
 ONPackedNeed(ng=2 and nt>=1 and nt<=8 and ng+nt<=16,
  "actual original two ambient generators and acquired endpoint generators");
 factors:=Concatenation(base.model.generators,e.generators);
 ONPackedNeed(base.y=base.model.a and Order(base.y)=2 and Order(e.c)=2
  and e.c<>base.y and base.y*e.c=e.c*base.y
  and ForAll(factors,g->IsPerm(g)and g in base.G)
  and ForAll(e.generators,g->base.y^g=base.y and e.c^g=e.c),
  "same actual a,c and complete factor membership/pointwise joins");
 ONPackedNeed(SizeStabChain(StabChainImmutable(e.T))=e.order
  and GeneratorsOfGroup(e.T)=e.generators,
  "existing small endpoint chain/generator identity, no new subgroup discovery");
 ONPackedNeed(not IsExistingFile(path),"fresh binary export path");
 stream:=OutputTextFile(path,false);ONPackedNeed(stream<>fail,"binary export stream");
 SetPrintFormattingStatus(stream,false);buffer:="";written:=0;
 flush:=function()
  if Length(buffer)>0 then
   ONPackedNeed(WriteAll(stream,buffer)=true,"complete raw-byte stream write");
   written:=written+Length(buffer);buffer:="";
  fi;
 end;
 byte:=function(x)
  ONPackedNeed(IsInt(x)and x>=0 and x<=255,"literal byte");
  Add(buffer,CHAR_INT(x));if Length(buffer)=4096 then flush();fi;
 end;
 u32:=function(x)
  local k;
  ONPackedNeed(IsInt(x)and x>=0 and x<2^32,"literal uint32");
  for k in [1..4]do byte(x mod 256);x:=QuoInt(x,256);od;
 end;
 u64:=function(x)
  local k;
  ONPackedNeed(IsInt(x)and x>=0 and x<2^64,"literal uint64");
  for k in [1..8]do byte(x mod 256);x:=QuoInt(x,256);od;
 end;
 for i in "PCKIN001"do byte(INT_CHAR(i));od;
 for i in [122760,2857239,Length(points),Length(factors),23,e.order,nt,ng]do u32(i);od;
 u64(460815505920);u64(161280);
 for i in points do ONPackedNeed(i>=1 and i<=122760,"actual base point");u32(i-1);od;
 for i in indices do u32(i);od;
 for i in [1..ng]do byte(i);od;
 for i in [1..nt]do byte(ng+i);od;
 for p in Concatenation([base.y,e.c],factors) do
  for j in [1..122760]do
   if j mod 4096=0 then ONPackedNeed(Runtime()-start<20000,"20s whole export CPU");fi;
   i:=j^p;ONPackedNeed(i>=1 and i<=122760,"whole actual point image");u32(i-1);
  od;
 od;
 flush();CloseStream(stream);
 ONPackedNeed(written=56+8*Length(points)+ng+nt+4*122760*(2+Length(factors))
  and written<=16777216 and Runtime()-start<20000,"exact whole bounded binary length");
 ONPackedNeed(IsIdenticalObj(base.index,oldindex)and IsIdenticalObj(base.index.rank,oldrank)
  and IsIdenticalObj(base.index.unrank,oldunrank),"unchanged public index identity");
 return rec(schema:="L026_PACKED_BASE_FACTOR_EXPORT_V1",degree:=122760,target:=2857239,
  endpoint:=endpoint,endpoint_order:=e.order,full_aut_order:=e.full_aut_order,
  endpoint_class_size:=e.class_size,strict_base:=points,strict_indices:=indices,
  terminal_stabilizer_order:=1,ambient_factors:=[1..ng],endpoint_factors:=[ng+1..ng+nt],
  factor_count:=Length(factors),bytes:=written,raw_little_endian:=true,
  accepted_chain_reused:=true,old_rank_checkpoint_transferred:=false,
  generation_counted:=false,whole_original_credit:=0);
end;;
