module instructions.math;

import cpu;
import instructions.instructions;



void add(ref Cpu chip){
    assert(matches(chip.opcode, "1101 ... . 10 ......"));

    ubyte data =cast(ubyte) getBits(chip.opcode, 4, 3);
    ubyte other = cast(ubyte)getBits(chip.opcode, 10, 6);
    ubyte incoming =cast(ubyte) getBits(chip.opcode, 7, 1);

    int* src;
    int* dst;
    if(incoming == 1){
        src = getMem(chip, 0b000, data, SIZE_LONG);
        dst = getDest(chip, other, SIZE_LONG);
    }else{
        src = getSource(chip, other, SIZE_LONG);
        dst = getMem(chip, 0b000, data, SIZE_LONG);
    }

    int val = readLoc(dst, SIZE_LONG) + readLoc(src, SIZE_LONG);
    writeLoc(dst, SIZE_LONG, &val);


}

unittest{
    Cpu chip;
    for(int i = 0; i < 1024*64; i++){
        chip.ram[i] = cast(ubyte) i;
    }
    for(int i = 0; i < 8; i++){
        chip.A[i] = i+1;
        chip.D[i] = i+1;
    }

    chip.pc = 0;
    ushort instr = 0b1101_001_110_000000; // Add d1 to d0 and store in d0
    chip.opcode = instr;
    add(chip);
    assert_eq(3, chip.D[0]);
    assert_eq(2, chip.D[1]);

    instr = 0b1101_001_010_000000; // Add d1 to d0 and store in d1
    chip.opcode = instr;
    add(chip);
    assert_eq(3, chip.D[0]);
    assert_eq(5, chip.D[1]);

}
