#!/usr/bin/env zsh

error_out(){
  echo "Install gsed on mac, or edit the script and replace sed with sed ''"
  exit 1
}

if [[ "$(uname -s)" == "Darwin" ]]
then
  command -v gsed >/dev/null || error_out
  sed="gsed"
else
  sed="sed"
fi

tleap=path/to/tleap
tleap_input=scripts/tleap.in

obabel -ixyz unlabelled.xyz -omol2 > polymer.mol2
lammps_to_gromacs_gaff_modify_mol2.py -d equil.data -m polymer.mol2 -l labelled.xyz
$sed -i '2s/.*/pol/;s/UNL1/pol1/' polymer.mol2
$tleap -f $tleap_input
amber_to_gmx.py
