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
### Sizer
This will take in the list of instructions and calculate the amount of memory each one will take. This is important for dealing with labels, and also for generating the s19 files later. It appends the memory information to each instruction
### Processor
The processor will take in a list of statements and process all the assembler directives. This includes .org(specifying memory locations), .equ(symbolic replacements), and data type storage, ex) .long, .ascii
### Assembler
This takes in the processed statements and generates an array of bytes for each one.
### s19_generator
This takes in the array of bytes and generates the s19 file, a type of srec file, which is the format used for loading data onto the coldfire.


## Emulator
Our emulator emulates a subset of the coldfire instructions. The goal is all the ones used in the ECE 212 labs. It will not operate anywhere near as fast as the actual hardware. Speed is not a priority here. The goal is to end up with a tool that can be used to run all the code we learn to write in the ECE 212 labs. This will be vastly simplified to what the actual coldfire hardware can support, as we likely won't even try to do anything with the mac registers, or floating point registers. I would like to avoid the whole supervisor mode as well.

What it will support is all the instructions learned in ECE 212, as well as nice debugging support. Breakpoints and stepping for sure, as well as viewing memory dumps, and register values. If there is time, I would like to add in a graphical debugging tool too, but that's a stretch.

- Side note. I know this course has a focus on python, but ideally I would like to write this not in python, but a language with finer control over memory and individual bits. And we already are doing the assembler in python. So would it be possible to write this emulator in another language? Preferably D, but possibly C++. D would be my preference as it allows for the same fine memory control as C, but with niceties of modern languages, like built in testing solutions, really nice OOP support, easy support for multithreading, and easy to use graphics libraries for if there's time to add in the graphical debugger. So, would we be allowed to write the emulator in D? And if not, would we be allowed to write the emulator in C++? Since we did learn that language in class last semester.


## How to use
I like the command line, it's simple and easy to use. The idea for how to use this is to be able to run two commands.

    $ assemble <input file> [output file]
    $ emulate <input file> [-d]
And it will start an emulator, and run the code, putting trap #15 to std_out. It should also support a -d flag, from this you should be able to run your code, set break points, and step through the code. As well as view memory, registers, and the condition flags.


## Milestones
- March 9.
Write the s19 file generator. This is the binary format the assembler needs to generate. A tool will be built to ease the work of the assembler.
Demo: Show off our knowledge of the s19 file format

- March 16.
Write a recursive descent parser to convert the raw input into an easier to deal with ast.
Demo: show off the generated ast

- March 23.
Actual assembler, at this point, it should generate binary data and write s19 files. These s19 files should be compatible with the coldfire hardware. The subset of instructions at this point will be relatively limited. Just the add and move instructions.
Demo: show off the complete generated s19 files.

- March 30.
Have the assembler support directives. At least some of them. Like add the .org and .equ directive. Also add support for labels and jump instructions. And also the `trap #15` instruction
Demo: cooler generated s19 files with jumps and labels

- March 30.
Basic emulator, it should support all the instructions our assembler supports. Loading from the s19 files, as well as `trap #15`.
Demo: being able to run code that we wrote in assembly. As well as output values of registers with the trap command

- April 6.
Add more instructions to the assembler and emulator. As many as we can. Support the debug mod in the emulator set break points, and step through the code. As well as view memory, registers, and the condition flags.
Demo: a cool debugger for our emulator

- April 10-12
Add as many instructions as we can until we demo.
Demo: a great emulator, a robust assembler, some working assembly code
