#############################################################################
##
##  PackageInfo file for the FORMAT package.   
##                                       Bettina Eick and Charles R.B. Wright
##

SetPackageInfo( rec(

PackageName := "FORMAT",
Subtitle := "Computing with formations of finite solvable groups.",
Version := "1.4.4",
Date := "09/01/2024", # dd/mm/yyyy format
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
      Institution   := "TU Braunschweig"
    ),

  rec(
      LastName := "Wright",
      FirstNames := "Charles R.B.",
      IsAuthor := true,
      IsMaintainer := false,
      Email := "wright@uoregon.edu",
      WWWHome := "https://pages.uoregon.edu/wright/",
      Place := "Eugene",
      Institution := "University of Oregon"
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
CommunicatedBy := "Joachim Neubüser (Aachen)",
AcceptDate := "12/2000",

PackageWWWHome  := "https://gap-packages.github.io/format/",
README_URL      := Concatenation( ~.PackageWWWHome, "README.md" ),
PackageInfoURL  := Concatenation( ~.PackageWWWHome, "PackageInfo.g" ),
SourceRepository := rec(
    Type := "git",
    URL := "https://github.com/gap-packages/format",
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/format-", ~.Version ),
ArchiveFormats := ".tar.gz",

AbstractHTML := "This package provides functions for computing with \
formations of finite solvable groups.",

PackageDoc := rec(
  BookName := "FORMAT",
  ArchiveURLSubset := ["doc", "htm"],
  HTMLStart := "htm/chapters.htm",
  PDFFile := "doc/manual.pdf",
  SixFile := "doc/manual.six",
  LongTitle := "Formations of Finite Soluble Groups",
  Autoload := true
),

Dependencies := rec(
  GAP := ">=4.5",
  NeededOtherPackages := [],
  SuggestedOtherPackages := [],
  ExternalConditions := []
),

AvailabilityTest := ReturnTrue,

TestFile := "tst/testall.g",

Keywords := ["formations", "soluble", "group"]

));

