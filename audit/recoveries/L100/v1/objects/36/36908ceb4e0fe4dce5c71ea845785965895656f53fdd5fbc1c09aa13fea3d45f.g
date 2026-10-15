SetPackageInfo( rec(
PackageName := "Browse",
Version := "1.8.21",
Date := "01/03/2023",
License := "GPL-3.0-or-later",
Subtitle := "browsing applications and ncurses interface",
ArchiveURL := "https://www.math.rwth-aachen.de/~Browse/Browse-1.8.21",
ArchiveFormats := ".tar.bz2",
Persons := [
  rec(
  LastName := "Breuer",
  FirstNames := "Thomas",
  IsAuthor := true,
  IsMaintainer := true,
  Email := "Thomas.Breuer@Math.RWTH-Aachen.De",
  WWWHome := "https://www.math.rwth-aachen.de/~Thomas.Breuer",
  PostalAddress := "Thomas Breuer\nLehrstuhl für Algebra und Zahlentheorie\nRWTH Aachen\nPontdriesch 14/16\n52062 Aachen\nGERMANY\n",
  Place := "Aachen",
  Institution := "Lehrstuhl für Algebra und Zahlentheorie, RWTH Aachen"
  ),
  rec(
  LastName := "Lübeck",
  FirstNames := "Frank",
  IsAuthor := true,
  IsMaintainer := true,
  Email := "Frank.Luebeck@Math.RWTH-Aachen.De",
  WWWHome := "https://www.math.rwth-aachen.de/~Frank.Luebeck",
  PostalAddress := "Frank Lübeck\nLehrstuhl für Algebra und Zahlentheorie\nRWTH Aachen\nPontdriesch 14/16\n52062 Aachen\nGERMANY\n",
  Place := "Aachen",
  Institution := "Lehrstuhl für Algebra und Zahlentheorie, RWTH Aachen"
  )
],
Status := "deposited",
README_URL := "https://www.math.rwth-aachen.de/~Browse/README",
PackageInfoURL :=
           "https://www.math.rwth-aachen.de/~Browse/PackageInfo.g",
AbstractHTML := "The <span class='pkgname'>Browse</span> package provides three levels of functionality</p><ul><li>A <span class='pkgname'>GAP</span> interface to the C-library <a href='http://www.gnu.org/software/ncurses/ncurses.html'>ncurses</a>.</li><li>A generic function for interactive browsing through two-dimensional arrays of data.</li><li>Several applications of the first two, e.g., a method for browsing character tables, browsing through the content of some data collections, or some games.</li></ul><p>",
PackageWWWHome := "https://www.math.rwth-aachen.de/~Browse",
PackageDoc := [
              rec(
  BookName := "Browse",
  ArchiveURLSubset := ["doc"],
  HTMLStart := "doc/chap0.html",
  PDFFile := "doc/manual.pdf",
  SixFile := "doc/manual.six",
  LongTitle := "ncurses interface and browsing applications",
  Autoload := true
)
],
Dependencies := rec(
  GAP := "4.12.0",  # because of IsKernelExtensionAvailable
                    # and LoadKernelExtension
                    # (StripMarkupFromUserPreferenceDescription if available)
  NeededOtherPackages := [ ["GAPDoc", ">= 1.6"], ], # more robust treatment of entries in *.bib files
  SuggestedOtherPackages := [ ["AtlasRep",">=2.0"], [ "IO", ">=2.2" ] ],
  ExternalConditions := ["C-compiler", "ncurses development library"]
),
Extensions := [
  rec( needed:= [
         [ "IO", "" ],
       ],
       filename:= "app/io_only.g" ),
  rec( needed:= [
         [ "TomLib", ">= 1.2.0" ],
       ],
       filename:= "app/tmdbattr.g" ),
  rec( needed:= [
         [ "AtlasRep", ">= 1.5.0" ],
       ],
       filename:= "app/atlasrep_only.g" ),
],
AvailabilityTest := function()
  if not IsKernelExtensionAvailable("Browse", "ncurses") then
    LogPackageLoadingMessage( PACKAGE_WARNING,
        [ "kernel functions for ncurses not available." ] );
    if UserPreference("browse", "loadwithoutncurses") = true then
      return true;
    else
      return false;
    fi;
  fi;
  return true;
end,
Keywords := ["Browse", "ncurses"],

));

