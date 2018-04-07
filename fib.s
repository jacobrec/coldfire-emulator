_start:
move.l #10, %D0 // Calculate fibbinaci of 10

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
