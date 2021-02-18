#!/usr/bin/env python3
"""
1. Takes charges from a LAMMPS datafile and places them in the TRIPOS mol2 file
2. Adds correct atom types from a labelled xyz
3. Redefines the atom names as C1, C2, C3 etc...
"""
import argparse
import sys
import re
import os
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--datafile', help='LAMMPS datafile', required=True)
parser.add_argument('-m',
                    '--mol2',
                    help='MOL2 file to place charges into',
                    required=True)
parser.add_argument('-l',
                    '--labelled',
                    help='Labelled xyz file of the structure',
                    required=True)
args = parser.parse_args()

if args.datafile is None or args.mol2 is None:
    print('Error: must give both arguments')
    parser.print_help()
    sys.exit()


def get_charges_from_lmps(datafile):
    charges = []
    atoms = False
    with open(datafile) as d:
        for line in d:
            if 'Atoms' in line:
                atoms = True
                continue
            if re.search('^\s*[A-Z]', line):
                atoms = False
            if atoms:
                line = line.split()
                if len(line) > 1:
                    charges.append(float(line[3]))
    return charges


def add_charges_to_mol2(mol2, charges):
    found = False
    newfile = []
    with open(mol2) as m:
        for line in m:
            if '@<TRIPOS>ATOM' in line:
                found = True
                newfile.append(line)
                continue
            if '@<TRIPOS>BOND' in line:
                found = False
            if found:
                line = re.split(r'(\s+)', line)  # preserve whitespace
                line[-3] = str(charges.pop(0))
                line = ''.join(line)
            newfile.append(line)
    return newfile


def change_atom_names_in_mol2(mol2_list):
    """
    Take 
    C
    O
    C
    O
    and convert into
    C1
    O1
    O2
    O2
    etc...
    """
    orig_names = []
    found = False
    for line in mol2_list:
        if '@<TRIPOS>ATOM' in line:
            found = True
            continue
        if '@<TRIPOS>BOND' in line:
            break
        if found:
            line = line.split()
            orig_names.append(line[1])
    counts = Counter(orig_names)
    replacements = {}  # {'C': ['C1', 'C2', ...]}
    for letter, count in counts.items():
        replacements[letter] = [f'{letter}{i}' for i in range(1, count + 1)]

    newfile = []
    found = False
    for line in mol2_list:
        if '@<TRIPOS>ATOM' in line:
            found = True
            newfile.append(line)
            continue
        if '@<TRIPOS>BOND' in line:
            found = False
        if found:
            line = re.split(r'(\s+)', line)
            line[4] = f'{replacements[line[4]].pop(0):<12s}'
            line[5] = ''
            line = ''.join(line)
        newfile.append(line)
    return newfile


def add_correct_atom_types_into_mol2(mol2_list, labelled):
    """
    Takes the atom types from a labelled xyz, adds them into the 
    6th column of the mol2 file
    """
    types = []
    with open(labelled) as f:
        for line in f.readlines()[2:]:
            types.append(line.split()[0].lower())

    newfile = []
    found = False
    for line in mol2_list:
        if '@<TRIPOS>ATOM' in line:
            found = True
            newfile.append(line)
            continue
        if '@<TRIPOS>BOND' in line:
            found = False
        if found:
            line = re.split(r'(\s+)', line)
            line[12] = f'{types.pop(0):<8}'
            line[13] = ''
            line = ''.join(line)
        newfile.append(line)
    return newfile


def main():
    charges = get_charges_from_lmps(args.datafile)
    mol2 = add_charges_to_mol2(args.mol2, charges)
    mol2 = change_atom_names_in_mol2(mol2)
    mol2 = add_correct_atom_types_into_mol2(mol2, args.labelled)
    os.system(f'mv {args.mol2} {args.mol2}.bak')
    with open(args.mol2, 'w') as f:
        for line in mol2:
            f.write(line)


if __name__ == "__main__":
    main()
