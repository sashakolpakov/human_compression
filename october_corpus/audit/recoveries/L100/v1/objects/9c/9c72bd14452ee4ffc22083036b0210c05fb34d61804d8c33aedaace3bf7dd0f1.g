#############################################################################
##
##  PackageInfo.g for the package "SymbCompCC"       Dörte Feichtenschlager
##

SetPackageInfo( rec(
PackageName := "SymbCompCC",
Subtitle := "Computing with parametrised presentations for p-groups of fixed coclass",
Version := "1.3.2",
Date := "10/02/2022", # dd/mm/yyyy format
License := "GPL-2.0-or-later",

Persons := [
  rec(
    LastName      := "Feichtenschlager",
    FirstNames    := "Dörte",
    IsAuthor      := true,
    IsMaintainer  := false,
    Email         := "d.feichtenschlager@tu-braunschweig.de",
    PostalAddress := Concatenation([
                     "Institut Computational Mathematics\n",
                     "TU Braunschweig\n",
                     "Pockelsstr. 14 \n D-38106 Braunschweig \n Germany"] ),
    Place         := "Braunschweig",
    Institution   := "TU Braunschweig"
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
CommunicatedBy := "Mike Newman (Canberra, Australia)",
AcceptDate := "11/2011",

PackageWWWHome  := "https://gap-packages.github.io/SymbCompCC/",
README_URL      := Concatenation( ~.PackageWWWHome, "README" ),
PackageInfoURL  := Concatenation( ~.PackageWWWHome, "PackageInfo.g" ),
SourceRepository := rec(
    Type := "git",
    URL := "https://github.com/gap-packages/SymbCompCC",
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/SymbCompCC-", ~.Version ),
ArchiveFormats := ".tar.gz",

AbstractHTML :=
  "The <span class=\"pkgname\">SymbCompCC</span> package computes with parametrised presentations for finite p-groups of fixed coclass.",

PackageDoc := rec(
BookName  := "SymbCompCC",
ArchiveURLSubset := ["doc", "htm"],
HTMLStart := "htm/chapters.htm",
PDFFile   := "doc/manual.pdf",
SixFile   := "doc/manual.six",
LongTitle := "SymbCompCC/Symbolic computation with p-groups of fixed coclass",
Autoload  := false
),

Dependencies := rec(
  GAP := ">=4.7",
  NeededOtherPackages := [["polycyclic", ">= 2.11"]],
  ExternalConditions := []
),

AvailabilityTest := ReturnTrue,
TestFile         := "tst/testall.g",
Keywords := ["parametrised presentations for p-groups of fixed coclass and calculations with these"]

));

