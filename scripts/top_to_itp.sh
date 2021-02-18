#!/usr/bin/env bash

[[ $# -ne 2 || $1 == "-h" || $2 == "-h" ]] && 
  echo "Syntax: $(basename $0) topology_file itp_file" &&
  exit 1

top=$1
itp=$2

$sed -n '/moleculetype/,/system/p' $top | sed '$d' > $itp

$sed '/moleculetype/Q' $top | sed '$d' > header
$sed -n '/\[ system \]/, $p' $top > footer

cat << EOF > addn
#include "$itp"

EOF

cat header addn footer > $top
rm header addn footer
