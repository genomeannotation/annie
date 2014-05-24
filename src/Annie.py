#!/usr/bin/env python
import sys

#The command-line arguments will be:
#Case 1: IPRScan
    # ipr <iprFileName> <outputFileName>
#Case 2: asdf
    # sprot <blastoutFileName> <gffFileName> <fastaFileName> <outputFileName>

def main(args):
    case = args[1]
    if case == "ipr":
        iprFile = open(args[2], 'r')
        fileOutput = open(args[3], 'w')
        results = read_ipr(iprFile)
    elif case == "sprot":
        blastFile = open(args[2], 'r')
        gffFile = open(args[3], 'r')
	fastaFile = open(args[4], 'r')
	fileOutput = open(args[5], 'w')
	results = read_case2(blastFile, gffFile, fastaFile)
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

def read_case2(blastFile, gffFile, fastaFile):
    return getFastaHeaders(fastaFile)

def getFastaHeaders(fastaFile):
    lines = []
    for line in fastaFile:
	if line[0] == '>':
	    words = line.split(" ")
            ref = words[0]
	    i=0
	    while words[i].find("OS=") == -1:
		i += 1
	    product = words[i-1]
	    if words[i+1].find("GN=") == -1:
		name = "UNKNOWN"
	    else:
		name = words[i+1]
	    lines.append([ref, product, name])
    return lines

def writeResults(results, fileOut):
    for line in results:
        fileOut.write(" ".join(line)+"\n")

main(sys.argv)
