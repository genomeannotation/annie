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
        if len(args) != 4:
            print("Annie wants to remind you that you should have 3 command-line arguments for ipr. You entered too many or too little")
            exit()
        try:
            ipr_file = open(args[2], 'r')
            file_output = open(args[3], 'w')
        except IOError:
            print("Sorry, Annie says either one of the files doesn't exist or it could not be read.")
            exit()
        whitelist = [word.strip().lower() for word in open("config/dbxref_whitelist",'r').readlines()]
        annotations = read_ipr(ipr_file, whitelist)
        ipr_file.close()
    elif case == "sprot":
        if len(args) != 6:
            print("Annie wants to remind you that you should have 5 command-line arguments for sprot. You entered too many or too little")
            exit()
        try:
            blast_file = open(args[2], 'r')
            gff_file = open(args[3], 'r')
            fasta_file = open(args[4], 'r')
            file_output = open(args[5], 'w')
        except IOError:
            print("Sorry, Annie says either one of the files doesn't exist or it could not be read.")
            exit()
        annotations = read_sprot(blast_file, gff_file, fasta_file)
        blast_file.close()
        gff_file.close()
        fasta_file.close()
    elif case == "help":
        print("Here are the allowed inputs for Annie:\n\tipr <ipr_file_name> <output_file_name>\n\tsprot <blastout_file_name> <gff_file_name> <fasta_file_name> <output_file_name>")
        exit()
    else:
        print("Sorry, Annie says that case is not yet supported. Please double check your first command-line argument.")
        exit()
    write_annotations(annotations, file_output)
    file_output.close()





main(sys.argv)
