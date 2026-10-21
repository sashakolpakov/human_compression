#############################################################################
##  
##  PackageInfo.g for the package `ITC'                        Volkmar Felsch

SetPackageInfo( rec(

PackageName := "ITC",
Subtitle := "Interactive Todd-Coxeter",
Version := "1.5.1",
Date := "01/03/2022", # dd/mm/yyyy format
License := "GPL-2.0-or-later",

Persons := [
  rec(
  LastName := "Felsch",
  FirstNames := "Volkmar",
  IsAuthor := true,
  IsMaintainer := false,
  Email := "Volkmar.Felsch@math.rwth-aachen.de",
  WWWHome := "http://www.math.rwth-aachen.de/LDFM/homes/Volkmar.Felsch/",
  Place := "Aachen",
  Institution := "Lehrstuhl D für Mathematik, RWTH Aachen"
  ),
  rec(
  LastName := "Hippe",
  FirstNames := "Ludger",
  IsAuthor := true,
  IsMaintainer := false,
  ),
  rec(
  LastName := "Neubüser",
  FirstNames := "Joachim",
  IsAuthor := true,
  IsMaintainer := false,
  Email := "Joachim.Neubueser@math.rwth-aachen.de",
  WWWHome := "http://www.math.rwth-aachen.de/LDFM/homes/Joachim.Neubueser/",
  Place := "Aachen",
  Institution := "Lehrstuhl D für Mathematik, RWTH Aachen"
  ),
  rec(
    LastName      := "GAP Team",
    FirstNames    := "The",
    IsAuthor      := false,
    IsMaintainer  := true,
    Email         := "support@gap-system.org",
  ),
],

Status := "accepted",
CommunicatedBy := "Edmund F. Robertson (St Andrews)",
AcceptDate := "03/2000",

PackageWWWHome  := "https://gap-packages.github.io/itc/",
README_URL      := Concatenation( ~.PackageWWWHome, "README" ),
PackageInfoURL  := Concatenation( ~.PackageWWWHome, "PackageInfo.g" ),
SourceRepository := rec(
    Type := "git",
    URL := "https://github.com/gap-packages/itc",
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/itc-", ~.Version ),
ArchiveFormats := ".tar.gz",

AbstractHTML :=
  "This <span class=\"pkgname\">GAP</span> package provides \
   access to interactive Todd-Coxeter computations \
   with finitely presented groups.",

PackageDoc := rec(
  BookName := "ITC",
  ArchiveURLSubset := ["doc", "htm"],
  HTMLStart := "htm/chapters.htm",
  PDFFile := "doc/manual.pdf",
  SixFile := "doc/manual.six",
  LongTitle := "Interactive Todd-Coxeter computations",
  Autoload := true
),

Dependencies := rec(
  GAP := "4.8",
  NeededOtherPackages := [["xgap", ">= 4.02"]],
  SuggestedOtherPackages := [],
  ExternalConditions := []
                      
),

AvailabilityTest := function()
      local test;
      test:= TestPackageAvailability( "xgap", "4.02" );
      if   test = fail then
        Info( InfoWarning, 1,
          "Package `itc' needs package `xgap' version at least 4.02" );
      elif test <> true then
        Info( InfoWarning, 1,
          "Package `itc' must be loaded from XGAP" );
      fi;
      return test = true;
    end,

BannerString := Concatenation(
    "\n",
    "          Loading  ITC ", ~.Version, "  (", ~.Subtitle, ")\n",
    "            by V. Felsch, L. Hippe, and J. Neubueser\n",
    "              (", ~.Persons[1].Email, ")\n\n" ),

Autoload := false,

#TestFile := "tst/testall.g",

Keywords := ["interactive Todd-Coxeter", "coset enumeration"]

));
