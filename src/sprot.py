#!/usr/bin/env python
import sys
from collections import namedtuple

Annotation = namedtuple('Annotation', 'feature_id key value')

def read_sprot(blast_file, gff_file, fasta_file):
    fasta_info = get_fasta_info(fasta_file)
    gff_info = get_gff_info(gff_file)
    blast_info = get_blast_info(blast_file)
    sprot_list = []
    for mrna, dbxref in blast_info.items():
        if dbxref not in fasta_info:
            print(mrna+" has dbxref "+dbxref+" that's not in the fasta. Skipping...")
            continue
        if mrna not in gff_info:
            print( mrna+" not in gff. Skipping...")
            continue
        product = fasta_info[dbxref][0]
        gene_name = fasta_info[dbxref][1]
        gene_id = gff_info[mrna]
        sprot_list.append(Annotation(gene_id, "name", gene_name))
        sprot_list.append(Annotation(mrna, "product", product))
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
                name = ref.split("|")[2].split("_")[0]
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
            parent_gene = (columns[8].strip().split(";")[1])[7:]
            mrna_genes[mrna_id] = parent_gene
    return mrna_genes


