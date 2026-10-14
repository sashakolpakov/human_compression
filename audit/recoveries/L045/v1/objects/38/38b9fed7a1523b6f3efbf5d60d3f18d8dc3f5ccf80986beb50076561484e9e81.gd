#############################################################################
##
#W  ctblothe.gd          GAP 4 package CTblLib                  Thomas Breuer
##
##  This file contains the declarations of functions for interfaces to
##  other data formats of character tables.
##
##  1. Interface to CAS
##  2. Interface to MOC
##  3. Interface to GAP 3
##  4. Interface to the Cambridge format
##  5. Interface to the MAGMA display format
##
##  <#GAPDoc Label="interfaces">
##  This chapter describes data formats for character tables that can be read
##  or created by &GAP;.
##  Currently these are the formats used by
##  <List>
##  <Item>
##    the &CAS; system (see&nbsp;<Ref Sect="sec:interface-cas"/>),
##  </Item>
##  <Item>
##    the &MOC; system (see&nbsp;<Ref Sect="sec:interface-moc"/>),
##  </Item>
##  <Item>
##    &GAP;&nbsp;3 (see&nbsp;<Ref Sect="sec:interface-gap3"/>),
##  </Item>
##  <Item>
##    the so-called <E>Cambridge format</E>
##    (see&nbsp;<Ref Sect="sec:interface-cambridge"/>), and
##  </Item>
##  <Item>
##    the <Package>MAGMA</Package> system
##    (see&nbsp;<Ref Sect="sec:interface-magma"/>).
##  </Item>
##  </List>
##  <#/GAPDoc>
##


#############################################################################
##
#T  TODO:
##
#a  MocData( <chi> )
#a  MocInfo( <tbl> )
#o  VirtualCharacterByMocData( <tbl>, <vector> )
#o  CharacterByMocData( <tbl>, <vector> )
##


#############################################################################
##
##  1. Interface to CAS
##
##  <#GAPDoc Label="interface_CAS">
##  The interface to &CAS; (see&nbsp;<Cite Key="NPP84"/>) is thought
##  just for printing the &CAS; data to a file.
##  The function <Ref Func="CASString"/> is available mainly
##  in order to document the data format.
##  <E>Reading</E> &CAS; tables is not supported;
##  note that the tables contained in the
##  &CAS; Character Table Library have been migrated to
##  &GAP; using a few <C>sed</C> scripts and <C>C</C> programs.
##  <#/GAPDoc>
##


#############################################################################
##
#F  CASString( <tbl> )
##
##  <#GAPDoc Label="CASString">
##  <ManSection>
##  <Func Name="CASString" Arg="tbl"/>
##
##  <Description>
##  is a string that encodes the &CAS; library format
##  of the character table <A>tbl</A>.
##  This string can be printed to a file which then can be read into the
##  &CAS; system using its <C>get</C> command (see&nbsp;<Cite Key="NPP84"/>).
##  <P/>
##  The used line length is the first entry in the list returned by
##  <Ref Func="SizeScreen" BookName="ref"/>.
##  <P/>
##  Only the known values of the following attributes are used.
##  <Ref Attr="ClassParameters" BookName="ref"/> (for partitions only),
##  <Ref Attr="ComputedClassFusions" BookName="ref"/>,
##  <Ref Attr="ComputedIndicators" BookName="ref"/>,
##  <Ref Attr="ComputedPowerMaps" BookName="ref"/>,
##  <Ref Attr="ComputedPrimeBlocks" BookName="ref"/>,
##  <Ref Attr="Identifier" Label="for character tables" BookName="ref"/>,
##  <Ref Attr="InfoText" BookName="ref"/>,
##  <Ref Attr="Irr" BookName="ref"/>,
##  <Ref Attr="OrdersClassRepresentatives" BookName="ref"/>,
##  <Ref Attr="Size" BookName="ref"/>,
##  <Ref Attr="SizesCentralizers" BookName="ref"/>.
##  <P/>
##  <Example><![CDATA[
##  gap> Print( CASString( CharacterTable( "Cyclic", 2 ) ), "\n" );
##  'C2'
##  00/00/00. 00.00.00.
##  (2,2,0,2,-1,0)
##  text:
##  (#computed using generic character table for cyclic groups#),
##  order=2,
##  centralizers:(
##  2,2
##  ),
##  reps:(
##  1,2
##  ),
##  powermap:2(
##  1,1
##  ),
##  characters:
##  (1,1
##  ,0:0)
##  (1,-1
##  ,0:0);
##  /// converted from GAP
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "CASString" );


#############################################################################
##
##  2. Interface to MOC
##
##  <#GAPDoc Label="interface_MOC">
##  The interface to &MOC; (see&nbsp;<Cite Key="HJLP92"/>)
##  can be used to print &MOC; input.
##  Additionally it provides an alternative representation of (virtual)
##  characters.
##  <P/>
##  The &MOC;&nbsp;3 code of a <M>5</M> digit number
##  in &MOC;&nbsp;2 code is given by the following list.
##  (Note that the code must contain only lower case letters.)
##  <P/>
##  <Verb>
##  ABCD    for  0ABCD
##  a       for  10000
##  b       for  10001          k       for  20001
##  c       for  10002          l       for  20002
##  d       for  10003          m       for  20003
##  e       for  10004          n       for  20004
##  f       for  10005          o       for  20005
##  g       for  10006          p       for  20006
##  h       for  10007          q       for  20007
##  i       for  10008          r       for  20008
##  j       for  10009          s       for  20009
##  tAB     for  100AB
##  uAB     for  200AB
##  vABCD   for  1ABCD
##  wABCD   for  2ABCD
##  yABC    for  30ABC
##  z       for  31000
##  </Verb>
##  <P/>
##  <E>Note</E> that any long number in &MOC;&nbsp;2 format
##  is divided into packages of length <M>4</M>,
##  the first (!) one filled with leading zeros if necessary.
##  Such a number with decimals <M>d_1, d_2, \ldots, d_{{4n+k}}</M>
##  is the sequence
##  <M>0 d_1 d_2 d_3 d_4 \ldots 0 d_{{4n-3}} d_{{4n-2}} d_{{4n-1}} d_{4n}
##  d_{{4n+1}} \ldots d_{{4n+k}}</M>
##  where <M>0 \leq k \leq 3</M>,
##  the first digit of <M>x</M> is <M>1</M> if the number is positive
##  and <M>2</M> if the number is negative,
##  and then follow <M>(4-k)</M> zeros.
##  <P/>
##  Details about the &MOC; system are explained
##  in&nbsp;<Cite Key="HJLP92"/>,
##  a brief description can be found in&nbsp;<Cite Key="LP91"/>.
##  <#/GAPDoc>
##


#############################################################################
##
#F  MAKElb11( <listofns> )
##
##  <#GAPDoc Label="MAKElb11">
##  <ManSection>
##  <Func Name="MAKElb11" Arg="listofns"/>
##
##  <Description>
##  For a list <A>listofns</A> of positive integers,
##  <Ref Func="MAKElb11"/> prints field information for all number fields
##  with conductor in this list.
##  <P/>
##  The output of <Ref Func="MAKElb11"/> is used by the &MOC; system;
##  Calling <C>MAKElb11( [ 3 .. 189 ] )</C> will print something very similar
##  to Richard Parker's file <F>lb11</F>.
##  <P/>
##  <Example><![CDATA[
##  gap> MAKElb11( [ 3, 4 ] );
##     3   2   0   1   0
##     4   2   0   1   0
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "MAKElb11" );


#############################################################################
##
#F  MOCTable( <gaptbl> )
#F  MOCTable( <gaptbl>, <basicset> )
##
##  <#GAPDoc Label="MOCTable">
##  <ManSection>
##  <Func Name="MOCTable" Arg="gaptbl[, basicset]"/>
##
##  <Description>
##  <Ref Func="MOCTable"/> returns the &MOC; table record of the
##  &GAP; character table <A>gaptbl</A>.
##  <P/>
##  The one argument version can be used only if <A>gaptbl</A> is an
##  ordinary (<M>G.0</M>) table.
##  For Brauer (<M>G.p</M>) tables, one has to specify a basic set
##  <A>basicset</A> of ordinary irreducibles.
##  <A>basicset</A> must then be a list of positions of the basic set
##  characters in the <Ref Attr="Irr" BookName="ref"/> list
##  of the ordinary table of <A>gaptbl</A>.
##  <P/>
##  The result is a record that contains the information of <A>gaptbl</A>
##  in a format similar to the &MOC;&nbsp;3 format.
##  This record can, e.&nbsp;g., easily be printed out or be used to print
##  out characters using <Ref Func="MOCString"/>.
##  <P/>
##  The components of the result are
##  <List>
##  <Mark><C>identifier</C></Mark>
##  <Item>
##    the string <C>MOCTable( </C><M>name</M><C> )</C> where <M>name</M> is
##    the <Ref Attr="Identifier" Label="for character tables" BookName="ref"/>
##    value of <A>gaptbl</A>,
##  </Item>
##  <Mark><C>GAPtbl</C></Mark>
##  <Item>
##    <A>gaptbl</A>,
##  </Item>
##  <Mark><C>prime</C></Mark>
##  <Item>
##    the characteristic of the field (label <C>30105</C> in &MOC;),
##  </Item>
##  <Mark><C>centralizers</C></Mark>
##  <Item>
##    centralizer orders for cyclic subgroups (label <C>30130</C>)
##  </Item>
##  <Mark><C>orders</C></Mark>
##  <Item>
##    element orders for cyclic subgroups (label <C>30140</C>)
##  </Item>
##  <Mark><C>fieldbases</C></Mark>
##  <Item>
##    at position <M>i</M> the Parker basis of the number field generated
##    by the character values of the <M>i</M>-th cyclic subgroup.
##    The length of <C>fieldbases</C> is equal to the value of label
##    <C>30110</C> in &MOC;.
##  </Item>
##  <Mark><C>cycsubgps</C></Mark>
##  <Item>
##    <C>cycsubgps[i] = j</C> means that class <C>i</C> of the &GAP; table
##    belongs to the <C>j</C>-th cyclic subgroup of the &GAP; table,
##  </Item>
##  <Mark><C>repcycsub</C></Mark>
##  <Item>
##    <C>repcycsub[j] = i</C> means that class <C>i</C> of the &GAP; table
##    is the representative of the <C>j</C>-th cyclic subgroup of the
##    &GAP; table.
##    <E>Note</E> that the representatives of &GAP; table and
##    &MOC; table need not agree!
##  </Item>
##  <Mark><C>galconjinfo</C></Mark>
##  <Item>
##    a list <M>[ r_1, c_1, r_2, c_2, \ldots, r_n, c_n ]</M>
##    which means that the <M>i</M>-th class of the &GAP; table is
##    the <M>c_i</M>-th conjugate of the representative of
##    the <M>r_i</M>-th cyclic subgroup on the &MOC; table.
##    (This is used to translate back to &GAP; format,
##    stored under label <C>30160</C>)
##  </Item>
##  <Mark><C>30170</C></Mark>
##  <Item>
##    (power maps) for each cyclic subgroup (except the trivial one)
##    and each prime divisor of the representative order store four values,
##    namely the number of the subgroup, the power,
##    the number of the cyclic subgroup containing the image,
##    and the power to which the representative must be raised to yield
##    the image class.
##    (This is used only to construct the <C>30230</C> power map/embedding
##    information.)
##    In <C>30170</C> only a list of lists (one for each cyclic subgroup)
##    of all these values is stored, it will not be used by &GAP;.
##  </Item>
##  <Mark><C>tensinfo</C></Mark>
##  <Item>
##    tensor product information, used to compute the coefficients
##    of the Parker base for tensor products of characters
##    (label <C>30210</C> in &MOC;).
##    For a field with vector space basis <M>(v_1, v_2, \ldots, v_n)</M>,
##    the tensor product information of a cyclic subgroup in
##    &MOC; (as computed by <C>fct</C>) is either <M>1</M>
##    (for rational classes)
##    or a sequence
##    <Display Mode="M">
##    n x_{1,1} y_{1,1} z_{1,1} x_{1,2} y_{1,2} z_{1,2}
##    \ldots x_{1,m_1} y_{1,m_1} z_{1,m_1} 0 x_{2,1} y_{2,1}
##    z_{2,1} x_{2,2} y_{2,2} z_{2,2} \ldots x_{2,m_2}
##    y_{2,m_2} z_{2,m_2} 0 \ldots z_{n,m_n} 0
##    </Display>
##    which means that the coefficient of <M>v_k</M> in the product
##    <Display Mode="M">
##    \left( \sum_{i=1}^{n} a_i v_i \right)
##    \left( \sum_{j=1}^{n} b_j v_j \right)
##    </Display>
##    is equal to
##    <Display Mode="M">
##    \sum_{i=1}^{m_k} x_{k,i} a_{y_{k,i}} b_{z_{k,i}} .
##    </Display>
##    On a &MOC; table in &GAP;,
##    the <C>tensinfo</C> component is a list of lists,
##    each containing exactly the sequence mentioned above.
##  </Item>
##  <Mark><C>invmap</C></Mark>
##  <Item>
##    inverse map to compute complex conjugate characters,
##    label <C>30220</C> in &MOC;.
##  </Item>
##  <Mark><C>powerinfo</C></Mark>
##  <Item>
##    field embeddings for <M>p</M>-th symmetrizations,
##    <M>p</M> a prime integer not larger than the largest element order,
##    label <C>30230</C> in &MOC;.
##  </Item>
##  <Mark><C>30900</C></Mark>
##  <Item>
##    basic set of restricted ordinary irreducibles in the
##    case of nonzero characteristic,
##    all ordinary irreducibles otherwise.
##  </Item>
##  </List>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "MOCTable" );


#############################################################################
##
#F  MOCString( <moctbl> )
#F  MOCString( <moctbl>, <chars> )
##
##  <#GAPDoc Label="MOCString">
##  <ManSection>
##  <Func Name="MOCString" Arg="moctbl[, chars]"/>
##
##  <Description>
##  Let <A>moctbl</A> be a &MOC; table record,
##  as returned by <Ref Func="MOCTable"/>.
##  <Ref Func="MOCString"/> returns a string describing the
##  &MOC;&nbsp;3 format of <A>moctbl</A>.
##  <P/>
##  If a second argument <A>chars</A> is specified,
##  it must be a list of &MOC;
##  format characters as returned by <Ref Func="MOCChars"/>.
##  In this case, these characters are stored under label <C>30900</C>.
##  If the second argument is missing then the basic set of ordinary
##  irreducibles is stored under this label.
##  <Example><![CDATA[
##  gap> moca5:= MOCTable( CharacterTable( "A5" ) );
##  rec( 30170 := [ [  ], [ 2, 2, 1, 1 ], [ 3, 3, 1, 1 ], [ 4, 5, 1, 1 ] ]
##      , 
##    30900 := [ [ 1, 1, 1, 1, 0 ], [ 3, -1, 0, 0, -1 ], 
##        [ 3, -1, 0, 1, 1 ], [ 4, 0, 1, -1, 0 ], [ 5, 1, -1, 0, 0 ] ], 
##    GAPtbl := CharacterTable( "A5" ), centralizers := [ 60, 4, 3, 5 ], 
##    cycsubgps := [ 1, 2, 3, 4, 4 ], 
##    fieldbases := 
##      [ CanonicalBasis( Rationals ), CanonicalBasis( Rationals ), 
##        CanonicalBasis( Rationals ), 
##        Basis( NF(5,[ 1, 4 ]), [ 1, E(5)+E(5)^4 ] ) ], fields := [  ], 
##    galconjinfo := [ 1, 1, 2, 1, 3, 1, 4, 1, 4, 2 ], 
##    identifier := "MOCTable(A5)", 
##    invmap := [ [ 1, 1, 0 ], [ 1, 2, 0 ], [ 1, 3, 0 ], 
##        [ 1, 4, 0, 1, 5, 0 ] ], orders := [ 1, 2, 3, 5 ], 
##    powerinfo := 
##      [ , 
##        [ [ 1, 1, 0 ], [ 1, 1, 0 ], [ 1, 3, 0 ], 
##            [ 1, 4, -1, 5, 0, -1, 5, 0 ] ], 
##        [ [ 1, 1, 0 ], [ 1, 2, 0 ], [ 1, 1, 0 ], 
##            [ 1, 4, -1, 5, 0, -1, 5, 0 ] ],, 
##        [ [ 1, 1, 0 ], [ 1, 2, 0 ], [ 1, 3, 0 ], [ 1, 1, 0, 0 ] ] ], 
##    prime := 0, repcycsub := [ 1, 2, 3, 4 ], 
##    tensinfo := 
##      [ [ 1 ], [ 1 ], [ 1 ], 
##        [ 2, 1, 1, 1, 1, 2, 2, 0, 1, 1, 2, 1, 2, 1, -1, 2, 2, 0 ] ] )
##  gap> str:= MOCString( moca5 );;
##  gap> str{[1..68]};
##  "y100y105ay110fey130t60edfy140bcdfy150bbbfcabbey160bbcbdbebecy170ccbb"
##  gap> moca5mod3:= MOCTable( CharacterTable( "A5" ) mod 3, [ 1 .. 4 ] );;
##  gap> MOCString( moca5mod3 ){ [ 1 .. 68 ] };
##  "y100y105dy110edy130t60efy140bcfy150bbfcabbey160bbcbdbdcy170ccbbdfbby"
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "MOCString" );


#############################################################################
##
#F  ScanMOC( <list> )
##
##  <#GAPDoc Label="ScanMOC">
##  <ManSection>
##  <Func Name="ScanMOC" Arg="list"/>
##
##  <Description>
##  returns a record containing the information encoded in the list
##  <A>list</A>.
##  The components of the result are the labels that occur in <A>list</A>.
##  If <A>list</A> is in &MOC;&nbsp;2 format (10000-format),
##  the names of components are 30000-numbers;
##  if it is in &MOC;&nbsp;3 format the names of components
##  have <C>yABC</C>-format.
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "ScanMOC" );


#############################################################################
##
#F  GAPChars( <tbl>, <mocchars> )
##
##  <#GAPDoc Label="GAPChars">
##  <ManSection>
##  <Func Name="GAPChars" Arg="tbl, mocchars"/>
##
##  <Description>
##  Let <A>tbl</A> be a character table or a &MOC;
##  table record,
##  and <A>mocchars</A> be either a list of &MOC; format
##  characters
##  (as returned by <Ref Func="MOCChars"/>)
##  or a list of positive integers such as a record component encoding
##  characters, in a record produced by <Ref Func="ScanMOC"/>.
##  <P/>
##  <Ref Func="GAPChars"/> returns translations of <A>mocchars</A> to &GAP;
##  character values lists.
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "GAPChars" );


#############################################################################
##
#F  MOCChars( <tbl>, <gapchars> )
##
##  <#GAPDoc Label="MOCChars">
##  <ManSection>
##  <Func Name="MOCChars" Arg="tbl, gapchars"/>
##
##  <Description>
##  Let <A>tbl</A> be a character table or a &MOC;
##  table record,
##  and <A>gapchars</A> be a list of (&GAP; format) characters.
##  <Ref Func="MOCChars"/> returns translations of <A>gapchars</A>
##  to &MOC; format.
##  <Example><![CDATA[
##  gap> scan:= ScanMOC( str );
##  rec( y050 := [ 5, 1, 1, 0, 1, 2, 0, 1, 3, 0, 1, 1, 0, 0 ], 
##    y105 := [ 0 ], y110 := [ 5, 4 ], y130 := [ 60, 4, 3, 5 ], 
##    y140 := [ 1, 2, 3, 5 ], y150 := [ 1, 1, 1, 5, 2, 0, 1, 1, 4 ], 
##    y160 := [ 1, 1, 2, 1, 3, 1, 4, 1, 4, 2 ], 
##    y170 := [ 2, 2, 1, 1, 3, 3, 1, 1, 4, 5, 1, 1 ], 
##    y210 := [ 1, 1, 1, 2, 1, 1, 1, 1, 2, 2, 0, 1, 1, 2, 1, 2, 1, -1, 2, 
##        2, 0 ], y220 := [ 1, 1, 0, 1, 2, 0, 1, 3, 0, 1, 4, 0, 1, 5, 0 ],
##    y230 := [ 2, 1, 1, 0, 1, 1, 0, 1, 3, 0, 1, 4, -1, 5, 0, -1, 5, 0 ], 
##    y900 := [ 1, 1, 1, 1, 0, 3, -1, 0, 0, -1, 3, -1, 0, 1, 1, 4, 0, 1, 
##        -1, 0, 5, 1, -1, 0, 0 ] )
##  gap> gapchars:= GAPChars( moca5, scan.y900 );
##  [ [ 1, 1, 1, 1, 1 ], [ 3, -1, 0, -E(5)-E(5)^4, -E(5)^2-E(5)^3 ], 
##    [ 3, -1, 0, -E(5)^2-E(5)^3, -E(5)-E(5)^4 ], [ 4, 0, 1, -1, -1 ], 
##    [ 5, 1, -1, 0, 0 ] ]
##  gap> mocchars:= MOCChars( moca5, gapchars );
##  [ [ 1, 1, 1, 1, 0 ], [ 3, -1, 0, 0, -1 ], [ 3, -1, 0, 1, 1 ], 
##    [ 4, 0, 1, -1, 0 ], [ 5, 1, -1, 0, 0 ] ]
##  gap> Concatenation( mocchars ) = scan.y900;
##  true
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "MOCChars" );


#############################################################################
##
##  3. Interface to GAP 3
##
##  <#GAPDoc Label="interface_GAP3">
##  The following functions are used to read and write character tables in
##  &GAP;&nbsp;3 format.
##  <#/GAPDoc>
##


#############################################################################
##
#V  GAP3CharacterTableData
##
##  <#GAPDoc Label="GAP3CharacterTableData">
##  <ManSection>
##  <Var Name="GAP3CharacterTableData"/>
##
##  <Description>
##  This is a list of pairs,
##  the first entry being the name of a component in a &GAP;&nbsp;3
##  character table and the second entry being the corresponding
##  attribute name in &GAP;&nbsp;4.
##  The variable is used by <Ref Func="GAP3CharacterTableScan"/>
##  and <Ref Func="GAP3CharacterTableString"/>.
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalVariable( "GAP3CharacterTableData",
    "list of pairs [ <GAP 3 component>, <GAP 4 attribute> ]" );


#############################################################################
##
#F  GAP3CharacterTableScan( <string> )
##
##  <#GAPDoc Label="GAP3CharacterTableScan">
##  <ManSection>
##  <Func Name="GAP3CharacterTableScan" Arg="string"/>
##
##  <Description>
##  Let <A>string</A> be a string that contains the output of the
##  &GAP;&nbsp;3 function <C>PrintCharTable</C>.
##  In other words, <A>string</A> describes a &GAP; record whose components
##  define an ordinary character table object in &GAP;&nbsp;3.
##  <Ref Func="GAP3CharacterTableScan"/> returns the corresponding
##  &GAP;&nbsp;4 character table object.
##  <P/>
##  The supported record components are given by the list
##  <Ref Var="GAP3CharacterTableData"/>.
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "GAP3CharacterTableScan" );


#############################################################################
##
#F  GAP3CharacterTableString( <tbl> )
##
##  <#GAPDoc Label="GAP3CharacterTableString">
##  <ManSection>
##  <Func Name="GAP3CharacterTableString" Arg="tbl"/>
##
##  <Description>
##  For an ordinary character table <A>tbl</A>,
##  <Ref Func="GAP3CharacterTableString"/> returns
##  a string that when read into &GAP;&nbsp;3 evaluates to a character table
##  corresponding to <A>tbl</A>.
##  A similar format is printed by the &GAP;&nbsp;3 function
##  <C>PrintCharTable</C>.
##  <P/>
##  The supported record components are given by the list
##  <Ref Var="GAP3CharacterTableData"/>.
##  <P/>
##  <Example><![CDATA[
##  gap> tbl:= CharacterTable( "Alternating", 5 );;
##  gap> str:= GAP3CharacterTableString( tbl );;
##  gap> Print( str );
##  rec(
##  centralizers := [ 60, 4, 3, 5, 5 ],
##  fusions := [ rec( map := [ 1, 3, 4, 7, 7 ], name := "Sym(5)" ) ],
##  identifier := "Alt(5)",
##  irreducibles := [
##  [ 1, 1, 1, 1, 1 ],
##  [ 4, 0, 1, -1, -1 ],
##  [ 5, 1, -1, 0, 0 ],
##  [ 3, -1, 0, -E(5)-E(5)^4, -E(5)^2-E(5)^3 ],
##  [ 3, -1, 0, -E(5)^2-E(5)^3, -E(5)-E(5)^4 ]
##  ],
##  orders := [ 1, 2, 3, 5, 5 ],
##  powermap := [ , [ 1, 1, 3, 5, 4 ], [ 1, 2, 1, 5, 4 ], , [ 1, 2, 3, 1, \
##  1 ] ],
##  size := 60,
##  text := "computed using generic character table for alternating groups\
##  ",
##  operations := CharTableOps )
##  gap> scan:= GAP3CharacterTableScan( str );
##  CharacterTable( "Alt(5)" )
##  gap> TransformingPermutationsCharacterTables( tbl, scan );
##  rec( columns := (), group := Group([ (4,5) ]), rows := () )
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "GAP3CharacterTableString" );


#############################################################################
##
##  4. Interface to the Cambridge format
##
##  <#GAPDoc Label="interface_cambridge">
##  The following functions deal with the so-called Cambridge format,
##  in which the source data of the character tables in the
##  &ATLAS; of Finite Groups&nbsp;<Cite Key="CCN85"/> and in the
##  &ATLAS; of Brauer Characters&nbsp;<Cite Key="JLPW95"/> are stored.
##  Each such table is stored on a file of its own.
##  The line length is at most <M>78</M>,
##  and each item of the table starts in a new line, behind one of the
##  following prefixes.
##  <P/>
##  <List>
##  <Mark><C>#23</C></Mark>
##  <Item>
##    a description and the name(s) of the simple group
##  </Item>
##  <Mark><C>#7</C></Mark>
##  <Item>
##    integers describing the column widths
##  </Item>
##  <Mark><C>#9</C></Mark>
##  <Item>
##    the symbols <C>;</C> and <C>@</C>, denoting columns between tables and
##    columns that belong to conjugacy classes, respectively
##  </Item>
##  <Mark><C>#1</C></Mark>
##  <Item>
##    the symbol <C>|</C> in columns between tables, and centralizer orders
##    otherwise
##  </Item>
##  <Mark><C>#2</C></Mark>
##  <Item>
##    the symbols <C>p</C> (in the first column only),
##    <C>power</C> (in the second column only, which belongs to the class
##    of the identity element), <C>|</C> in other columns between tables,
##    and descriptions of the powers of classes otherwise
##  </Item>
##  <Mark><C>#3</C></Mark>
##  <Item>
##    the symbols <C>p'</C> (in the first column only),
##    <C>part</C> (in the second column only, which belongs to the class
##    of the identity element), <C>|</C> in other columns between tables,
##    and descriptions of the <M>p</M>-prime parts of classes otherwise
##  </Item>
##  <Mark><C>#4</C></Mark>
##  <Item>
##    the symbols <C>ind</C> and <C>fus</C> in columns between tables,
##    and class names otherwise
##  </Item>
##  <Mark><C>#5</C></Mark>
##  <Item>
##    either <C>|</C> or strings composed from the symbols <C>+</C>,
##    <C>-</C>, <C>o</C>, and integers in columns where the lines
##    starting with <C>#4</C> contain <C>ind</C>;
##    the symbols <C>:</C>, <C>.</C>, <C>?</C> in columns where these
##    lines contain <C>fus</C>;
##    character values or <C>|</C> otherwise
##  </Item>
##  <Mark><C>#6</C></Mark>
##  <Item>
##    the symbols <C>|</C>, <C>ind</C>, <C>and</C>, and <C>fus</C>
##    in columns between tables;
##    the symbol <C>|</C> and element orders of preimage classes in downward
##    extensions otherwise
##  </Item>
##  <Mark><C>#8</C></Mark>
##  <Item>
##    the last line of the data, may contain the date of the last change
##  </Item>
##  <Mark><C>#C</C></Mark>
##  <Item>
##    comments.
##  </Item>
##  </List>
##  <#/GAPDoc>
##


#############################################################################
##
#F  CambridgeMaps( <tbl> )
##
##  <#GAPDoc Label="CambridgeMaps">
##  <ManSection>
##  <Func Name="CambridgeMaps" Arg="tbl"/>
##
##  <Description>
##  For a character table <A>tbl</A>, <Ref Func="CambridgeMaps"/> returns
##  a record with the following components.
##  <P/>
##  <List>
##  <Mark><C>names</C></Mark>
##  <Item>
##    a list of strings denoting class names,
##  </Item>
##  <Mark><C>power</C></Mark>
##  <Item>
##    a list of strings, the <M>i</M>-th entry encodes the <M>p</M>-th powers
##    of the <M>i</M>-th class,
##    for all prime divisors <M>p</M> of the group order,
##  </Item>
##  <Mark><C>prime</C></Mark>
##  <Item>
##    a list of strings, the <M>i</M>-th entry encodes the <M>p</M>-prime
##    parts of the <M>i</M>-th class,
##    for all prime divisors <M>p</M> of the group order.
##  </Item>
##  </List>
##  <P/>
##  The meaning of the entries of the lists is defined in
##  <Cite Key="CCN85" Where="Chapter&nbsp;7, Sections&nbsp;3&ndash;5"/>).
##  <P/>
##  <Ref Func="CambridgeMaps"/> is used for example by
##  <Ref Func="Display" Label="for a character table" BookName="ref"/>
##  in the case that the <C>powermap</C> option has the value
##  <C>"ATLAS"</C>.
##  <P/>
##  Note that the value of the <C>names</C> component may differ from the
##  class names of the character table shown in the &ATLAS; of Finite Groups;
##  an example is the character table of the group <M>J_1</M>.
##  <P/>
##  <Example><![CDATA[
##  gap> CambridgeMaps( CharacterTable( "A5" ) );
##  rec( names := [ "1A", "2A", "3A", "5A", "B*" ], 
##    power := [ "", "A", "A", "A", "A" ], 
##    prime := [ "", "A", "A", "A", "A" ] )
##  gap> CambridgeMaps( CharacterTable( "A5" ) mod 2 );
##  rec( names := [ "1A", "3A", "5A", "B*" ], 
##    power := [ "", "A", "A", "A" ], prime := [ "", "A", "A", "A" ] )
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "CambridgeMaps" );


#############################################################################
##
#F  StringOfCambridgeFormat( <tblnames>[, <p>][: OmitDashedRows] )
#F  StringOfCambridgeFormat( <simpname>[, <p>][: OmitDashedRows] )
#F  StringOfCambridgeFormat( <tbls> ) . . . . . . . . backwards compatibility
##
##  <#GAPDoc Label="StringOfCambridgeFormat">
##  <ManSection>
##  <Func Name="StringOfCambridgeFormat" Arg="tblnames[, p]"/>
##
##  <Description>
##  Let <A>tblnames</A> be a matrix of identifiers of ordinary character
##  tables, which describe the bicyclic extensions of a simple group from the
##  &ATLAS; of Finite Groups.
##  The class fusions between the character tables must be stored on the
##  tables.
##  <P/>
##  If the required information is available then
##  <Ref Func="StringOfCambridgeFormat"/> returns a string that encodes an
##  approximation of the Cambridge format file for the simple group in
##  question (whose identifier occurs in the upper left corner of
##  <A>tblnames</A>).
##  Otherwise, that is, if some character table or class fusion is missing,
##  <K>fail</K> is returned.
##  <P/>
##  If a prime integer <A>p</A> is given as a second argument then the
##  result describes <A>p</A>-modular character tables, otherwise the
##  ordinary character tables are described by the result.
##  <P/>
##  Differences to the original format may occur for irrational character
##  values; the descriptions of these values have been chosen deliberately
##  for the original files, it is not obvious how to compute these
##  descriptions from the character tables in question.
##  <P/>
##  <Example><![CDATA[
##  gap> str:= StringOfCambridgeFormat( [ [   "A5",   "A5.2" ],
##  >                                     [ "2.A5", "2.A5.2" ] ] );;
##  gap> Print( str );
##  #23 ? A5
##  #7 4 4 4 4 4 4 4 4 4 4 4 
##  #9 ; @ @ @ @ @ ; ; @ @ @ 
##  #1 | 60 4 3 5 5 | | 6 2 3 
##  #2 p power A A A A | | A A AB 
##  #3 p' part A A A A | | A A AB 
##  #4 ind 1A 2A 3A 5A B* fus ind 2B 4A 6A 
##  #5 + 1 1 1 1 1 : ++ 1 1 1 
##  #5 + 3 -1 0 -b5 * . + 0 0 0 
##  #5 + 3 -1 0 * -b5 . | | | | 
##  #5 + 4 0 1 -1 -1 : ++ 2 0 -1 
##  #5 + 5 1 -1 0 0 : ++ 1 -1 1 
##  #6 ind 1 4 3 5 5 fus ind 2 8 6 
##  #6 | 2 | 6 10 10 | | | 8 6 
##  #5 - 2 0 -1 b5 * . - 0 0 0 
##  #5 - 2 0 -1 * b5 . | | | | 
##  #5 - 4 0 1 -1 -1 : oo 0 0 i3 
##  #5 - 6 0 0 1 1 : oo 0 i2 0 
##  #8
##  gap> str:= StringOfCambridgeFormat( [ [   "A5",   "A5.2" ],
##  >                                     [ "2.A5", "2.A5.2" ] ], 3 );;
##  gap> Print( str );
##  #23 A5 (Mod 3)
##  #7 4 4 4 4 4 4 4 4 4 
##  #9 ; @ @ @ @ ; ; @ @ 
##  #1 | 60 4 5 5 | | 6 2 
##  #2 p power A A A | | A A 
##  #3 p' part A A A | | A A 
##  #4 ind 1A 2A 5A B* fus ind 2B 4A 
##  #5 + 1 1 1 1 : ++ 1 1 
##  #5 + 3 -1 -b5 * . + 0 0 
##  #5 + 3 -1 * -b5 . | | | 
##  #5 + 4 0 -1 -1 : ++ 2 0 
##  #6 ind 1 4 5 5 fus ind 2 8 
##  #6 | 2 | 10 10 | | | 8 
##  #5 - 2 0 b5 * . - 0 0 
##  #5 - 2 0 * b5 . | | | 
##  #5 - 6 0 1 1 : oo 0 i2 
##  #8
##  gap> StringOfCambridgeFormat( [ [ "L10(11)" ] ], 0 );
##  fail
##  ]]></Example>
##  <P/>
##  The global option <C>OmitDashedRows</C> can be used to control whether
##  the two-line description of <Q>dashed</Q> row portions
##  (concerning tables of, e. g., <M>2'.Sz(8)</M>)
##  are omitted (value <K>true</K>) or shown (value <K>false</K>).
##  The default is to show information about dashed row portions in the
##  case of ordinary tables, and to omit this information for Brauer tables.
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "StringOfCambridgeFormat" );


#############################################################################
##
##  5. Interface to the MAGMA display format
##
##  <#GAPDoc Label="interface_magma">
##  This interface is intended to convert character tables given in
##  <Package>MAGMA</Package>'s (see&nbsp;<Cite Key="CP96"/>) display format
##  into &GAP; character tables.
##  <P/>
##  The function <Ref Func="BosmaBase"/> is used for the translation of
##  irrational values; this function may be of interest independent of the
##  conversion of character tables.
##  <#/GAPDoc>
##


#############################################################################
##
#F  BosmaBase( <n> )
##
##  <#GAPDoc Label="BosmaBase">
##  <ManSection>
##  <Func Name="BosmaBase" Arg="n"/>
##
##  <Description>
##  For a positive integer <A>n</A> that is not congruent to <M>2</M> modulo
##  <M>4</M>, <Ref Func="BosmaBase"/> returns the list of exponents <M>i</M>
##  for which <C>E(<A>n</A>)^</C><M>i</M> belongs to the canonical basis of
##  the <A>n</A>-th cyclotomic field that is defined in
##  <Cite Key="Bos90" Where="Section&nbsp;5"/>.
##  <P/>
##  As a set, this basis is defined as follows.
##  Let <M>P</M> denote the set of prime divisors of <A>n</A> and
##  <A>n</A> <M>= \prod_{{p \in P}} n_p</M>.
##  Let <M>e_l =</M> <C>E</C><M>(l)</M> for any positive integer <M>l</M>,
##  and
##  <M>\{ e_{{m_1}}^j \}_{{j \in J}} \otimes \{ e_{{m_2}}^k \}_{{k \in K}} =
##  \{ e_{{m_1}}^j \cdot e_{{m_2}}^k \}_{{j \in J, k \in K}}</M>
##  for any positive integers <M>m_1</M>, <M>m_2</M>.
##  (This notation is the same as the one used in the description of
##  <Ref Func="ZumbroichBase" BookName="ref"/>.)
##  <P/>
##  Then the basis is
##  <Display Mode="M">
##  B_n = \bigotimes_{{p \in P}} B_{{n_p}}
##  </Display>
##  where
##  <Display Mode="M">
##  B_{{n_p}} = \{ e_{{n_p}}^k; 0 \leq k \leq \varphi(n_p)-1 \};
##  </Display>
##  here <M>\varphi</M> denotes Euler's function,
##  see <Ref Func="Phi" BookName="ref"/>.
##  <P/>
##  <M>B_n</M> consists of roots of unity, it is an integral basis
##  (that is, exactly the integral elements in <M>&QQ;_n</M> have integral
##  coefficients w.r.t.&nbsp;<M>B_n</M>,
##  cf.&nbsp;<Ref Func="IsIntegralCyclotomic" BookName="ref"/>),
##  and for any divisor <M>m</M> of <A>n</A> that is not congruent to
##  <M>2</M> modulo <M>4</M>, <M>B_m</M> is a subset of <M>B_n</M>.
##  <P/>
##  Note that the list <M>l</M>, say, that is returned by
##  <Ref Func="BosmaBase"/> is in general not a set.
##  The ordering of the elements in <M>l</M> fits to the coefficient lists
##  for irrational values used by <Package>MAGMA</Package>'s display format.
##  <P/>
##  <Example><![CDATA[
##  gap> b:= BosmaBase( 8 );
##  [ 0, 1, 2, 3 ]
##  gap> b:= Basis( CF(8), List( b, i -> E(8)^i ) );
##  Basis( CF(8), [ 1, E(8), E(4), E(8)^3 ] )
##  gap> Coefficients( b, Sqrt(2) );
##  [ 0, 1, 0, -1 ]
##  gap> Coefficients( b, Sqrt(-2) );
##  [ 0, 1, 0, 1 ]
##  gap> b:= BosmaBase( 15 );
##  [ 0, 5, 3, 8, 6, 11, 9, 14 ]
##  gap> b:= List( b, i -> E(15)^i );
##  [ 1, E(3), E(5), E(15)^8, E(5)^2, E(15)^11, E(5)^3, E(15)^14 ]
##  gap> Coefficients( Basis( CF(15), b ), EB(15) );
##  [ -1, -1, 0, 0, -1, -2, -1, -2 ]
##  gap> BosmaBase( 48 );
##  [ 0, 3, 6, 9, 12, 15, 18, 21, 16, 19, 22, 25, 28, 31, 34, 37 ]
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "BosmaBase" );


#############################################################################
##
#F  GAPTableOfMagmaFile( <file>, <identifier> )
#F  GAPTableOfMagmaFile( <str>, <identifier>, "string" )
##
##  <#GAPDoc Label="GAPTableOfMagmaFile">
##  <ManSection>
##  <Func Name="GAPTableOfMagmaFile" Arg='file, identifier'
##   Label="for a file"/>
##  <Func Name="GAPTableOfMagmaFile" Arg='str, identifier[, "string"]'
##   Label="for a string"/>
##
##  <Description>
##  In the first form,
##  let <A>file</A> be the name of a file that contains a character table in
##  <Package>MAGMA</Package>'s display format,
##  and <A>identifier</A> be a string.
##  <Ref Func="GAPTableOfMagmaFile" Label="for a file"/>
##  returns the corresponding &GAP; character table,
##  with <Ref Attr="Identifier" BookName="ref"/> value <A>identifier</A>.
##  <P/>
##  In the second form,
##  <A>str</A> must be a string that describes the contents of a file
##  as described for the first form, and the third argument must be the
##  string <C>"string"</C>.
##  <P/>
##  <Example><![CDATA[
##  gap> tmpdir:= DirectoryTemporary();;
##  gap> file:= Filename( tmpdir, "magmatable" );;
##  gap> str:= "\
##  > Character Table of Group G\n\
##  > --------------------------\n\
##  > \n\
##  > ---------------------------\n\
##  > Class |   1  2  3    4    5\n\
##  > Size  |   1 15 20   12   12\n\
##  > Order |   1  2  3    5    5\n\
##  > ---------------------------\n\
##  > p  =  2   1  1  3    5    4\n\
##  > p  =  3   1  2  1    5    4\n\
##  > p  =  5   1  2  3    1    1\n\
##  > ---------------------------\n\
##  > X.1   +   1  1  1    1    1\n\
##  > X.2   +   3 -1  0   Z1 Z1#2\n\
##  > X.3   +   3 -1  0 Z1#2   Z1\n\
##  > X.4   +   4  0  1   -1   -1\n\
##  > X.5   +   5  1 -1    0    0\n\
##  > \n\
##  > Explanation of Character Value Symbols\n\
##  > --------------------------------------\n\
##  > \n\
##  > # denotes algebraic conjugation, that is,\n\
##  > #k indicates replacing the root of unity w by w^k\n\
##  > \n\
##  > Z1     = (CyclotomicField(5: Sparse := true)) ! [\n\
##  > RationalField() | 1, 0, 1, 1 ]\n\
##  > ";;
##  gap> FileString( file, str );;
##  gap> tbl:= GAPTableOfMagmaFile( file, "MagmaA5" );;
##  gap> Display( tbl );
##  MagmaA5
##  
##       2  2  2  .  .  .
##       3  1  .  1  .  .
##       5  1  .  .  1  1
##  
##         1a 2a 3a 5a 5b
##      2P 1a 1a 3a 5b 5a
##      3P 1a 2a 1a 5b 5a
##      5P 1a 2a 3a 1a 1a
##  
##  X.1     1  1  1  1  1
##  X.2     3 -1  .  A *A
##  X.3     3 -1  . *A  A
##  X.4     4  .  1 -1 -1
##  X.5     5  1 -1  .  .
##  
##  A = -E(5)-E(5)^4
##    = (1-Sqrt(5))/2 = -b5
##  gap> tbl2:= GAPTableOfMagmaFile( str, "MagmaA5", "string" );;
##  gap> Irr( tbl ) = Irr( tbl2 );
##  true
##  gap> str:= "\
##  > Character Table of Group G\n\
##  > --------------------------\n\
##  > \n\
##  > ------------------------------\n\
##  > Class |   1  2   3   4   5   6\n\
##  > Size  |   1  1   1   1   1   1\n\
##  > Order |   1  2   3   3   6   6\n\
##  > ------------------------------\n\
##  > p  =  2   1  1   4   3   3   4\n\
##  > p  =  3   1  2   1   1   2   2\n\
##  > ------------------------------\n\
##  > X.1   +   1  1   1   1   1   1\n\
##  > X.2   +   1 -1   1   1  -1  -1\n\
##  > X.3   0   1  1   J-1-J-1-J   J\n\
##  > X.4   0   1 -1   J-1-J 1+J  -J\n\
##  > X.5   0   1  1-1-J   J   J-1-J\n\
##  > X.6   0   1 -1-1-J   J  -J 1+J\n\
##  > \n\
##  > \n\
##  > Explanation of Character Value Symbols\n\
##  > --------------------------------------\n\
##  > \n\
##  > J = RootOfUnity(3)\n\
##  > ";;
##  gap> FileString( file, str );;
##  gap> tbl:= GAPTableOfMagmaFile( file, "MagmaC6" );;
##  gap> Display( tbl );
##  MagmaC6
##  
##       2  1  1  1  1   1   1
##       3  1  1  1  1   1   1
##  
##         1a 2a 3a 3b  6a  6b
##      2P 1a 1a 3b 3a  3a  3b
##      3P 1a 2a 1a 1a  2a  2a
##  
##  X.1     1  1  1  1   1   1
##  X.2     1 -1  1  1  -1  -1
##  X.3     1  1  A /A  /A   A
##  X.4     1 -1  A /A -/A  -A
##  X.5     1  1 /A  A   A  /A
##  X.6     1 -1 /A  A  -A -/A
##  
##  A = E(3)
##    = (-1+Sqrt(-3))/2 = b3
##  ]]></Example>
##  <P/>
##  The <Package>MAGMA</Package> output for the above two examples
##  is obtained by the following commands.
##  <P/>
##  <Log>
##  > G1 := Alt(5);
##  > CT1 := CharacterTable(G1);
##  > CT1;
##  > G2:= CyclicGroup(6);
##  > CT2:= CharacterTable(G2);
##  > CT2;
##  </Log>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "GAPTableOfMagmaFile" );


#############################################################################
##
#F  UserPreference( "CTblLib", "MagmaPath" )
##
##  <#GAPDoc Label="MagmaPath">
##  <Subsection Label="subsect:magmapath">
##  <Heading>User preference <C>MagmaPath</C></Heading>
##  <Index Subkey="MagmaPath">user preferences</Index>
##
##  This preference describes the path for calling &MAGMA;.
##  An empty string (the default) means that &MAGMA; is not available.
##  <P/>
##  This preference is used by <Ref Func="CharacterTableComputedByMagma"/>.
##  </Subsection>
##  <#/GAPDoc>
##
##  We cannot set a reasonable default path:
##  Only a call to &MAGMA; would make sure that the program can be called,
##  and we do not want to get an error message on startup if not.
##
DeclareUserPreference( rec( name:= "MagmaPath",
    description:= [ "This preference describes the path for calling Magma. \
An empty string (the default) means that Magma is not available." ],
    default:= "" ) );


#############################################################################
##
#F  CharacterTableComputedByMagma( <G>, <identifier> )
##
##  <#GAPDoc Label="CharacterTableComputedByMagma">
##  <ManSection>
##  <Func Name="CharacterTableComputedByMagma" Arg="G, identifier"/>
##
##  <Description>
##  For a permutation group <A>G</A> and a string <A>identifier</A>,
##  <Ref Func="CharacterTableComputedByMagma"/> calls the &MAGMA; system
##  for computing the character table of <A>G</A>,
##  and converts the output into &GAP; format
##  (see <Ref Func="GAPTableOfMagmaFile" Label="for a string"/>).
##  The returned character table has the 
##  <Ref Attr="Identifier" BookName="ref"/> value <A>identifier</A>.
##  <P/>
##  If the &MAGMA; system is not available then <K>fail</K> is returned.
##  The availability of &MAGMA; is determined by calling &MAGMA;
##  where the path for this call is given by the user preference
##  <C>MagmaPath</C> of the package &CTblLib;;
##  if the value of this preference is empty
##  or if &MAGMA; cannot be called via this path then
##  &MAGMA; is regarded as not available.
##  <P/>
##  If the attribute <Ref Attr="ConjugacyClasses" BookName="ref"/>
##  of <A>G</A> is set before the call of
##  <Ref Func="CharacterTableComputedByMagma"/>
##  then the columns of the returned character table fit to the
##  conjugacy classes that are stored in <A>G</A>.
##  <P/>
##  <Example><![CDATA[
##  gap> if CTblLib.IsMagmaAvailable() then
##  >      g:= MathieuGroup( 24 );
##  >      ccl:= ConjugacyClasses( g );
##  >      t:= CharacterTableComputedByMagma( g, "testM24" );
##  >      if t = fail then
##  >        Print( "#E  Magma did not compute a character table.\n" );
##  >      elif ( not HasConjugacyClasses( t ) ) or
##  >           ( ConjugacyClasses( t ) <> ccl ) then
##  >        Print( "#E  The conjugacy classes do not fit.\n" );
##  >      elif TransformingPermutationsCharacterTables( t,
##  >               CharacterTable( "M24" ) ) = fail then
##  >        Print( "#E  Inconsistency of character tables?\n" );
##  >      fi;
##  >    fi;
##  ]]></Example>
##  </Description>
##  </ManSection>
##  <#/GAPDoc>
##
DeclareGlobalFunction( "CharacterTableComputedByMagma" );


#############################################################################
##
#E

