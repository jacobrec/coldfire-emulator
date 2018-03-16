# Cpu
16 registers %A0-%A7/%D0-%D7
each register is 32 bits

Long is 32 bits
Word is 16 bits
Byte is 8 bits

CCR is 16 bits [T*SMIII***XNZVC]
T: Trace Mode

S: Supervisor State
M: Master/Interrupt State
I: I2 Interrupt
I: I1 Interrupt
I: I0 Interrupt



X: Extend Flag
N: Negative Flag
Z: Zero Flag
V: Overflow Flag
C: Carry Flag


# C code
/**************************************************************************************************************/
#define FLAG_CLEAR    1
#define FLAG_OVERFLOW 2
#define FLAG_ZERO     4
#define FLAG_NEG      8
#define FLAG_CARRY    16


struct CPU{
    int32_t A[8];
    int32_t D[8];
    uint16_t CCR;
    char ram[1024*64]; // 64 kilobytes of static ram
    uint32_t PC;
};

/**************************************************************************************************************/

# Questions:

How do you assemble something like?
    move.l 32(%A0, %D1*2), 8(%A2, %D3*1)





