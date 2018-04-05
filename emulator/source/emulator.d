module emulator;

import cpu;
import fileLoader;
import instructions.instructions;
/**
  * Coldfire is the system to be emulated, this holds the fetch, decode, exucute loop
  * as well as the cpu which is passed to the decoded functions as a refernce
  */
class Coldfire{
    Cpu chip;
    instruction[ushort] funTable;

    this(){
        chip = Cpu();
        funTable = getInstructionMap();
    }



    /**
     * The main loop
     *
     * Runs every frame and performs a fetch, decode, execute cycle
     */
    void run(){

        fetch();
        decode()(chip);
    }




    /**
     * Handles loading of files into memory
     *
     * Expects the filepath to a s19 file, and will load it into
     * the chip's memory.
     */
    void loadFile(string filepath){
        parseFile(filepath, this.chip.ram, this.chip.pc);
    }





    /**
     * Decodes the instruction and returns a function to mimic
     * the execution of the instruction.
     *
     * The function that it returns will be held in a table of functions
     * and this will just refernce that.
     */
    instruction decode(){
        return funTable[this.chip.opcode];
    }

    /**
     * Sets the next opcode from the cpu to decode
     * The opcode is stored in chip.opcode
     */
    void fetch(){
        chip.opcode = swapEndien(*(cast(ushort*) &chip.ram[chip.pc]));
        chip.pc += 2;
    }
}

