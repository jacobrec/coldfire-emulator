/*
#### Factorial ####
Computes the factorial of the number in %D2
Stores result in %D3

Requires %D2 to be a positive integer smaller then 13
*/
.org 0x100
Moveq #6, %D2
moVeq.w #1, %D3
moVeq #1, 0x12345678.l
mOve.b 8(%A0), -(%A0)
movE (%A0)+, 8(%A0, /*Fun fact, mid line comments are a thing*/         %D0*2)
clr %A0

nop

movE.l 0x333.w, 0x343.w



mulLoop:
cmpi #1, %D2
bEq end

mULu %D2, %D3
subq #1, %D2
bRa muLLoop

end:
move %D3, %D1
moveq #10, %D2
trap #15
