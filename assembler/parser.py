from tokens import *
from memory import *
import tokens


class Parser:
    ############## init code ###############
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
                if not e.tok.toktype is EOF: # deal with this better
                    print(e)  # TODO: deal with errors

        return stmts
########### recursive descent parser ###########

    def _line(self):
        if self._match(Terminator):  # allow blank lines
            return self._line()
        elif self._check(Directive):
            return self._directive()
        elif self._check(Operator):
            return self._operator()
        elif self._check(LabelDef):
            return self._label(True)
        else:
            raise ParseError("Unexecpected token", self._peek())

    def _directive(self):
        dirType = self._consume(
            Directive, "This should definataly be a directive.")
        data = []
        while not self._match(Terminator):
            data.append(self._advance())
        return Direct(dirType, data)

    def _label(self, isDef=False):
        return Label(self._advance().data, isDef)

############ operator and memory functions #############
    def _operator(self):
        opcode = self._consume(
            Operator, "This should definataly be a operator.")
        if self._match(Terminator):
            return Instruction(opcode)
        if self._check(tokens.Label):
            return Instruction(opcode, self._label())
        mem1 = self._memory()
        if self._match(Terminator):
            return Instruction(opcode, mem1)
        self._consume(Comma, "am I missing a comma?")
        mem2 = self._memory()

        return Instruction(opcode, mem1, mem2)

    def _memory(self):
        if self._match(Register):  # DataDirect, and AddressDirect
            reg = self._peek(-1).data
            regType = reg[0]
            regNum = reg[1]
            if regType == "a":
                return AddressDirect(regNum)
            if regType == "d":
                return DataDirect(regNum)
        elif self._match(Decrement):  # AddressIndirectPreDecrement
            self._consume(GroupStart, "decrement expecting a '('")
            reg = self._consume(Register, "expecting a 'register'").data
            self._consume(GroupEnd, "expecting a ')'")
            assert(reg[0] == 'a')
            return AddressIndirectPreDecrement(reg[1])
        elif self._match(Literal):  # ImmediateData
            return ImmediateData(self._peek(-1).data)
        elif self._match(MemLocLiteral):  # AbsoluteLong and AbsoluteShort
            loc = self._peek(-1).data
            if loc[1] == "l":
                return AbsoluteLong(loc[0])
            if loc[1] == "w":
                return AbsoluteShort(loc[0])
        elif self._match(GroupStart):  # AddressIndirect, AddressIndirectPostIncrement
            reg = self._consume(Register, "expecting a 'register'").data
            if self._match(Comma):  # ScaledAddressWithOffset
                return self.partialScaledIndirectWithOffset(0, reg[1])
            self._consume(GroupEnd, "expecting a ')'")
            if self._match(Increment):  # ScaledAddressWithOffset
                return AddressIndirectPostIncrement(reg[1])
            return AddressIndirect(reg[1])
        elif self._match(Number):  # AddressIndirectWithOffset
            num = self._peek(-1).data
            self._consume(GroupStart, "number expecting a '('")
            reg = self._consume(Register, "expecting a 'register'").data
            if self._match(Comma):  # ScaledAddressWithOffset
                return self.partialScaledIndirectWithOffset(num, reg[1])
            self._consume(GroupEnd, "expecting a ')'")
            return AddressIndirectWithOffset(reg[1], num)

    def partialScaledIndirectWithOffset(self, offset, addReg):
        # n(%An, Xn*SF)
        reg2 = self._consume(Register, "expecting a 'register'").data
        self._consume(Star, "expecting a '*'")
        scaleFactor = self._consume(Number, "expecting a number").data
        self._consume(GroupEnd, "expecting a ')'")
        return ScaledAddressWithOffset(addReg, reg2[1], reg2[0], scaleFactor, offset)


########  Helper functions  #############

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
        self.calculateSize()

    def calculateSize(self):
        self.size = 2 + (self.mem_src.additionalsize if self.mem_src is not None else 0) + \
            (self.mem_dest.additionalsize if self.mem_dest is not None else 0)

        if self.opcode.data[0][-1] == "q":
            if isinstance(self.mem_src, ImmediateData):
                self.size -= 4

        if self.size > 6:
            raise ParseError(
                "Invalid memory access for instruction", self.opcode)

    def __len__(self):
        return self.size

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.mem_dest is None:
            if self.mem_src is None:
                return "{}:    {}.{}".format(self.size, self.opcode.data[0], self.opcode.data[1])
            return "{}:    {}.{} {}".format(self.size, self.opcode.data[0], self.opcode.data[1], str(self.mem_src))
        return "{}:    {}.{} {}, {}".format(self.size, self.opcode.data[0], self.opcode.data[1], str(self.mem_src), str(self.mem_dest))


class Direct:
    """
    An directive is an name followed by any additional data
    """

    def __init__(self, directive, data=None):
        self.directive = directive
        self.data = data

    def __str__(self):
        return "      .{} {}".format(self.directive.data, ", ".join([str(x.data) for x in self.data]))
