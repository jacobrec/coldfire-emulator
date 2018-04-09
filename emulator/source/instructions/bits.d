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

void ls(ref Cpu chip){
    int dx;
    int dy;
    int* reg0;
    int* reg1;
    int result;
    ushort instr = chip.opcode;
    assert(matches(instr, "1110 .... 10.0 1..."));
    if (cast(int)getBits(instr, 10, 1) == 0b0) { // for immediate Dy
        dy = cast(int)getBits(instr, 4, 3);
        reg1 = getMem(chip, 0b000, cast(ubyte)getBits(instr, 13, 3), 0b10);
        dx = swapEndien(readLoc(reg1, 0b10));
    }else{
        reg0 = getMem(chip, 0b000, cast(ubyte)getBits(instr, 4, 3), 0b10);
        reg1 = getMem(chip, 0b000, cast(ubyte)getBits(instr, 13, 3), 0b10);
        dy = swapEndien(readLoc(reg0, 0b10)) % 64;
        dx = swapEndien(readLoc(reg1, 0b10));
    }
    if (cast(int)getBits(instr, 7, 1) == 0b0) { //lsr
        result = dx >> dy;
    }else{
        result = dx << dy;
    }
    writeLoc(reg1, 0b10, &result);
}

unittest{
    Cpu chip = Cpu();
    chip.D[1] = 0b00000010; //2
    chip.D[0] = 0b00000111; //7
    chip.opcode = 0b1110001010101000; //d[0] is right shifted by d[1]
    ls(chip);
    assert_eq(chip.D[0], 0b0001);
}
