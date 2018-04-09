module instructions.bits;

import cpu;
import instructions.instructions;
import std.stdio;

void and(ref Cpu chip){
    ushort instr = chip.opcode;
    assert(matches(instr, "1100 .... .... ...."));
    int* reg = getMem(chip, 0b000, cast(ubyte)getBits(instr, 4, 3), 0b10);
    int* eff = getSource(chip, cast(ubyte)getBits(instr, 10, 6), 0b10);
    int result = swapEndien(readLoc(eff, 0b10)) & swapEndien(readLoc(reg, 0b10));
    int opmode = cast(int)getBits(instr, 7, 3);
    if (opmode == 0b010){
        writeLoc(reg, 0b10, &result);
    }else if(opmode == 0b110){
        writeLoc(eff, 0b10, &result);
    }
}

unittest{
    Cpu chip = Cpu();
    chip.D[1] = 0b00001100;
    chip.D[0] = 0b00000111;
    chip.opcode = 0b1100000010000001;
    and(chip);
    assert_eq(chip.D[0], 0b0100);
}
