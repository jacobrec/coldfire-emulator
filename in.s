_start:
move.l #5, %D0
move.l #6, %D1
move.l #3, %D2
and.l %D0, %D1
trap #15       // something should be printed here
