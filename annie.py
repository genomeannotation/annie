#!/usr/bin/env python
import os
import sys
import argparse
from src.ipr import read_ipr
from src.sprot import read_sprot
from src.sprot import get_fasta_info
from src.sprot import get_blast_info
from src.sprot import get_gff_info
from src.annotation import write_annotations
from src.fix import fix_anno

def main(args):
    parser = argparse.ArgumentParser(
    epilog="""
    Docs at http://genomeannotation.github.io/annie/
    Bugs and feature requests at https://github.com/genomeannotation/annie/issues
    """,
    formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-ipr', '--iprscan', help="IPRScan output file, tab-separated")
    parser.add_argument('-b', '--blast-output')
    parser.add_argument('-g', '--gff', help="GFF3 file corresponding to assembly")
    parser.add_argument('-db', '--blast-database', help="The fasta file against which BLAST was run")
    parser.add_argument('--blacklist')
    parser.add_argument('--whitelist')
    parser.add_argument('-o', '--output')
    parser.add_argument('--fix_bad_products', action='store_true',
            help="Attempt to fix annotations that violate NCBI guidelines")
    args = parser.parse_args()

    # Make sure we got enough args
    ipr = False
    sprot = False
    if args.iprscan:
        ipr = True
    if args.blast_output and args.gff and args.blast_database:
        sprot = True
    if not (ipr or sprot):
        sys.stderr.write("Error: must provide --iprscan OR --blast-output, --gff and --blast-database\n\n")
        parser.print_help()
        sys.exit()

    # Open output file
    out = "annie_output.tsv"
    if args.output:
        out = args.output
    outfile = open(out, 'w')

    # Create an empty list to store Annotation objects
    annotations = []

    # Add IPRScan results if requested
    if ipr:
        try:
            ipr_file = open(args.iprscan, 'r')
        except IOError:
            print("Sorry, Annie says either one of the files doesn't exist or it could not be read.")
            exit()
        if args.whitelist:
            #obtain whitelist and get rid of lowercase and whitespace padding
            whitelist = [word.strip().lower() for word in open(args.whitelist,'r').readlines()]            
            args.whitelist.close()
        else:
            whitelist = []
        annotations.extend(read_ipr(ipr_file, whitelist))
        ipr_file.close()

    # Add SwissProt results if requested
    if sprot:
        try:
            blast_file = open(args.blast_output, 'r')
            gff_file = open(args.gff, 'r')
            fasta_file = open(args.blast_database, 'r')
        except IOError:
            print("Sorry, Annie says either one of the files doesn't exist or it could not be read.")
            exit()
        annotations.extend(read_sprot(blast_file, gff_file, fasta_file))
        blast_file.close()
        gff_file.close()
        fasta_file.close()

    # Now go back and remove stuff if requested
    if args.blacklist:
        with open(args.blacklist, "r") as bad_products_file:
            bad_products = []
            bad_features = []
            keepers = []
            # Get bad products
            for line in bad_products_file:
                bad_products.append(line.strip())
        # Find bad features
        for anno in annotations:
            for product in bad_products:
                if anno.key == "product" and anno.value == product:
                    bad_features.append(anno.feature_id)
        # Decide what to keep
        for anno in annotations:
            if anno.feature_id not in bad_features:
                keepers.append(anno)
        annotations = keepers

    # Optional step to fix annotations
    if args.fix_bad_products:
        with open("fix_bad_products.log", 'w') as fixlog:
            fixlog.write("Original\tUpdated\n")
            for anno in annotations:
                # only fix if it's a 'product'
                if anno.key == "product":
                    new_value = fix_anno(anno.value)
                    if new_value != anno.value:
                        fixlog.write(anno.value + "\t" + new_value + "\n")
                    anno.value = new_value

    #write the annotations to file and close
    write_annotations(annotations, outfile)
    outfile.close()

####################################################################################################

if __name__ == "__main__":
    main(sys.argv)
