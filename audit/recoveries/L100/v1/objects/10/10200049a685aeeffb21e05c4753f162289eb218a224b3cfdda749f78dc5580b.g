#############################################################################
##  
SetPackageInfo( rec(

PackageName := "fwtree",
Subtitle := "Computing trees related to some pro-p-groups of finite width",
Version := "1.3",
Date := "28/01/2020", # dd/mm/yyyy format
License := "GPL-2.0-or-later",

Persons := [
  rec(
    LastName      := "Eick",
    FirstNames    := "Bettina",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "beick@tu-bs.de",
    WWWHome       := "http://www.iaa.tu-bs.de/beick",
    PostalAddress := Concatenation(
               "Institut Analysis und Algebra\n",
               "TU Braunschweig\n",
               "Universitätsplatz 2\n",
               "D-38106 Braunschweig\n",
               "Germany" ),
    Place         := "Braunschweig",
    Institution   := "TU Braunschweig"),

  rec(
    LastName      := "Rossmann",
    FirstNames    := "Tobias",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "tobias.rossmann@googlemail.com",
    PostalAddress := Concatenation( [
                       "School of Mathematics, Statistics and Applied Mathematics\n",
                       "National University of Ireland, Galway\n",
                       "University Road, Galway\n",
                       "Ireland" ] ),
    Place         := "Galway",
    Institution   := "NUI Galway"),

  rec(
    LastName      := "GAP Team",
    FirstNames    := "The",
    IsAuthor      := false,
    IsMaintainer  := true,
    Email         := "support@gap-system.org",
  ),

],

Status := "deposited",

PackageWWWHome  := "https://gap-packages.github.io/fwtree/",
README_URL      := Concatenation( ~.PackageWWWHome, "README" ),
PackageInfoURL  := Concatenation( ~.PackageWWWHome, "PackageInfo.g" ),
SourceRepository := rec(
    Type := "git",
    URL := "https://github.com/gap-packages/fwtree",
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/fwtree-", ~.Version ),
ArchiveFormats := ".tar.gz",

AbstractHTML :=
  "The <span class=\"pkgname\">fwtree</span> package contains some code related to the computation of trees corresponding to some groups of finite rank, width and obliquity.",

PackageDoc := rec(
  BookName  := "fwtree",
  ArchiveURLSubset := ["doc", "htm"],
  HTMLStart := "htm/chapters.htm",
  PDFFile   := "doc/manual.pdf",
  SixFile   := "doc/manual.six",
  LongTitle := "Computing trees related to some pro-p-groups of finite width",
  Autoload  := true
),

Dependencies := rec(
  GAP := ">=4.4",
  NeededOtherPackages := [["Polycyclic", ">=1.0"],
                          ["Autpgrp", ">=1.0"],
                          ["anupq",">=1.0"]],
  SuggestedOtherPackages := [["XGAP", ">=1.0"]],
  ExternalConditions := []
),

TestFile := "tst/testall.g",
AvailabilityTest := ReturnTrue,
Keywords := ["finite width", "p-groups", "trees"],
 
));
