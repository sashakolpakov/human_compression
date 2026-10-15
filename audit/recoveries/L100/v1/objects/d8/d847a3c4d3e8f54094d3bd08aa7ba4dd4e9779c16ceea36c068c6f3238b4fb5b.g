#############################################################################
##  
##  PackageInfo.g for the package `Aclib'                      Bettina Eick
##  

SetPackageInfo( rec(

PackageName := "AClib",
Subtitle := "Almost Crystallographic Groups - A Library and Algorithms",
Version := "1.3.3",
Date := "28/08/2025", # dd/mm/yyyy format
License := "Artistic-2.0",

Persons := [
   rec(
      LastName      := "Dekimpe",
      FirstNames    := "Karel",
      IsAuthor      := true,
      IsMaintainer  := false,
      Email         := "Karel.Dekimpe@kuleuven.be",
      WWWHome       := "https://www.kuleuven-kulak.be/~dekimpe/",
      PostalAddress := Concatenation( [
                       "Katholieke Universiteit Leuven\n",
                       "Campus Kortrijk, Universitaire Campus\n",
                       "Kortrijk, B 8500\n",
                       "Belgium"]),
      Place         := "Kortrijk",
      Institution   := "KU Leuven Kulak"),

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
      Institution   := "TU Braunschweig") ],

Status := "accepted",
CommunicatedBy := "Gerhard Hiss (Aachen)",
AcceptDate := "02/2001",

PackageWWWHome  := "https://gap-packages.github.io/aclib/",
README_URL      := Concatenation( ~.PackageWWWHome, "README" ),
PackageInfoURL  := Concatenation( ~.PackageWWWHome, "PackageInfo.g" ),
SourceRepository := rec(
    Type := "git",
    URL := "https://github.com/gap-packages/aclib",
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/aclib-", ~.Version ),
ArchiveFormats := ".tar.gz",

AbstractHTML := 
"The <span class=\"pkgname\">AClib</span> package contains a library of almost crystallographic groups and a some algorithms to compute with these groups. A group is called almost crystallographic if it is finitely generated nilpotent-by-finite and has no non-trivial finite normal subgroups. Further, an almost crystallographic group is called almost Bieberbach if it is torsion-free. The almost crystallographic groups of Hirsch length 3 and a part of the almost cyrstallographic groups of Hirsch length 4 have been classified by Dekimpe. This classification includes all almost Bieberbach groups of Hirsch lengths 3 or 4. The AClib package gives access to this classification; that is, the package contains this library of groups in a computationally useful form. The groups in this library are available in two different representations. First, each of the groups of Hirsch length 3 or 4 has a rational matrix representation of dimension 4 or 5, respectively, and such representations are available in this package. Secondly, all the groups in this libraray are (infinite) polycyclic groups and the package also incorporates polycyclic presentations for them. The polycyclic presentations can be used to compute with the given groups using the methods of the Polycyclic package.",

PackageDoc := rec(
  BookName  := "AClib",
  ArchiveURLSubset := ["doc", "htm"],
  HTMLStart := "htm/chapters.htm",
  PDFFile   := "doc/manual.pdf",
  SixFile   := "doc/manual.six",
  LongTitle := "Almost Crystallographic Groups - A Library and Algorithms",
),

Dependencies := rec(
  GAP := ">=4.7",
  NeededOtherPackages := [["polycyclic",">=1.0"]],
  SuggestedOtherPackages := [["crystcat",">=1.1"]],
  ExternalConditions := [] ),

AvailabilityTest := ReturnTrue,

TestFile := "tst/testall.g",

Keywords := ["almost crystallographic groups", "almost Bieberbach group",
             "virtually nilpotent group", "nilpotent-by-finite group", 
             "datalibrary of almost Bieberbach groups"]

));


