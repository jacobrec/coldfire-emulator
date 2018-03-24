import parser
import memory
from s19_gen import to_byte_array
import s19_gen

def assembleAdd(instr):  # currently only supports first op mode
    bin_str = "1101" + instr.mem_dest.regStr()
    if True:  # conditional if storing in eff destination
        bin_str += "010" + instr.mem_dest.modeStr() + instr.mem_dest.regStr()
    else:
        bin_str += "110" + instr.mem_src.modeStr() + instr.mem_src.regStr()
    returnData = [bin_str]

    if len(instr) > 2:  # for extra bits in case
        returnData += assembleExtraData(instr)
    return returnData

def assembleAddA(instr):
    bin_str = "1101" + instr.mem_dest.regStr() + "111"
    bin_str += bin_str += instr.mem_src.modeStr() + instr.mem_src.regStr()
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
