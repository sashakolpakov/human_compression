###########################################################################
##  

SetPackageInfo( rec(

PackageName := "SglPPow",
Subtitle := "Database of groups of prime-power order for some prime-powers",
Version := "2.4",
Date := "20/03/2024",
License := "Artistic-2.0",

Persons := [
  rec(
    LastName      := "Vaughan-Lee",
    FirstNames    := "Michael",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "michael.vaughan-lee@chch.ox.ac.uk",
    WWWHome       := "https://users.ox.ac.uk/~vlee",
    Place         := "Oxford",
    Institution   := "Oxford University"),
  rec(
    LastName      := "Eick",
    FirstNames    := "Bettina",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "beick@tu-bs.de",
    WWWHome       := "http://www.iaa.tu-bs.de/beick",
    Place         := "Braunschweig",
    Institution   := "TU Braunschweig"),
],

Status           := "accepted",
CommunicatedBy   := "Leonard Soicher (QMUL)",
AcceptDate       := "08/2016",

PackageWWWHome  := "https://gap-packages.github.io/sglppow/",
README_URL      := Concatenation( ~.PackageWWWHome, "README.md" ),
PackageInfoURL  := Concatenation( ~.PackageWWWHome, "PackageInfo.g" ),
SourceRepository := rec(
    Type := "git",
    URL := "https://github.com/gap-packages/sglppow",
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/sglppow-", ~.Version ),
ArchiveFormats := ".tar.gz",

AbstractHTML := "",

PackageDoc := rec(
  BookName  := "SglPPow",
  ArchiveURLSubset := ["doc","htm"],
  HTMLStart := "htm/chapters.htm",
  PDFFile   := "doc/manual.pdf",
  SixFile   := "doc/manual.six",
  LongTitle := "Database of groups of prime-power order",
),

AvailabilityTest := ReturnTrue,

Dependencies := rec(
  GAP := ">=4.7",
  NeededOtherPackages := [],
  SuggestedOtherPackages := [["LiePRing", ">=1.8"],["LieRing", ">=2.2"]],
  ExternalConditions := []
),

BannerString := Concatenation(
    "----------------------------------------------------------------\n",
    "Loading SglPPow ", ~.Version, "\n",
    "by Michael Vaughan-Lee and Bettina Eick \n",
    "----------------------------------------------------------------\n" ),

TestFile := "tst/testall.g",

Keywords := ["", "", ""]

));

