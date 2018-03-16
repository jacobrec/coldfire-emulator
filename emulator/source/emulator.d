import std.file;
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

    }

    void loadFile(string filepath){
        auto data = readText(filepath);
        for(int i = 0; i < data.length; i++){
            chip.ram[i] = data[i];
        }
    }
}
