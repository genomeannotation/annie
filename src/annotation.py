#!/usr/bin/env python
import sys

class Annotation:

    def __init__(self, feature_id='', key='', value=''):
        self.feature_id = feature_id
        self.key = key
        self.value = value

    def __eq__(self, other):
        if self.feature_id == other.feature_id and\
           self.key == other.key and\
           self.value == other.value:
            return True
        return False

    def __lt__(self, other):
        if self.feature_id < other.feature_id:
            return True
        return False

def write_annotations(annotations, file_out):
    # First, resolve duplicate gene names
    dups = {}
    for annotation in annotations:
        if annotation.key != "name":
            continue
        if annotation.value in dups:
            dups[annotation.value].append(annotation)
        else:
            dups[annotation.value] = [annotation]
    for dup in dups.values():
        if len(dup) > 1:
            for i, annotation in enumerate(dup):
                annotation.value += "_"+str(i)
    for annotation in annotations:
        file_out.write(annotation.feature_id+"\t"+annotation.key+"\t"+annotation.value+"\n")
