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

    int val = swapEndien(readLoc(dst, SIZE_LONG)) + swapEndien(readLoc(src, SIZE_LONG));
    writeLoc(dst, SIZE_LONG, &val);


}

unittest{
    Cpu chip;
    for(int i = 0; i < 1024*64; i++){
        chip.ram[i] = 0;
    }
    for(int i = 0; i < 8; i++){
        chip.A[i] = i+1;
        chip.D[i] = i+1;
    }

    chip.D[0] = 0x01000000;
    chip.D[1] = 0x02000000;

    chip.pc = 0;
    ushort instr = 0b1101_001_110_000000; // Add d1 to d0 and store in d0
    chip.opcode = instr;
    add(chip);
    assert_eq(0x03000000, chip.D[0]);
    assert_eq(0x02000000, chip.D[1]);

    chip.ram[3] = 5;
    chip.pc = 4;
    instr = 0b1101_000_110_001111; // Add 0x0 to d0 and store in 0x0
    chip.opcode = instr;
    add(chip);
    assert_eq(chip.pc, 8);
    assert_eq(8, chip.ram[3]);
    assert_eq(0x03000000, chip.D[0]);


    instr = 0b1101_001_010_000000; // Add d1 to d0 and store in d1
    chip.opcode = instr;
    add(chip);
    assert_eq(0x03000000, chip.D[0]);
    assert_eq(0x05000000, chip.D[1]);

}
