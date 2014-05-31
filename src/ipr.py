#!/usr/bin/env python
import sys
from collections import namedtuple

Annotation = namedtuple('Annotation', 'feature_id key value')

def read_ipr(io_buffer, whitelist=None):
    """Returns a list of lists, each containing mrna_id, "Dbxref" and annotation."""
    ipr_list = []
    for line in io_buffer:
        columns = line.split("\t")
        if len(columns)>1 and (columns[3].strip().lower() in whitelist):
             ipr_list.append(Annotation(columns[0], "Dbxref", columns[3]+":"+columns[4]))
    ipr_list = sorted(ipr_list)
    ipr_list = [ipr_list[i] for i in range(len(ipr_list)) if i
                             == 0 or ipr_list[i] != ipr_list[i-1]]
    return ipr_list
    
