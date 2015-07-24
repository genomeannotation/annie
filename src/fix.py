#!/usr/bin/env python

import re
from src.whitelist import whitelist
from src.known_fixes import known_fixes

def remove_extra_whitespace(line):
    """Helper method"""
    # make sure we didn't leave extra whitespace
    fields = line.strip().split()
    return " ".join([f.strip() for f in fields])

def contains_3_or_more_numbers_in_a_row(word):
    """Helper method"""
    numcount = 0
    numrun = False
    for letter in word:
        if letter in '0123456789':
            numrun = True
            numcount += 1
            if numcount >= 3:
                return True
        else:
            numcount = 0
            numrun = False
    return False

def remove_protein_homolog(line):
    if "protein homolog" in line:
        line = re.sub("protein homolog", "", line)
    if "homolog protein" in line:
        line = re.sub("homolog protein", "", line)
    if "homolog" in line:
        line = re.sub("homolog", "", line)
    return remove_extra_whitespace(line)

def remove_fragment(anno):
    fields = anno.strip().split()
    if fields[-1].startswith("(Fragment"):
        fields = fields[:-1]
    return " ".join(fields)

def remove_string_containing_underscore(anno):
    anno = re.sub("\S*_\S*", "", anno)
    return remove_extra_whitespace(anno)

def remove_kDa(anno):
    anno = re.sub("of [0-9]* kDa", "", anno)
    anno = re.sub("[0-9]* kDa", "", anno)
    return remove_extra_whitespace(anno)

def remove_gene_optionally_followed_by_numbers(anno):
    anno = re.sub("gene [0-9]*", "", anno)
    return remove_extra_whitespace(anno)

def remove_trailing_hyphens(anno):
    if anno.endswith("-"):
        anno = anno[:-1]
    return anno

def fix_anno(anno):
    # Do nothing if we know it's okay
    if anno in whitelist:
        return anno
    # If we've fixed it by hand before, we know the answer
    elif anno in known_fixes:
        return known_fixes[anno]
    # Otherwise, patch and duct tape ...
    else:
        anno = remove_fragment(anno)
        anno = remove_protein_homolog(anno)
        anno = remove_kDa(anno)
        anno = remove_trailing_hyphens(anno)
        return anno
