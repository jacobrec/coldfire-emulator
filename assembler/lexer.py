from tokens import *
from utils import assertAs
instructions = {
    "add", "adda", "addi", "addq", "addx",
    "and", "andi",
    "asl", "asr",
    "bra", "b**",  # TODO figure out how to deal with wildcards
    "bchg", "bclr", "bset", "btst",
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
        self.source = source.lower()
        self.current = 0
        self.line = 1
        self.toks = []

    def lex(self):
        self.toks = []
        self._addTok(Terminator)
        while not self._isEnd():
            self._scanTok()
        self._addTok(EOF)
        return self.toks

    def _scanTok(self):  # TODO, negative literals don't word
        c = self._advance()

        if c == "\n":
            self.line += 1
            if not (self.toks[-1].toktype is Terminator):
                self._addTok(Terminator)
        elif c in skipchar:
            pass
        elif (c == ";") or ((c == "/") and (self._peek() == "/")):
            while c != "\n":
                c = self._advance()
            self.line += 1
            if not (self.toks[-1].toktype is Terminator):
                self._addTok(Terminator)
        elif (c == "/") and (self._peek() == "*"):
            while not ((c == "*") and (self._peek() == "/")):
                if c == "\n":
                    if not (self.toks[-1].toktype is Terminator):
                        self._addTok(Terminator)
                    self.line += 1
                c = self._advance()
            self._advance()
        elif c == "%":
            self._register()
        elif c == "#":
            self._literal()
        elif c.isdigit():
            num = self._number()
            if(self._peek() == "."):
                self._advance()
                self._addTok(MemLocLiteral, (num, self._peek()))
                self._advance()
            else:
                self._addTok(Number, num)
        elif c == "-":
            if self._peek() == "(":
                self._addTok(singlechars[c])
            else:
                num = self._number()
                if(self._peek() == "."):
                    self._advance()
                    self._addTok(MemLocLiteral, (num, self._peek()))
                    self._advance()
                else:
                    self._addTok(Number, num)
        elif c.isalpha() or c == "_":
            self._operator()
        elif c in singlechars:
            self._addTok(singlechars[c])
        elif c == ".":
            if self.toks[-1].toktype is Terminator:
                self._directive()
        else:
            print("on line {}".format(self.line))
            assertAs(0, "Unrecognized charactor (%c)" % c)

    def _register(self):
        regType = self._advance()
        regNum = self._advance()
        self._addTok(Register, (regType, int(regNum)))

    def _literal(self):
        isNeg = 1
        if self._peek() == "-":
            self._advance()
            isNeg = -1

        if self._peek().isdigit():
            self._advance()
            self._addTok(Literal, isNeg*self._number())
        elif self._peek().isalpha():
            self._advance()
            self._addTok(Literal, self._word())

    def _number(self):
        num = self._peek(-1)
        base = 10
        while self._peek().isdigit() or self._peek() == "b" or self._peek() == "x":
            num += self._peek()
            if num[-1] == 'x':
                num = ""
                base = 16
            elif num[-1] == 'b':
                num = ""
                base = 2
            self._advance()
        return int(num, base)

    def _operator(self):
        name = self._word()
        if len(name) == 3 and name[0] == "b":
            self._addTok(Operator, (name, "l"))
            return
        if name in instructions:
            size = "l"
            if self._peek() == ".":
                self._advance()
                size = self._advance()
            self._addTok(Operator, (name, size))
        else:
            if self._peek() == ":":
                self._addTok(LabelDef, name)
                self._advance()
            else:
                self._addTok(Label, name)

    def _directive(self):
        self._advance()
        name = self._word()
        assertAs(name in directives, "_directive [%s] not supported" % name)
        self._addTok(Directive, name)

    def _word(self):
        name = self._peek(-1)
        while self._peek().isalnum() or self._peek() == "_":
            name += self._advance()

        return name

    def _addTok(self, type, data=None):
        self.toks.append(Token(type, data, self.line))

    def _advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def _peek(self, skip=0):
        if self._isEnd():
            return '\0'
        return self.source[self.current + skip]

    def _isEnd(self):
        return self.current >= len(self.source)


def lex(filename):
    """
    Turns the input file into a token stream

    """
    with open(filename, "r") as f:
        lexer = Lexer(f.read())
        return lexer.lex()
