#!/usr/bin/env python
import sys

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
        results = read_ipr(ipr_file)
    elif case == "sprot":
        blast_file = open(args[2], 'r')
        gff_file = open(args[3], 'r')
	fasta_file = open(args[4], 'r')
	file_output = open(args[5], 'w')
	results = read_sprot(blast_file, gff_file, fasta_file)
    else:
	print "That case is not yet supported"
	exit()
    write_results(results, file_output)

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

def read_sprot(blast_file, gff_file, fasta_file):
    fasta_info = get_fasta_info(fasta_file)
    gff_info = get_gff_info(gff_file)
    blast_info = get_blast_info(blast_file)
    sprot_list = []
    for mrna in gff_info:
	product = fasta_info[blast_info[mrna]][0]
	gene_name = fasta_info[blast_info[mrna]][1]
	gene_id = gff_info[mrna]
	sprot_list.append([gene_id, "name", gene_name])
	sprot_list.append([mrna, "product", product])
    return sprot_list

def get_fasta_info(fasta_file):
    dbxrefs = {}
    for line in fasta_file:
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
	    dbxrefs[ref] = (product,name)
    return dbxrefs

def get_blast_info(blast_file):
    mrna_dbxrefs = {}
    for line in blast_file:
        columns = line.split("\t")
        mrna = columns[0]
	ref = columns[1]
	mrna_dbxrefs[mrna] = ref
    return mrna_dbxrefs

def get_gff_info(gff_file):
    mrna_genes = {}
    for line in gff_file:
	columns = line.split("\t")
	if len(columns)>1 and columns[2] == "mRNA":
	    mrna_id = (columns[8].split(";")[0])[3:]
	    parent_gene = (columns[8].split(";")[1])[7:-1]
	    mrna_genes[mrna_id] = parent_gene
    return mrna_genes


def write_results(results, file_out):
    for line in results:
        file_out.write("\t".join(line)+"\n")

main(sys.argv)
