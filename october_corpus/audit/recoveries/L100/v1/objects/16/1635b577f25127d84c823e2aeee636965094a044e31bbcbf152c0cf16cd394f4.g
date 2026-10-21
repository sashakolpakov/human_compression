L100PositiveWitnesses:=[];
Add(L100PositiveWitnesses,rec(
  generator_images := [ (1,2), (3,4) ],
  rank := 2,
  source := [ 1, 1 ],
  target := [ 1, 1 ],
  type_permutation := () ));
Add(L100PositiveWitnesses,rec(
  generator_images := [ (1,2), (1,2)(3,4) ],
  rank := 2,
  source := [ 1, 1 ],
  target := [ 1, 2 ],
  type_permutation := () ));
Add(L100PositiveWitnesses,rec(
  generator_images := [ (3,4), (1,2)(3,4) ],
  rank := 2,
  source := [ 1, 1 ],
  target := [ 1, 3 ],
  type_permutation := () ));
