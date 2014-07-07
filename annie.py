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
    #in the case that the user doesn't give any command-line arguments
    if len(args) == 1:
        print("Sorry, Annie.py can't be run without additional command-line arguments. Type \"python annie.py help\" for more information.")
        exit()

    #check which case the user is doing: ipr, sprot, etc
    case = args[1]
    if case == "ipr": # if ipr case
        if len(args) != 4: #if wrong number of command-line args
            print("Annie wants to remind you that you should have 3 command-line arguments for ipr. You entered too many or too little")
            exit()
        try:
            ipr_file = open(args[2], 'r')
            file_output = open(args[3], 'w')
        except IOError:
            print("Sorry, Annie says either one of the files doesn't exist or it could not be read.")
            exit()
        whitelist = [word.strip().lower() for word in open("config/dbxref_whitelist",'r').readlines()] #obtain whitelist and get rid of lowercase and whitespace padding
        annotations = read_ipr(ipr_file, whitelist)
        ipr_file.close()
    elif case == "sprot": #if sprot case
        if len(args) != 6: #if wrong number of command-line args
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
    elif case == "filter":
        with open(args[2], "r") as annotations_file, open(args[3], "r") as bad_products_file, open(args[4], "w") as outfile:
            bad_products = []
            bad_features = []
            annotations = []
            # Get bad products
            for line in bad_products_file:
                bad_products.append(line.strip())
            # Find bad features
            for line in annotations_file:
                anno = line.strip().split("\t")
                annotations.append(anno)
                for product in bad_products:
                    if anno[1] == "product" and anno[2] == product:
                        bad_features.append(anno[0])
            # Write new file
            for anno in annotations:
                if anno[0] not in bad_features:
                    outfile.write("\t".join(anno) + "\n")
            exit()
    elif case == "help": #if help case
        print("Here are the allowed inputs for Annie:\
        \n\tipr <ipr_file_name> <output_file_name>\
        \n\tsprot <blastout_file_name> <gff_file_name> <fasta_file_name> <output_file_name>\
        \n\tfilter <annotations_file> <product_blacklist> <output_file_name>")
        exit()
    else: #if invalid case
        print("Sorry, Annie says that case is not yet supported. Please double check your first command-line argument.")
        exit()

    #write the annotations to file and close
    write_annotations(annotations, file_output)
    file_output.close()





main(sys.argv)
