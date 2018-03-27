module cpu;

/**
 * The coldfire cpu
 *
 * A struct for storing info about the hardware
 *
 * 8 data registers, marked by D[0] - D[7]
 * 8 address registers, marked by A[0] - A[7]
 * CCR is the condition register 16 bits [T*SMIII***XNZVC], see coldfire.md for more details
 */
struct Cpu{
    int[8] A;
    int[8] D;
    ushort CCR;
    ubyte[1024*64] ram;
    uint pc;

    ushort opcode;
}
enum AddressMode{
    REG_DIRECT,
    ADD_DIRECT,
    ADD_INDIRECT,
    ADD_INDIRECT_INC,
    ADD_INDIRECT_DEC,
    ADD_INDIRECT_OFF,
    ADD_INDIRECT_SCALED,
    ABS_LONG,
    ABS_SHORT,
    IMMEDIATE, 
}

int* getMem(ref Cpu chip, ubyte mode, ubyte reg){
    int* mem_loc;
    switch(mode){
        case 0b000:
            mem_loc = &chip.D[reg];
            break;
        case 0b001:
            mem_loc = &chip.A[reg];
            break;
        case 0b010:
            mem_loc = cast(int*)&chip.ram[chip.A[reg]];
            break;
        case 0b011:
            mem_loc = cast(int*)&chip.ram[chip.A[reg]++];
            break;
        case 0b100:
            mem_loc = cast(int*)&chip.ram[--chip.A[reg]];
            break;
        case 0b101:
            // mem_loc = &chip.ram[chip.A[reg]];// TODO: add offset data
            break;
        case 0b110:
            // mem_loc = &chip.ram[chip.A[reg]];// TODO: add scaled data
            break;
        case 0b111:
            switch(reg){
                case 0b000:
                    // TODO: abs short
                    break;
                case 0b001:
                    // TODO: abs long
                    break;
                case 0b010:
                    // TODO: PC offset
                    break;
                case 0b011:
                    // TODO: PC scaled
                    break;
                case 0b100:
                    // TODO: immediate
                    break;
                default:
                    import std.stdio;
                    stderr.writeln("Not a real thing ");
                    assert(0);
            } 
            break;
        default:
            import std.stdio;
            stderr.writeln("Error memory type invalid");
            assert(0);
   } 
   assert(mem_loc);
   return mem_loc;
}

int* getSource(Cpu chip, ubyte bits){
    ubyte reg = bits & 0b111;
    ubyte mode = (bits & 0b111000) >> 3;
    return getMem(chip, mode, reg);
} 
int* getDest(Cpu chip, ubyte bits){
    ubyte mode = bits & 0b111;
    ubyte reg = (bits & 0b111000) >> 3;
    return getMem(chip, mode, reg);
} 


void assert_eq(int a, int b){
    if(a != b){
        import std.stdio;
        writef("%d != %d\n", a, b);
        assert(0);
    }
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


    assert(*getDest(chip, 0b111000) == 7);
    assert(*getDest(chip, 0b011000) == 3);
    assert(*getDest(chip, 0b111001) == 7);
    assert(*getDest(chip, 0b001001) == 1);
    assert(*getDest(chip, 0b000010) == 0x03020100); // is this the right Endian?
  

    assert(*getMem(chip, 0b000, 0b000) == 0);
    assert_eq(*getMem(chip, 0b011, 0b000) & 0xFF, 0);
    assert_eq(*getMem(chip, 0b011, 0b000) & 0xFF, 1);
    assert_eq(*getMem(chip, 0b011, 0b000) & 0xFF, 2);
    assert_eq(*getMem(chip, 0b100, 0b000) & 0xFF, 2);
    assert_eq(*getMem(chip, 0b100, 0b000) & 0xFF, 1);
    assert_eq(*getMem(chip, 0b100, 0b000) & 0xFF, 0);
}
