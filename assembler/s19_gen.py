from utils import assertAs


def generate_s19_file(bin_list, start_loc=0):
    """
    this will take that list, and return the list of records, it also takes the start location of the program
    the list it takes in is a list of tuples containing the data, then the memory location

    >>> generate_s19_file([(15, 0),(10, 4)], 0)
    ['S10400000FEC', 'S10400040AED', 'S5030002FA', 'S9030000FC']
    """
    srecs = []
    for binl in bin_list:
        srecs.append(s1_rec(*binl))
    srecs.append(s5_rec(len(srecs)))
    srecs.append(s9_rec(start_loc))
    return srecs


def s1_rec(data, loc):
    """
    Generates s1 records from a given address and a byte array


    >>> s1_rec([int("00000000",2),int("00000000",2)], 0)
    'S10500000000FA'

    >>> s1_rec(15, 0)
    'S10400000FEC'

    >>> s1_rec([0, 0, 0], 0)
    'S1060000000000F9'

    >>> s1_rec(0xCCC, 0)
    'S10500000CCC22'

    >>> s1_rec([124, 8, 2, 166, 144, 1, 0, 4, 148, 33, 255, 240, 124, 108, 27, 120, 124, 140, 35, 120, 60, 96, 0, 0, 56, 99, 0, 0], 0)
    'S11F00007C0802A6900100049421FFF07C6C1B787C8C23783C6000003863000026'

    >>> s1_rec([75, 255, 255, 229, 57, 128, 0, 0, 125, 131, 99, 120, 128, 1, 0, 20, 56, 33, 0, 16, 124, 8, 3, 166, 78, 128, 0, 32], int("001C", 16))
    'S11F001C4BFFFFE5398000007D83637880010014382100107C0803A64E800020E9'

    >>> s1_rec([72, 101, 108, 108, 111, 32, 119, 111, 114, 108, 100, 46, 10, 0], int("0038", 16))
    'S111003848656C6C6F20776F726C642E0A0042'
    """

    addr = to_hex_string(loc, 4)
    byts = to_hex_string(data)
    byts = to_hex_string(data, ((len(byts) + 1) // 2) * 2)
    size = len(byts) + len(addr) + 2

    assert(size % 2 == 0)
    size = size // 2

    checksum = get_checksum(size, to_byte_array(addr + byts))

    return "S1{}{}{}{}".format(to_hex_string(size, 2), addr, byts, checksum)


def s5_rec(num):
    """
    Generates the s5 record based on a given number of records

    >>> s5_rec(3)
    'S5030003F9'

    >>> s5_rec(20)
    'S5030014E8'
    """
    assertAs(num < (2 ** 16 - 1),
             "Number of records must be 16 bits for S5 record")
    data = ([0, 0] + to_byte_array(num))[-2:]
    size = 3
    checksum = get_checksum(size, data)

    return "S5{}{}{}".format(to_hex_string(size, 2), "".join(
        [to_hex_string(x, 2) for x in data]), checksum)


def s9_rec(address):
    """
    Generates the s9 record based on a given start address

    >>> s9_rec(0)
    'S9030000FC'
    """
    assertAs(address < (2 ** 16 - 1),
             "Number of records must be 16 bits for S5 record")
    data = ([0, 0] + to_byte_array(address))[-2:]
    size = 3
    checksum = get_checksum(size, data)

    return "S9{}{}{}".format(to_hex_string(size, 2), "".join(
        [to_hex_string(x, 2) for x in data]), checksum)


def get_checksum(size, data):
    """
    Computes the checksum according to this https://en.wikipedia.org/wiki/SREC_(file_format)#Checksum_calculation

    >>> get_checksum(3, [0, 3])
    'F9'

    >>> get_checksum(int("13", 16), to_byte_array("7AF00A0A0D"))
    '61'
    """
    return to_hex_string((~(sum(data) + size) & 0b11111111), 2)


def to_hex_string(num, minDigits=0):
    """
    Helper function that converts a number to a 0 padded hex string

    >>> to_hex_string(5, 4)
    '0005'

    >>> to_hex_string(16)
    '10'

    >>> to_hex_string(20, 4)
    '0014'

    >>> to_hex_string(255)
    'FF'

    >>> to_hex_string([255, 255])
    'FFFF'

    >>> to_hex_string([1, 1])
    '0101'

    >>> to_hex_string([0, 0, 0])
    '000000'

    >>> to_hex_string(0, 4)
    '0000'
    """
    if isinstance(num, int):
        s = hex(num)[2:]
        if minDigits > len(s):
            s = "0" * (minDigits - len(s)) + s
        if s.endswith('L') or s.endswith('l'):
            s = s[:-1]
    else:
        s = "".join([to_hex_string(x, 2) for x in num])
        if minDigits > len(s):
            s = "0" * (minDigits - len(s)) + s
    return s.upper()


def to_byte_array(number, minDigits=0):
    """
    Converts number to a variable size array of bytes

    >>> to_byte_array(10)
    [10]

    >>> to_byte_array(257)
    [1, 1]

    >>> to_byte_array(256)
    [1, 0]

    >>> to_byte_array('FFFFFF')
    [255, 255, 255]

    """
    byts = []
    if isinstance(number, str):
        number = int(number, 16)
    while number != 0:
        byts.insert(0, number % 256)
        number = number // 256

    if minDigits > len(byts):
        s = [0] * (minDigits - len(byts)) + byts

    return byts


if __name__ == "__main__":
    import doctest
    doctest.testmod()
