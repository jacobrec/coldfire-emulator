_start:

// Print "Enter a Number n, 0<= n <= 45"
move.l #6, %D0
move.l #69, %D1
trap #15
move.l #110, %D1
trap #15
move.l #116, %D1
trap #15
move.l #101, %D1
trap #15
move.l #114, %D1
trap #15
move.l #32, %D1
trap #15
move.l #97, %D1
trap #15
move.l #32, %D1
trap #15
move.l #78, %D1
trap #15
move.l #117, %D1
trap #15
move.l #109, %D1
trap #15
move.l #98, %D1
trap #15
move.l #101, %D1
trap #15
move.l #114, %D1
trap #15
move.l #32, %D1
trap #15
move.l #110, %D1
trap #15
move.l #44, %D1
trap #15
move.l #32, %D1
trap #15
move.l #48, %D1
trap #15
move.l #32, %D1
trap #15
move.l #60, %D1
trap #15
move.l #61, %D1
trap #15
move.l #32, %D1
trap #15
move.l #110, %D1
trap #15
move.l #32, %D1
trap #15
move.l #60, %D1
trap #15
move.l #61, %D1
trap #15
move.l #32, %D1
trap #15
move.l #52, %D1
trap #15
move.l #53, %D1
trap #15
move.l #10, %D1
trap #15
move.l #13, %D1
trap #15

move.l #4, %D0
trap #15



move.l %D1, %D0 // Calculate fibbinaci of input

// Initial values
move.l #1, %D1  
move.l #0, %D2  
move.l #1, %D3  

/*
Bottom up dynamic programming approch for the fibbinici sequence
calculate each element and hold onto those values for a little bit
then shift them down, and sum. Runs in O(n) time when n is the number
in %D0.
*/
fibLoop:
cmp.l #0, %D0
beq done
add.l #-1, %D0

move.l %D1, %D3
add.l  %D2, %D3

move.l %D1, %D2
move.l %D3, %D1

bra fibLoop

done:
move.l %D2, %D1
move.l #15, %D0
move.l #10, %D2
trap #15
trap #9
