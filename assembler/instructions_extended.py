import parser
import memory
from s19_gen import to_byte_array
import s19_gen
import assembler
'''
Operations to be done later: (we really need to figure out wild wildcards)
Add
Move
B**
Bra
Make a function to add immediate data in form: addImmediateData(instr, w/l)
Check mode if abs short or long
'''

def assembleAdd(instr):  # currently only supports first op mode
    bin_str = "1101"
    if True:  # condition for if the destination is Register
        bin_str += instr.mem_dest.regStr() + "010"
        bin_str += instr.mem_src.modeStr() + instr.mem_src.regStr()
    else:
        bin_str += instr.mem_src.regStr() + "110"
        bin_str += instr.mem_dest.modeStr() + instr.mem_dest.regStr()
    returnData = [bin_str]
    if len(instr) > 2:
        returnData += assembleExtraData(instr)
    return returnData

def assembleAddA(instr):
    bin_str = "1101" + instr.mem_dest.regStr() + "111"
    bin_str += instr.mem_src.modeStr() + instr.mem_src.regStr()
    returnData = [bin_str]
    if len(instr) > 2:
        returnData += assembleExtraData(instr)
    return returnData

def assembleAddI(instr):
    bin_str = "0000011010"
    bin_str += instr.mem_dest.regStr()  # not sure about This
    bin_str += numToBitStr(instr.mem_src.val, 32)
    return [bin_str]

def assembleAddQ(instr):
    assert(instr.mem_src.val < 256)
    bin_str = "0101" + numToBitStr(instr.mem_src.val, 8) + "010"
    bin_str += instr.mem_dest.modeStr() + instr.mem_dest.regStr()
    returnData = [bin_str]
    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleAddX(instr):
    bin_str = "1101" + instr.mem_dest.regStr() + "110000"
    bin_str += instr.mem_src.regStr()
    return[bin_str]

def assembleAnd(instr):
    bin_str = "1100" + instr.mem_dest.regStr()
    if isinstance(instr, instr.mem_dest) == register:  # if final dest is register
        bin_str += "010" + instr.mem_src.modeStr() + instr.mem_src.regStr()
    else:
        bin_str += "110" + instr.mem_src.modeStr() + instr.mem_src.regStr()
    returnData = [bin_str]
    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleAndI(instr):
    bin_str = "0000001010000" + instr.mem_dest.regStr()
    bin_str += numToBitStr(instr.mem_src.val, 32)
    return [bin_str]

def assembleAsL(instr):
    bin_str += "1110"
    if True:  # if from Register
        bin_str += instr.mem_src.regStr()
        bin_str += "110100"
    else:  # immediate value
        assert(instr.mem_src.val < 8)
        bin_str += numToBitStr(instr.mem_src.val, 3)
        bin_str += "110000"
    return [bin_str]

def assembleAsR(instr):
    bin_str += "1110"
    if True:  # if from Register
        bin_str += instr.mem_src.regStr()
        bin_str += "010100"
    else:  # immediate value
        assert(instr.mem_src.val < 8)
        bin_str += numToBitStr(instr.mem_src.val, 3)
        bin_str += "010000"
    return [bin_str]

def assembleBcc(instr):
    # TODO: make work
    return None

def assembleBchg(instr):
    bin_str = "0000"
    if isinstance(instr, instr.mem_src) == ImmediateData:  # if literal
        bin_str += "100010" + instr.mem_dest.modeStr() + instr.mem_dest.regStr()
        bin_str += "00000000" + numToBitStr(instr.mem_src.val, 8)
    else:
        bin_str += instr.mem_src.regStr() + "101"
        bin_str += instr.mem_dist.modeStr() + instr.mem_dist.modeStr()
    return [bin_str]

def assembleBclr(instr):
    bin_str = "0000"
    if isinstance(instr, instr.mem_src) == ImmediateData:  # if literal
        bin_str += "100010" + instr.mem_dest.modeStr() + instr.mem_dest.regStr()
        bin_str += "00000000" + numToBitStr(instr.mem_src.val, 8)
    else:
        bin_str += instr.mem_src.regStr() + "110"
        bin_str += instr.mem_dist.modeStr() + instr.mem_dist.modeStr()
    return [bin_str]

def assembleBitrev(instr):
    return ["0000000011000" + instr.mem_src.regDest()]

def assembleBset(instr):
    bin_str = "0000"
    if isinstance(instr, instr.mem_src) == ImmediateData:  # if literal
        bin_str += "100011" + instr.mem_dest.modeStr() + instr.mem_dest.regStr()
        bin_str += "00000000" + numToBitStr(instr.mem_src.val, 8)
    else:
        bin_str += instr.mem_src.regStr() + "100"
        bin_str += instr.mem_dist.modeStr() + instr.mem_dist.modeStr()
    return [bin_str]

def assembleBsr(instr):
    bin_str = "01100001"
    bin_str += symbolicLocation(instr.mem_src.name, 8, True)
    return [bin_str]

def assembleBtst(instr):
    bin_str = "0000"
    if isinstance(instr, instr.mem_src) == ImmediateData:  # if literal
        bin_str += "100000" + instr.mem_dest.modeStr() + instr.mem_dest.regStr()
        bin_str += "00000000" + numToBitStr(instr.mem_src.val, 8)
    else:
        bin_str += instr.mem_src.regStr() + "111"
        bin_str += instr.mem_dist.modeStr() + instr.mem_dist.modeStr()
    return [bin_str]

def assembleByterev(instr):
    return ["0000001011000" + instr.mem_src.regStr()]

def assembleClr(instr):
    bin_str = "01000010" + getSizeBitString(instr.opcode.data[1])
    bin_str += instr.mem_src.modeStr() + instr.mem_src.regStr()
    returnData = [bin_str]
    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleCmp(instr):
    bin_str = "1011" + instr.mem_dest.regStr()
    if instr.opcode.data[1] == 'b':
        bin_str += "000"
    elif instr.opcode.data[1] == 'w':
        bin_str += "001"
    elif instr.opcode.data[1] == 'l':
        bin_str += "010"
    bin_str += instr.mem_src.modeStr() + instr.mem_src.regStr()
    returnData = [bin_str]
    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleCmpA(instr):
    bin_str = "1011" + instr.mem_dest.regStr()
    if instr.opcode.data[1] == 'w':
        bin_str += "011"
    elif instr.opcode.data[1] == 'l':
        bin_str += "111"
    bin_str += instr.mem_src.modeStr() + instr.mem_src.regStr()
    returnData = [bin_str]
    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleCmpI(instr):
    bin_str = "00001100" + getSizeBitString(instr.opcode.data[1])
    bin_str += "000" + instr.mem_dest.regStr()
    bin_str += numToBitStr(instr.mem_dest.val, 32, True)
    return [bin_str]

def assembleDivs(instr):
    if instr.opcode.data[1] == 'w':
        bin_str = "1000" + instr.mem_dest.regStr() + "111"
        bin_str += instr.mem_src.modeStr() + instr.mem_src.regStr()
    else:
        bin_str = "0100110001" + instr.mem_src.modeStr() + instr.mem_src.regStr()
        bin_str += "0" + instr.mem_dest.regStr() + "100000000"
        bin_str += instr.mem_dest.regStr()
    returnData = [bin_str]
    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleDivu(instr):
    if instr.opcode.data[1] == 'w':
        bin_str = "1000" + instr.mem_dest.regStr() + "011"
        bin_str += instr.mem_src.modeStr() + instr.mem_src.regStr()
    else:
        bin_str = "0100110001" + instr.mem_src.modeStr() + instr.mem_src.regStr()
        bin_str += "0" + instr.mem_dest.regStr() + "000000000"
        bin_str += instr.mem_dest.regStr()
    returnData = [bin_str]
    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleEor(instr):
    bin_str = "1011" + instr.mem_src.regStr() + "110"
    bin_str += instr.mem_dest.modeStr() + instr.mem_dest.regStr()
    returnData = [bin_str]
    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleEorI(instr):
    bin_str = "0000101010000" + instr.mem_dest.regStr()
    bin_str += numToBitStr(instr.mem_src.val, 32)
    return[bin_str]

def assembleExt(instr):
    if instr.opcode.data[1] == 'w':
        bin_str = "0100100010000" + instr.mem_src.regStr()
    else:
        bin_str = "0100100011000" + instr.mem_src.regStr()
    return [bin_str]

def assembleIllegal(instr):
    return ["0100101011111100"]

def assembleJsr(instr):
    bin_str = "0100111010" + instr.mem_src.modeStr() + instr.mem_src.regStr()
    returnData = [bin_str]
    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleLea(instr):
    bin_str = "0100" + instr.mem_dest.regStr() + "111"
    bin_str += instr.mem_src.modeStr() + instr.mem_src.regStr()
    returnData = [bin_str]
    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleLink(instr):
    bin_str = "0100111001010" + instr.mem_src.regStr()
    bin_str += numToBitStr(instr.mem_dest.val, 16)
    return [bin_str]

def assembleLsl(instr):
    if isinstance(instr, instr.mem_src) == ImmediateData:
        bin_str = "1110" + numToBitStr(instr.mem_src.val, 3) + "110001"
        bin_str += instr.mem_dest.regStr()
    else:
        bin_str = "1110" + instrmem_src.regStr() + "110101"
        bin_str += instr.mem_dest.regStr()
    return [bin_str]

def assembleLsr(instr):
    if isinstance(instr, instr.mem_src) == ImmediateData:
        bin_str = "1110" + numToBitStr(instr.mem_src.val, 3) + "010001"
        bin_str += instr.mem_dest.regStr()
    else:
        bin_str = "1110" + instrmem_src.regStr() + "010101"
        bin_str += instr.mem_dest.regStr()
    return [bin_str]



def assembleNop(instr):
    return ["0100111001110001"]

def assembleNot(instr):
    return ["0100011010000" + instr.mem_src.regStr()]

def assembleRts(instr):
    return ["0100111001110101"]

def assembleStop(instr):
    return ["0100111001110010"]

def assembleSwap(instr):
    return ["0100100001000" + instr.mem_src.regStr()]
