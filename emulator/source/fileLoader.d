import std.conv;
import std.file;
import std.string;
/**
 * A convinance function, creates a new fileLoader, and loads the file
 */
void parseFile(string filepath, ref ubyte[64*1024] memory, ref uint pc){
    FileLoader fl = new FileLoader();
    fl.parseFile(filepath, memory, pc);
}


/**
 * A class to load srec files
 * loads contents into internal buffer in correct position, then
 * it can be copied into the emulators memory
 */
class FileLoader{

    ubyte[64*1024] memory;
    uint startLoc;


    void parseFile(string filepath, ref ubyte[64*1024] memory, ref uint pc){
        auto data = readText(filepath);
        string[] lines = split(data, '\n');
        foreach(string line; lines){
            if (line.length < 2){
                continue;
            }
            char indicator = line[1];
            switch(indicator){
                case '1':
                    this.parseS1Rec(line);
                    break;
                case '9':
                    this.parseS9Rec(line);
                    break;
                default:
                    // ignore s5 records and all other records
            }
        }
        for(int i = 0; i < 64*1024; i++){
            memory[i] = this.memory[i];
        }
        pc = this.startLoc;
    }






    /**
     * Parses the S1 record into an array of bytes
     *
     * Note, will check size but ignore checksum of the record
     *
     * Format of s1 rec is as follows
     * S1[size:2][loc:4][data:fill][checksum:2]
     */
    void parseS1Rec(string record){

        assert(record[0] == 'S');
        assert(record[1] == '1');

        int size = to!int(record[2..4], 16) - 3;
        int loc = to!int(record[4..8], 16);
        char[] item = cast(char[]) record[8..$]; // a slice of char[] needs to be created from the string to allow quick mutations

        for(int i = 0; i < size; i++){
            this.memory[i + loc] = to!ubyte(item[0..2], 16);
            item = item[2..$]; // slice operations in D are fast, and this won't create additiona arrays
        }
    }

    /**
     * Parses the S9 record into an unsigned short
     *
     * Will ignore the checksum
     *
     * Format of an S9 record
     * S9[size:2][startLoc:4][checksum:2]
     */
    void parseS9Rec(string record){
        assert(record[0] == 'S');
        assert(record[1] == '9');

        this.startLoc = to!uint(record[4..8], 16);
    }
}
unittest{
    FileLoader fl = new FileLoader();
    fl.parseS1Rec("S11F00007C0802A6900100049421FFF07C6C1B787C8C23783C6000003863000026");
    ubyte[] start = [124, 8, 2, 166, 144, 1, 0, 4, 148, 33, 255, 240, 124, 108, 27, 120, 124, 140, 35, 120, 60, 96, 0, 0, 56, 99, 0, 0];

    for(int i = 0; i < start.length; i++){
        assert(fl.memory[i] == start[i]);
    }

    fl.parseS9Rec("S9030000FC");
    assert(fl.startLoc == 0);
}
