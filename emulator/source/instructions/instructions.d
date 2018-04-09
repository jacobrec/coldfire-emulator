module instructions.instructions;

import cpu;
import std.conv;
import std.regex;
import instructions.math;
import instructions.move;
import instructions.bits;
import instructions.other;
import instructions.branch;


alias instruction = void function(ref Cpu chip);
immutable ushort instruction_length = 16;
instruction[ushort] getInstructionMap(){
    instruction[ushort] cached;
    for (ushort i = 0; i < 0xFFFF; i++) {
        cached[i] = getInstruction(i);
    }
    return cached;
}

instruction getInstruction(ushort instr){
    if (     matches(instr, "1101 .... 10.. ....")){
        return &add;
    }else if(matches(instr, "0110 0001 .... ....")){
        return &bsr;
    }else if(matches(instr, "0100 1110 10.. ....")){
        return &jsr;
    }else if(matches(instr, "1011 ...0 .... ....")){
        return &cmp;
    }else if(matches(instr, "0110 .... .... ....")){
        return &bcc;
    }else if(matches(instr, "0100 1110 0100 ....")){
        return &trap;
    }else if(matches(instr, "00.. .... .... ....")){
        return &move;
    }else if(matches(instr, "0100 1110 0111 0101")){
        return &rts;
    }else if(matches(instr, "1100 .... .... ....")){
        return &and;
    }else if(matches(instr, "1110 .... 10.0 1...")){
        return &ls;
    }
    return null;
}

/**
 * matches takes in the operator, as well as an op string,
 * and if the operator matches the opstring,
 * then it returns true, else false
 *
 * The op string looks as follows "001010.0100.11"
 * all charactors are either 0, 1, or ., if . the operator
 * can have the bit set or not
 */
bool matches(ushort op, string match_string){
    auto guess = replaceAll(match_string, regex(r"\s","g"), "");
    assert(guess.length == instruction_length);
    for(int i = 0; i < instruction_length; i++){
        if(guess[i] != '.'){ // the thing is a dot, then that matches
            if(guess[i] - '0' != ((op >> (15 - i)) & 1)){
                return false;
            }
        }
    }
    return true;
}

/**
 * Returns n bits from the src starting at index first
 */
uint getBits(int src, int first, int n, int bits=16){
    uint ans = 0;
    uint tmp = src >> (bits-n-first);


    for(int i = 0; i < n; i++){
        ans |= (tmp & (1 << i));
    }
    return ans;
}
unittest{
    assert(getBits(0b00001111, 2, 4, 8) == 0b0011);
    assert(getBits(0b0001000011000000, 2, 2) == 0b01);
    assert(getBits(0b0001000011000000, 4, 6) == 0b000011);
    assert(getBits(0b0001000011000000, 10, 6) == 0b000000);
}


unittest{
    assert(matches(0b0000000000000000u, "0000000000000000"));
    assert(matches(0b1111111111111111u, "1111111111111111"));
    assert(matches(0b1001010110101010u, "................"));
    assert(!matches(0b1111000011110000u, "1011000011110000"));
    assert(!matches(0b0000000000000000u, "0000000000000001"));
    assert(matches(0b1101010011101101u, "1101..0.111.1101"));
    assert(matches(0b1101010011101101u, "1101. .0.111. 1101"));
    assert(matches(0b1101010011101101u, "1101..0. 111.1101"));
}
