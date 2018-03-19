
import assembler


class Memory:
    pass


class Label:
    def __init__(self, name, isDef=False):
        self.name = name
        self.isDef = isDef
        self.additionalsize = 0

    def __str__(self):
        return "{}:".format(self.name)


class DataDirect(Memory):
    def __init__(self, regNum):
        self.num = regNum
        self.additionalsize = 0

    def __str__(self):
        return "%D{}".format(self.num)

    def modeStr(self):
        return "000"

    def regStr(self):
        return assembler.numToBitStr(self.num, 3)


class AddressDirect(Memory):
    def __init__(self, regNum):
        self.num = regNum
        self.additionalsize = 0

    def __str__(self):
        return "%A{}".format(self.num)

    def modeStr(self):
        return "001"

    def regStr(self):
        return assembler.numToBitStr(self.num, 3)


class AddressIndirect(Memory):
    def __init__(self, regNum):
        self.num = regNum
        self.additionalsize = 0

    def __str__(self):
        return "(%A{})".format(self.num)

    def modeStr(self):
        return "010"

    def regStr(self):
        return assembler.numToBitStr(self.num, 3)


class AddressIndirectPostIncrement(Memory):
    def __init__(self, regNum):
        self.num = regNum
        self.additionalsize = 0

    def __str__(self):
        return "(%A{})+".format(self.num)

    def modeStr(self):
        return "011"

    def regStr(self):
        return assembler.numToBitStr(self.num, 3)


class AddressIndirectPreDecrement(Memory):
    def __init__(self, regNum):
        self.num = regNum
        self.additionalsize = 0

    def __str__(self):
        return "-(%A{})".format(self.num)

    def modeStr(self):
        return "100"

    def regStr(self):
        return assembler.numToBitStr(self.num, 3)


class AddressIndirectWithOffset(Memory):
    def __init__(self, regNum, offset):
        self.num = regNum
        self.offset = offset
        self.additionalsize = 2

    def __str__(self):
        return "{1}(%A{0})".format(self.num, self.offset)

    def modeStr(self):
        return "101"

    def regStr(self):
        return assembler.numToBitStr(self.num, 3)

    def extraData(self):
        return [self.offset]


class ScaledAddressWithOffset(Memory):
    def __init__(self, addRegNum, reg2Num, reg2Type, scaleFactor, offset):
        self.offset = offset
        self.addRegNum = addRegNum
        self.reg2Type = reg2Type
        self.reg2Num = reg2Num
        self.scaleFactor = scaleFactor
        self.additionalsize = 2

    def __str__(self):
        return "{}(%A{}, %{}{}*{})".format(self.offset, self.addRegNum, self.reg2Type.upper(), self.reg2Num, self.scaleFactor)

    def modeStr(self):
        return "110"

    def regStr(self):
        return assembler.numToBitStr(self.num, 3)

    def extraData(self):
        print("##############################")
        print("# Find out the order of this #")
        print("##############################")
        assert(0)


class AbsoluteShort(Memory):
    def __init__(self, data):
        self.val = data
        self.additionalsize = 2

    def __str__(self):
        return "{}.w".format(hex(self.val))

    def modeStr(self):
        return "111"

    def regStr(self):
        return "000"

    def extraData(self):
        return self.val


class AbsoluteLong(Memory):
    def __init__(self, data):
        self.val = data
        self.additionalsize = 4

    def __str__(self):
        return "{}.l".format(hex(self.val))

    def modeStr(self):
        return "111"

    def regStr(self):
        return "001"

    def extraData(self):
        return self.val


class ImmediateData(Memory):
    def __init__(self, data):
        self.val = data
        self.additionalsize = 4

    def __str__(self):
        return "#{}".format(self.val)

    def modeStr(self):
        return "111"

    def regStr(self):
        return "100"

    def extraData(self):
        return self.val

    # | n(PC)             # PC with offset
    # | n(PC, Xn * SF)      # Scaled pc with offset
