import parser
from s19_gen import to_byte_array
import s19_gen


class Assembler():
    """
    a two pass assembler

    first it goes through and deals with directive, and subdivides the instructions into blocks

    Then, it goes through and assembles each block
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
            if isinstance(instr, parser.Label) or (isinstance(instr, parser.Direct) and instr.directive.data == "org"):
                self.blocks.append(block)
            else:
                block.addInstructions(assembleInstruction(instr))

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
    bin_str = "B"
    err = "NOP"

    if instr.opcode.data[0] == "move":
        bin_strs, err = assembleMove(instr)
    elif instr.opcode.data[0] == "movea":
        bin_strs, err = assembleMove(instr)
    elif instr.opcode.data[0] == "moveq":
        bin_strs, err = assembleMoveq(instr)
    elif instr.opcode.data[0] == "trap":
        bin_strs, err = assembleTrap(instr)

    if err == "NOP":
        return "None"

    return bin_strs


def assembleMove(instr):
    bin_str = "00" + getSizeBitString(instr.opcode.data[1])
    bin_str += instr.mem_dest.regStr() + instr.mem_dest.modeStr()
    bin_str += instr.mem_src.modeStr() + instr.mem_src.regStr()
    returnData = [bin_str]
    if len(instr) > 2:
        returnData += assembleExtraData(instr)
    return returnData, ""


def assembleMoveq(instr):
    bin_str = "0111"
    bin_str += instr.mem_dest.regStr() + "0"
    assert(instr.mem_src.val < 256)
    bin_str += numToBitStr(instr.mem_src.val, 8)
    return [bin_str], ""


def assembleTrap(instr):
    bin_str = "010011100100"
    assert(instr.mem_src.val < 16)
    bin_str += numToBitStr(instr.mem_src.val, 4)
    return [bin_str], ""


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
