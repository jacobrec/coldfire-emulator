module instructions.branch;

import cpu;
import instructions.instructions;

void rts(ref Cpu chip){
    assert(matches(chip.opcode, "0100 1110 0111 0101"));
    chip.pc = pop(chip);
}
void bsr(ref Cpu chip){
    ushort dsp  = cast(ushort) getBits(chip.opcode, 8, 8);
    push(chip, chip.pc);
    chip.pc += dsp;
}
void jsr(ref Cpu chip){
    push(chip, chip.pc);
    chip.pc = (readLoc(getSource(chip, cast(ubyte) getBits(chip.opcode, 10, 6), SIZE_LONG), SIZE_LONG));

}

void cmp(ref Cpu chip){
    assert(matches(chip.opcode, "1011 ...0 .. ......"));
    ubyte data =cast(ubyte) getBits(chip.opcode, 4, 3);
    ubyte other = cast(ubyte)getBits(chip.opcode, 10, 6);
    ubyte size =cast(ubyte) getBits(chip.opcode, 8, 2);


    int src = readLoc(getSource(chip, other, size), size);
    int dst = readLoc(getMem(chip, 0b000, data, size), size);

    long val = dst - src;
    chip.setZero(val == 0);
    chip.setNegative(val < 0);
    chip.setCarry(val != (cast(int) val));
    chip.setOverflow(val != (cast(int) val) && ((val>0 && (cast(int) val) < 0) || ((cast(int) val) > 0 && val < 0)));
    // TODO: make sure carry and overflow are correct
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



    chip.CCR = 0b00000;
    chip.opcode = 0b1011_0000_10_000001; //1011 DDD0 SS eeeeee
    cmp(chip);
    assert_eq(chip.CCR & 0b11111, 0b01000);



    chip.pc = 100;
    chip.opcode = 0b0110_0001_0000_0010;
    bsr(chip);
    assert_eq(102, chip.pc);
    assert_eq(chip.ram[chip.A[7]], 100);

    immutable a7tmp = chip.A[7];
    chip.opcode = 0b0100111001110101;
    rts(chip);
    assert_eq(100, chip.pc);
    assert_eq(a7tmp+4, chip.A[7]);


    chip.pc = 100;
    chip.D[0] = 0x49000000;
    chip.opcode = 0b0100111010_000000;
    jsr(chip);
    assert_eq(chip.pc, 0x49);
    jsr(chip);
    assert_eq(chip.pc, 0x49);
    chip.opcode = 0b0100111001110101;
    rts(chip);
    assert_eq(chip.pc, 0x49);
    rts(chip);
    assert_eq(chip.pc, 100);
}
