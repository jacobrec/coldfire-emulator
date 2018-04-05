module instructions.branch;

import cpu;
import instructions.instructions;



void cmp(ref Cpu chip){
    assert(matches(chip.opcode, "1011 ...0 .. ......"));
}

void bcc(ref Cpu chip){
    assert(matches(chip.opcode, "0110 .... ........"));
    immutable ubyte ct = cast(ubyte) getBits(chip.opcode, 4, 4);
    immutable byte dspl = cast(byte) getBits(chip.opcode, 8, 8);

    bool shouldBranch = false;
    switch(ct & 0b1111){
        case 0b0000:
            shouldBranch = true;
            break;
        case 0b0001:
            shouldBranch = false;
            break;
        case 0b0010:
            shouldBranch = !chip.isCarry && !chip.isZero;
            break;
        case 0b0011:
            shouldBranch = chip.isCarry || chip.isZero;
            break;
        case 0b0100:
            shouldBranch = !chip.isCarry;
            break;
        case 0b0101:
            shouldBranch = chip.isCarry;
            break;
        case 0b0110:
            shouldBranch = !chip.isZero;
            break;
        case 0b0111:
            shouldBranch = chip.isZero;
            break;
        case 0b1000:
            shouldBranch = !chip.isOverflow;
            break;
        case 0b1001:
            shouldBranch = chip.isOverflow;
            break;
        case 0b1010:
            shouldBranch = !chip.isNegative;
            break;
        case 0b1011:
            shouldBranch = chip.isNegative;
            break;
        case 0b1100:
            shouldBranch = (chip.isNegative && chip.isOverflow) ||(!chip.isNegative && !chip.isOverflow);
            break;
        case 0b1101:
            shouldBranch = (chip.isNegative && !chip.isOverflow) ||(!chip.isNegative && chip.isOverflow);
            break;
        case 0b1110:
            shouldBranch = (chip.isNegative && chip.isOverflow && !chip.isZero) || (!chip.isNegative && !chip.isOverflow && !chip.isZero);
            break;
        case 0b1111:
            shouldBranch = (chip.isZero) || (chip.isNegative && !chip.isOverflow) || (!chip.isNegative && chip.isOverflow);
            break;
        default:
            assert(0);
    }
    if(shouldBranch){
        chip.pc += dspl;
    }
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
    chip.CCR = 0b00100;


    chip.opcode = 0b0110_0111_01111111;
    bcc(chip);
    assert_eq(chip.pc, 127);
}
