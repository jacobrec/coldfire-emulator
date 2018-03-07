

class Instruction:
    """
    An instruction is an opcode(op, size) followed by 0-2 data locations
    """

    def __init__(self, opcode, mem1=None, mem2=None):
        self.opcode = opcode
        self.mem_src = mem1
        self.mem_dest = mem2


class Directive:
    """
    An directive is an name followed by any additional data
    """

    def __init__(self, directive, data=None):
        self.directive = opcodirectivede
        self.data = data


# Jarrett, you'll need to write this class as you see fit
# this basically the data register mode
class Data:
    pass
