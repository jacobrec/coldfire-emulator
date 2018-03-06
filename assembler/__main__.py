import sys
from utils import assertAs
from lexer import lex
from tokens import *


def main():
    if len(sys.argv) >= 2 and len(sys.argv) <= 3:
        outfile = (sys.argv[1])[0:-2] + ".s19"
        if len(sys.argv) == 3:
            outfile = sys.argv[2]
        assertAs(sys.argv[1].endswith(".s"), "Must load a .s file")
        assembleFile(sys.argv[1], outfile)
    else:
        print("Usage: assembler [asm file] [Optional: output file]")


def assembleFile(f_in_name, f_out_name):
    """
        Okay, so this is the entry point for the assembler.
        This calls the lexer, which calls the parser, which
        calls the assembler, which calls the s19 generator.

        The flow will look like this
        f_in_name >> lexer >> parser >> assembler >> s19_gen >> f_out_name

        The lexer will take in the in file, and return a token stream
        The parser will take in the token stream and return an ast
        The assembler will take in an ast and return a list of binary data, with it's memory location
        The s19 gen will take that list, and return the list of records.
        Then this function, now that it has this list of records, will write them to the file.
    """
    print(f_in_name + " >> " + f_out_name)
    print("\n".join("" if x.toktype is Terminator else str(x)
                    for x in lex(f_in_name)))


main()
