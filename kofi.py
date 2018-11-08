#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, pathlib, argparse, re

# V�rifie l'argument 
parser=argparse.ArgumentParser()
parser.add_argument("vcf" ,help="Take vcf file as argument/ vcf file path needed if it's outside your working directory")
args=parser.parse_args()
# print(args.vcf)

# R�cup�re le chemin v�rifie si le fichier est bien un fichier
from pathlib import Path
filename=Path(args.vcf)
if Path.is_file(filename):
	print(filename.name) # debug � retirer
else:
	print("Oops, this is not a file!")

# V�rifie que le fichier existe
if not filename.exists():
    print("Oops, file doesn't exist!")
else:
	print(filename.name) #Debug � retirer 

# V�rifie que c'est bien un vcf
if filename.suffix==".vcf":
	fd=filename.read_text()
	
else:
	print("Oops, ", filename.suffix, " extention is missing!")
	exit()
	
#print(fd)




	
	