#!/usr/bin/env bash

box=12
gmx_mpi insert-molecules -ci polymer.gro -nmol 20 -box $box $box $box -try 200 -o pack.gro
gmx_mpi insert-molecules -f pack.gro -ci tip4p.gro -nmol 4800 -box $box $box $box -try 200 -o pack.gro
gmx_mpi insert-molecules -f pack.gro -ci cl.gro -nmol 96 -box $box $box $box -try 200 -o pack.gro
gmx_mpi insert-molecules -f pack.gro -ci sodium.gro -nmol 576 -box $box $box $box -try 200 -o pack.gro
