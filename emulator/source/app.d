import std.stdio;
import std.file;
import emulator;

/**
 * Author: Jacob Reckhard, reckhard@ualberta.ca
 * Author: Jarrett Yu, jarrett@ualberta.ca
 * Date: March 15, 2018
 */

void main(string[] args){
    writeln("Coldfire Emulator");
    writeln("2018 Dave");

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
}
