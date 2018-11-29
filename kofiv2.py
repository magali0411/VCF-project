#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, pathlib, argparse, re

# Vérifie l'argument 
parser=argparse.ArgumentParser()
parser.add_argument("vcf" ,help="Take vcf file as argument/ vcf file path needed if it's outside your working directory")
parser.add_argument("-m","--missing_data", type=int, default=5, choices=range(0, 101), help=" The percentage of tolerated missing data shall fall within 0-100 interval!")
parser.add_argument("-dp","--readDepth_genotype", type=int, default=10, help="Minimum Depth of coverage (DP) per genotype")
parser.add_argument("-p","--geno_percent", type=int, default=95, help="Minimum percentage of genotype required harboring the defined DP")

args=parser.parse_args()
#print(args.vcf,"\n")
# print (args.missing_data, "\n")
# print (args.readDepth_genotype, "\n")
# print (args.geno_percent, "\n")

# Récupère le chemin vérifie si le fichier est bien un fichier
from pathlib import Path
filename=Path(args.vcf)
# print(filename.stem)
# exit()

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

############################################################################################
#                          Step 1 VCF cleaning and filtration  and conversion file                            # 
############################################################################################

#Creation d'un nouveau fichier vcf

kofile = open(filename.stem+'-m'+str(args.missing_data)+'-DP'+str(args.readDepth_genotype)+'-P'+str(args.geno_percent)+'.vcf','a')
konvfile=open(filename.stem+'-m'+str(args.missing_data)+'-DP'+str(args.readDepth_genotype)+'-P'+str(args.geno_percent)+'.txt','a')

#Ecriture de l'entête dans le nouveau vcf kofile
from re import finditer
for line in fd : 
   
    headline = re.search("^##.+",line)
   
    if headline :
        
#        print(headline.group(0))
        kofile.write("\n"+ headline.group(0))
    
    chromline = re.search("#CHROM.+",line)
    if chromline : 
        kofile.write("\n" + chromline.group(0))
        # Comptage du nombre d'individus dans le vcf
        liste = chromline.group(0).split("\t")
        liste_ind=liste[9:]
#        print(liste_ind)
#        exit()
        konvfile.write("\n"+ liste[0]+"\t"+liste[1]+"\t"+ liste[3]+"\t"+liste[4])
        for i in liste_ind:
#            print(i)
            konvfile.write("\t"+i)
#        exit()
#        print(liste[9:])
        #print(len(liste[9:]))
        nb_indiv = len(liste[9:])
        # print("nombre indiv "+ str(nb_indiv)+"\n")
 #       print(chromline.group(0))

#Extraction des qualité et DP générale
    qual = re.search("\s(\d+\.\d+)\s",line)
    dp_g = re.search(";(DP=)(\d+);",line)
    
    
    

    
    if qual and dp_g:
        # print("qualité "+ qual.group(0)+"\n")
        # print (dp_g.group(1)+ " "+ dp_g.group(2)+ "\n")
        # # print(dp_geno.group(2),"\n", line)
        # exit()
        # 
#Filtre sur la qualité et la DP générale
        if (float(qual.group(0)) > 30 and int(dp_g.group(2))>= (int(nb_indiv)*10)) :
            # exit()
            
            #Filtre sur un pourcentage max de données manquantes tolérées 
            missing_iterator = finditer("\.\/\.", line)
            missing_count = 0
            for match in missing_iterator:
                missing_count +=1
            # print(line, "\n")
            # print(missing_count, "\n")
            # print("qualité "+ qual.group(0)+"\n")
            # print (dp_g.group(1)+ " "+ dp_g.group(2)+ "\n")
            # print(dp_geno.group(2),"\n")
            if float((missing_count*100)/nb_indiv)<=args.missing_data:
                # print(line, "\n")
                # print(missing_count, "\n")
                dp_geno_it=finditer(":(\d+):", line)
                dp_geno_count=0
                for mat in dp_geno_it:
                    if(int(mat.group(1))>=args.readDepth_genotype):
                        dp_geno_count+=1
                    # else:
                    #     print("toto", mat.group(1))
                    #print(dp_geno_count, "\n")
                # print(line, "\n")
                # print("count= " ,dp_geno_count, "\n")
                if float((dp_geno_count*100)/nb_indiv)>=args.geno_percent:
                    # print("count1= " ,dp_geno_count, "\n")
                    kofile.write("\n" + line)
fd.close()
kofile.close()

#Ouverture du nouveau fichier vcf
ko = open(filename.stem+'-m'+str(args.missing_data)+'-DP'+str(args.readDepth_genotype)+'-P'+str(args.geno_percent)+'.vcf',"r").readlines()        
# 
for line in ko :
    #print(line)
    geno = re.search("(^[a-zA-Z]+\d+)\s+(\d+)\s+.+\s+([a-zA-Z]+)\s+([a-zA-Z]),*([a-zA-Z]*)\s",line)
    if geno:
#        print("toto", geno)
        ref=geno.group(3)
        alt=geno.group(4)
        alts=geno.group(5)
        geno_iterator = finditer("(\d)\/(\d)", line)
        geno_count = 0
        for mag in geno_iterator:
            if(mag.group(1)=="0"):
                g1=ref
                
                
            geno_count +=1
        
#        print(ref, alt, alts)
    
    
#     
# #Var cherche les infos importantes : Le chromosome, la position, les nucléotides et la qualité
#         
# 
# 
#    var = re.search("LG([0-9]+)\s([0-9]+)\s.\s([A-Z]+)\s([A-Z]+,*)+\s+([0-9]+.[0-9]+)", line)
#    print("toto",var)
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
#        # qual = var.group(5)
# 
#         # Création d'un dictionnaire qui renvoit la position exactes, les nucléotides et la qualité et fonction de la position
#      
#        Dico[pos] =(str(chr),str(pos),str(nucl1),str(nucl2),)
# 
#    else :
# 
#        print("Oops, it seems that something's wrong with your vcf file.")
#        exit ()
# #
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



