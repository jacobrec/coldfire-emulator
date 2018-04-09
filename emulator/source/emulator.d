module emulator;

import cpu;
import fileLoader;
import instructions.instructions;
import instructions.other: get_number_string;
/**
  * Coldfire is the system to be emulated, this holds the fetch, decode, exucute loop
  * as well as the cpu which is passed to the decoded functions as a refernce
  */
class Coldfire{
    Cpu chip;
    instruction[ushort] funTable;

    this(){
        chip = Cpu();
        chip.A[7] = chip.ram.length - 1; // set stack pointer to end of memory
        funTable = getInstructionMap();
    }



    /**
     * The main loop
     *
     * Runs every frame and performs a fetch, decode, execute cycle
     */
    void run(bool verbose = false){

        fetch();

        if(verbose){
            import std.stdio;
            string s = get_number_string(chip.opcode,2);
            while(s.length < 16){
                s = "0" ~ s;
            }
            writeln(s);
        }
        try{
            decode()(chip);
        }catch (Error e){
            import std.stdio;
            writeln("Error executing instruction at memory location ", (this.chip.pc-2));
            writeln(e);
            assert(0);
        }
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

