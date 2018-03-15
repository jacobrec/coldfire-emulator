/*
#### Factorial ####
Computes the factorial of the number in %D2
Stores result in %D3

Requires %D2 to be a positive integer smaller then 13
*/
_start:
move.l #49, %D1
moveq.l #10, %D2
trap #15
bra _start

