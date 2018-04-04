module instructions.move;

import cpu;
import instructions.instructions;

void move(ref Cpu chip){
    immutable ushort instr = chip.opcode;
    assert(matches(instr, "00.. .... .... ...."));

    ubyte size = cast(ubyte)getBits(instr, 2, 2);
    if(size == 0b01){
        size = 0b00;
    }else if(size == 0b11){
        size = 0b01;
    }

    immutable ubyte dst = cast(ubyte)getBits(instr, 4, 6);
    immutable ubyte src = cast(ubyte)getBits(instr, 10, 6);

    writeLoc(getDest(chip, dst, size), size, getSource(chip, src, size));

}


unittest{
    Cpu chip;
    for(int i = 0; i < 1024*64; i++){
        chip.ram[i] = cast(ubyte) i;
    }
    for(int i = 0; i < 8; i++){
        chip.A[i] = i;
        chip.D[i] = i;
    }

    chip.pc = 0;
    ushort instr = 0b0001000011000000;
    
    chip.ram[1] = (instr >> 8) & 0xFF;
    chip.ram[0] = instr & 0xFF; 

    chip.opcode = *(cast(ushort*) &chip.ram[chip.pc]);
    chip.pc -= 2; 

    chip.D[0] = 49;
    move(chip);

    assert_eq(49, chip.ram[0]);
    assert_eq(chip.D[0], 49);
    assert_eq(chip.A[0],  1);
 

}
