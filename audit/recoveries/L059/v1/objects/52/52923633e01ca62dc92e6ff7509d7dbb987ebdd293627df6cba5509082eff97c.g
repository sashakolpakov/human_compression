L059Subdivision := rec(
  A_subdivision := Group( [ (4,8)(6,7), (2,4)(5,6), (1,2)(3,5)(4,6)(7,8) ] ),
  edges_original := [ [ 1, 2 ], [ 1, 4 ], [ 1, 8 ], [ 2, 6 ], [ 2, 7 ], 
      [ 3, 5 ], [ 3, 6 ], [ 3, 7 ], [ 4, 5 ], [ 4, 7 ], [ 5, 8 ], [ 6, 8 ] ],
  label := "VT3_8_2",
  n_original := 8,
  search := rec(
      method := "index_two_normalizer_extension",
      steps := [ rec(
              K := Group( [ (4,8)(6,7), (2,4)(5,6), (1,5)(2,3) ] ),
              N := Group( [ (4,8)(6,7), (2,8,4)(5,7,6), (1,6)(2,8)(3,4)(5,7), 
                  (1,5)(2,3)(4,8)(6,7), (1,2)(3,5)(4,6)(7,8) ] ),
              tests := [ rec(
                      reason := "preserves_parts",
                      x := () ), rec(
                      reason := "retained_class",
                      target := 1,
                      x := (1,2)(3,5)(4,6)(7,8) ) ] ), rec(
              K := 
               Group( [ (2,8,4)(5,7,6), (1,6)(2,8)(3,4)(5,7), 
                  (1,5)(2,3)(4,8)(6,7) ] ),
              N := 
               Group( [ (2,8,4)(5,7,6), (1,6)(2,8)(3,4)(5,7), 
                  (1,7)(2,4)(3,8)(5,6), (2,8)(5,7), (1,2,6,3,5,4)(7,8) ] ),
              tests := [ rec(
                      reason := "preserves_parts",
                      x := () ), rec(
                      reason := "preserves_parts",
                      x := (4,8)(6,7) ), rec(
                      reason := "retained_class",
                      target := 2,
                      x := (1,4,5,3,6,2)(7,8) ), rec(
                      reason := "retained_class",
                      target := 3,
                      x := (1,4,7,2)(3,6,8,5) ) ] ) ] ),
  witnesses := [ rec(
          B := Group( [ (4,8)(6,7) ] ),
          H := 
           Group( [ (4,8)(6,7), (2,4)(5,6), (1,5)(2,3), (1,2)(3,5)(4,6)(7,8) 
             ] ),
          H0 := Group( [ (4,8)(6,7), (2,8,4)(5,7,6) ] ),
          H1 := Group( [ (4,8)(6,7), (1,2)(3,5)(4,6)(7,8) ] ),
          dualorder := 0,
          group_order := 48,
          maxcode := [ "2T", "2T", "X", "X" ],
          maxorder := 6,
          normcode := [ true, false, false, false ],
          subgroup_orders := [ 6, 4, 2 ] ), rec(
          B := Group( () ),
          H := 
           Group( [ (2,8,4)(5,7,6), (1,6)(2,8)(3,4)(5,7), 
              (1,7)(2,4)(3,8)(5,6), (1,4,5,3,6,2)(7,8) ] ),
          H0 := Group( [ (2,8,4)(5,7,6) ] ),
          H1 := Group( [ (1,2)(3,5)(4,7)(6,8) ] ),
          dualorder := 0,
          group_order := 24,
          maxcode := [ "M", "2T", "X", "X" ],
          maxorder := 6,
          normcode := [ true, false, false, true ],
          subgroup_orders := [ 3, 2, 1 ] ), rec(
          B := Group( () ),
          H := 
           Group( [ (2,8,4)(5,7,6), (1,6)(2,8)(3,4)(5,7), 
              (1,7)(2,4)(3,8)(5,6), (1,4,7,2)(3,6,8,5) ] ),
          H0 := Group( [ (2,8,4)(5,7,6) ] ),
          H1 := Group( [ (1,2)(3,5)(4,6)(7,8) ] ),
          dualorder := 0,
          group_order := 24,
          maxcode := [ "M", "2T", "X", "X" ],
          maxorder := 4,
          normcode := [ true, false, false, true ],
          subgroup_orders := [ 3, 2, 1 ] ) ] );
