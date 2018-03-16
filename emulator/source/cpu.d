/**
 * The coldfire cpu
 *
 * A struct for storing info about the hardware
 *
 * 8 data registers, marked by D[0] - D[7]
 * 8 address registers, marked by A[0] - A[7]
 * CCR is the condition register 16 bits [T*SMIII***XNZVC], see coldfire.md for more details
 */
struct Cpu{
    int[8] A;
    int[8] D;
    ushort CCR;
    char[1024*64] ram;
    uint pc;

    ushort opcode;
}
