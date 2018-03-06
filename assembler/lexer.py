from tokens import *
from utils import assertAs
instructions = {
    "add", "adda", "addi", "addq", "addx",
    "and", "andi",
    "asl", "asr",
    "bra", "b**",  # TODO figure out how to deal with wildcards
    "bchg", "bclr", "bset", "btst"
    "clr",
    "cmp", "cmpa", "cmpi",
    "divs", "divu",
    "eor", "eori",
    "ext",
    "illegal",
    "jmp", "jsr",
    "lea",
    "link",
    "lsl", "lsr",
    "move", "moveq", "movea", "move",
    "muls", "mulu",
    "neg", "negx",
    "nop",
    "not",
    "or", "ori",
    "pea",
    "rts",
    "sub", "suba", "subi", "subq", "subx",
    "swap",
    "tas",
    "trap",
    "tst",
    "unlk"
}
directives = {
    "org", "equ", "asciz", "ascii", "long", "byte"
}

sizes = {"l", "w", "b"}
skipchar = {"\t", "\r", " "}

singlechars = {
    "(": GroupStart,
    ")": GroupEnd,
    ",": Comma,
    "*": Star,
    "/": Slash,
    "-": Decrement,
    "+": Increment
}


class Token:
    def __init__(self, toktype, data, line):
        self.toktype = toktype
        self.data = data
        self.line = line

    def __str__(self):
        return "{}({}): [line {}]".format(self.toktype.__name__, self.data, self.line)

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, source):
        self.source = source
        self.current = 0
        self.line = 1
        self.toks = []

    def lex(self):
        self.toks = []
        self.addTok(Terminator)
        while not self.isEnd():
            self.scanTok()
        self.addTok(EOF)
        return self.toks

    def scanTok(self):
        c = self.advance()

        if c == "\n":
            self.line += 1
            if not (self.toks[-1].toktype is Terminator):
                self.addTok(Terminator)
        elif c in skipchar:
            pass
        elif (c == ";") or ((c == "/") and (self.peek() == "/")):
            while c != "\n":
                c = self.advance()
            self.line += 1
        elif (c == "/") and (self.peek() == "*"):
            while not ((c == "*") and (self.peek() == "/")):
                c = self.advance()
            self.advance()
        elif c == "%":
            self.register()
        elif c == "#":
            self.literal()
        elif c.isdigit():
            num = self.number()
            self.addTok(Number, num)
        elif c.isalpha():
            self.operator()
        elif c in singlechars:
            self.addTok(singlechars[c])
        elif c == ".":
            if self.toks[-1].toktype is Terminator:
                self.directive()
        else:
            assertAs(0, "Unrecognized charactor (%c)" % c)

    def register(self):
        regType = self.advance()
        regNum = self.advance()
        self.addTok(Register, (regType, int(regNum)))

    def literal(self):
        self.advance()
        self.addTok(Literal, self.number())

    def number(self):
        num = self.peek(-1)
        base = 10
        while self.peek().isdigit() or self.peek() == "b" or self.peek() == "x":
            num += self.peek()
            if num[-1] == 'x':
                num = ""
                base = 16
            elif num[-1] == 'b':
                num = ""
                base = 2
            self.advance()
        return int(num, base)

    def operator(self):
        name = self.word()
        if len(name) == 3 and name[0] == "b":
            self.addTok(Operator, (name))
            return
        if name in instructions:
            size = "l"
            if self.peek() == ".":
                self.advance()
                size = self.advance()
            self.addTok(Operator, (name, size))
        else:
            if self.peek() == ":":
                self.addTok(LabelDef, name)
                self.advance()
            else:
                self.addTok(Label, name)

    def directive(self):
        self.advance()
        name = self.word()
        assertAs(name in directives, "Directive [%s] not supported" % name)
        self.addTok(Directive, name)

    def word(self):
        name = self.peek(-1)
        while self.peek().isalnum():
            name += self.advance()

        return name

    def addTok(self, type, data=None):
        self.toks.append(Token(type, data, self.line))

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def peek(self, skip=0):
        if self.isEnd():
            return '\0'
        return self.source[self.current + skip]

    def isEnd(self):
        return self.current >= len(self.source)


def lex(filename):
    """
    Turns the input file into a token stream

    """
    with open(filename, "r") as f:
        lexer = Lexer(f.read())
        return lexer.lex()
