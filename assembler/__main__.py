import sys
from utils import assertAs
from s19_gen import assembleFile
from preprocessor import preprocess


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
    records = []
    content = []

    with open(f_in_name, "r") as inFile:
        content = f.readlines()

    blocks = preprocess(content)
    startloc, _ = blocks[0]

    for loc, lines in blocks:
        for line in lines:
            data = assembleLine(line)
            records.append(s1_rec(data, loc))

    records.append(s5_rec(len(content)))
    records.append(s9_rec(startloc))

    with open(f_out_name, "w+") as outFile:
        for rec in records:
            print(rec, file=outFile)


def assembleLine(line):
    pass


main()
