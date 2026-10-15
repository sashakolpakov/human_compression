#############################################################################
##  
##  PackageInfo.g for the package `IntPic'              Manuel Delgado
##                                                    

SetPackageInfo( rec(

PackageName := "IntPic",
Subtitle := "A package for drawing integers",
Version := "0.4.0",
#Version := "0.3.0 dev",
Date := "30/08/2024", # dd/mm/yyyy format
License := "GPL-2.0-or-later",
        
##  Information about authors and maintainers.
Persons := [
 rec(
    LastName      := "Delgado",
    FirstNames    := "Manuel",
    IsAuthor      := true,
    IsMaintainer  := true,
    Email         := "mdelgado@fc.up.pt",
    WWWHome       := "http://www.fc.up.pt/cmup/mdelgado/",
    PostalAddress := Concatenation( [
                   "CMUP, Departamento de Matemática\n",
                   "Faculdade de Ciências, Universidade do Porto\n",
                   "Rua do Campo Alegre s/n\n",
                   "4169-007 Porto\n",
                   "Portugal" ] ),
    Place         := "Porto",
    Institution   := "Faculdade de Ciências"
           )
            ],

Status := "deposited",       

SourceRepository := rec(
  Type := "git",
  URL := "https://github.com/gap-packages/intpic"
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
PackageWWWHome  := "https://gap-packages.github.io/intpic",
README_URL      := Concatenation( ~.PackageWWWHome, "/README.md" ),
PackageInfoURL  := Concatenation( ~.PackageWWWHome, "/PackageInfo.g" ),
ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/", ~.PackageName, "-", ~.Version ),
ArchiveFormats := ".tar.gz",
        
AbstractHTML := 
   "The <span class=\"pkgname\">IntPic</span> package, is a package for drawing integers, by emphasizing some subsets.",
                   

PackageDoc := rec(
  BookName  := "IntPic",
  ArchiveURLSubset := ["doc","images"],
  HTMLStart := "doc/chap0_mj.html",
  PDFFile   := "doc/manual.pdf",
  SixFile   := "doc/manual.six",
  LongTitle := "IntPic, a GAP package for drawing integers",
),
                   
Dependencies := rec(
  GAP := "4.7",
  NeededOtherPackages := [["numericalsgps", "1.0"], ["GAPDoc", "1.5"]],
  SuggestedOtherPackages := [],
  ExternalConditions := []

),

AvailabilityTest := ReturnTrue,
BannerString := Concatenation( 
  "----------------------------------------------------------------\n",
  "Loading  IntPic ", ~.Version, " (drawing integers)\n",
  "by ", ~.Persons[1].FirstNames, " ", ~.Persons[1].LastName,
        " (", ~.Persons[1].WWWHome, ")\n",
#  "   ", ~.Persons[2].FirstNames, " ", ~.Persons[2].LastName,"\n",
#        " (", ~.Persons[2].WWWHome, ")\n",
#  "   ", ~.Persons[3].FirstNames, " ", ~.Persons[3].LastName,
#        " (", ~.Persons[3].WWWHome, ")\n",
  "For help, type: ?IntPic;\n",
  "----------------------------------------------------------------\n" ),

TestFile := "tst/testall.g",

Keywords := ["emphasize", "highlight", "draw", "integer", "picture"]

                    ));
