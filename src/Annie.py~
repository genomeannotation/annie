#!/usr/bin/env python
import sys

#The command-line arguments will be:
#Case 1: IPRScan
    # ipr <iprFileName> <outputFileName>
#Case 2: asdf
    # case2 <file1> <file 2> <outputFileName>

def main(args):
    case = args[1]
    if case == "ipr":
        fileInput = open(args[2], 'r')
        fileOutput = open(args[3], 'w')
        results = read_ipr(fileInput)
    elif case == "case2":
        fileInput1 = open(args[2], 'r')
        fileInput2 = open(args[3], 'r')
	fileOutput = open(args[4], 'w')
	results = read_case2(fileInput1, fileInput2)
    writeResults(results, fileOutput)

    #myFile = open(arg1, 'r')
    #print myFile.read()

def read_ipr(io_buffer):
    """Returns a list of lists, each containing mrna_id, "Dbxref" and annotation."""
    ipr_list = []
    for line in io_buffer:
        columns = line.split("\t")
        if len(columns)>1:
             ipr_list.append([columns[0], "Dbxref", columns[3]+":"+columns[4]])
    ipr_list = sorted(ipr_list)
    ipr_list = [ipr_list[i] for i in range(len(ipr_list)) if i
                             == 0 or ipr_list[i] != ipr_list[i-1]]
    return ipr_list

def read_case2(file1, file2):
    print ""

def writeResults(results, fileOut):
    for line in results:
        fileOut.write(" ".join(line)+"\n")

main(sys.argv)
