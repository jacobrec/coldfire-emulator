module instructions.other;

import cpu;
import instructions.instructions;


void trap(ref Cpu chip){
    immutable trap_num = getBits(chip.opcode, 12, 4);
    switch(trap_num){
        case 15:
            trap15(chip);
            break;
        case 9:
            trap9(chip);
            break;
        default:
            import std.stdio;
            writef("Error, trap #%d is not defined\n", trap_num);
            assert(0);
    }

}

void trap9(ref Cpu chip){
    import std.stdio;
    import std.c.stdlib;
    writeln("Exiting(Trap 9)...");
    //printRegisters(chip);
    exit(0);
}

void trap15(ref Cpu chip){
    import std.stdio;
    switch(swapEndien(chip.D[0])){
        case 0x0F:
            writeln(get_number_string(swapEndien(chip.D[1]), swapEndien(chip.D[2])));
            break;
        default:
            writef("Error, trap #15 task %d(%X) is not defined\n", chip.D[0],chip.D[0]);
            assert(0);
    }

}

immutable string basechars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
string get_number_string(int num, int base){
    string ans = "";
    assert(2 <= base && base <= 36);
    while (num > 0){
        ans = basechars[num % base] ~ ans;
        num /= base;
    }
    return ans;
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

    ushort instr = 0b010011100100_1111;

    assert("A" == get_number_string(10, 16));
    assert("Z" == get_number_string(35, 36));
    assert("49" == get_number_string(49, 10));
    assert("101" == get_number_string(5, 2));
}
