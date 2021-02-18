#!/usr/bin/env python3

import sys
if not 2 <= len(sys.argv) <= 3:
    sys.exit("Uses Ovito to unwrap a datafile and write an xyz.\n"
             "Atom type labels must be present in the Masses section\n"
             "i.e. 7 12.011 # C3\n"
             "Syntax: datafile_to_unwrapped_xyz.py input [output (optional)]")
from ovito.io import import_file, export_file
from ovito.modifiers import UnwrapTrajectoriesModifier

traj = sys.argv[1]
if len(sys.argv) == 2:
    output = traj.rsplit('.')[0] + '.unwrapped.xyz'
else:
    output = sys.argv[2]

pipeline = import_file(traj)
pipeline.modifiers.append(UnwrapTrajectoriesModifier())
export_file(
    pipeline,
    output,
    'xyz',
    columns=["Particle Type", "Position.X", "Position.Y", "Position.Z"])
