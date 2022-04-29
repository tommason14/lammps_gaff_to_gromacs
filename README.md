# lammps_gaff_to_gromacs

Takes the output of a LAMMPS polymer simulation with the GAFF forcefield and converts the datafile to a Gromacs topology.

Requirements:
- Openbabel
- Ambertools, for tleap
- Python3 (using the Ovito and ParmEd modules)
 
Firstly, store the python and shell scripts in a directory found in your $PATH variable. Also edit the path to the tleap and tleap_input variables inside `lammps_to_gromacs_gaff_create_top.sh`.

# First steps

These scripts expect a LAMMPS data file named `equil.data`, a labelled xyz file named `labelled.xyz`, and an unlabelled xyz file named `unlabelled.xyz`.

To get these, edit the data file as shown below:

Labelled data file:

```
Masses                 
                       
1      12.0100    # CA 
2       1.0080    # HA 
3       1.0080    # HC 
4       1.0080    # H1 
5      12.0100    # C3
6      12.0100    # C3
7      16.0000    # OH 
8      16.0000    # O  
9      32.0600    # S6 
10     12.0100    # C3 
                       
Pair Coeffs            
```

Unlabelled data file:

```
Masses                 
                       
1      12.0100    # C 
2       1.0080    # H 
3       1.0080    # H 
4       1.0080    # H 
5      12.0100    # C
6      12.0100    # C
7      16.0000    # O 
8      16.0000    # O  
9      32.0600    # S 
10     12.0100    # C 
                       
Pair Coeffs            
```

Then run `datafile_to_unwrapped_xyz.py equil.data unlabelled.xyz` and `datafile_to_unwrapped_xyz.py equil.data labelled.xyz`.

# Generating a GROMACS topology

Run `lammps_to_gromacs_gaff_create_top.sh`. This will produce a coordinate file named `polymer.gro` and a topology file named `polymer.top`.

# Optionally, add in salinated water

To add parameters for sodium, chloride and water simulated using the TIP4P model, run `lammps_to_gromacs_modify_top.sh`. These parameters are compatible with the itp files supplied in this repo.

If you wish to add other molecules, the itp information of the polymer needs to be extracted from the topology file generated.
To do this, run `top_to_itp.sh polymer.top polymer.itp` and then add other molecules to the topology file as desired.

# Possible issues

Sometimes Parmed fails to read atom names correctly when converting large systems, which can give errors when running `gmx grompp` and also when post-processing trajectories. To fix this, save a pdb before writing the prmtop file, and then assign atom names from the pdb with parmed. After this, atom names in the GRO file will be correct.

```
# tleap.in
source leaprc.gaff
mol = loadmol2 polymer.mol2
savepdb mol polymer.pdb
saveamberparm mol polymer.prmtop polymer.inpcrd
quit
```

```
# amber_to_gmx.py
import parmed as pmd
p = pmd.load_file('polymer.prmtop', xyz='polymer.pdb')

pdb = pmd.load_file('polymer.pdb')
for old, new in zip(p.atoms, pdb.atoms):
    old.name = new.name

p.save('conf.gro')
p.save('topol.top')
```
