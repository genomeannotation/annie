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
	results = read_sprot(blastFile, gffFile, fastaFile)
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

def read_sprot(blastFile, gffFile, fastaFile):
    fastaInfo = getFastaInfo(fastaFile)
    gffInfo = getGffInfo(gffFile)
    blastInfo = getBlastInfo(blastFile)
    sprot_list = []
    for mRNA in gffInfo:
	product = fastaInfo[blastInfo[mRNA]][0]
	geneName = fastaInfo[blastInfo[mRNA]][1]
	geneID = gffInfo[mRNA]
	sprot_list.append([geneID, "name", geneName])
	sprot_list.append([mRNA, "product", product])
    return sprot_list

def getFastaInfo(fastaFile):
    myDict = {}
    for line in fastaFile:
	if line[0] == '>':
	    words = line.split(" ")
            ref = words[0][1:]
	    i=0
	    while words[i].find("OS=") == -1:
		i += 1
	    product = " ".join(words[1:i])
	    i=0
	    while words[i].find("GN=") == -1 and words[i].find("PE=") == -1:
		i += 1
	    if not words[i].find("GN=") == -1:
		j=i
		while words[j].find("PE=") == -1:
		    j += 1
		name = (" ".join(words[i:j]))[3:]		
	    else:
		name = "UNNAMED"
	    myDict[ref] = (product,name)
    return myDict

def getBlastInfo(blastFile):
    myDict = {}
    for line in blastFile:
        columns = line.split("\t")
        mrna = columns[0]
	ref = columns[1]
	myDict[mrna] = ref
    return myDict

def getGffInfo(gffFile):
    myDict = {}
    for line in gffFile:
	columns = line.split("\t")
	if columns[2] == "mRNA":
	    mRNA_ID = (columns[8].split(";")[0])[3:]
	    parentGene = (columns[8].split(";")[1])[7:-1]
	    myDict[mRNA_ID] = parentGene
    return myDict


def writeResults(results, fileOut):
    for line in results:
        fileOut.write("\t".join(line)+"\n")

main(sys.argv)
