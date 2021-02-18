#!/usr/bin/env bash

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

cp polymer.top polymer.top.bak
$sed -n '/moleculetype/,/system/p' polymer.top | sed '$d' > polymer.itp

# remove itp info from topology file

$sed '/moleculetype/Q' polymer.top > header
$sed -n '/\[ system \]/, $p' polymer.top > footer

# add additional info to topology file

cat << EOF > addn
; taken from amber03.ff/ffnonbonded.itp for tip4p                
Cl          17      35.45    0.0000  A   4.40104e-01  4.18400e-01
Na          11      22.99    0.0000  A   3.32840e-01  1.15897e-02
; tip4p                                                          
HW_tip4p     1       1.008   0.0000  A   0.00000e+00  0.00000e+00
OW_tip4p     8      16.00    0.0000  A   3.15365e-01  6.48520e-01
; MW=Dummy mass for tip4p/EW/5p water extra point charge         
MW           0       0.0000  0.0000  D   0.00000e+00  0.00000e+00

#include "tip4p.itp"
#include "polymer.itp"
#include "ions.itp"
EOF

cat header addn <(echo) footer > polymer.top
rm header addn footer

$sed -i 's/Generic title/Polymer in salinated water/' polymer.top
echo "Add the required number of each residue at the bottom of polymer.top after packing,"
echo "then run the job."
