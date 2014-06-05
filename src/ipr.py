#!/usr/bin/env python
import sys
from src.annotation import Annotation

def read_ipr(io_buffer, whitelist=None):
    """Returns a list of lists, each containing mrna_id, "Dbxref" and annotation."""
    ipr_list = []
    for line in io_buffer:
        columns = line.split("\t")
        if len(columns)>3 and (columns[3].strip().lower() in whitelist):
            ipr_list.append(Annotation(columns[0].strip(), "Dbxref", columns[3].strip()+":"+columns[4].strip()))
            if len(columns)>13 and columns[13].find("GO:") != -1:
                ipr_list.append(Annotation(columns[0].strip(), "GO", columns[13].strip()))
            if len(columns)>11 and columns[11].find("IPR") != -1:
                ipr_list.append(Annotation(columns[0].strip(), "InterPro", columns[11].strip()))
    ipr_list = sorted(ipr_list)
    ipr_list = [ipr_list[i] for i in range(len(ipr_list)) if i== 0 or ipr_list[i] != ipr_list[i-1]]
    return ipr_list

