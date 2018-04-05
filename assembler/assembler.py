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


def getSizeBitString(size):
    if size == 'l':
        return "10"
    if size == 'w':
        return "01"
    if size == 'b':
        return "00"


def numToBitStr(num, minLength=0):
    return format(num, '0' + str(minLength) + 'b')


########## assemble instructions #############
def assembleInstruction(instr):
    """
        This is how it determines which instruction to assemble, it is a big
        if else statement that calls other functions based on the op code
    """
    bin_strs = ""
    # TODO: do something more elegent with this. maybe use decorators?
    if instr.opcode.data[0] == "move":
        bin_strs = assembleMove(instr)
    elif instr.opcode.data[0] == "movea":
        bin_strs = assembleMove(instr)
    elif instr.opcode.data[0] == "moveq":
        bin_strs = assembleMoveq(instr)
    elif instr.opcode.data[0] == "trap":
        bin_strs = assembleTrap(instr)
    elif instr.opcode.data[0] == "bra":
        bin_strs = assembleBra(instr)
    elif instr.opcode.data[0] == "jmp":
        bin_strs = assembleJmp(instr)
    elif instr.opcode.data[0] == "add":
        bin_strs = assembleAdd(instr)
    '''
    Proposal for new technique: (need to import string)
    instrDict = {
    "move"    : assembleMove
    "movea"   : assembleMove
    "moveq"   : assembleMoveq
    }
    return instrDict[instr.opcode.data[0]](instr)
    '''
    return bin_strs


def assembleMove(instr):
    bin_str = "00" + getSizeBitString(instr.opcode.data[1])
    bin_str += instr.mem_dest.regStr() + instr.mem_dest.modeStr()
    bin_str += instr.mem_src.modeStr() + instr.mem_src.regStr()
    returnData = [bin_str]
    if len(instr) > 2:
        returnData += assembleExtraData(instr)
    return returnData


def assembleBra(instr):
    return ["01100000", symbolicLocation(instr.mem_src.name, 8, True)]

def assembleJmp(instr):
    # TODO: allow more type for jump
    ee = "111001" # Locked into absolute long mode for now
    ed = symbolicLocation(instr.mem_src.name, 16, False)
    return ["0100111011", ee, ed]


def assembleMoveq(instr):
    bin_str = "0111"
    bin_str += instr.mem_dest.regStr() + "0"
    assert(instr.mem_src.val < 256)
    bin_str += numToBitStr(instr.mem_src.val, 8)
    return [bin_str]


def assembleTrap(instr):
    bin_str = "010011100100"
    assert(instr.mem_src.val < 16)
    bin_str += numToBitStr(instr.mem_src.val, 4)
    return [bin_str]


def assembleExtraData(instr):
    data = []
    if instr.mem_src.additionalsize > 0:
        new_dat = numToBitStr(instr.mem_src.extraData(),
                              8 * instr.mem_src.additionalsize)
        data += [new_dat[i:i + 16] for i in range(0, len(new_dat), 16)]

    if instr.mem_dest.additionalsize > 0:
        new_dat = numToBitStr(instr.mem_dest.extraData(),
                              8 * instr.mem_dest.additionalsize)
        data += [new_dat[i:i + 16] for i in range(0, len(new_dat), 16)]
    return data


class symbolicLocation:
    def __init__(self, name, size, isRelative):
        self.name = name
        self.size = size
        self.isRelative = isRelative

    def __str__(self):
        return "({}, size:{})".format(self.name, self.size)

    def __repr__(self):
        return str(self)
