#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, pathlib, argparse, re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from math import * 
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
                       "\t"+"Ho1"+"\t"+"aHo1_Total"+"\t"+"Ho2"+"\t"+"aHo2_Total"+"\t"+"Ho3"+
                       "\t"+"aHo3_Total"+"\t"+"He1"+"\t"+"bHe1_Total"+"\t"+"He2"+"\t"+"bHe2_Total"+
                       "\t"+"He3"+"\t"+"bHe3_Total"+"\t"+"MD"+"\t"+"mD_Total"
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


dico = {}
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
   
        geno_iterator = finditer("(.)\/(.)", line)
        g1=1
        g2=1
        g3=1
        g4=1
        g5=1
        g6=1
        # g7=1
        # g8=1
        # g9=1
        gg=1

        for mag in geno_iterator:


            if mag.group(0)=="0/0" or mag.group(0)=="0|0":
                konvfile.write("\t"+ref+"/"+ref)
#                print(ref+"/"+ref)
                g1+=1
                
#                kogefile.write("\t"+ref+"/"+ref+"\t"+str(g1))
            
            elif mag.group(0)=="1/1"or mag.group(0)=="1|1":
                g2+=1
                konvfile.write("\t"+alt+"/"+alt)
            
            elif mag.group(0)=="2/2"or mag.group(0)=="2|2":
                g3+=1
                konvfile.write("\t"+alts+"/"+alts)
            elif mag.group(0) in ('0/1','0|1', '1/0','1|0'):
                g4+=1
                konvfile.write("\t"+ref+"/"+alt)
#                kogefile.write("\t"+ref+"/"+alt+"\t"+str(g1))
            # elif mag.group(0)=="1/0"or mag.group(0)=="1|0":
            #     g3+=1
            #     konvfile.write("\t"+alt+"/"+ref)
            elif mag.group(0) in ('0/2','0|2', '2/0','2|0'):
                g5+=1
                konvfile.write("\t"+ref+"/"+alts)
            # elif mag.group(0)=="2/0"or mag.group(0)=="2|0":
            #     g5+=1
            #     konvfile.write("\t"+alts+"/"+ref) 
            
            elif mag.group(0) in ('1/2','1|2', '2/1','2|1'):
                g6+=1
                konvfile.write("\t"+alt+"/"+alts)
            # elif mag.group(0)=="2/1"or mag.group(0)=="2|1":
            #     g8+=1
            #     konvfile.write("\t"+alts+"/"+alt)
            else:
                gg+=1
                konvfile.write("\t"+mag.group(0))
#                kogefile.write("\t"+mag.group(0)+"\t"+str(g0))
                

#        print("\n",gg)

        
        kogefile.write("\t"+ref+"/"+ref+"\t"+str(g1)+"\t"+alt+"/"+alt+"\t"+str(g2)+"\t"+alts+"/"+alts+"\t"+str(g3)+
                               "\t"+ref+"/"+alt+"\t"+str(g4)+"\t"+ref+"/"+alts+"\t"+str(g5)+"\t"+alt+"/"+alts+"\t"+str(g6)+
                               "\t"+mag.group(0)+"\t"+str(gg))
konvfile.close()
kogefile.close()

######################################################
############# STATS SUPPLEMENTAIRES ##################
######################################################

ins = 0
dell = 0
sub = 0

# Ouverture du fichier de génotypage
ko = open(filename.stem+'-m'+str(args.missing_data)+'-DP'+str(args.readDepth_genotype)+'-P'+str(args.geno_percent)+'.geno'+ '.distrib'+'.txt','r').readlines()        

# Ouverture d'un nouveau fichier stat
kostatfile=open(filename.stem+'-m'+str(args.missing_data)+'-DP'+str(args.readDepth_genotype)+'-P'+str(args.geno_percent)+'.stat'+'.txt','a')

dico = {}

for line in ko: 

    #keys cherche le chromosome et la position, var cherche l'alt et le ref
    keys= re.search("LG(\d+)_(\d+)", line)
    var = re.search("\d+\s([a-zA-Z]+)\s(([a-zA-Z]+),?([a-zA-Z]+)?)",line)

    if keys:

        # On associe les resultats à des variables
        chrom = keys.group(1)
        pos = keys.group(2)

        ref = var.group(1)
        alt = var.group(3)
        alts = var.group(2)

        # On initialise deux compteurs : un pour le nucl ref l'autre pour l'alternatif
        count = 0
        co = 0

        # comptage des caractères du référent
        for char in ref :
            count +=1

        #Comptage des caractères de l'alt (si il y'en a plusieurs, on prend en compte uniquement le premier)
        for char in alt :
            co += 1

        #Comparaison pour trouver le nombre de substitutions, d'insertions et de délétions. 
        if int(count)-int(co) == 0 :
            sub +=1
        elif int(count)-int(co) <= 0 :
            ins += 1
        else :
            dell += 1

        ######## DICTIONNAIRE ##########
        
        if chrom in dico.keys():
            dico[chrom][pos] = (ref, alts)

        else :
            dico[chrom] = {}
            dico[chrom][pos] = (ref, alts)


# Taux de mutation
tsub = ceil((sub/ (sub+ins+dell)) * 100)
tins = ceil((ins/ (sub+ins+dell)) * 100)
tdel = ceil((dell/ (sub+ins+dell)) * 100)

# Ecriture dans le nouveau fichier de stat
kostatfile.write('Types de mutation \t' + 'Substitutions' +'\t Insertions' +'\t Deletions \n')
kostatfile.write('Nombre \t' + str(sub) +'\t' + str(ins) +'\t' + str(dell) + '\n')
kostatfile.write('Pourcentage\t' + str(tsub) +'\t' + str(tins) +'\t' + str(tdel) + '\n\n')

#Comptages de toutes les positions
nb_pos = 0
for item in dico : 
    for keys in dico[chrom] :
        nb_pos += 1


# Comptage des mutations par chromosomes 
nb_mut = 0
liste_ch = []
liste_sch = []

kostatfile.write('Chromosome \t' + 'Nombre de mutations \t' + 'Pourcentage \n')

for item in dico :
    nb_mut = 0
    for posi in dico[item] :
        nb_mut +=1

    # Arrondi supérieur
    a = ceil((nb_mut/nb_pos)*100)

    # Ecriture dans le fichier
    kostatfile.write(str(item) +'\t' + str(nb_mut) + '\t ' + str(a) + '\n')

    liste_ch.append(str(item))
    liste_ch.append(str(nb_mut))
    liste_sch.append(str(a))

data = pd.read_table(filename.stem+'-m'+str(args.missing_data)+'-DP'+str(args.readDepth_genotype)+'-P'+str(args.geno_percent)+'.geno'+ '.distrib'+'.txt', delimiter="\t")

df=pd.DataFrame(data[['POS','CHROM','aHo1_Total','aHo2_Total','aHo3_Total','bHe1_Total','bHe2_Total','bHe3_Total','mD_Total']])



df = df.pivot_table(index=data[['POS']],
                        values=data[['POS','aHo1_Total','aHo2_Total','aHo3_Total','bHe1_Total','bHe2_Total','bHe3_Total','mD_Total']])
#                        columns=data[['G1','G2','G3','G4','G5','G6','G7','G8','G9','G10']])


#print(data)
#exit()
#print(nb_indiv)
p1 = sns.heatmap(df,vmin=0,vmax=250,cmap="RdBu_r")

plt.show()
#print()



