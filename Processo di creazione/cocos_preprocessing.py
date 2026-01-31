# Builds a COCOS input file from the prototypes of two concepts in input

import sys
import os


# returns a list containing the rigid properties read from the specified path
def getRigidProperties(path_file):
    prop_list = list()

    if os.path.exists(path_file):
        with open(path_file) as f:
            for p in f.readlines():
                prop_list.append(p.strip())

    return prop_list


# write the input file for COCOS
def write_cocos_file(head, head_value, modifier, modifier_value, folder):
    rigid = None
    if folder == 'typical':
        rigid = 'rigid'
    else:
        rigid = folder + "_rigid"

    with open(f'prototipi/{head}_{modifier}.txt', "w") as f:
        f.write(f'Title: {head}-{modifier}\n\n')
        f.write(f'Head Concept Name: {head}\n')
        f.write(f'Modifier Concept Name: {modifier}\n\n')

        # rigid properties
        for p in getRigidProperties(f'{rigid}/{head}'):
            f.write(f"head, {p}\n")
        f.write("\n")

        for p in getRigidProperties(f'{rigid}/{modifier}'):
            f.write(f"modifier, {p}\n")
        f.write("\n")

        # typical properties
        for p, v in modifier_value.items():
            f.write(f'T(modifier), {p}, {v}\n')
        f.write("\n")

        for p, v in head_value.items():
            f.write(f'T(head), {p}, {v}\n')
        f.write("\n")