%mem=1GB
%nprocshared=1
%chk=0_qm.chk
#p nosymm geom=nocrowd opt=(modredundant,maxcycle=100)  nosymm B3LYP/def2TZVP 

Title

 0,1
  C                                                -0.536850000000      0.104174000000      0.014636000000
  O                                                -1.636322000000     -0.676373000000     -0.068268000000
  C                                                 0.726013000000     -0.717700000000      0.105280000000
  H                                                 0.716994000000     -1.157121000000      1.114447000000
  H                                                 0.643380000000     -1.553795000000     -0.592281000000
  N                                                 1.889013000000      0.097733000000     -0.195097000000
  H                                                 1.748159000000      1.040807000000      0.145925000000
  H                                                 2.723536000000     -0.278432000000      0.231888000000
  O                                                -0.586810000000      1.305633000000      0.046275000000
  H                                                -2.405088000000     -0.088514000000     -0.077854000000

 1 2 1.000 3 1.000 9 2.000
 2 1 1.000 10 1.000
 3 1 1.000 4 1.000 5 1.000 6 1.000
 4 3 1.000
 5 3 1.000
 6 3 1.000 7 1.000 8 1.000
 7 6 1.000
 8 6 1.000
 9 1 2.000
 10 2 1.000
 