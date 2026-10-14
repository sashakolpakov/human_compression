#############################################################################
##
##  PackageInfo.g for the GAP 4 package CTblLib                 Thomas Breuer
##
SetPackageInfo( rec(
PackageName :=
  "CTblLib",
Dates_all := [
  [ "2002-01-21", "1.0" ],
  [ "2003-11-18", "1.1.0" ],
  [ "2003-11-20", "1.1.1" ],
  [ "2003-11-27", "1.1.2" ],
  [ "2004-03-31", "1.1.3" ],
  [ "2012-05-07", "1.2.0" ],
  [ "2012-05-30", "1.2.1" ],
  [ "2013-03-07", "1.2.2" ],
  [ "2019-12-30", "1.3.0" ],
  [ "2020-04-08", "1.3.1" ],
  [ "2021-03-28", "1.3.2" ],
  [ "2022-01-02", "1.3.3" ],
  [ "2022-04-26", "1.3.4" ],
  [ "2023-03-07", "1.3.5" ],
  [ "2023-05-16", "1.3.6" ],
  [ "2024-01-01", "1.3.7" ],
  [ "2024-03-13", "1.3.8" ],
  [ "2024-03-14", "1.3.9" ],
  [ "2025-05-05", "1.3.10" ],
  [ "2025-05-25", "1.3.11" ],
  ],
Version :=
  Last( ~.Dates_all )[2],
Date :=
  Last( ~.Dates_all )[1],
MyWWWHome :=
  "https://www.math.rwth-aachen.de/~Thomas.Breuer",
Subtitle :=
  "The GAP Character Table Library",
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
#   rec(  
#     LastName      := "Claßen-Houben",
#     FirstNames    := "Michael",
#     IsAuthor      := true, 
#     IsMaintainer  := false,
#     Email         := "michael@oph.rwth-aachen.de",
#     Place         := "Aachen",
#     Institution   := "RWTH Aachen"
#   ),
  ],
Status :=
  "deposited",
README_URL :=
  Concatenation( ~.PackageWWWHome, "/README.md" ),
PackageInfoURL :=
  Concatenation( ~.PackageWWWHome, "/PackageInfo.g" ),
AbstractHTML := Concatenation( [
  "The package contains the <span class=\"pkgname\">GAP</span> ",
  "Character Table Library."
  ] ),
PackageDoc := [
  rec(
    BookName :=
      "CTblLib",
    ArchiveURLSubset :=
      [ "doc", "htm" ],  # files in htm are cross-references from the manual
    HTMLStart :=
      "doc/chap0.html",
    PDFFile :=
      "doc/manual.pdf",
    SixFile :=
      "doc/manual.six",
    LongTitle :=
      "The GAP Character Table Library",
  ),
  rec(
    BookName :=
      "CTblLibXpls",
    ArchiveURLSubset :=
      [ "doc2" ],
    HTMLStart :=
      "doc2/chap0.html",
    PDFFile :=
      "doc2/manual.pdf",
    SixFile :=
      "doc2/manual.six",
    LongTitle :=
      "Computations with the GAP Character Table Library",
  ) ],
Dependencies := rec(
  GAP :=
    ">= 4.13.0",                 # want package extensions
  OtherPackagesLoadedInAdvance := [
    ],
  NeededOtherPackages := [
      [ "gapdoc", ">= 1.6.2" ],  # want extended `InitialSubstringUTF8String'
      [ "AtlasRep", ">= 2.1" ],  # want the JSON interface,
                                 # want the user preference `DisplayFunction',
                                 # want `AGR.Pager',
                                 # want `ScanMeatAxeFile'
    ],
  SuggestedOtherPackages := [
      [ "Browse", ">= 1.8.10" ],  # because of overview functions,
                                  # want new JSON related features
      [ "chevie", ">= 1.0" ],     # because of Deligne-Lusztig names
      [ "PrimGrp", ">= 1.0" ],    # because of group info
      [ "SmallGrp", ">= 1.0" ],   # because of group info
      [ "SpinSym", ">= 1.5" ],    # because SpinSym extends the library
      [ "tomlib", ">= 1.0" ],     # because of the interface
      [ "TransGrp", ">= 1.0" ],   # because of group info
    ],
  ExternalConditions := [
    ],
  ),
Extensions := [
    rec( needed:= [
             [ "Browse", ">= 1.8.10" ],
           ],
         filename:= "gap4/browse_only.g" ),
    rec( needed:= [
             [ "AtlasRep", ">= 2.1" ],
           ],
         filename:= "gap4/atlasrep_only.g" ),
    rec( needed:= [
             [ "tomlib", ">= 1.0" ],
           ],
         filename:= "gap4/tomlib_only.g" ),
    rec( needed:= [
             [ "SpinSym", ">= 1.5" ],
           ],
         filename:= "gap4/spinsym_only.g" ),
    rec( needed:= [
             [ "chevie", ">= 1.0" ],
           ],
         filename:= "gap4/chevie_only.g" ),
  ],
AvailabilityTest :=
  ReturnTrue,
TestFile :=
  "tst/testauto.g",  # regularly running `tst/testall.g' is not acceptable
Keywords :=
  [ "ordinary character table", "Brauer table", "generic character table",
    "decomposition matrix", "class fusion", "power map",
    "permutation character", "table automorphism",
    "central extension", "projective character",
    "Atlas Of Finite Groups" ],
) );


#############################################################################
##
#E

