module app;

import std.stdio;
import std.file;
import core.stdc.stdlib;

import emulator;

/**
 * Author: Jacob Reckhard, reckhard@ualberta.ca
 * Author: Jarrett Yu, jarrett@ualberta.ca
 * Date: March 15, 2018
 */

void main(string[] args){
    writeln("############################################");
    writeln("########      Coldfire Emulator     ########");
    writeln("# For when you are too lazy to walk up the #\n# five flights of stairs to test your code #");
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
    writeln("Exiting emulator");
    exit(0);
}
