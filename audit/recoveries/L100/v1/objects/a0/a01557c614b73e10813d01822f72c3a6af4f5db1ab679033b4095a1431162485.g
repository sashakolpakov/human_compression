#
# uuid: RFC 4122 UUIDs
#
# This file contains package meta data. For additional information on
# the meaning and correct usage of these fields, please consult the
# manual of the "Example" package as well as the comments in its
# PackageInfo.g file.
#
SetPackageInfo( rec(

PackageName := "uuid",
Subtitle := "RFC 4122 UUIDs",
Version := "0.7",
Date := "01/03/2022", # dd/mm/yyyy format
License := "BSD-3-Clause",

Persons := [
  rec(
    IsAuthor := true,
    IsMaintainer := false,
    FirstNames := "Markus",
    LastName := "Pfeiffer",
    WWWHome := "http://www.morphism.de/~markusp/",
    Email := "markus.pfeiffer@morphism.de",
    PostalAddress := Concatenation(
             "School of Computer Science",
             "Jack Cole Building",
             "North Haugh",
             "St Andrews",
             "Fife",
             "KY16 9SS",
             "Scotland"),
    Place := "St Andrews",
    Institution := "University of St Andrews",
  ),
  rec(
    LastName      := "GAP Team",
    FirstNames    := "The",
    IsAuthor      := false,
    IsMaintainer  := true,
    Email         := "support@gap-system.org",
  ),
],

PackageWWWHome := "https://gap-packages.github.io/uuid/",

ArchiveURL     := Concatenation("https://github.com/gap-packages/uuid/",
                                "releases/download/v", ~.Version,
                                "/uuid-", ~.Version),
README_URL     := Concatenation( ~.PackageWWWHome, "README.md" ),
PackageInfoURL := Concatenation( ~.PackageWWWHome, "PackageInfo.g" ),
SourceRepository := rec( 
  Type := "git", 
  URL := "https://github.com/gap-packages/uuid"
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
ArchiveFormats := ".tar.gz",

##  Status information. Currently the following cases are recognized:
##    "accepted"      for successfully refereed packages
##    "submitted"     for packages submitted for the refereeing
##    "deposited"     for packages for which the GAP developers agreed
##                    to distribute them with the core GAP system
##    "dev"           for development versions of packages
##    "other"         for all other packages
##
Status := "deposited",

AbstractHTML   :=  "UUIDs for GAP",

PackageDoc := rec(
  BookName  := "uuid",
  ArchiveURLSubset := ["doc"],
  HTMLStart := "doc/chap0.html",
  PDFFile   := "doc/manual.pdf",
  SixFile   := "doc/manual.six",
  LongTitle := "RFC 4122 UUIDs",
),

Dependencies := rec(
  GAP := ">= 4.8",
  NeededOtherPackages := [ [ "GAPDoc", ">= 1.5" ] ],
  SuggestedOtherPackages := [ ],
  ExternalConditions := [ ],
),

AvailabilityTest := function()
        return true;
    end,

TestFile := "tst/testall.g",

Keywords := [ "UUID", "RFC4122" ],

));


