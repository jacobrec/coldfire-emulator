# Coldfire
Emulator and Assembler.
A project by Jacob Reckhard and Jarrett Yu

One of the problems with ECE 212 labs is in order to test your code, you have to go all the way to the lab room. Then you have to fight with the machine to run you code. The development process is a struggle, and it's due to the tools available. Clearly a nice emulator is the solution. Yet, if you look for a coldfire emulator, you have 2 options. One, easy68k, a relatively nice emulator for windows only, where you must use the clunky GUI interface, and the emulator isn't even for the right system. Two, Dave's coldfire emulator. It seems a series of tools for coldfire including an emulator, an assembler and a compiler, were developed in the early 90's. But these are all challenging to find, poorly documented and are all made by a different guy's but all named Dave.  The goal of this is to have a coldfire emulator that's not necessarily complete with all the instructions, but complete enough for the ECE 212 labs.

This was built for our Ualberta CMPUT 275 Final project

## Assembler
Our coldfire assembler accepts a syntax identical to that of the assembler used in the ECE 212 labs(whatever the eclipse netburner uses). It supports some, but not all directives. This will be written entirely in python, it will be a multipass assembler. With this, the goal isn't to make the fastest assembler, but one that works and is easy to maintain. The phases of the assembler are written in order as follows.
### Lexer
The lexer will take in the name of the file and produce a token stream.
### Parser
The parser will take in the token stream and produce a list of statements. Each statement is an abstract syntax tree representing an instruction. The plan is to write a recursive descent parser for this.
### Processor
The processor will take in a list of statements and process all the assembler directives. This includes .org(specifying memory locations), .equ(symbolic replacements), and data type storage, ex) .long, .ascii
### Assembler
This takes in the processed statements and generates an array of bytes for each one.
### Linker
This takes in the assembled file and links it, dealing with memory locations, I.E. labels
### s19_generator
This takes in the array of bytes and generates the s19 file, a type of srec file, which is the format used for loading data onto the coldfire.


## Emulator
Our emulator emulates a subset of the coldfire instructions. The goal is all the ones used in the ECE 212 labs. It will not operate anywhere near as fast as the actual hardware. Speed is not a priority here. The goal is to end up with a tool that can be used to run all the code we learn to write in the ECE 212 labs. This will be vastly simplified to what the actual coldfire hardware can support, as we likely won't even try to do anything with the mac registers, or floating point registers. I would like to avoid the whole supervisor mode as well.

What it will support is all the instructions learned in ECE 212, as well as nice debugging support. Breakpoints and stepping for sure, as well as viewing memory dumps, and register values. If there is time, I would like to add in a graphical debugging tool too, but that's a stretch.



## How to use
I like the command line, it's simple and easy to use. The idea for how to use this is to be able to run two commands.

    $ assemble <input file> [output file]
    $ emulate <input file> [-d]
And it will start an emulator, and run the code, putting trap #15 to std_out. It should also support a -d flag, from this you should be able to run your code, set break points, and step through the code. As well as view memory, registers, and the condition flags.


# What we actually got done
- Assembler works
- Emulator works
- Debugging works
- Not all instructions that we hoped were implemented on the emulator
- Only add, move, cmp, bsr, b**, trap, and, lsr, lsl were implemented on the emulator

