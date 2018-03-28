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

    int[1024] text;
    ushort tp;

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
immutable ubyte SIZE_BYTE = 0b00;
immutable ubyte SIZE_WORD = 0b01;
immutable ubyte SIZE_WORDM = 0b11;
immutable ubyte SIZE_LONG = 0b10;


int* getMem(ref Cpu chip, ubyte mode, ubyte reg, ubyte size){
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
            mem_loc = cast(int*)&chip.ram[chip.A[reg]];
            if(size == SIZE_BYTE){
                chip.A[reg]++;
            }else if(size == SIZE_WORD || size == SIZE_WORDM){
                chip.A[reg]+=2;
            }else if(size == SIZE_LONG){
                chip.A[reg]+=4;
            }
            break;
        case 0b100:
            if(size == SIZE_BYTE){
                chip.A[reg]--;
            }else if(size == SIZE_WORD || size == SIZE_WORDM){
                chip.A[reg]-=2;
            }else if(size == SIZE_LONG){
                chip.A[reg]-=4;
            }
            mem_loc = cast(int*)&chip.ram[chip.A[reg]];
            break;
        case 0b101:
            immutable int off = (((chip.ram[chip.pc++]) << 8) + chip.ram[chip.pc++]);
            mem_loc = cast(int*) &chip.ram[chip.A[reg] + off];// TODO: add offset data
            break;
        case 0b110:
            // mem_loc = &chip.ram[chip.A[reg]];// TODO: add scaled data
            break;
        case 0b111:
            switch(reg){
                case 0b000:
                    int loc = (((chip.ram[chip.pc++]) << 8) + chip.ram[chip.pc++]);
                    mem_loc = cast(int*) &chip.ram[loc];
                    break;
                case 0b001:
                    int loc = chip.ram[chip.pc++] << 24;
                    loc    += chip.ram[chip.pc++] << 16;
                    loc    += chip.ram[chip.pc++] << 8;
                    loc    += chip.ram[chip.pc++];
                    mem_loc = cast(int*) &chip.ram[loc];
                    break;
                case 0b010:
                    // TODO: PC offset
                    break;
                case 0b011:
                    // TODO: PC scaled
                    break;
                case 0b100: // This will return a literal that is the next 4 bytes
                    // TODO: find a more effecient way to do this
                    chip.text[++chip.tp] = *(cast(int*) &chip.ram[chip.pc]);
                    chip.pc += 4;
                    mem_loc = &chip.text[chip.tp];
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

int* getSource(Cpu chip, ubyte bits, ubyte size = SIZE_BYTE){
    ubyte reg = bits & 0b111;
    ubyte mode = (bits & 0b111000) >> 3;
    return getMem(chip, mode, reg, size);
}
int* getDest(Cpu chip, ubyte bits, ubyte size = SIZE_BYTE){
    ubyte mode = bits & 0b111;
    ubyte reg = (bits & 0b111000) >> 3;
    return getMem(chip, mode, reg, size);
}
int readLoc(int* loc, ubyte size){
    int i = *loc;
    if(size == SIZE_BYTE){
        return i & 0xFF;
    }else if(size == SIZE_LONG){
        return (((i & 0xFF)<<24) | ((i&0xFF00) << 8) | ((i&0xFF0000)>>8) | ((i&0xFF000000) >> 24));
    }else{ // WORD size
        i = i & 0xFFFF;
        immutable int low = i & 0xFF;
        immutable int high = i & 0xFF00;
        return ((low << 8) | (high >> 8));
    }

}

void assert_eq(int a, int b){
    if(a != b){
        import std.stdio;
        writef("%X != %X\n", a, b);
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


    // testing direct, indirect and pre and post increment
    assert(readLoc(getMem(chip, 0b000, 0b000, SIZE_BYTE), SIZE_BYTE) == 0);
    assert_eq(readLoc(getMem(chip, 0b011, 0b000, SIZE_BYTE), SIZE_BYTE), 0);
    assert_eq(readLoc(getMem(chip, 0b011, 0b000, SIZE_BYTE), SIZE_BYTE), 1);
    assert_eq(readLoc(getMem(chip, 0b011, 0b000, SIZE_BYTE), SIZE_BYTE), 2);
    assert_eq(readLoc(getMem(chip, 0b100, 0b000, SIZE_BYTE), SIZE_BYTE), 2);
    assert_eq(readLoc(getMem(chip, 0b100, 0b000, SIZE_BYTE), SIZE_BYTE), 1);
    assert_eq(readLoc(getMem(chip, 0b100, 0b000, SIZE_BYTE), SIZE_BYTE), 0);
    assert_eq(readLoc(getMem(chip, 0b011, 0b000, SIZE_LONG), SIZE_LONG), 0x00010203);
    assert_eq(readLoc(getMem(chip, 0b011, 0b000, SIZE_LONG), SIZE_LONG), 0x04050607);
    assert_eq(readLoc(getMem(chip, 0b011, 0b000, SIZE_LONG), SIZE_LONG), 0x08090A0B);

    assert_eq(readLoc(getMem(chip, 0b011, 0b000, SIZE_BYTE), SIZE_BYTE), 0x0C);
    assert_eq(readLoc(getMem(chip, 0b100, 0b000, SIZE_WORD), SIZE_WORD), 0x0B0C);
    assert_eq(chip.A[0], 11);

    // Testing indirect with offset
    chip.pc = 100;
    chip.ram[100] = 0x00;
    chip.ram[101] = 0x02;
    assert_eq(readLoc(getMem(chip, 0b101, 0b001, SIZE_BYTE), SIZE_BYTE), 3);
    assert_eq(chip.pc, 102);

    chip.pc = 0;
    assert_eq(readLoc(getMem(chip, 0b101, 0b001, SIZE_BYTE), SIZE_BYTE), 2);
    assert_eq(chip.pc, 2);

    chip.pc = 100;
    chip.ram[100] = 0x01;
    chip.ram[101] = 0x00;
    assert_eq(readLoc(getMem(chip, 0b101, 0b001, SIZE_BYTE), SIZE_BYTE), 1);
    assert_eq(chip.pc, 102);

    // testing literal

    chip.pc = 0;
    chip.ram[0] = 0;
    chip.ram[1] = 0;
    chip.ram[2] = 0;
    chip.ram[3] = 0x49;

    assert_eq(readLoc(getMem(chip, 0b111, 0b100, SIZE_LONG), SIZE_LONG), 0x49);
    assert_eq(chip.pc, 4);


    //testing absolute short
    chip.pc = 100;
    chip.ram[1] = 0x49;
    chip.ram[100] = 0;
    chip.ram[101] = 1;
    assert_eq(readLoc(getMem(chip, 0b111, 0b000, SIZE_LONG), SIZE_BYTE), 0x49);
    assert_eq(chip.pc, 102);


    //testing absolute long
    chip.pc = 98;
    chip.ram[1] = 0x49;
    chip.ram[98] = 0;
    chip.ram[99] = 0;
    chip.ram[100] = 0;
    chip.ram[101] = 1;
    assert_eq(readLoc(getMem(chip, 0b111, 0b001, SIZE_LONG), SIZE_BYTE), 0x49);
    assert_eq(chip.pc, 102);
}
