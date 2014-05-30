#!/usr/bin/env python
import sys
from src.ipr import read_ipr
from src.sprot import read_sprot
from src.sprot import get_fasta_info
from src.sprot import get_blast_info
from src.sprot import get_gff_info
from src.annotation import write_annotations

#The command-line arguments will be:
#Case 1: IPRScan
    # ipr <ipr_file_name> <output_file_name>
#Case 2: Sprot Scan
    # sprot <blastout_file_name> <gff_file_name> <fasta_file_name> <output_file_name>

def main(args):
    case = args[1]
    if case == "ipr":
        ipr_file = open(args[2], 'r')
        file_output = open(args[3], 'w')
        annotations = read_ipr(ipr_file)
    elif case == "sprot":
        blast_file = open(args[2], 'r')
        gff_file = open(args[3], 'r')
        fasta_file = open(args[4], 'r')
        file_output = open(args[5], 'w')
        annotations = read_sprot(blast_file, gff_file, fasta_file)
    else:
        print("That case is not yet supported")
        exit()
    write_annotations(annotations, file_output)





main(sys.argv)
