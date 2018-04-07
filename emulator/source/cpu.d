module cpu;

import instructions.other : get_number_string;
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

    bool isExtend(){
        return (this.CCR & 0b10000) != 0;
    }
    bool isNegative(){
        return (this.CCR & 0b01000) != 0;
    }
    bool isZero(){
        return (this.CCR & 0b00100) != 0;
    }
    bool isOverflow(){
        return (this.CCR & 0b00010) != 0;
    }
    bool isCarry(){
        return (this.CCR & 0b00001) != 0;
    }
    void setExtend(bool val){
        if(val){
            this.CCR |= 0b10000;
        }else{
            this.CCR &= ((-1) ^ 0b10000);
        }
    }
    void setNegative(bool val){
        if(val){
            this.CCR |= 0b01000;
        }else{
            this.CCR &= ((-1) ^ 0b01000);
        }
    }
    void setZero(bool val){
        if(val){
            this.CCR |= 0b00100;
        }else{
            this.CCR &= ((-1) ^ 0b00100);
        }
    }
    void setOverflow(bool val){
        if(val){
            this.CCR |= 0b00010;
        }else{
            this.CCR &= ((-1) ^ 0b00010);
        }
    }
    void setCarry(bool val){
        if(val){
            this.CCR |= 0b00001;
        }else{
            this.CCR &= ((-1) ^ 0b00001);
        }
    }
}

void printRegisters(ref Cpu chip){
    import std.stdio;
    for(int i = 0; i < 8; i++){
        writef("D%d: 0x%X\t\t",i, chip.D[i]);
    }
    writeln();
    for(int i = 0; i < 8; i++){
        writef("A%d: 0x%X\t\t",i, chip.A[i]);
    }
    writeln();
}
void printMemory(ref Cpu chip, int fromByte, int totalBytes){
    import std.stdio;
    int b = 0;
    while(b < totalBytes){
        for(int i = 0; i < 8; i++){
            string num = get_number_string(chip.ram[b + fromByte], 2);
            while(num.length < 8){
                num = "0"~num;
            }
            writef("%s ", num);
            b++;
        }
        writeln();
    }
    writeln();
}

unittest{
    Cpu chip = Cpu();
    chip.CCR = 0b11010;
    assert(chip.isExtend);
    assert(chip.isNegative);
    assert(!chip.isZero);
    assert(chip.isOverflow);
    assert(!chip.isCarry);

    chip.setExtend(false);
    assert(!chip.isExtend);
    assert(chip.isNegative);
    assert(!chip.isZero);
    assert(chip.isOverflow);
    assert(!chip.isCarry);

    chip.setCarry(true);
    assert(!chip.isExtend);
    assert(chip.isNegative);
    assert(!chip.isZero);
    assert(chip.isOverflow);
    assert(chip.isCarry);

    chip.setOverflow(false);
    assert(!chip.isExtend);
    assert(chip.isNegative);
    assert(!chip.isZero);
    assert(!chip.isOverflow);
    assert(chip.isCarry);

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
                    mem_loc = newValue(chip, (*(cast(int*) &chip.ram[chip.pc])));
                    chip.pc += 4;
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
void push(ref Cpu chip, int val, ubyte size = SIZE_LONG){
    if(size == SIZE_BYTE){
        chip.A[7]--;
    }else if(size == SIZE_WORD || size == SIZE_WORDM){
        chip.A[7]-=2;
    }else if(size == SIZE_LONG){
        chip.A[7]-=4;
    }

    ubyte* loc = &chip.ram[chip.A[7]];
    if(size == SIZE_BYTE){
        *(loc) = cast(ubyte) val;
    }else if(size == SIZE_WORD || size == SIZE_WORDM){
        *(cast(ushort*) loc) = cast(ushort) val;
    }else if(size == SIZE_LONG){
        *(cast(int*) loc) = val;
    }

}
int pop(ref Cpu chip, ubyte size = SIZE_LONG){

    ubyte* loc = &chip.ram[chip.A[7]];
    int val;
    if(size == SIZE_BYTE){
        val = cast(int) *(loc);
    }else if(size == SIZE_WORD || size == SIZE_WORDM){
        val = cast(int) *(cast(ushort*) loc);
    }else if(size == SIZE_LONG){
        val = *(cast(int*) loc);
    }


    if(size == SIZE_BYTE){
        chip.A[7]++;
    }else if(size == SIZE_WORD || size == SIZE_WORDM){
        chip.A[7]+=2;
    }else if(size == SIZE_LONG){
        chip.A[7]+=4;
    }

    return val;

}
unittest{
    Cpu chip = Cpu();
    chip.A[7] = 100;
    push(chip, 10);
    push(chip, 20);
    push(chip, 30);

    assert_eq(30, pop(chip));
    assert_eq(20, pop(chip));
    assert_eq(10, pop(chip));

}
int* newValue(ref Cpu chip, int value){
    chip.text[++chip.tp] = value;
    return &chip.text[chip.tp];
}

int* getSource(ref Cpu chip, ubyte bits, ubyte size = SIZE_BYTE){
    ubyte reg = bits & 0b111;
    ubyte mode = (bits & 0b111000) >> 3;
    return getMem(chip, mode, reg, size);
}
int* getDest(ref Cpu chip, ubyte bits, ubyte size = SIZE_BYTE){
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

void writeLoc(int* loc, ubyte size, int* data){
    if(size == SIZE_BYTE){
        *loc &= 0xFFFFFF00;
        *loc |= (*data) & 0x000000FF;
    }else if (size == SIZE_LONG){
        *loc &= 0x00000000;
        *loc |= (*data) & 0xFFFFFFFF;
    }else{
        *loc &= 0xFFFF0000;
        *loc |= (*data) & 0x0000FFFF;
    }
}

int swapEndien(int i){
    return (((i & 0xFF)<<24) | ((i&0xFF00) << 8) | ((i&0xFF0000)>>8) | ((i&0xFF000000) >> 24));
}
short swapEndien(short i){
    return cast(short)(((i&0xFF) << 8) | ((i&0xFF00)>>8));
}
unittest{
    assert_eq(0x11223344, swapEndien(0x44332211));
    assert_eq(0x1122, swapEndien(cast(short)0x2211));
}


void assert_eq(int a, int b){
    if(a != b){
        import std.stdio;
        writef("0x%X(%d) != 0x%X(%d)\n", a,a, b,b);
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
    assert(*getDest(chip, 0b000010) == 0x03020100);


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


    // testing write
    chip.pc = 98;
    chip.ram[98] = 0;
    chip.ram[99] = 0;
    chip.ram[100] = 0;
    chip.ram[101] = 2;
    chip.ram[102] = 0;
    chip.ram[103] = 0;
    chip.ram[104] = 0;
    chip.ram[105] = 1;

    chip.ram[1] = 0x49;
    chip.ram[2] = 0;

    assert_eq(readLoc(getMem(chip, 0b111, 0b001, SIZE_LONG), SIZE_BYTE), 0x0);
    assert_eq(chip.pc, 102);
    assert_eq(readLoc(getMem(chip, 0b111, 0b001, SIZE_LONG), SIZE_BYTE), 0x49);
    chip.pc = 98;
    writeLoc(getDest(chip, 0b001111), SIZE_BYTE, getSource(chip, 0b111001));

    assert_eq(chip.ram[2], 0x49);
    assert_eq(chip.ram[1], 0x49);


    // testing write

    chip.ram[0] = 0;
    chip.A[0] = 0;
    chip.D[0] = 31;

    writeLoc(getMem(chip, 0b011, 0b000, SIZE_BYTE), SIZE_BYTE, getMem(chip, 0b000, 0b000, SIZE_BYTE));

    assert_eq(chip.A[0], 1);
    assert_eq(chip.D[0], chip.ram[0]);

    // testing write

    chip.ram[0] = 0;
    chip.A[0] = 0;
    chip.D[0] = 49;


    writeLoc(getDest(chip, 0b000011, SIZE_BYTE), SIZE_BYTE, getSource(chip, 0b000000, SIZE_BYTE));

    assert_eq(chip.A[0], 1);
    assert_eq(chip.D[0], chip.ram[0]);


}
