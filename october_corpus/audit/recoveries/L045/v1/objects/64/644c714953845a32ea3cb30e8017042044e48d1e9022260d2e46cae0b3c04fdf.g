# Export complete named-table inputs and recompute the fourteen inequalities.
# Classification of the named groups, automorphism groups and Maxes lists is
# retained; the arithmetic below does not purport to prove those premises.
SizeScreen([240,40]);;
HC_Need:=function(test,message)
    if not test then Print("REJECT ",message,"\n");FORCE_QUIT_GAP(1);fi;
end;;
HC_Need(LoadPackage("ctbllib")=true,"CTblLib unavailable");;
HC_Need(GAPInfo.Version="4.15.1","recorded GAP version");;
HC_Need(PackageInfo("ctbllib")[1].Version="1.3.11","recorded CTblLib version");;
HC_Rows:=[
 ["J4","J4",41,29,51747149311,29,101486051],
 ["Fi23","Fi23",80,23,12895196031,976120,0],
 ["Fi24'","Fi24",88,29,7824165773823,58,747921369827],
 ["M","M",169,71,10^20,4970,0],
 ["B","B",172,47,10^12,0,0],
 ["Th","Th",42,31,976841775,44826,0],
 ["Ly","Ly",45,37,1296826875,74,15054375],
 ["Co1","Co1",78,23,12792894975,72100538,0],
 ["Co2","Co2",53,23,29771775,7590,0],
 ["Co3","Co3",38,23,2778975,7590,0],
 ["Ru","Ru",35,29,1846575,870,390195],
 ["Fi22","Fi22.2",49,13,37706175,1443546,18669235],
 ["ON","ON.2",29,31,2857239,1860,95945],
 ["HN","HN.2",37,19,75603375,7182,2662869]
];;
HC_SavedNames:=[];;HC_SavedTables:=[];;
HC_SaveTable:=function(name)
    local t,os,sz,cs,ip,mx,n;
    if name in HC_SavedNames then return;fi;
    t:=CharacterTable(name);HC_Need(t<>fail,Concatenation("missing table ",name));
    os:=OrdersClassRepresentatives(t);sz:=SizesConjugacyClasses(t);
    cs:=SizesCentralizers(t);ip:=PowerMap(t,-1);n:=Length(os);
    HC_Need(Length(sz)=n and Length(cs)=n and Length(ip)=n,"full class arrays");
    HC_Need(Sum(sz)=Size(t),"class sizes partition group");
    HC_Need(ForAll([1..n],i->sz[i]*cs[i]=Size(t)),"class centralizer equation");
    if HasMaxes(t) then mx:=Maxes(t);else mx:=[];fi;
    Add(HC_SavedNames,name);
    Add(HC_SavedTables,[name,Identifier(t),Size(t),os,sz,cs,ip,mx]);
end;;
HC_CountOrder:=function(t,d)
    local os,sz;
    os:=OrdersClassRepresentatives(t);sz:=SizesConjugacyClasses(t);
    return Sum(Filtered([1..Length(os)],i->os[i]=d),i->sz[i]);
end;;
HC_Calculate:=function(row)
    local gn,an,g,a,cl,p,f,os,cs,ac,j,m,mt,b,mu,r,ni,realAut,
          omitted,inner,targets,over,details;
    gn:=row[1];an:=row[2];cl:=row[3];p:=row[4];
    g:=CharacterTable(gn);a:=CharacterTable(an);
    HC_Need(g<>fail and a<>fail,"named simple and automorphism tables");
    HC_Need(HasMaxes(g) and HasMaxes(a),"complete maximal subgroup inputs");
    HC_SaveTable(gn);HC_SaveTable(an);
    os:=OrdersClassRepresentatives(g);cs:=SizesCentralizers(g);ac:=SizesCentralizers(a);
    HC_Need(IsPrimeInt(p) and p>2 and os[cl]=p,"selected odd prime class");
    if gn=an then f:=[1..Length(os)];
    else
        HC_Need(Size(a)=2*Size(g),"index two extension");
        f:=GetFusionMap(g,a);HC_Need(f<>fail,"recorded actual fusion into Aut(G)");
    fi;
    HC_Need(Length(f)=Length(os),"complete inclusion fusion");
    HC_Need(ForAll([1..Length(os)],i->os[i]=OrdersClassRepresentatives(a)[f[i]]),"fusion preserves orders");
    inner:=[];
    if gn<>an then
        for j in Filtered([1..Length(os)],i->os[i]=2) do
            HC_Need(ac[f[j]]=2*cs[j],"every inner involution has an outer centralizer element");
            Add(inner,[j,f[j],cs[j],ac[f[j]]]);
        od;
    fi;
    b:=0;details:=[];
    for m in Maxes(g) do
        HC_SaveTable(m);mt:=CharacterTable(m);
        HC_Need(Size(mt)<Size(g) and Size(g) mod Size(mt)=0,"proper G maximal order");
        over:=cs[cl]*HC_CountOrder(mt,p)/Size(mt);
        b:=b+over*HC_CountOrder(mt,2);
        Add(details,[m,HC_CountOrder(mt,p),HC_CountOrder(mt,2),NumeratorRat(over),DenominatorRat(over)]);
    od;
    mu:=0;omitted:=[];
    for m in Maxes(a) do
        HC_SaveTable(m);mt:=CharacterTable(m);
        HC_Need(Size(mt)<Size(a) and Size(a) mod Size(mt)=0,"proper A maximal order");
        if gn<>an and Identifier(mt)=Identifier(g) then
            HC_Need(Size(mt)=Size(g),"identified simple socle has correct order");
            Add(omitted,m);
        else mu:=Maximum(mu,HC_CountOrder(mt,2));fi;
    od;
    if gn<>an then HC_Need(Length(omitted)=1,"exactly one identified socle class omitted");fi;
    realAut:=PowerMap(a,-1)[f[cl]]=f[cl];
    if realAut then r:=ac[f[cl]]*mu;else r:=0;fi;
    ni:=HC_CountOrder(g,2);
    HC_Need(ni>=row[5] and b=row[6] and r=row[7] and b+r<row[5],"fourteen exact inequalities");
    Print("PASS ",gn," ",p," ",ni," ",b," ",r,"\n");
    return [gn,an,cl,p,row[5],f,inner,omitted,details,
            [NumeratorRat(b),DenominatorRat(b)],mu,r,ni,realAut];
end;;
HC_Computed:=List(HC_Rows,HC_Calculate);;
HC_Need(Length(HC_Computed)=14,"all fourteen cases");;
HC_Out:=OutputTextFile(OutputPath,false);;SetPrintFormattingStatus(HC_Out,false);;
HC_Json:=function(v)
    local s;
    if IsBool(v) then return String(v);fi;
    if IsInt(v) then return String(v);fi;
    if IsString(v) and Length(v)>0 then
        s:=ReplacedString(v,"\\","\\\\");s:=ReplacedString(s,"\"","\\\"");
        return Concatenation("\"",s,"\"");
    fi;
    HC_Need(IsList(v),"JSON-compatible integer/list input");
    return Concatenation("[",JoinStringsWithSeparator(List(v,HC_Json),","),"]");
end;;
PrintTo(HC_Out,HC_Json(["sporadic-counting-inputs-v1",GAPInfo.Version,
                  PackageInfo("ctbllib")[1].Version,HC_SavedTables,HC_Computed]),"\n");;
CloseStream(HC_Out);;
Print("TERMINAL_PASS 14 sporadic counting cases\n");
QUIT;
