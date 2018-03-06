/*
#### Factorial ####
Computes the factorial of the number in %D2
Stores result in %D3

Requires %D2 to be a positive integer smaller then 13
*/
.org 0x100
moveq.l #6, %D2
moveq.l #1, %D3
move.l 8(%A0), -(%A0)
move.l (%A0)+, 8(%A0, %D0*2)


mulLoop:
cmpi.l #1, %D2
beq end

mulu.l %D2, %D3
subq.l #1, %D2
bra mulLoop

end:
move.l %D3, %D1
moveq.l #10, %D2
trap #15
