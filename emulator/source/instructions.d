import cpu;
import std.conv;

alias instruction = void function(Cpu chip);
immutable ushort instruction_length = 16;
pure instruction[ushort] getInstructionMap(){
    instruction[ushort] cached;
    for (ushort i = 0; i < 0xFFFF; i++) {
        cached[i] = getInstruction(i);
    }
    return cached;
}

pure instruction getInstruction(ushort instr){
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
bool matches(ushort op, string guess){
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


unittest{
    assert(matches(0b0000000000000000u, "0000000000000000"));
    assert(matches(0b1111111111111111u, "1111111111111111"));
    assert(matches(0b1001010110101010u, "................"));
    assert(!matches(0b1111000011110000u, "1011000011110000"));
    assert(!matches(0b0000000000000000u, "0000000000000001"));
    assert(matches(0b1101010011101101u, "1101..0.111.1101"));
}
