import std.stdio;
import std.file;

/**
 * Author: Jacob Reckhard, reckhard@ualberta.ca
 * Author: Jarrett Yu, jarrett@ualberta.ca
 * Date: March 15, 2018
 */


void init(){
}

void run(){
}


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
    auto data = readText(args[1]);
}
