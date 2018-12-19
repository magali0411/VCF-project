#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, pathlib, argparse, re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
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
#gg=1



############################################################################################
#                          Step 1  nettoyage & filtres du VCF                              # 
############################################################################################



    ####### Etape 1.1 nettoyage & filtres   ####### 


#Creation d'un nouveau fichier vcf
kofile = open(filename.stem+'-m'+str(args.missing_data)+'-DP'+str(args.readDepth_genotype)+'-P'+str(args.geno_percent)+'.vcf','a')

#Creation du nouveau fichier de genotypage (conversion du vcf)
konvfile=open(filename.stem+'-m'+str(args.missing_data)+'-DP'+str(args.readDepth_genotype)+'-P'+str(args.geno_percent)+'.geno'+'.txt','a')

#Creation du nouveau fichier de genotypage distrib

kogefile=open(filename.stem+'-m'+str(args.missing_data)+'-DP'+str(args.readDepth_genotype)+'-P'+str(args.geno_percent)+'.geno'+ '.distrib'+'.txt','a')

#Ecriture de l'entête dans le nouveau vcf kofile
from re import finditer
for line in fd : 
   
    headline = re.search("^##.+",line)
   
    if headline :
        
#        print(headline.group(0))
        kofile.write("\n"+ headline.group(0))
    
    chromline = re.search("#CHROM.+",line)
    if chromline : 
        kofile.write("\n"+chromline.group(0))
        # Comptage du nombre d'individus dans le vcf
        liste = chromline.group(0).split("\t")
        nb_indiv = len(liste[9:])
        
       #Ecriture de l'entete du fichier de conversion konvfile
        konvfile.write("\n"+"SNP_ID"+"\t"+"CHROM"+"\t"+"POS"+"\t"+"REF"+"\t"+"ALT")
        
       #Ecriture de l'entete du fichier de geno distrib kogefile
        kogefile.write("\n"+"SNP_ID"+"\t"+"CHROM"+"\t"+"POS"+"\t"+"REF"+"\t"+"ALT"+
                       "\t"+"G1"+"\t"+"G1_Total"+"\t"+"G2"+"\t"+"G2_Total"+"\t"+"G3"+
                       "\t"+"G3_Total"+"\t"+"G4"+"\t"+"G4_Total"+"\t"+"G5"+"\t"+"G5_Total"+
                       "\t"+"G6"+"\t"+"G6_Total"+"\t"+"G7"+"\t"+"G7_Total"+"\t"+"G8"+"\t"+"G8_Total"+
                       "\t"+"G9"+"\t"+"G9_Total"+"\t"+"G10"+"\t"+"GG_Total"
                       )
        liste_ind=liste[9:]
        for i in liste_ind:
            # print(indiv)
            konvfile.write("\t"+i)
        
#        exit()
#        print(liste[9:])
        #print(len(liste[9:]))


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

            # Condition sur le pourcentage de données manquantes tolérées choisi par l'utilisateur ou celle par défaut
            if float((missing_count*100)/nb_indiv)<=args.missing_data:

                dp_geno_it=finditer(":(\d+):", line)
                dp_geno_count=0
                
                # Condition sur la DP/genotype minimale choisie par l'utilisateur ou celle par défaut
                for mat in dp_geno_it:
                    if(int(mat.group(1))>=args.readDepth_genotype):
                        dp_geno_count+=1

                # Condition sur le pourcentage minimal d'individus choisi par l'utilisateur ayant la DP/genotype minimale  ou par défaut
                if float((dp_geno_count*100)/nb_indiv)>=args.geno_percent:
                    # Ecriture du nouveau vcf filtré kofile
                    kofile.write("\n"+line)
fd.close()
kofile.close()



    ####### Etape 1.2 VCF2genofile #######
    
# Ouverture du nouveau fichier vcf
ko = open(filename.stem+'-m'+str(args.missing_data)+'-DP'+str(args.readDepth_genotype)+'-P'+str(args.geno_percent)+'.vcf',"r").readlines()        

# Remplissage du geno file 
for line in ko :
    #print(line)
    geno = re.search("(^[a-zA-Z]+\d+)\s+(\d+)\s+.+\s+([a-zA-Z]+)\s+([a-zA-Z]),*([a-zA-Z]*)\s",line)
    
    
    if not line.startswith('\n') and not line.startswith('#')  :
        head=line.split("\t")
        # print(head[0:5])
        konvfile.write("\n"+head[0]+"_"+head[1]+"\t"+head[0]+"\t"+head[1]+"\t"+head[3]+"\t"+head[4])
        kogefile.write("\n"+head[0]+"_"+head[1]+"\t"+head[0]+"\t"+head[1]+"\t"+head[3]+"\t"+head[4])
    
    
    # Conversion du format des genotypes (numerique --> allélique)
    if geno:
        
        ref=geno.group(3)
        alt=geno.group(4)
        alts=geno.group(5)
        # print(ref+"/"+alt)
        geno_iterator = finditer("(.)\/(.)", line)
        g1=1
        g2=1
        g3=1
        g4=1
        g5=1
        g6=1
        g7=1
        g8=1
        g9=1
        gg=1

        for mag in geno_iterator:
            if mag.group(0)=="0/0" or mag.group(0)=="0|0":
                konvfile.write("\t"+ref+"/"+ref)
#                print(ref+"/"+ref)
                g1+=1
#                kogefile.write("\t"+ref+"/"+ref+"\t"+str(g1))
            
            elif mag.group(0)=="0/1"or mag.group(0)=="0|1":
                g2+=1
                konvfile.write("\t"+ref+"/"+alt)
#                kogefile.write("\t"+ref+"/"+alt+"\t"+str(g1))
            elif mag.group(0)=="1/0"or mag.group(0)=="1|0":
                g3+=1
                konvfile.write("\t"+alt+"/"+ref)
            elif mag.group(0)=="0/2"or mag.group(0)=="0|2":
                g4+=1
                konvfile.write("\t"+ref+"/"+alts)
            elif mag.group(0)=="2/0"or mag.group(0)=="2|0":
                g5+=1
                konvfile.write("\t"+alts+"/"+ref) 
            elif mag.group(0)=="1/1"or mag.group(0)=="1|1":
                g6+=1
                konvfile.write("\t"+alt+"/"+alt)
            elif mag.group(0)=="1/2"or mag.group(0)=="1|2":
                g7+=1
                konvfile.write("\t"+alt+"/"+alts)
            elif mag.group(0)=="2/1"or mag.group(0)=="2|1":
                g8+=1
                konvfile.write("\t"+alts+"/"+alt)
            elif mag.group(0)=="2/2"or mag.group(0)=="2|2":
                g9+=1
                konvfile.write("\t"+alts+"/"+alts)
            else:
                gg+=1
                konvfile.write("\t"+mag.group(0))
#                kogefile.write("\t"+mag.group(0)+"\t"+str(g0))
                

#        print("\n",gg)

        
        kogefile.write("\t"+ref+"/"+ref+"\t"+str(gg)+"\t"+ref+"/"+alt+"\t"+str(g2)+"\t"+alt+"/"+ref+"\t"+str(g3)+
                               "\t"+ref+"/"+alts+"\t"+str(g4)+"\t"+alts+"/"+ref+"\t"+str(g5)+"\t"+alt+"/"+alt+"\t"+str(g6)+
                               "\t"+alt+"/"+alts+"\t"+str(g7)+"\t"+alts+"/"+alt+"\t"+str(g8)+"\t"+alts+"/"+alts+"\t"+str(g9)+
                               "\t"+mag.group(0)+"\t"+str(gg))
konvfile.close()
kogefile.close()

# #Dans Pandas
# 

data = pd.read_table(filename.stem+'-m'+str(args.missing_data)+'-DP'+str(args.readDepth_genotype)+'-P'+str(args.geno_percent)+'.geno'+ '.distrib'+'.txt', delimiter="\t")

df=pd.DataFrame(data[['POS','G1_Total','G2_Total','G3_Total','G4_Total','G5_Total','G6_Total','G7_Total','G8_Total','G9_Total','GG_Total']])
#print(df.columns)
#exit()
#print(df)
#df = pd.DataFrame(np.random.random((5,5)), columns=["a","b","c","d","e"])
 
# Default heatmap: just a visualization of this square matrix
df = df.pivot_table(index=data[['POS']],
                        values=data[['G1_Total','G2_Total','G3_Total','G4_Total','G5_Total','G6_Total','G7_Total','G8_Total','G9_Total','GG_Total']])
#                        columns=data[['G1','G2','G3','G4','G5','G6','G7','G8','G9','G10']])
#print(data)
#exit()
#print(nb_indiv)
p1 = sns.heatmap(df,vmin=0,vmax=250,cmap="RdBu_r")

plt.show()
#print()




#print(data)
# print(data.describe())
# data.plot.hist()
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



