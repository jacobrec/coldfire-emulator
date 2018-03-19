import cpu;

class Coldfire{
    Cpu chip;

    this(){
        chip = Cpu();

        while(true){
            run();
        }
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
        auto data = readText(filepath);
        // TODO: parsing of s19 file
    }


    /**
      * Decodes the instruction and returns a function to mimic
      * the execution of the instruction.
      *
      * The function that it returns will be held in a table of functions
      * and this will just refernce that.
      */
    void function(ref Cpu) placeholder;
    ref void function(ref Cpu) decode(){
        return placeholder;
    }

    /**
      * Sets the next opcode from the cpu to decode
      * The opcode is stored in chip.opcode
      */
    void fetch(){
        chip.opcode = chip.ram[chip.pc];
        chip.pc -= 2;
    }
}
