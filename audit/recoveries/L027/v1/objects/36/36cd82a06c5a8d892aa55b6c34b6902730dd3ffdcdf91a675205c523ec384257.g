Need:=function(ok,msg)if not ok then Error(msg);fi;end;
Read("point_input.g");Read("case_input.g");
RunCase:=function(ii)
 local r,u,v,w,a,b,c,pp,G,H,K,gg,ss,S,i,j,z,intervals,gens,idx,ip,sz,orders;
 r:=reps[ii];u:=r.u;v:=r.v;w:=r.w;a:=w*v;b:=v*w*u;c:=u*w;
 pp:=List([a,b,c],m->Permutation(m,LL,OnLines));Need(ForAll(pp,g->g<>fail),"unitary action");
 orders:=List(pp,Order);Need(orders=[3,r.k,3],"requested exact projective type");
 G:=Group(pp);sz:=Size(G);Print("GROUP ",ii," ",orders," ",sz,"\n");
 H:=Group(pp{[1,2]});K:=Group(pp{[2,3]});Print("ENDS ",Size(H)," ",Size(K),"\n");
 if Size(H)=sz or Size(K)=sz then Print("REJECT_NONPROPER_END\n");return;fi;
 intervals:=[rec(pair:=[0,1],g:=pp[1]),rec(pair:=[0,2],g:=pp[1]*pp[2]),rec(pair:=[0,3],g:=pp[1]*pp[2]*pp[3]),rec(pair:=[1,2],g:=pp[2]),rec(pair:=[1,3],g:=pp[2]*pp[3]),rec(pair:=[2,3],g:=pp[3])];
 ss:=Combinations([0,1,2,3]);gg:=[];
 for S in ss do gens:=List(Filtered(intervals,r->IsSubset(S,r.pair)),r->r.g);if IsEmpty(gens)then Add(gg,Group(()));else Add(gg,Group(gens));fi;od;
 ip:=true;
 for i in [1..Length(ss)]do for j in [1..Length(ss)]do
  idx:=Position(ss,Intersection(ss[i],ss[j]));
  if IsSubset(ss[i],ss[j])then Need(IsSubgroup(gg[i],gg[j]),"nested actual groups");
  elif IsSubset(ss[j],ss[i])then Need(IsSubgroup(gg[j],gg[i]),"nested actual groups");
  elif Intersection(gg[i],gg[j])<>gg[idx]then ip:=false;fi;
 od;od;
 Print("FULL_IP ",ip," 256\n");Print("PASS_CASE ",ii," ",sz," ",orders," ",ip,"\n");
end;
RunCase(CaseNumber);QUIT;
