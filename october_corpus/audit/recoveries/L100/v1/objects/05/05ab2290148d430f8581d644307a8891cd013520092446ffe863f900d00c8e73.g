####################################################################################################
##
##  PackageInfo.g                      GAP4 Package `ResClasses'                         Stefan Kohl
##
####################################################################################################

SetPackageInfo( rec(

PackageName      := "ResClasses",
Subtitle         := "Set-Theoretic Computations with Residue Classes",
Version          := "4.7.4",
Date             := "24/09/2025", # dd/mm/yyyy format
License          := "GPL-2.0-or-later",
Persons          := [
                      rec( LastName      := "Kohl",
                           FirstNames    := "Stefan",
                           IsAuthor      := true,
                           IsMaintainer  := true,
                           Email         := "sk239@st-andrews.ac.uk",
                           WWWHome       := "https://stefan-kohl.github.io/"
                         )
                    ],
Status           := "deposited",

PackageWWWHome  := "https://gap-packages.github.io/resclasses/",
README_URL      := Concatenation( ~.PackageWWWHome, "README"        ),
PackageInfoURL  := Concatenation( ~.PackageWWWHome, "PackageInfo.g" ),
SourceRepository := rec(
    Type := "git",
    URL := "https://github.com/gap-packages/resclasses",
),
IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                 "/releases/download/v", ~.Version,
                                 "/resclasses-", ~.Version ),
ArchiveFormats   := ".tar.gz",

AbstractHTML     := Concatenation("This package permits to compute with set-theoretic ",
                                  "unions of residue classes of&nbsp;Z and a few other rings. ",
                                  "In particular it provides methods for computing unions, ",
                                  "intersections and differences of these sets."),
PackageDoc       := rec(
                         BookName         := "ResClasses",
                         ArchiveURLSubset := ["doc"],
                         HTMLStart        := "doc/chap0_mj.html",
                         PDFFile          := "doc/manual.pdf",
                         SixFile          := "doc/manual.six",
                         LongTitle        := Concatenation("Computations with Residue Classes ",
                                                           "and their Set-Theoretic Unions"),
                       ),
Dependencies     := rec(
                         GAP                    := ">=4.11.1",
                         NeededOtherPackages    := [ ["GAPDoc",">=1.5.1"], ["Polycyclic",">=2.11"],
                                                     ["utils", ">=0.40"] ],
                         SuggestedOtherPackages := [ ["IO",">=4.4.5"] ],
                         ExternalConditions     := [ ]
                       ),
AvailabilityTest := ReturnTrue,
BannerString     := Concatenation( "\nLoading ResClasses ", ~.Version,
                                   " (Computations with Residue Classes)",
                                   "\nby Stefan Kohl, sk239@st-andrews.ac.uk\n\n" ),
TestFile         := "tst/testall.g",
Keywords         := [ "residue classes", "integers", "number theory" ],

AutoDoc := rec(
    TitlePage := rec(
        Copyright := """
&copyright; 2003 - 2017 by Stefan Kohl. <P/>

&ResClasses; is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version. <P/>

&ResClasses; is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details. <P/>

For a copy of the GNU General Public License, see 
the file <F>GPL</F> in the <F>etc</F> directory of the &GAP;
distribution or see <URL>https://www.gnu.org/licenses/gpl.html</URL>.
        """,
        Abstract := """<#Include SYSTEM "abstract.xml">""",
    ),
),

) );

####################################################################################################
##
#E  PackageInfo.g  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ends here
