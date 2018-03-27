_start:
move.l #1, %D0
move.l #2, %D1
move.l #3, %D2
add.l %D0, %D1 // %D1 should be set to 3
cmp.l %D1, %D2 // should be equal now
trap #15       // something should be printed here
