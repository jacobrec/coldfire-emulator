import parser
import memory
from s19_gen import to_byte_array
import s19_gen
from instructions_extended import *


class Assembler():
    """

    """

    def __init__(self, instructions):
        self.blocks = []
        self.source = instructions
        self.isBlocksAssembled = False

        self.assembled = ""

    def assemble(self):
        if len(self.blocks) == 0:
            self.makeBlocks()
        if not self.isBlocksAssembled:
            self.assembleBlocks()
        return self.assembled

    def reset(self):
        self.blocks = []
        self.isBlocksAssembled = False

    def makeBlocks(self):
        block = Block()
        for instr in self.source:
            if isinstance(instr, memory.Label):
                block.addInstructions([symbolicLocation(instr.name, 0, False)])
            elif isinstance(instr, parser.Direct):
                pass
            else:
                block.addInstructions(assembleInstruction(instr))
        self.blocks = [block]

    def assembleBlocks(self):
        # for now, only assemble the first block
        self.assembled = self.blocks[0].instructions


class Block():
    """
    Objects that the assembler creates, each block has a list of instructions, and a name
    """

    def __init__(self):
        self.instructions = []  # instructions
        self.name = ""  # name

    def addInstructions(self, instr):
        self.instructions += instr

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "\n,".join(str(x) for x in self.instructions)


def assemble(stmts):
    a = Assembler(stmts)
    return a.assemble()



########## assemble instructions #############
def assembleInstruction(instr):
    """
        This is how it determines which instruction to assemble, it is a big
        if else statement that calls other functions based on the op code
    """

    instrDict = {
        "move": assembleMove,
        "movea": assembleMove,
        "moveq": assembleMoveq,
        "add": assembleAdd,
        "adda": assembleAddA,
        "addi": assembleAddI,
        "addq": assembleAddQ,
        "addx": assembleAddX,
        "and": assembleAnd,
        "andi": assembleAndI,
        "asl": assembleAsL,
        "asr": assembleAsR,
        "bhi": assembleBcc,
        "bls": assembleBcc,
        "bcc": assembleBcc,
        "bra": assembleBcc,
        "bt": assembleBcc,
        "bcs": assembleBcc,
        "bne": assembleBcc,
        "beq": assembleBcc,
        "bvc": assembleBcc,
        "bvs": assembleBcc,
        "bpl": assembleBcc,
        "bmi": assembleBcc,
        "bge": assembleBcc,
        "blt": assembleBcc,
        "bgt": assembleBcc,
        "ble": assembleBcc,
        "bchg": assembleBchg,
        "bclr": assembleBclr,
        "bitrev": assembleBitrev,
        "bset": assembleBset,
        "btst": assembleBtst,
        "byterev": assembleByterev,
        "clr": assembleClr,
        "cmp": assembleCmp,
        "cmpa": assembleCmpA,
        "cmpi": assembleCmpI,
        "divs": assembleDivs,
        "divu": assembleDivu,
        "eor": assembleEor,
        "eori": assembleEorI,
        "ext": assembleExt,
        "illegal": assembleIllegal,
        "lea": assembleLea,
        "link": assembleLink,
        "lsl": assembleLsl,
        "lsr": assembleLsr,
        "trap": assembleTrap,
        "bsr": assembleBsr,
        "rts": assembleRts
    }
    if not (instr.opcode.data[0] in instrDict):
        print(instr)
        return ""

    return instrDict[instr.opcode.data[0]](instr)


