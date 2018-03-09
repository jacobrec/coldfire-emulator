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


class AddressDirect(Memory):
    def __init__(self, regNum):
        self.num = regNum
        self.additionalsize = 0

    def __str__(self):
        return "%A{}".format(self.num)


class AddressIndirect(Memory):
    def __init__(self, regNum):
        self.num = regNum
        self.additionalsize = 0

    def __str__(self):
        return "(%A{})".format(self.num)


class AddressIndirectPostIncrement(Memory):
    def __init__(self, regNum):
        self.num = regNum
        self.additionalsize = 0

    def __str__(self):
        return "(%A{})+".format(self.num)


class AddressIndirectPreDecrement(Memory):
    def __init__(self, regNum):
        self.num = regNum
        self.additionalsize = 0

    def __str__(self):
        return "-(%A{})".format(self.num)


class AddressIndirectWithOffset(Memory):
    def __init__(self, regNum, offset):
        self.num = regNum
        self.offset = offset
        self.additionalsize = 2

    def __str__(self):
        return "{1}(%A{0})".format(self.num, self.offset)


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


class AbsoluteShort(Memory):
    def __init__(self, data):
        self.loc = data
        self.additionalsize = 2

    def __str__(self):
        return "{}.w".format(hex(self.loc))


class AbsoluteLong(Memory):
    def __init__(self, data):
        self.loc = data
        self.additionalsize = 4

    def __str__(self):
        return "{}.l".format(hex(self.loc))


class ImmediateData(Memory):
    def __init__(self, data):
        self.val = data
        self.additionalsize = 4

    def __str__(self):
        return "#{}".format(self.val)

    # | n(PC)             # PC with offset
    # | n(PC, Xn * SF)      # Scaled pc with offset
