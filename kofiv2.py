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
    file=filename.read_text()
    
else:
    print("Oops, ", filename.suffix, " extention is missing!")
    exit()

#Vérification du format à l'intérieur du fichier    

fileformat = re.findall("##fileformat=VCFv4",file)
chrom = re.findall("#CHROM",file)
                     
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
    
fd = open(filename,"r")

Dico = {}
nb_indiv = 0

#Creation d'un nouveau fichier

kofile = open('kofile.vcf','a')

#Ecriture de l'entête dans le nouveau vcf kofile
for line in fd : 
   
    headline = re.search("^##.+",line)
   
    if headline :
        
#        print(headline.group(0))
        kofile.write("\n"+ headline.group(0))
    
    chromline = re.search("#CHROM.+",line)
    if chromline : 
        kofile.write("\n" + chromline.group(0))
        
        liste = chromline.group(0).split("\t")
#        print(liste[9:])
#        print(len(liste[9:]))
        nb_indiv = len(liste[9:])
 
#        print(chromline.group(0))

    qual = re.search("\s(\d+\.\d+)\s",line)
    
    if qual :
#        print(qual.group(0))
        if (float(qual.group(0)) > 30) :
#            print (qual.group(0))
            kofile.write("\n" + line)
        
        


#Var cherche les infos importantes : Le chromosome, la position, les nucléotides et la qualité
        


#    var = re.search("LG([0-9]+)\s([0-9]+)\s.\s([A-Z]+)\s([A-Z]+,*)+\s+([0-9]+.[0-9]+)", line)
#    print(var)
#    if var :
#        nb_var+=1
#
#        chr = var.group(1)
#
#        pos = var.group(2)
#        
#        nucl1 = var.group(3)
#        
#        nucl2 = var.group(4)
#        
#        qual = var.group(5)

        #Création d'un dictionnaire qui renvoit la position exactes, les nucléotides et la qualité et fonction de la position
#      
#        Dico[pos] =(str(chr),str(pos),str(nucl1),str(nucl2),str(qual))
#
#    else :
#
#        print("Oops, it seems that something's wrong with your vcf file.")
#        exit ()
#
#for cle,valeur in Dico.items() :
#    print(cle + " " + str(valeur))

#
#print("Nombre de variant :"+ str(nb_var))
#
##Utilisation de la librairie PANDAS pour le dataframe.
##Si données manquantes, complète automatique par "NaN"
##Permet de filtrer les données "à la sql"
##A TESTER
#
#filtered = pandas.dataframe(data = Dico, index = "locus", columns ="locus" "chromosomes" "qualité" "nucléotide de base" "variant")
#
#print(filtered)
#
##if not os.path.isfile('kofile.txt'):
##    filtered.to_csv("kofile.txt",sep="\t",encoding="utf-8", index="locus")
##
##
##with open("kofile.txt", "a", encoding="utf-8") as f : 
##    f.write(headline)
##    print(f.read_text())
#
## Extraction d'une ligne 
##filtered.iloc[1]
#
##Filtre
##DataFrame.filter(items=None, like=None, regex=None, axis=None)
#
##On crée un index sur la position
##dfi = df.set_index("locus")
#
## Renvoit la ligne en position 14 !!
##print(dfi.loc["14"])
#
## Extraction des chromosomes et des locus entre 1000 et 50000
##df.loc[1000:50000,["chr","locus"]



