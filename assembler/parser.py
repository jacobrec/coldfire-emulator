from tokens import *


class Parser:
    def __init__(self, toks):
        self.toks = toks
        self.current = 0

    def parse(self):
        stmts = []
        self._match(Terminator)
        while not self._isAtEnd():
            try:
                stmts.append(self._line())
            except ParseError as e:
                self._sync()
                print(e)  # TODO: deal with errors

        print(stmts)
        return stmts

    def _line(self):
        if self._check(Directive):
            return self._directive()
        elif self._check(Operator):
            return self._operator()
        elif self._check(LabelDef):
            return self._label()
        else:
            raise ParseError("Unexecpected token", self._peek())

    def _directive(self):
        dirType = self._consume(Directive)
        data = []
        while not self._match(Terminator):
            data.append(self._advance())
        return Direct(dirType, data)

    def _label(self):
        return Label(self._advance().data)

    def _operator(self):
        self._sync()  # TODO add this

    def _match(self,  *types):
        for type in types:
            if self._check(type):
                self._advance()
                return True
        return False

    def _check(self, type):
        if self._isAtEnd():
            return False
        else:
            return self._peek().toktype is type

    def _peek(self, skip=0):
        return self.toks[self.current + skip]

    def _advance(self):
        if not self._isAtEnd():
            self.current += 1
        return self._peek(-1)

    def _consume(self, tokType, message=""):
        if self._check(tokType):
            return self._advance()

        raise self._error(self._peek(), message + " Got %s" %
                          str(self._peek().toktype))

    def _error(self, tok, message):
        return ParseError(message, tok)

    def _sync(self):
        while not self._match(Terminator) and not self._isAtEnd():
            self._advance()

    def _isAtEnd(self):
        return self._peek().toktype is EOF


def parse(toks):
    p = Parser(toks)
    return p.parse()


class ParseError(Exception):
    def __init__(self, msg, tok):
        self.msg = msg
        self.tok = tok


class Instruction:
    """
    An instruction is an opcode(op, size) followed by 0-2 data locations
    """

    def __init__(self, opcode, mem1=None, mem2=None):
        self.opcode = opcode
        self.mem_src = mem1
        self.mem_dest = mem2


class Label:
    def __init__(self, name):
        self.name = name


class Direct:
    """
    An directive is an name followed by any additional data
    """

    def __init__(self, directive, data=None):
        self.directive = directive
        self.data = data


# Jarrett, you'll need to write this class as you see fit
# this basically the data register mode
class Data:
    pass
