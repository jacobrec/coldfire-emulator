from assembler import symbolicLocation
import s19_gen

def link(objects):
    ob = objects[0] # don't yet support multiple files
    labelLoc = {}
    loc = 0
    for line in ob:
        if isinstance(line, symbolicLocation) and line.size == 0:
            labelLoc[line.name] = loc
        elif isinstance(line, symbolicLocation):
            loc += line.size
        else:
            loc += len(line)

        
    loc = 0
    data = []
    for line in ob:
        if isinstance(line, symbolicLocation) and line.size == 0:
            pass # don't care about empty labels here
        elif isinstance(line, symbolicLocation):
            if line.isRelative:
                l = labelLoc[line.name] - loc
            else:
                l = labelLoc[line.name]
            data.append(symLoc(l, line))

        else:
            data.append(line)
            loc += len(line)
    return (s19File(labelLoc["_start"], "".join(data)))


def symLoc(loc, sym):
    return bin(((1 << sym.size) -1) & loc)[2:].zfill(sym.size)


def toByteArray(binStr):
    """
    converts to bytes while preserving leading 0s
    
    >>> toByteArray("000000000000000000000000")
    [0, 0, 0]
    """

    a = []
    d = [binStr[i:i+8] for i in range(0, len(binStr), 8)]
    for b in d:
        a.append(int(b))

    return a

def s19File(startLoc, data):
    n = 64 # Split data into 64 bit blocks for s19 file
    d = [data[i:i+n] for i in range(0, len(data), n)]
    loc = 0
    s19 = []
    for b in d:
        s19.append(s19_gen.s1_rec(toByteArray(b), loc))
        loc += 64
    s19.append(s19_gen.s5_rec(len(d)))
    s19.append(s19_gen.s9_rec(startLoc))

    return("\n".join(s19))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
