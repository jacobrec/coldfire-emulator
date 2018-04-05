_start:
move.l #15, %D0
move.l #34, %D1
move.l #10, %D2
add.l %D0, %D1 // %D1 should be set to 49
trap #15       // 49 should be printed here
trap #9        // exit the simulator
