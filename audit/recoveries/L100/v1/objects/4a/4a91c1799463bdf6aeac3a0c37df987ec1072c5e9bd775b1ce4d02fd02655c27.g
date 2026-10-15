#############################################################################
##
##  PackageInfo.g for the GAP 4 package AtlasRep                Thomas Breuer
##
SetPackageInfo( rec(
PackageName :=
  "AtlasRep",
Dates_all := [
  [ "03/04/2001", "1.0" ],
  [ "23/10/2002", "1.1" ],
  [ "06/11/2003", "1.2" ],
  [ "05/04/2004", "1.2.1" ],
  [ "06/06/2007", "1.3" ],
  [ "01/10/2007", "1.3.1" ],
  [ "23/06/2008", "1.4" ],
  [ "12/07/2011", "1.5.0" ],
  [ "30/03/2016", "1.5.1" ],
  [ "02/05/2019", "2.0.0" ],
  [ "10/05/2019", "2.1.0" ],
  [ "23/02/2022", "2.1.1" ],
  [ "30/03/2022", "2.1.2" ],
  [ "04/08/2022", "2.1.3" ],
  [ "05/08/2022", "2.1.4" ],
  [ "22/08/2022", "2.1.5" ],
  [ "19/10/2022", "2.1.6" ],
  [ "17/08/2023", "2.1.7" ],
  [ "03/01/2024", "2.1.8" ],
  [ "27/08/2024", "2.1.9" ],
  ],
Version :=
  Last( ~.Dates_all )[2],
Date :=
  Last( ~.Dates_all )[1],
MyWWWHome :=
  "https://www.math.rwth-aachen.de/~Thomas.Breuer",
Subtitle :=
  "A GAP Interface to the Atlas of Group Representations",
License :=
  "GPL-3.0-or-later",
PackageWWWHome :=
  Concatenation( ~.MyWWWHome, "/", LowercaseString( ~.PackageName ) ),
ArchiveURL :=
  Concatenation( ~.PackageWWWHome, "/", LowercaseString( ~.PackageName ),
                 "-", ~.Version ),
ArchiveFormats :=
  ".tar.gz",
Persons := [
  rec(
    LastName := "Wilson",
    FirstNames := "Robert A.",
    IsAuthor := true,
    IsMaintainer := false,
    Email := "R.A.Wilson@qmul.ac.uk",
    WWWHome := "http://www.maths.qmw.ac.uk/~raw",
    Place := "London",
    Institution := Concatenation( [
      "School of Mathematical Sciences, ",
      "Queen Mary, University of London",
      ] ),
    ),
  rec(
    LastName := "Parker",
    FirstNames := "Richard A.",
    IsAuthor := true,
    IsMaintainer := false,
    Email := "richpark7920@gmail.com",
  ),
  rec(
    LastName := "Nickerson",
    FirstNames := "Simon",
    IsAuthor := true,
    IsMaintainer := false,
    WWWHome := "http://nickerson.org.uk/groups",
    Institution := Concatenation( [
      "School of Mathematics, ",
      "University of Birmingham",
      ] ),
  ),
  rec(
    LastName := "Bray",
    FirstNames := "John N.",
    IsAuthor := true,
    IsMaintainer := false,
    Email := "J.N.Bray@qmul.ac.uk",
    WWWHome := "http://www.maths.qmw.ac.uk/~jnb",
    Place := "London",
    Institution := Concatenation( [
      "School of Mathematical Sciences, ",
      "Queen Mary, University of London",
      ] ),
  ),
  rec(
    LastName := "Breuer",
    FirstNames := "Thomas",
    IsAuthor := true,
    IsMaintainer := true,
    Email := "sam@math.rwth-aachen.de",
    WWWHome := ~.MyWWWHome,
    Place := "Aachen",
    Institution := "Lehrstuhl für Algebra und Zahlentheorie, RWTH Aachen",
    PostalAddress := Concatenation( [
      "Thomas Breuer\n",
      "Lehrstuhl für Algebra und Zahlentheorie\n",
      "Pontdriesch 14/16\n",
      "52062 Aachen\n",
      "Germany"
      ] ),
  ),
  ],
Status :=
  "accepted",
CommunicatedBy :=
  "Herbert Pahlings (Aachen)",
AcceptDate :=
  "04/2001",
README_URL :=
  Concatenation( ~.PackageWWWHome, "/README.md" ),
PackageInfoURL :=
  Concatenation( ~.PackageWWWHome, "/PackageInfo.g" ),
AbstractHTML := Concatenation( [
  "The package provides a <span class=\"pkgname\">GAP</span> interface ",
  "to the <a href=\"http://atlas.math.rwth-aachen.de/Atlas/v3\">",
  "Atlas of Group Representations</a>"
  ] ),
PackageDoc := rec(
  BookName :=
    "AtlasRep",
  ArchiveURLSubset :=
    [ "doc" ],
  HTMLStart :=
    "doc/chap0.html",
  PDFFile :=
    "doc/manual.pdf",
  SixFile :=
    "doc/manual.six",
  LongTitle :=
    "An Atlas of Group Representations",
  ),
Dependencies := rec(
  GAP :=
    ">= 4.11.0",  # need extended 'IntegratedStraightLineProgram'
#T could require 4.12.0, because of IsMatrixOrMatrixObj (and simplify code)
  NeededOtherPackages := [
      [ "gapdoc", ">= 1.6.2" ],  # want extended 'InitialSubstringUTF8String'
      [ "utils", ">= 0.77" ],  # want 'Download'
    ],
  SuggestedOtherPackages := [
      [ "browse", ">= 1.8.3" ], # want extended 'BrowseAtlasInfo'
      [ "ctbllib", ">= 1.2" ], # want 'StructureDescriptionCharacterTableName'
      [ "ctblocks", ">= 1.0" ], # yields a data extension
      [ "io", ">= 3.3" ], # want 'IO_chmod', 'IO_mkdir', 'IO_stat'
      [ "mfer", ">= 1.0" ], # yields a data extension
      [ "recog", ">= 1.3.1" ], # because of some functions in 'gap/test.g'
      [ "standardff", ">= 0.9" ], # support the fields when creating matrices
      [ "tomlib", ">= 1.0" ], # used in tests and min. degree computations
    ],
  ExternalConditions :=
    []
  ),
Extensions := [
    rec( needed:= [
             [ "Browse", ">= 1.8.3" ],
           ],
         filename:= "gap/browse_only.g" ),
    rec( needed:= [
             [ "CTblLib", ">= 1.2" ],
           ],
         filename:= "gap/ctbllib_only.g" ),
    rec( needed:= [
             [ "Browse", ">= 1.8.3" ],
             [ "CTblLib", ">= 1.2" ],
           ],
         filename:= "gap/browsectbllib_only.g" ),
  ],
AvailabilityTest :=
  ReturnTrue,
TestFile :=
  "tst/testauto.g",
Keywords :=
  [ "group representations", "finite simple groups" ],
) );


#############################################################################
##
#E

