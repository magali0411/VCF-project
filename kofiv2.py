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

if not Path.is_file(filename):
	print(filename.name) # debug à retirer
	print("Oops, this is not a file! \n")
	exit()

# Vérifie que c'est bien un vcf
if filename.suffix==".vcf":
	fd=filename.read_text()
	
else:
    print("Oops, ", filename.suffix, " extention is missing!")
    exit()

#Vérification du format à l'intérieur du fichier    

fileformat = re.findall("##fileformat=VCFv4",fd)
chrom = re.findall("#CHROM",fd)
                     
#if fileformat :
#    print (fileformat)
        
#if chrom :
#    print(chrom)

if not chrom or not fileformat :
    print ("Oops, mandatory header line doesn't match with vcf type")
    exit()
else : 
    print("file successfully loaded")
		
# Imaginer une méthode pour vérifier que le vcf soit plein 

#VALEURS A EXTRAIRE
Dico = {}
nb_var= 0



#Creation d'un nouveau fichier
if not os.path.isfile('kofile.txt'):
    newf = open('kofile.txt','a')

else :
    print("Fichier déjà existant")

Lecture de fd en ligne (NE MARCHE PAS)
with open(filename,'r') as fl :
    print (fl.readline())
    for line in fl :
        print(line)


    headline = re.search("^#",line)

    print(headline)
    
    if headline :
            newf.write(line)

#Var cherche les infos importantes : Le chromosome, la position, les nucléotides et la qualité

    var = re.search("LG([0-9]+)\s([0-9]+)\s.\s([A-Z]+)\s([A-Z]+,*)+\s+([0-9]+.[0-9]+)", line)
    print(var)
    if var :
        nb_var+=1

        chr = var.group(1)

        pos = var.group(2)
        
        nucl1 = var.group(3)
        
        nucl2 = var.group(4)
        
        qual = var.group(5)

        # Création d'un dictionnaire qui renvoit la position exactes, les nucléotides et la qualité et fonction de la position
      
        Dico[pos] =(str(chr),str(pos),str(nucl1),str(nucl2),str(qual))

    else :

        print("Oops, it seems that something's wrong with your vcf file.")
        exit ()

for cle,valeur in Dico.items() :
    print(cle + " " + str(valeur))


print("Nombre de variant :"+ str(nb_var))

  
  
