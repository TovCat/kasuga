"""
molecular.py is a unit of Kasuga computational package responsible for all operations with molecular geometries such as:
    1. Reading, writing and processing .cif files containing crystal packing data.
    2. Reading, writing and processing .xyz, .mol2 and .pdb files containing single molecule and molecular cluster data
    3. Reading and processing .out (Gaussian), .cube and .fchk files containing computational properties for single
        molecules and molecular clusters.
    4. Symmetry operations with single molecules and molecular clusters, molecular cluster generation.
    5. Modification of a molecular geometry: changing bond lengths, angles and dihedral angles, changing atomic and
        molecular properties.

As a rule of thumb, if you need to process and modify molecular geometries or read and store any property (such as
electron density) of a single molecule - it is most likely handled by molecular.py unit. Any other, more advanced
processing down the line (such as integration, IC and ISC calculations) is handled by other modules.

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣿⢿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⢿⣿⢿⡿⣿⡿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣯⣟⣯⣿⣿⣽⣾⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣡⢺⡆⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣷⣻⣯⣿⣷⣆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⢹⣿⣿⡿⢋⠞⠃⠀⣷⠀⠈⠻⣿⣿⣿⣿⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣡⣿⣿⡿⠧⠤⣾⡿⢋⠤⠊⠀⠀⠀⢸⡄⠀⠀⠈⠻⣿⣿⡦⠬⠽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⣸⣿⣯⣤⣤⣼⣏⡠⠎⠀⠀⠀⠀⠀⠈⢷⠀⠀⠀⠀⣈⣻⣷⣤⣤⣬⣻⣧⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⡿⠋⢀⣴⢾⢏⣿⣿⣿⣿⣿⣮⣅⠀⠀⠀⠀⠀⠀⠀⠘⠙⠀⠀⠀⣩⣵⣿⣿⣿⣷⣮⡙⢳⣦⠻⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡿⠃⢠⣿⠁⢠⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣷⠀⢻⣧⠈⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⡇⠀⢹⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⢸⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣷⠀⠀⠁⠀⠈⢷⣤⣼⣿⣿⣿⠿⠗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠧⢤⣾⣿⣿⣿⣿⠟⠀⠘⠉⠀⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⠆⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣄⣀⣀⠀⣁⢐⣀⣠⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠿⠟⠉⠋⠉⠋⠙⠛⢿⡇⠀⠀⠀⠀⠀⠀⠀⣀⢀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣤⣀⣀⠀⠀⠀⠀⠀⠙⣦⣀⡆⠈⡄⠀⣘⣠⡞⠁⠀⠀⢀⡀⣄⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣀⣰⣀⢈⠙⠛⠛⠛⠛⠋⠉⣀⣶⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢛⣧⠉⠉⠙⠒⠛⠛⠛⠚⠛⠉⠉⢰⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⡿⠟⠋⠁⠰⣯⠟⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠄⢺⣡⡆⠀⠈⠻⢿⡛⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠊⠉⠀⠀⠀⠀⠀⢹⡀⠀⠈⠑⠲⢤⣄⣂⣈⣐⣀⣀⣠⣟⣀⠤⠔⠒⠀⠀⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣯⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⡒⣒⠲⣒⢒⢲⣶⡒⠖⡲⢶⡞⠁⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⢠⣣⠔⡊⠖⢫⠘⡴⣱⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣨⣿⣇⢻⣿⣿⣿⣿⡢⣀⠀⠀⠀⠀⠀⣀⣀⣠⡀⠀⠈⣧⠳⡘⠴⡉⢆⠽⣿⠋⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⣼⣿⣿⣿⣿⢛⣿⠿⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢄⡾⣣⢁⡛⢣⢉⡻⡿⢿⣷⢦⣉⠓⢒⣊⣭⡭⢀⡏⠀⠀⠀⠈⢳⣱⡢⠑⡌⡿⠁⠀⠀⠀⠀⢀⡇⠨⣭⣖⠢⣼⣿⣿⠿⠋⣄⣾⠏⡒⣽⣦⠀⠀⠀⠀
⠀⠀⠀⠀⣠⡟⢚⢄⡒⢌⢂⠣⡑⠤⡃⢍⠣⡌⢍⣃⢲⣏⡀⠸⠤⣀⣀⠀⠀⠀⠹⣦⠣⣼⠃⠀⢀⣀⡤⠤⠚⢁⣀⣷⠄⢿⡟⢫⢁⠎⡱⢌⠡⢃⠜⣘⡹⣇⠀⠀⠀
⠀⠀⠀⣰⠏⣷⡃⢆⡘⠤⢃⣌⡇⠖⡩⢌⠢⣑⠊⡔⢢⢒⠩⣉⠓⡒⠦⠭⠭⢥⣒⣚⣻⣗⣈⠭⠥⢖⢒⡚⠩⡍⡒⢤⡉⠆⡍⢒⠌⡒⣡⢊⡴⢃⠜⣠⢑⡼⠀⠀⠀
⠀⠀⣰⢫⢰⣉⣿⡌⣴⣁⢣⣼⡏⡜⢰⣈⢱⢠⢩⣐⢡⢊⢱⢠⡍⣰⢉⡜⣤⢓⢸⣏⣀⣀⣿⡘⢢⢡⡒⣌⡑⣆⡑⢢⣌⢱⣈⣬⡘⣤⡁⣎⡟⡌⢢⢡⣾⢃⠀⠀⠀
⠀⢰⡟⡏⠷⡙⢎⣿⡶⡉⢇⣿⡷⢙⠳⡉⠇⡎⢳⠉⢇⢋⠞⢳⢁⠳⠞⡁⢇⠞⡸⢹⡟⣿⡏⢇⡎⠷⡙⢎⡹⢈⡹⢃⠞⡰⣉⠆⢳⠆⢳⡘⣿⡁⡏⣾⠇⢏⠀⠀⠀
⢀⡾⣥⢋⠴⡁⠆⣿⣷⣱⣿⣻⡇⢎⠰⡁⢎⠰⡁⢎⠢⢌⡘⠄⡎⠱⡨⢑⠌⡢⠅⣿⡇⣻⣏⠦⡘⠰⡉⠆⡔⢣⢐⡡⢊⠔⡰⢨⡁⢎⡡⢘⣿⣷⣼⡟⣌⠢⠀⠀⠀
⢸⢇⠹⢌⠢⢅⠓⢾⣟⡿⣷⣿⠇⡊⢔⠡⡊⢔⠡⡊⠔⢢⠘⡰⢈⡱⢐⡉⢆⠡⢍⣿⢦⢙⣿⢂⡍⠱⡘⠌⡔⢡⢂⠒⡡⢊⠔⡡⡘⢄⡒⡡⣿⣿⣿⠒⡄⢣⠀⠀⠀
⣿⢂⠣⢌⠣⡘⢌⠺⣿⣽⢻⣿⢀⠓⡌⢒⠡⢊⠒⡡⡉⢆⡑⢢⢁⠦⢡⠘⠤⣉⢺⣟⢸⡌⣿⡆⡌⢱⠈⡜⢠⠃⡌⢒⠡⢊⠔⡡⡘⢄⠆⡱⣿⢯⡽⢃⠜⡠⠀⠀⠀
⢠⡇⢎⢂⠧⢌⠱⡈⠜⣿⣞⣯⡗⢨⡘⠤⢃⠥⢃⡱⠤⡑⢢⠘⡄⡊⠔⡡⢊⠔⡤⢻⡏⡤⡇⢿⡧⡘⢄⠣⡘⢄⠣⡘⠤⡉⢆⠚⠤⡑⢊⡔⢡⣿⣻⡏⠴⡘⠰⠀⠀⠀
⣼⠓⡌⡒⢌⣂⠣⡉⢆⡹⢯⣷⡏⠔⡨⢒⡉⠆⠥⢂⡱⢈⠆⡱⠠⢅⠓⡄⢣⠘⠤⣿⡇⢇⡹⢸⣷⢁⠎⡰⢁⠎⡰⢁⡒⢡⠊⡜⢠⠃⡥⠘⠤⣿⣳⡟⠤⡑⢃⠀⠀⠀
"""

import os
import kasuga_io
import numpy as np

# Atomic weights for each respected atom
element_weight = {
    'H': 1.0075,
    'He': 4.002,
    'Li': 6.9675,
    'Be': 9.012,
    'B': 10.8135,
    'C': 12.0106,
    'N': 14.0065,
    'O': 15.999,
    'F': 18.998,
    'Ne': 20.1797,
    'Na': 22.989,
    'Mg': 24.3050,
    'Al': 26.981,
    'Si': 28.085,
    'P': 30.973,
    'S': 32.0675,
    'Cl': 35.4515,
    'Ar': 39.948,
    'K': 39.0983,
    'Ca': 40.078,
    'Sc': 44.955,
    'Ti': 47.867,
    'V': 50.9415,
    'Cr': 51.9961,
    'Mn': 54.938,
    'Fe': 55.845,
    'Co': 58.933,
    'Ni': 58.6934,
    'Cu': 63.546,
    'Zn': 65.38,
    'Ga': 69.723,
    'Ge': 72.63,
    'As': 74.921,
    'Se': 78.96,
    'Br': 79.904,
    'Kr': 83.798,
    'Rb': 85.4678,
    'Sr': 87.62,
    'Y': 88.905,
    'Zr': 91.224,
    'Nb': 92.906,
    'Mo': 95.96,
    'Tc': 98,
    'Ru': 101.07,
    'Rh': 102.905,
    'Pd': 106.42,
    'Ag': 107.8682,
    'Cd': 112.411,
    'In': 114.818,
    'Sn': 118.710,
    'Sb': 121.760,
    'Te': 127.60,
    'I': 126.904,
    'Xe': 131.293,
    'Cs': 132.905,
    'Ba': 137.327,
    'La': 138.905,
    'Ce': 140.116,
    'Pr': 140.907,
    'Nd': 144.242,
    'Pm': 145,
    'Sm': 150.36,
    'Eu': 151.964,
    'Gd': 157.25,
    'Tb': 158.925,
    'Dy': 162.500,
    'Ho': 164.930,
    'Er': 167.259,
    'Tm': 168.934,
    'Yb': 173.054,
    'Lu': 174.9668,
    'Hf': 178.49,
    'Ta': 180.947,
    'W': 183.84,
    'Re': 186.207,
    'Os': 190.23,
    'Ir': 192.217,
    'Pt': 195.084,
    'Au': 196.966,
    'Hg': 200.59,
    'Tl': 204.3835,
    'Pb': 207.2,
    'Bi': 208.980,
    'Po': 209,
    'At': 210,
    'Rn': 222,
    'Fr': 223,
    'Ra': 226,
    'Ac': 227,
    'Th': 232.038,
    'Pa': 231.035,
    'U': 238.028,
    'Np': 237,
    'Pu': 244,
    'Am': 243,
    'Cm': 247,
    'Bk': 247,
    'Cf': 251,
    'Es': 252,
    'Fm': 257,
    'Md': 258,
    'No': 259,
    'Lr': 262,
    'Rf': 267,
    'Db': 268,
    'Sg': 271,
    'Bh': 272,
    'Hs': 270,
    'Mt': 276,
    'Ds': 281,
    'Rg': 280,
    'Cn': 285
}

covalent_radius = {
    'H': 0.32,
    'Ne': 0.71,
    'F': 0.72,
    'O': 0.73,
    'N': 0.75,
    'C': 0.77,
    'B': 0.82,
    'Be': 0.90,
    'He': 0.93,
    'Ar': 0.98,
    'Cl': 0.99,
    'S': 1.02,
    'P': 1.06,
    'Si': 1.11,
    'Kr': 1.12,
    'Br': 1.14,
    'Ni': 1.15,
    'Se': 1.16,
    'Co': 1.16,
    'Cu': 1.17,
    'Fe': 1.17,
    'Mn': 1.17,
    'Al': 1.18,
    'Cr': 1.18,
    'As': 1.20,
    'Ge': 1.22,
    'V': 1.22,
    'Li': 1.23,
    'Rh': 1.25,
    'Ru': 1.25,
    'Zn': 1.25,
    'Ga': 1.26,
    'Os': 1.26,
    'Ir': 1.27,
    'Tc': 1.27,
    'Re': 1.28,
    'Pd': 1.28,
    'W': 1.30,
    'Pt': 1.30,
    'Mo': 1.30,
    'Xe': 1.31,
    'Ti': 1.32,
    'I': 1.33,
    'Ta': 1.34,
    'Nb': 1.34,
    'Ag': 1.34,
    'Au': 1.34,
    'Te': 1.36,
    'Mg': 1.36,
    'Sn': 1.41,
    'Sb': 1.41,
    'U': 1.42,
    'In': 1.44,
    'Sc': 1.44,
    'Hf': 1.44,
    'Zr': 1.45,
    'At': 1.45,
    'Bi': 1.46,
    'Po': 1.46,
    'Pb': 1.47,
    'Cd': 1.48,
    'Tl': 1.48,
    'Hg': 1.49,
    'Na': 1.54,
    'Tm': 1.56,
    'Lu': 1.56,
    'Er': 1.57,
    'Ho': 1.58,
    'Dy': 1.59,
    'Tb': 1.59,
    'Gd': 1.61,
    'Y': 1.62,
    'Sm': 1.62,
    'Pm': 1.63,
    'Nd': 1.64,
    'Th': 1.65,
    'Ce': 1.65,
    'Pr': 1.65,
    'La': 1.69,
    'Yb': 1.74,
    'Ca': 1.74,
    'Eu': 1.85,
    'Pu': 1.87,
    'Sr': 1.91,
    'Ba': 1.98,
    'K': 2.03,
    'Rb': 2.16,
    'Cs': 2.35
}


class Vector:
    """
    Vector is a base class containing coordinates represented as a np.array(3)
    """

    def __init__(self):
        self.coord = np.zeros(3)

    def transform(self, matrix: np.array):
        """
        General method for vector coordinate transformation using a transformation matrix.
        :param matrix: transformation 3x3 matrix (np.array)
        """
        self.coord = np.matmul(self.coord, matrix)

    def invert(self, inv_coord=np.zeros(3)):
        """
        Invert vector around arbitrary center.
        :param inv_coord: inversion center coordinates (np.array, [0,0,0] by default)
        """
        shift = inv_coord - self.coord
        self.coord += 2 * shift

    def mirror(self, normal=np.array([1, 0, 0]), point=np.zeros(3)):
        """
        Mirror vector in an arbitrary mirror plane
        :param normal: normal vector of a mirror plane (np.array, [1,0,0] by default)
        :param point: arbitrary point that belongs to a mirror plane (np.array, [0,0,0] by default)
        :return:
        """
        # normalize n just to be safe
        n = normal / np.linalg.norm(normal)
        # plane equation coefficients
        a = normal[0]
        b = normal[1]
        c = normal[2]
        d = -1 * (a * point[0] + b * point[1] + c * point[2])
        # distance between a point (our vector) and a mirror plane
        distance = abs(a * self.coord[0] + b * self.coord[1] + c * self.coord[3] + d) / np.sqrt(
            a ** 2 + b ** 2 + c ** 2)
        # provided normal vector can either face the same direction as mirrored point or the opposite
        test1 = self.coord + 2 * n * distance
        test2 = self.coord - 2 * n * distance
        distance_test1 = abs(a * test1[0] + b * test1[1] + c * test1[3] + d) / np.sqrt(a ** 2 + b ** 2 + c ** 2)
        distance_test2 = abs(a * test2[0] + b * test2[1] + c * test2[3] + d) / np.sqrt(a ** 2 + b ** 2 + c ** 2)
        if distance_test1 < distance_test2:
            # same direction
            self.coord = test1
        else:
            # opposite direction
            self.coord = test2

    def xyz_mirror(self, plane="xy", plane_point=np.zeros(3)):
        """
        Simplified mirror method to reflect vector in xy, xz and yz planes
        :param plane: string representing one of default planes: "xy", "xz", "yz" or "ab", "ac", "bc"
        :param plane_point: arbitrary point that belongs to a mirror plane (np.array, [0,0,0] by default)
        :return:
        """
        match plane:
            case "xy" | "ab":
                self.mirror(np.array([0, 0, 1]), plane_point)
            case "xz" | "ac":
                self.mirror(np.array([0, 1, 0]), plane_point)
            case "yz" | "bc":
                self.mirror(np.array([1, 0, 0]), plane_point)

    def rotate(self, angle: float, axis_vector: np.array, axis_point=np.zeros(3)):
        """
        Rotate Vector around arbitrary axis.
        :param angle: angle of rotation (in degrees)
        :param axis_point: point of origin for rotation axis (np.array) (np.array, [0,0,0] by default)
        :param axis_vector:
        """
        axis_diff = self.coord - axis_point
        axis_vector = axis_vector / np.linalg.norm(axis_vector)
        angle_rad = np.deg2rad(angle)
        matrix = np.zeros((3, 3))
        matrix[0, 0] = np.cos(angle_rad) + axis_vector[0] ** 2 * (1 - np.cos(angle_rad))
        matrix[0, 1] = axis_vector[0] * axis_vector[1] * (1 - np.cos(angle_rad)) - axis_vector[2] * np.sin(angle_rad)
        matrix[0, 2] = axis_vector[0] * axis_vector[0] * (1 - np.cos(angle_rad)) + axis_vector[1] * np.sin(angle_rad)
        matrix[1, 1] = np.cos(angle_rad) + axis_vector[1] ** 2 * (1 - np.cos(angle_rad))
        matrix[1, 2] = axis_vector[1] * axis_vector[2] * (1 - np.cos(angle_rad)) - axis_vector[0] * np.sin(angle_rad)
        matrix[2, 2] = np.cos(angle_rad) + axis_vector[2] ** 2 * (1 - np.cos(angle_rad))
        matrix[1, 0] = matrix[0, 1]
        matrix[2, 0] = matrix[0, 2]
        axis_diff_rotated = np.matmul(axis_diff, matrix)
        axis_translation = axis_diff - axis_diff_rotated
        self.coord += axis_translation

    def improper_rotate(self, angle: float, axis_vector=np.zeros(3), point=np.zeros(3)):
        self.rotate(angle, axis_vector, point)
        self.mirror(axis_vector, point)

    def screw_axis(self, angle: float, axis_vector=np.zeros(3), point=np.zeros(3), translation_vector=np.zeros(3)):
        self.rotate(angle, axis_vector, point)
        self.coord += translation_vector

    def glide_plane(self, normal=np.array([1, 0, 0]), point=np.zeros(3), translation_vector=np.zeros(3)):
        self.mirror(normal, point)
        self.coord += translation_vector

    def distance(self, v2):
        delta = self.coord - v2.coord
        return np.linalg.norm(delta)

    def distance_rough(self, v2):
        delta = self.coord - v2.coord
        return max(float(abs(delta[0])), float(abs(delta[1])), float(abs(delta[2])))


class ConnectivityGraph:

    def __init__(self, size):
        self.size = size
        self.nodes = np.zeros((size, size))

    def flood_fill_search(self, startpoint: int, excluded=()):
        inside = np.zeros(self.size)  # points that are connected to the starting one
        checked = np.zeros(self.size)  # points that we have already checked
        while True:
            for i in range(self.size):
                if self.nodes[startpoint, i] == 1 or self.nodes[i, startpoint] == 1:
                    if i not in excluded:
                        inside[i] = 1  # include all points that are connected to current start point
            checked[startpoint] = 1  # so, we've checked current start point
            count_inside = 0
            count_checked = 0
            for i in range(self.size):
                if checked[i] == 1:
                    count_checked += 1
                if inside[i] == 1:
                    count_inside += 1
                if checked[i] != 0 and inside[i] == 1:
                    startpoint = i
            if count_inside == count_checked:
                return inside

    def subsets_connected(self, subset_one=np.zeros((1)), subset_two=np.zeros((1))):
        for i1 in range(subset_one.size):
            for i2 in range(subset_two.size):
                if self.nodes[i1, i2] == 1 or self.nodes[i2, i1] == 1:
                    return True
        return False


class Atom(Vector):

    def assign_weight(self):
        if self.symbol in element_weight:
            self.weight = element_weight[self.symbol]
        else:
            kasuga_io.quit_with_error(f'Unrecognized {self.symbol} atom encountered!')

    def __init__(self, symbol=""):
        self.weight = 0.0  # Atomic weight
        self.symbol = ""  # Chemical symbol of an atom
        super().__init__()
        if symbol != "":
            self.assign_weight()

    def __eq__(self, other):
        distance = np.linalg.norm(self.coord - other.coord)
        if distance < 0.001 and self.symbol == other.symbol:
            return True
        else:
            return False

    def __ne__(self, other):
        distance = np.linalg.norm(self.coord - other.coord)
        if distance < 0.001 and self.symbol == other.symbol:
            return False
        else:
            return True

    def connected(self, b, simplified=False, cutoff=0.025):
        if simplified:
            d = Vector.distance_rough(self, b)
        else:
            d = Vector.distance(self, b)
        if d <= cutoff:
            return True
        else:
            return False


class Molecule:

    def __init__(self):
        self.atoms = []
        self.mass_center = None
        self.molecular_formula = None
        self.connectivity_graph = None
        self.inertia_eigenvectors = None
        self.inertia_eigenvalues = None
        self.inertia_vector_x, self.inertia_vector_y, self.inertia_vector_z = None, None, None
        self.symmetrized = False
        self.point_group = ""

    def __add__(self, other):
        for i in other.atoms:
            self.atoms.append(i)

    def __sub__(self, other):
        for_deletion = []
        for i1 in other.atoms:
            for num, i2 in enumerate(self.atoms):
                if i1 == i2:
                    for_deletion.append(self.atoms[num])
        for i1 in for_deletion:
            if i1 in self.atoms:
                self.atoms.remove(i1)

    def __eq__(self, other):
        diff = 0.0
        # Simple tests first to potentially save the hassle
        if self.get_molecular_formula() != self.get_molecular_formula():
            return False
        # For symmetry cloned molecules it's safe to assume that the order of atoms is still the same
        # But generally it's not always the case, especially if molecules originate from different sources
        for i1 in range(len(self.atoms)):
            current_min = 1000
            for i2 in range(len(other.atoms)):
                # We look for the closest atom with the same symbol
                if self.atoms[i1].symbol == other.atoms[i2].symbol:
                    current_diff = self.atoms[i1].distance(other.atoms[i2])
                    if current_diff < current_min:
                        current_min = current_diff
            diff += current_min
        if diff < 0.05:
            return True
        else:
            return False

    def __ne__(self, other):
        diff = 0.0
        if self.get_molecular_formula() != self.get_molecular_formula():
            return False
        for i1 in range(len(self.atoms)):
            current_min = 1000
            for i2 in range(len(other.atoms)):
                if self.atoms[i1].symbol == other.atoms[i2].symbol:
                    current_diff = self.atoms[i1].distance(other.atoms[i2])
                    if current_diff < current_min:
                        current_min = current_diff
            diff += current_min
        if diff < 0.05:
            if diff < 0.05:
                return False
            else:
                return True

    def is_connected(self, other):
        for i1 in self.atoms:
            for i2 in other.atoms:
                if i1.connected(i2):
                    return True
        return False

    def get_mass_center(self):
        if self.mass_center is None:
            self.mass_center = Vector()
        mass = 0.0
        mass_vector = np.zeros((3, 1))
        for atom in self.atoms:
            mass += element_weight[atom.symbol]
            mass_vector += atom.coord * element_weight[atom.symbol]
        self.mass_center = mass_vector / mass
        return self.mass_center

    def get_molecular_formula(self):
        if self.molecular_formula is None:
            self.molecular_formula = ""
        atom_list = []
        count_list = []
        for i, atom in enumerate(self.atoms):
            if atom.symbol not in atom_list:
                atom_list.append(atom.symbol)
        atom_list.sort()
        for i1, atom_in_formula in enumerate(atom_list):
            count_list.append(0)
            for i2, atom_in_list in enumerate(self.atoms):
                if atom_in_formula == atom_in_list:
                    count_list[i1] += 1
        result = ""
        for i, atom in enumerate(atom_list):
            result += (atom + str(count_list[i]))
        self.molecular_formula = result
        return self.molecular_formula

    def get_connectivity_matrix(self):
        if self.connectivity_graph is None:
            self.connectivity_graph = ConnectivityGraph(len(self.atoms))
        for i1 in range(len(self.atoms)):
            for i2 in range(i1, len(self.atoms)):
                if self.atoms[i1].connected(self.atoms[i2]):
                    self.connectivity_graph.nodes[i1, i2] = 1
                    self.connectivity_graph.nodes[i2, i1] = 1
        return self.connectivity_graph.nodes

    def get_inertia_vectors(self):
        if self.inertia_eigenvalues is None or self.inertia_eigenvectors is None:
            self.inertia_eigenvectors = np.zeros((3, 3))
            self.inertia_eigenvalues = np.zeros(3)
        # First, we translate origin to mass center
        if self.mass_center is None:
            mass_center = self.get_mass_center()
        else:
            mass_center = self.mass_center
        atoms_mc_system = []
        for a in self.atoms:
            new_a = Atom()
            new_a.coord = a.coord - mass_center
            new_a.symbol = a.symbol
            atoms_mc_system.append(new_a)
        # Calculate inertia tensor
        for a in atoms_mc_system:
            # xx
            self.inertia_eigenvectors[0, 0] += element_weight[a.symbol] * (a.coord[1, 0] ** 2 + a.coord[2, 0] ** 2)
            # xy
            self.inertia_eigenvectors[0, 1] += -1 * element_weight[a.symbol] * a.coord[0, 0] * a.coord[1, 0]
            # xz
            self.inertia_eigenvectors[0, 2] += -1 * element_weight[a.symbol] * a.coord[0, 0] * a.coord[2, 0]
            # yy
            self.inertia_eigenvectors[1, 1] += element_weight[a.symbol] * (a.coord[0, 0] ** 2 + a.coord[2, 0] ** 2)
            # yz
            self.inertia_eigenvectors[1, 2] += -1 * element_weight[a.symbol] * a.coord[1, 0] * a.coord[2, 0]
            # zz
            self.inertia_eigenvectors[2, 2] += element_weight[a.symbol] * (a.coord[0, 0] ** 2 + a.coord[1, 0] ** 2)
        self.inertia_eigenvectors[1, 0] = self.inertia_eigenvectors[0, 1]
        self.inertia_eigenvectors[2, 0] = self.inertia_eigenvectors[0, 2]
        self.inertia_eigenvectors[2, 1] = self.inertia_eigenvectors[1, 2]
        # Calculate eigenvalues and eigenvectors of the inertia tensor
        self.inertia_eigenvalues, self.inertia_eigenvectors = np.linalg.eig(self.inertia_eigenvectors)
        # Assign eigenvectors to Cartesian axis: highest for Z, lowest for X
        internal_e = self.inertia_eigenvalues
        if self.inertia_vector_x is None or self.inertia_vector_y is None or self.inertia_vector_z is None:
            self.inertia_vector_x = Vector()
            self.inertia_vector_y = Vector()
            self.inertia_vector_z = Vector()
        for i in range(3):
            index = np.where(internal_e == internal_e.max())
            if self.inertia_vector_z.coord != np.zeros(3):
                self.inertia_vector_z = (self.inertia_eigenvalues[index[0] - 1:index[0], :] /
                                         np.linalg.norm(self.inertia_eigenvalues[index[0] - 1:index[0], :]))
            elif self.inertia_vector_y.coord != np.zeros(3):
                self.inertia_vector_y.coord = (self.inertia_eigenvalues[index[0] - 1:index[0], :] /
                                               np.linalg.norm(self.inertia_eigenvalues[index[0] - 1:index[0], :]))
            elif self.inertia_vector_x.coord != np.zeros(3):
                self.inertia_vector_x.coord = (self.inertia_eigenvalues[index[0] - 1:index[0], :] /
                                               np.linalg.norm(self.inertia_eigenvalues[index[0] - 1:index[0], :]))
            internal_e[index[0], 0] = -1.0
        return self.inertia_vector_x, self.inertia_vector_y, self.inertia_vector_z

    def match_rotation_to(self, other):
        # Extract principal axes for each molecule
        # Static stays in place, rotated is transformed
        rotated_x, rotated_y, rotated_z = self.get_inertia_tensor()
        static_x, static_y, static_z = other.get_inertia_tensor()
        # Since the vectors are stored in ((3,1)) shape we need transpose them first
        rotated_x = np.transpose(rotated_x)
        rotated_y = np.transpose(rotated_y)
        rotated_z = np.transpose(rotated_z)
        static_x = np.transpose(static_x)
        static_y = np.transpose(static_y)
        static_z = np.transpose(static_z)
        # Create matrices that rotate standard coordinate system 0 to molecule's principal axes
        rot_mat_rotated = np.array([[rotated_x], [rotated_y], [rotated_z]])
        rot_mat_static = np.array([[static_x], [static_y], [static_z]])
        # Combine two rotations: Rotated -> 0  (inverted 0 -> Rotated) and 0 -> Static
        final_rotation = np.matmul(np.linalg.inv(rot_mat_rotated), rot_mat_static)
        # We translate Rotated to 0 system, perform rotation, and translate it back
        mass_center = self.get_mass_center()
        for i in range(len(self.atoms)):
            self.atoms[i].coord -= mass_center
            self.atoms[i].coord = np.transpose(np.matmul(np.transpose(self.atoms[i].coord), final_rotation))
            self.atoms[i].coord += mass_center

    def change_bond(self, bond: tuple, delta: float):
        first_fragment = self.connectivity_graph.flood_fill_search(bond[0], (bond[1]))
        second_fragment = self.connectivity_graph.flood_fill_search(bond[1], (bond[0]))
        translation_vector = self.atoms[bond[0]].coord - self.atoms[bond[1]].coord
        translation_vector = np.linalg.norm(translation_vector)
        if self.connectivity_graph.subsets_connected(first_fragment, second_fragment):
            self.atoms[bond[0]].coord += delta * translation_vector / 2
            self.atoms[bond[1]].coord -= delta * translation_vector / 2
        else:
            for i in first_fragment:
                self.atoms[i].coord += delta * translation_vector / 2
            for i in second_fragment:
                self.atoms[i].coord -= delta * translation_vector / 2

    def change_angle(self, angle: tuple, delta: float):
        first_fragment = self.connectivity_graph.flood_fill_search(angle[0], (angle[1]))
        second_fragment = self.connectivity_graph.flood_fill_search(angle[2], (angle[1]))
        v1 = self.atoms[angle[0]].coord - self.atoms[angle[1]].coord
        v2 = self.atoms[angle[2]].coord - self.atoms[angle[1]].coord
        rotation_vector = np.cross(v1, v2)
        if self.connectivity_graph.subsets_connected(first_fragment, second_fragment):
            self.atoms[angle[0]].rotate(delta / 2, rotation_vector, self.atoms[angle[1]])
            self.atoms[angle[0]].rotate(-1 * delta / 2, rotation_vector, self.atoms[angle[1]])
        else:
            for i in first_fragment:
                self.atoms[i].rotate(delta / 2, rotation_vector, self.atoms[angle[1]])
            for i in second_fragment:
                self.atoms[i].rotate(-1 * delta / 2, rotation_vector, self.atoms[angle[1]])

    def change_dihedral(self, dihedral: tuple, delta: float):
        first_fragment = self.connectivity_graph.flood_fill_search(dihedral[0], (dihedral[1], dihedral[2], dihedral[3]))
        second_fragment = self.connectivity_graph.flood_fill_search(dihedral[3], (dihedral[0], dihedral[1], dihedral[2]))
        rotation_vector = self.atoms[dihedral[1]].coord - self.atoms[dihedral[2]].coord
        if self.connectivity_graph.subsets_connected(first_fragment, second_fragment):
            self.atoms[dihedral[0]].rotate(delta / 2, rotation_vector, self.atoms[dihedral[1]])
            self.atoms[dihedral[3]].rotate(-1 * delta / 2, rotation_vector, self.atoms[dihedral[1]])
        else:
            for i in first_fragment:
                self.atoms[i].rotate(delta / 2, rotation_vector, self.atoms[dihedral[1]])
            for i in second_fragment:
                self.atoms[i].rotate(-1 * delta / 2, rotation_vector, self.atoms[dihedral[1]])


class GaussianFile:

    def __init__(self):
        self.path = ""
        self.file_raw_contents = []
        self.__start_end = None
        self.version = ""
        self.revision_date = ""
        self.execution_date = ""
        self.link0_instructions = {}
        self.calculation_instructions = []
        self.iops_instructions = []
        self.calculation_title = ""
        self.geometries = []

    def link1(self):

        def get_title(lines):
            for n, line in enumerate(lines):
                if line[1:4] == "***":
                    first = lines[n + 1].strip().split()
                    second = lines[n + 1].strip().split()
                    self.version = f'{first[0]} {first[1]}'
                    self.revision_date = first[2]
                    self.execution_date = second[0]
                    return n + 2

        def get_link0(start_pos: int, lines):
            for i in range(start_pos, len(lines)):
                a = lines[i].strip()
                if a[0] == "-":
                    return i + 1
                else:
                    splitted = a.split("=")
                    self.link0_instructions[splitted[0].strip()[1:]] = splitted[1].strip()

        def get_calculation_instructions(start_pos: int, lines):
            for i in range(start_pos, len(lines)):
                a = lines[i].strip()
                if a[0] == "-":
                    return i + 1
                else:
                    self.calculation_instructions.append(a)

        extracted_lines = self.file_raw_contents[self.__start_end[0]: self.__start_end[1]]
        last_line = get_title(extracted_lines)
        last_line = get_link0(last_line, extracted_lines)
        last_line = get_calculation_instructions(last_line, extracted_lines)
        for i in range(last_line, len(extracted_lines)):
            self.iops_instructions.append(extracted_lines[i].strip())

    def link101(self):
        extracted_lines = self.file_raw_contents[self.__start_end[0]: self.__start_end[1]]
        self.calculation_title = extracted_lines[1].strip()
        for num, s in enumerate(extracted_lines):
            if s[0] == " ":
                return None
            new_atom = Atom()
            line = s.split()
            new_atom.symbol = line[0]
            new_atom.coord[0] = float(line[1])
            new_atom.coord[1] = float(line[2])
            new_atom.coord[2] = float(line[3])
            self.initial_geometry.atoms.append(new_atom)

    def link103(self):
        extracted_lines = self.file_raw_contents[self.__start_end[0]: self.__start_end[1]]
        if extracted_lines[3].strip() == "Initialization pass.":
            return None

    def link202(self):
        extracted_lines = self.file_raw_contents[self.__start_end[0]: self.__start_end[1]]
        new_molecule = Molecule()
        if extracted_lines[0].strip() == "Symmetry turned off by external request.":
            new_molecule.symmetrized = False
        else:
            new_molecule = True
        a = extracted_lines[4].split()
        new_molecule.point_group = a[1]
        i = 0
        check_line = extracted_lines[i + 10]
        while check_line.strip()[0] != "-":
            a = check_line.split()
            atom_index = int(a[1])
            new_atom = Atom()
            new_atom.symbol = list(element_weight)[atom_index]
            new_atom.assign_weight()
            new_atom.coord[0] = float(a[3])
            new_atom.coord[1] = float(a[4])
            new_atom.coord[2] = float(a[5])
            new_molecule.atoms.append(new_atom)
            i += 1
            check_line = extracted_lines[i + 10]
        self.geometries.append(new_molecule)

    links_dict = {
        "L1": link1(),
        "L101": link101(),
        "L103": link103(),
        "L202": link202(),
        "L301": None,
        "L302": None,
        "L303": None,
        "L308": None,
        "L310": None,
        "L311": None,
        "L314": None,
        "L316": None,
        "L319": None,
        "L401": None,
        "L402": None,
        "L405": None,
        "L502": None,
        "L503": None,
        "L506": None,
        "L508": None,
        "L510": None,
        "L601": None,
        "L602": None,
        "L604": None,
        "L607": None,
        "L608": None,
        "L609": None,
        "L610": None,
        "L701": None,
        "L702": None,
        "L703": None,
        "L716": None,
        "L801": None,
        "L802": None,
        "L804": None,
        "L811": None,
        "L901": None,
        "L902": None,
        "L903": None,
        "L904": None,
        "L905": None,
        "L906": None,
        "L908": None,
        "L913": None,
        "L914": None,
        "L915": None,
        "L916": None,
        "L918": None,
        "L923": None,
        "L1002": None,
        "L1003": None,
        "L1014": None,
        "L1101": None,
        "L1102": None,
        "L1110": None,
        "L1111": None,
        "L1112": None,
        "L9999": None
    }

    def read(self, file_path=""):
        self.path = file_path

        try:
            if "\\" not in file_path:  # Try to open file in the same directory
                file = open(os.path.join(os.getcwd(), file_path), "r")
            else:
                file = open(file_path, "r")
            self.file_raw_contents = file.readlines()
            file.close()
        except OSError:
            kasuga_io.quit_with_error(f'Can`t open: {file_path}')




class CifFile:
    # Parser and processor for .cif files according to CIF v1.1 standard

    def __init__(self):
        tags = {}  # Single fields from CIF
        loops = []  # Looped fields from CIF
        # Cell parameters
        cell_length_a = float
        cell_length_b = float
        cell_length_c = float
        cell_angle_alpha = float
        cell_angle_beta = float
        cell_angle_gamma = float
        # Cartesian translation vectors
        translation_a = np.zeros((3, 1))
        translation_b = np.zeros((3, 1))
        translation_c = np.zeros((3, 1))
        # Transformation matrix from abc-system to Cartesian
        transform_matrix = np.zeros((3, 3))
        # Asymmetric unit of a primitive cell
        as_unit = Molecule

    @staticmethod
    def parse_line(line):
        line = line.strip()
        if line == "?" or line == ".":
            return ""
        if line[0] == "'" and line[len(line) - 1] == "'":
            return line[1:len(line) - 1]
        split = line.split()
        out = []
        for s in split:
            if s[0] == "'" and s[len(s) - 1] == "'":
                out.append(s[1:len(s) - 1])
                continue
            else:
                try:
                    pre = int(s)
                    out.append(pre)
                except ValueError:
                    try:
                        pre = float(s)
                        out.append(pre)
                    except ValueError:
                        if isinstance(s, str):
                            out.append(s)
                        elif "(" in s and ")" in s:
                            temp = float(s[0:s.find("(")])
                            for i in range(3):
                                l1 = len(s[s.find(".") + 1: s.find("(")])
                                l2 = len(s[s.find("(") + 1: s.find(")")])
                                temp += float(s[s.find("(") + 1:s.find(")")]) * 10 ** (-1 * (l1 + (i + 1) * l2))
                            out.append(temp)
                        else:
                            kasuga_io.quit_with_error(f'Unrecognized variable in "{line}"!')
        if len(out) == 1:
            return out[0]
        else:
            return out

    @staticmethod
    def transform_abc_to_cartesian(vector: np.array, transform: np.array):
        if transform.shape != (3, 3):
            kasuga_io.quit_with_error(f'Wrong dimensions of a transformation matrix!')
        if vector.shape == (3, 1):
            return np.matmul(transform, vector)
        elif vector.shape == (1, 3):
            return np.transpose(transform, np.transpose(vector))
        else:
            kasuga_io.quit_with_error(f'Wrong dimensions of a transformed vector!')

    @staticmethod
    def transform_cartesian_to_abc(vector: np.array, transform: np.array):
        if transform.shape != (3, 3):
            kasuga_io.quit_with_error(f'Wrong dimensions of a transformation matrix!')
        transform_revert = np.linalg.inv(transform)
        if vector.shape == (3, 1):
            return np.matmul(transform_revert, vector)
        elif vector.shape == (1, 3):
            return np.transpose(transform_revert, np.transpose(vector))
        else:
            kasuga_io.quit_with_error(f'Wrong dimensions of a transformed vector!')

    @classmethod
    def read_raw(cls, file_path):
        file_contents = []
        parsed_loop = []
        loop_tags = []
        loop_contents = []
        try:
            if "\\" not in file_path:  # Try to open file in the same directory
                file = open(os.path.join(os.getcwd(), file_path), "r")
            else:
                file = open(file_path, "r")
            file_contents = file.readlines()
            file.close()
        except OSError:
            kasuga_io.quit_with_error(f'Can`t open: {file_path}')

        for i in range(len(file_contents)):  # Initial survey for any Shelxl data to be expunged
            if "_shelx_res_file" in file_contents[i]:
                file_contents = file_contents[:i]  # Slice away everything below first Shelxl tag
                break

        in_loop = False
        loop_parsed = False

        for index in range(len(file_contents)):
            if "loop_" in file_contents[index]:
                in_loop = True
                parsed_loop = []
                loop_tags = []
                loop_contents = []
                continue

            if in_loop and loop_parsed:
                if file_contents[index].strip() == "":
                    in_loop = False
                    loop_parsed = False
                    continue
                else:
                    continue

            if in_loop:
                start_index = index
                reading_tags = True

                for i in range(start_index, len(file_contents)):
                    if file_contents[i].strip()[0] == "_":
                        split = file_contents[i].split()
                        loop_tags.append(split[0][1:])
                    else:
                        reading_tags = False
                        start_index = i
                        break

                if not reading_tags:
                    for i in range(start_index, len(file_contents)):
                        if file_contents[i].strip() == "":
                            if len(loop_contents) % len(loop_tags) != 0:
                                kasuga_io.quit_with_error(f'Faulty loop block around "{file_contents[index]}" '
                                                          f'and "{file_contents[i]}"! '
                                                          f'Please verify "{file_path}" integrity.')
                            else:
                                for i1 in range(len(loop_contents) // len(loop_tags)):
                                    d = {}
                                    for i2 in range(len(loop_tags)):
                                        d[loop_tags[i2]] = loop_contents[i1 + i2]
                                    parsed_loop.append(d)
                                cls.loops.append(parsed_loop)
                                loop_parsed = True
                                break
                        else:
                            loop_pre_contents = cls.parse_line(file_contents[i])
                            if isinstance(loop_pre_contents, list):
                                for i2 in loop_pre_contents:
                                    loop_contents.append(i2)
                            else:
                                loop_contents.append(loop_pre_contents)

            if file_contents[index][0] == "_" and not in_loop:
                split = file_contents[index].split()
                tag_content = ""

                cd_block_encountered = False
                if len(split) > 1:
                    for i in range(1, len(split)):
                        tag_content += split[i]
                elif ";" in file_contents[index + 1]:
                    cd_block_encountered = True
                    ind = index + 2
                    if file_contents[ind] == ";":
                        kasuga_io.quit_with_error(f'Faulty tag ;-; block encountered around "{file_contents[index]}"! '
                                                  f'Please verify "{file_path}" integrity.')
                    else:
                        for i in range(ind, len(file_contents)):
                            if ";" in file_contents[i]:
                                break
                            else:
                                tag_content += file_contents[i]
                else:
                    tag_content = file_contents[index + 1]

                if tag_content == "" or split[0] == "_":
                    kasuga_io.quit_with_error(f'Faulty CIF tag encountered around "{file_contents[index]}"!'
                                              f' Please verify "{file_path}" integrity.')
                else:
                    if cd_block_encountered:
                        cls.tags[split[0][1:]] = tag_content
                    else:
                        cls.tags[split[0][1:]] = cls.parse_line(tag_content)

    @classmethod
    def parse_raw(cls):
        # Primitive cell dimensions
        cls.cell_length_a = cls.tags['cell_length_a']
        cls.cell_length_b = cls.tags['cell_length_b']
        cls.cell_length_c = cls.tags['cell_length_c']

        # Primitive cell angles
        cls.cell_angle_alpha = cls.tags['cell_angle_alpha']  # Between c and b
        cls.cell_angle_beta = cls.tags['cell_angle_beta']  # Between c and a
        cls.cell_angle_gamma = cls.tags['cell_angle_gamma']  # Between a and b

        # Generate transformation matrix from abc to Cartesian
        cosa = np.cos(np.deg2rad(cls.cell_angle_alpha))
        cosb = np.cos(np.deg2rad(cls.cell_angle_beta))
        cosg = np.cos(np.deg2rad(cls.cell_angle_gamma))
        sing = np.sin(np.deg2rad(cls.cell_angle_gamma))
        volume = np.sqrt(1.0 - cosa ** 2.0 - cosb ** 2.0 - cosg ** 2.0 + 2.0 * cosa * cosb * cosg)
        cls.transform_matrix = np.array([[cls.cell_length_a, cls.cell_length_b * cosg, cls.cell_length_c * cosb],
                                         [0, cls.cell_length_b * sing, cls.cell_length_c * (cosa - cosb * cosg) / sing],
                                         [0, 0, cls.cell_length_c * volume / sing]])

        # Translation vectors in cartesian coordinates
        # Most of the symmetry operations are performed in the abc-system for the sake of simplicity
        # Yet, for some processing down the line we might need cartesian vectors as well
        cls.translation_a[0, 0] = cls.cell_length_a  # We assume that X-axis is aligned with a-axis
        cls.translation_b = CifFile.transform_abc_to_cartesian(np.array([0, 1, 0]), cls.transform_matrix)
        cls.translation_c = CifFile.transform_abc_to_cartesian(np.array([0, 0, 1]), cls.transform_matrix)

        # Extract fractional coordinates from CIF loops
        found_as = False
        for i1 in range(len(cls.loops)):
            if "atom_site_label" in cls.loops[i1][0]:
                if found_as:
                    kasuga_io.quit_with_error(f'Duplicated asymmetric units in CIF file!')
                else:
                    found_as = True
                for i2 in range(len(cls.loops[i1])):
                    a = Atom
                    a.symbol = cls.loops[i1][i2]['atom_site_type_symbol']
                    a.assign_weight()
                    a.coord_abc[0, 1] = cls.loops[i1][i2]['atom_site_fract_x']
                    a.coord_abc[1, 1] = cls.loops[i1][i2]['atom_site_fract_y']
                    a.coord_abc[2, 1] = cls.loops[i1][i2]['atom_site_fract_z']
                    cls.as_unit.atoms.append(a)


# Cluster is an array of molecules either natively generated from an associated CifFile or appended through other means
class Cluster:
    molecules = [Molecule]
    cif = CifFile
