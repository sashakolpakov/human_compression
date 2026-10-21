#############################################################################
##
#W  PackageInfo.g          liealgdb Package                  Csaba Schneider
##


SetPackageInfo( rec(
  PackageName := "LieAlgDB",
  Subtitle := "A database of Lie algebras",
  Version := "2.3.0",
  Date    := "24/09/2025", # dd/mm/yyyy format
  License := "GPL-2.0-or-later",

  Persons := [

    rec(
      LastName      := "Cicalò",
      FirstNames    := "Serena",
      IsAuthor      := true,
      IsMaintainer  := false,
      Email         := "cicalo@science.unitn.it",
      PostalAddress := Concatenation( [
                         "Dipartimento di Matematica e Informatica\n",
                         "Via Ospedale 72\n",
                         "Italy" ]),
      Place         := "Cagliari",
      Institution   := "Universita' di Cagliari"

    ),

    rec(
      LastName      := "de Graaf",
      FirstNames    := "Willem Adriaan",
      IsAuthor      := true,
      IsMaintainer  := false,
      Email         := "degraaf@science.unitn.it",
      WWWHome       := "http://www.science.unitn.it/~degraaf",
      PostalAddress := Concatenation( [
                         "Dipartimento di Matematica\n",
                         "Via Sommarive 14\n",
                         "Italy" ]),
      Place         := "Trento",
      Institution   := "Universita' di Trento"
    ),

    rec(
      LastName      := "Schneider",
      FirstNames    := "Csaba",
      IsAuthor      := true,
      IsMaintainer  := false,
      Email         := "csaba@mat.ufmg.br",
      WWWHome       := "http://www.mat.ufmg.br/~csaba/",
      PostalAddress := Concatenation( [
                         "Departamento de Matemática\n",
                         "Instituto de Ciências Exatas\n",
                         "Universidade Federal de Minas Gerais (UFMG)\n",
                         "Belo Horizonte, Brasil" ]),
      Place         := "Belo Horizonte",
      Institution   := "Universidade Federal de Minas Gerais"
    ),

    rec(
      LastName      := "GAP Team",
      FirstNames    := "The",
      IsAuthor      := false,
      IsMaintainer  := true,
      Email         := "support@gap-system.org",
    ),
  ],

  Status  := "accepted",
  CommunicatedBy := "Bettina Eick (Braunschweig)",
  AcceptDate  := "09/2007",

  PackageWWWHome  := "https://gap-packages.github.io/liealgdb/",
  README_URL      := Concatenation( ~.PackageWWWHome, "README" ),
  PackageInfoURL  := Concatenation( ~.PackageWWWHome, "PackageInfo.g" ),
  SourceRepository := rec(
      Type := "git",
      URL := "https://github.com/gap-packages/liealgdb",
  ),
  IssueTrackerURL := Concatenation( ~.SourceRepository.URL, "/issues" ),
  ArchiveURL      := Concatenation( ~.SourceRepository.URL,
                                   "/releases/download/v", ~.Version,
                                   "/liealgdb-", ~.Version ),
  ArchiveFormats := ".tar.gz",

  AbstractHTML := "",

  PackageDoc := rec(
    BookName  := "LieAlgDB",
    ArchiveURLSubset := ["doc"],
    HTMLStart := "doc/chap0_mj.html",
    PDFFile   := "doc/manual.pdf",
    SixFile   := "doc/manual.six",
    LongTitle := "A library of Lie algebras",
  ),

  Dependencies := rec(
    GAP := ">= 4.8",
    NeededOtherPackages := [],
    SuggestedOtherPackages := [],
    ExternalConditions := []
  ),

  AvailabilityTest := ReturnTrue,
  TestFile := "tst/testall.g",
  Keywords := [ "Lie algebras" ],

  AutoDoc := rec(
      TitlePage := rec(
          Abstract := """
This package provides access to the classification of the following
families of Lie algebras:
<List>
<Item> non-solvable Lie algebras over finite fields up to dimension 6;
</Item>
<Item> nilpotent Lie algebras of dimension up to 9 over <A>GF(2)</A>, of dimension
up to 7 over <A>GF(3)</A> or <A>GF(5)</A>;</Item>
<Item> simple Lie algebras of dimensions between 7 and 9 over <A>GF(2)</A>;
</Item>
<Item> the classification of solvable Lie algebras of dimension at most 4;
</Item>
<Item> the classification of nilpotent Lie algebras of dimensions at most 6.
</Item>
</List>
""",
          Copyright := """
<Index>License</Index>
&copyright; 2006--2007 Willem de Graaf and Csaba Schneider<P/>
The &LieAlgDB; package is free software;
you can redistribute it and/or modify it under the terms of the
<URL Text="GNU General Public License">http://www.fsf.org/licenses/gpl.html</URL>
as published by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.
""",
          Acknowledgements := """
We are grateful to Andrea Caranti, Marco Costantini, Bettina Eick,
Helmut Strade, Michael Vaughan-Lee. Without
their help, interest, and encouragement, this package would not have been
made. We also acknowledge the effort of the referees to improve the
implementation and the documentation.<P/>
Serena Cical&#242; would like to thank the Centro de &#193;lgebra da
Universidade de Lisboa for their kind hospitality during July - December 2009 and May - September 2010, when the
classification of the 6-dimensional nilpotent Lie algebras over
fields of characteristic 2 was made and added to the package.
""",
      ),
  ),

));
