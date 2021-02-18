#!/usr/bin/env python3
import parmed as pmd

amber = pmd.load_file('polymer.prmtop','polymer.inpcrd')

amber.save('polymer.top')
amber.save('polymer.gro')
