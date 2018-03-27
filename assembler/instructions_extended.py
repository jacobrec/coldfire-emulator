import parser
import memory
from s19_gen import to_byte_array
import s19_gen

'''
Operations to be done later: (we really need to figure out wild wildcards)
Add
Move
As*
B**
Bsr
'''

def assembleAdd(instr):  # currently only supports first op mode, also need to integrate adda
    bin_str = "1101" + instr.mem_dest.regStr()
    if True:  # conditional if storing in eff destination
        bin_str += "010" + instr.mem_src.modeStr() + instr.mem_src.regStr()
    else:
        bin_str += "110" + instr.mem_dest.modeStr() + instr.mem_dest.regStr()
    returnData = [bin_str]
    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleAddA(instr):
    bin_str = "1101" + instr.mem_dest.regStr() + "111"
    bin_str += instr.mem_src.modeStr() + instr.mem_src.regStr()
    returnData = [bin_str]
    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleAddI(instr):
    bin_str = "0000011010"
    bin_str += instr.mem_dest.regStr()  # not sure about This
    returnData = [bin_str] + assembleExtraData(instr)
    return returnData

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
    if instr.mem_dest._match(Register):  # if final dest is register
        bin_str += "010" + instr.mem_src.modeStr() + instr.mem_src.regStr()
    else:
        bin_str += "110" + instr.mem_src.modeStr() + instr.mem_src.regStr()
    returnData = [bin_str]
    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleAndI(instr):
    bin_str = "0000001010000" + instr.mem_dest.regStr()
    returnData = [bin_str] + assembleExtraData(instr)
    return returnData

def assembleAs(instr):
    bin_str += "1110"
    if True:  # if from Register
        bin_str += instr.mem_src.regStr()
        if True:  # right shift
            bin_str += "0"
        else:
            bin_str += "1"
        bin_str += "10100"
    else:  # immediate value
        assert(instr.mem_src.val < 8)
        bin_str += numToBitStr(instr.mem_src.val, 3)
        if True:  # right shift
            bin_str += "0"
        else:
            bin_str += "1"
        bin_str += "10000"
    return [bin_str]

def assembleBcc(instr):
    conditions = {
    "true"  : "0000",
    "false" : "0001",
    "high"  : "0010",
    "low/=" : "0011",
    "cClear": "0100",
    "cSet"  : "0101",
    "NE"    : "0110",
    "EQ"    : "0111",
    "VC"  : "1000",
    "VS" : "1001",
    "PL"  : "1010",
    "MI" : "1011",
    "GE": "1100",
    "LT"  : "1101",
    "GT"    : "1110",
    "LE"    : "1111",
    }

    '''
    needs to reference, "0000" if filler for conditions
    '''
    bin_str = "0110" + "0000"
    return [bin_str, symbolicLocation(instr.mem_src.name, 8, True)]

def assembleBchg(instr):
    bin_str = "0000"
    if instr.mem_src._match(Literal):  # if literal
        bin_str += "100010" + instr.mem_dest.modeStr() + instr.mem_dest.regStr()
        bin_str += "00000000" + numToBitStr(instr.mem_src.val)
    else:
        bin_str += instr.mem_src.regStr() + "101"
        bin_str += instr.mem_dist.modeStr() + instr.mem_dist.modeStr()
    return [bin_str]

def assembleBclr(instr):
    bin_str = "0000"
    if instr.mem_src._match(Literal):  # if literal
        bin_str += "100010" + instr.mem_dest.modeStr() + instr.mem_dest.regStr()
        bin_str += "00000000" + numToBitStr(instr.mem_src.val)
    else:
        bin_str += instr.mem_src.regStr() + "110"
        bin_str += instr.mem_dist.modeStr() + instr.mem_dist.modeStr()
    return [bin_str]

def assembleBitrev(instr):
    return ["0000000011000" + instr.mem_src.regDest()]

def assembleBra(instr):
    # TODO: make functional
    return None

def assembleBset(instr):
    bin_str = "0000"
    if instr.mem_src._match(Literal):  # if literal
        bin_str += "100011" + instr.mem_dest.modeStr() + instr.mem_dest.regStr()
        bin_str += "00000000" + numToBitStr(instr.mem_src.val)
    else:
        bin_str += instr.mem_src.regStr() + "100"
        bin_str += instr.mem_dist.modeStr() + instr.mem_dist.modeStr()
    return [bin_str]

def assembleBtst(instr):
    bin_str = "0000"
    if instr.mem_src._match(Literal):  # if literal
        bin_str += "100000" + instr.mem_dest.modeStr() + instr.mem_dest.regStr()
        bin_str += "00000000" + numToBitStr(instr.mem_src.val)
    else:
        bin_str += instr.mem_src.regStr() + "111"
        bin_str += instr.mem_dist.modeStr() + instr.mem_dist.modeStr()
    return [bin_str]

def assembleByterev(instr):
    return ["0000001011000" + instr.mem_src.regStr()]


def assembleIllegal(instr):
    return ["0100101011111100"]

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
