_start:

bsr hello_world



trap #9        // exit the simulator



hello_world:
move.l #6, %D0
move.l #72, %D1
trap #15
move.l #101, %D1
trap #15
move.l #108, %D1
trap #15
move.l #108, %D1
trap #15
move.l #111, %D1
trap #15
move.l #44, %D1
trap #15
move.l #32, %D1
trap #15
move.l #87, %D1
trap #15
move.l #111, %D1
trap #15
move.l #114, %D1
trap #15
move.l #108, %D1
trap #15
move.l #100, %D1
trap #15
move.l #10, %D1
trap #15
move.l #13, %D1
trap #15
rts
