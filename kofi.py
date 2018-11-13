#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, pathlib, argparse, re

# Vérifie l'argument 
parser=argparse.ArgumentParser()
parser.add_argument("vcf" ,help="Take vcf file as argument/ vcf file path needed if it's outside your working directory")
args=parser.parse_args()
#print(args.vcf,"\n")


# Récupère le chemin vérifie si le fichier est bien un fichier
from pathlib import Path
filename=Path(args.vcf)
# Vérifie que le fichier existe
if not filename.exists():
    print("Oops, file doesn't exist! \n")
    exit()
else:
	print(filename.name, "\n") #Debug à retirer 

if Path.is_file(filename):
	print(filename.name) # debug à retirer
else:
    print("Oops, this is not a file! \n")
    exit()


# Vérifie que c'est bien un vcf
if filename.suffix==".vcf":
	fd=filename.read_text()
	
else:
	print("Oops, ", filename.suffix, " extention is missing!")
	exit()
	
#print(fd)

#Vérification du format à l'intérieur du fichier    
#for line in fd :
#    line=line.strip("\n")
fileformat = re.findall("##fileformat=VCFv4",fd)
chrom = re.findall("#CHROM",fd)
                      
if fileformat :
    print (fileformat)
        
if chrom :
    print(chrom)
    #exit()
    if not chrom or not fileformat :
        print ("Oops, file format doesn't match with vcf type")
        exit()



	
	