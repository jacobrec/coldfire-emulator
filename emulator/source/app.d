module app;

import std.stdio;
import std.file;
import core.stdc.stdlib;

import emulator;
import cpu;

/**
 * Author: Jacob Reckhard, reckhard@ualberta.ca
 * Author: Jarrett Yu, jarrett@ualberta.ca
 * Date: March 15, 2018
 */

void main(string[] args){
    writeln("############################################");
    writeln("########      Coldfire Emulator     ########");
    writeln("# For when you are too lazy to walk up the #");
    writeln("# five flights of stairs to test your code #");
    writeln("############################################");

    if (args.length < 2 || args.length >= 3){
        writeln("Usage: dub -- <filename>");
        return;
    }

    if(!exists(args[1])){
        writeln("File <"~ args[1] ~"> not found.");
        return;
    }
    Coldfire emulator = new Coldfire();
    emulator.loadFile(args[1]);
    
    // printMemory(emulator.chip, 0, 24);
    for(int i = 0; i < 1000; i++){ // TODO: do somthing better
        emulator.run();
    }


    writeln("Exiting emulator");
    exit(0);
}
