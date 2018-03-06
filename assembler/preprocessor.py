from utils import assertAs
"""
Deals with the first pass of the assembler.
That is, labels, named jumps, and directives

Planned to support
.byte
.long
.word

Currently supported
.org
.equ

"""


def preprocess(lines):
    """
    main function of the file, does the first pass

    This will return an list of blocks, each block is a tuple as follows
    (location_in_memory, list_of_instructions)

    so the return may look something like this
    [
        (3242, ["addi.l #5, %D2", "addi.l #5, %D2", "addi.l #5, %D2"]),
        (3012, ["addi.l #5, %D2", "addi.l #5, %D2", "addi.l #5, %D2"]),
        (3432, ["addi.l #5, %D2", "addi.l #5, %D2", "addi.l #5, %D2"])
    ]

    >>> preprocess([".org 0x1000", "moveq.l #1, %D2", "moveq.l #2, %D2", ".org 0x2000", "moveq.l #3, %D2"])
    [(4096, ['moveq.l #1, %D2', 'moveq.l #2, %D2']), (8192, ['moveq.l #3, %D2'])]

    >>> preprocess([".org 0x1000", "moveq.l #0x10, %D2"])
    [(4096, ['moveq.l #16, %D2'])]

    """
    lines = replaceEquDirectives(lines)

    blocks = []
    current_loc = 0
    current_list = []
    for line in lines:
        line = line.strip()
        if line.startswith("."):
            if line.startswith(".org"):
                if len(current_list) != 0:
                    blocks.append((current_loc, current_list))
                    current_list = []
                current_loc = processOrgDirective(line)
        else:  # it's actually an instruction
            line = processConstants(line)
            current_list.append(line)
    blocks.append((current_loc, current_list))
    return blocks


def processConstants(line):
    """
    Deals with 0x and 0b constants

    >>> processConstants("moveq.l #0x10, %D2")
    'moveq.l #16, %D2'

    """
    words = line.split()
    outwords = []

    for word in words:
        if word.startswith("#"):
            if word.startswith("#0b"):

                stripped = word[3:]
                for i in range(len(stripped)):
                    if not stripped[i].isdigit():
                        x = i
                        break
                rside = word[x:]
                stripped = word[3:x]
                word = "#" + str(int(stripped, 2)) + rside

            if word.startswith("#0x"):
                stripped = word[3:]
                for i in range(len(stripped)):
                    if not stripped[i].isdigit():
                        x = i
                        break
                rside = stripped[x:]
                stripped = stripped[:x]
                word = "#" + str(int(stripped, 16)) + rside

        outwords.append(word)

    return " ".join(outwords)


def replaceEquDirectives(lines):
    """
    replaces the constants defined with .equ with their values

    >>> replaceEquDirectives([".equ thi,0x1000", ".equ that, #0x1000", "move.l that, %D2", "add.l thi, %D2"])
    ['move.l #0x1000, %D2', 'add.l 0x1000, %D2']
    """

    equMap = {}
    for line in lines:
        line = line.strip()
        if line.startswith(".equ"):
            data = line.replace(",", " ").split()
            equMap[data[1]] = data[2]
    newlines = []
    for line in lines:
        for k, v in equMap.items():
            line = line.replace(k, v)
        if not line.startswith(".equ"):
            newlines.append(line)
    return newlines


def processOrgDirective(line):
    """
    Returns the memory address from the org derective

    >>> processOrgDirective(".org 0x1000")
    4096

    >> > processOrgDirective(".org 0b11111111")
    255

    >> > processOrgDirective(".org 400")
    400
    """

    items = line.split()
    assertAs(items[0] == ".org", "processOrgDirective requires a .org command")
    assertAs(len(items) == 2, "malformated .org directiv")

    if items[1].startswith("0b"):
        return int(items[1][2:], 2)

    if items[1].startswith("0x"):
        return int(items[1][2:], 16)

    return int(items[1])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
