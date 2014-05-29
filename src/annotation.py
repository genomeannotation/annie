#!/usr/bin/env python
import sys
from collections import namedtuple

Annotation = namedtuple('Annotation', 'feature_id key value')

def write_annotations(annotations, file_out):
    for annotation in annotations:
        file_out.write("\t".join(annotation)+"\n")
