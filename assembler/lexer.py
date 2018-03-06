words = {
    "move", "moveq", "movei", "movea"
    "add", "addq", "addi", "adda"
}

sizes = {
    "l": "long",
    "w": "word",
    "b": "byte"
}


def lex(lines):
    instructionArray = []
    for line in lines:
        instructionArray.append(Instruction(line))


instructBaseSizes = {
    "move": 2, "moveq": 2, "movea": 2,
    "add": 2, "addq": 2, "addi": 6, "adda": 2

}
addressingSizes = {
    "datadirect": 0,
    "addressdirect": 0,
    "addressindirect": 0,
    "postincrement": 0,
    "predecrement": 0,
    "displacement": 2,
    "scaled": 2,
    "long": 4,
    "short": 2
}


class Instruction:
    def __init__(self, instruction):
        """
        >>> Instruction("moveq.l #1, %D3")
        ''

        >>> Instruction("moveq.l #1, 8(%A2, %D2*1)")
        ''

        >>> Instruction("moveq.l 8(%A2, %D2*1), 8(%A2, %D2*1)")
        ''
        """
        oper = instruction.split()[0].split(".")

        op = oper[0]
        opsize = oper[1]
        opands = []
        curword = ""
        bracket = 0
        for c in str(instruction[len(op) + len(opsize) + 1:]):
            if c == "(":
                pass
            elif c == ")":
                pass

        self.set(opsize, op, Operand(opands[0]), Operand(opands[1]))

    def set(self, opsize, op, src=None, dest=None):
        self.opsize = opsize
        self.op = op
        self.src = src
        self.dest = dest
        self.size = self.__calculateSize()

    def __calculateSize(self):
        size = instructBaseSizes[self.op]
        if self.src is not None:
            size += addressingSizes[self.src.mode]
        if self.dest is not None:
            size += addressingSizes[self.dest.mode]
        return size

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{} {}[{}] ({}, {})".format(self.op, self.opsize, self.size, self.src, self.dest)


class Operand:
    def __init__(self, string_operand):
        self.mode = "datadirect"
        self.string = string_operand

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.string


if __name__ == "__main__":
    import doctest
    doctest.testmod()
