module app;

import std.stdio;
import std.conv;
import std.file;
import std.string;
import core.stdc.stdlib;

import emulator;
import cpu;


bool debug_mode;

/**
 * Author: Jacob Reckhard, reckhard@ualberta.ca
 * Author: Jarrett Yu, jarrett@ualberta.ca
 * Date: March 15, 2018
 */

void main(string[] args){
    /+writeln("############################################");
    writeln("########      Coldfire Emulator     ########");
    writeln("# For when you are too lazy to walk up the #");
    writeln("# five flights of stairs to test your code #");
    writeln("############################################");
    +/

        int l = cast(int)args.length;

    foreach(string s; args){
        if(s[0] == '-'){
            if(s == "-d"){
                debug_mode = true;
            }
            l--;
        }
    }

    if(debug_mode){
        writeln("Debug mode:");
        writeln("- Press enter to execute next instruction");
        writeln("- Enter number to view memory at that location");
        writeln("- Enter 'r' to view register at that location");
    }
    if (l < 2 || l >= 3){
        writeln("Usage: dub -- <filename>");
        return;
    }

    if(!exists(args[1])){
        writeln("File <"~ args[1] ~"> not found.");
        return;
    }
    Coldfire emulator = new Coldfire();
    emulator.loadFile(args[1]);

    //printMemory(emulator.chip, 0, 128);
    for(int i = 0; ; i++){
        if(debug_mode){
            string s = readln().strip();
            if(isNumeric(s)){
                printMemory(emulator.chip, to!int(s), 64);
                continue;
            }else if(s == "r"){
                printRegisters(emulator.chip);
            }
        }
        emulator.run(debug_mode);
    }
}
