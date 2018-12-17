
# Petites stats #

#Initialisation des variables
ins = 0
dell = 0
sub = 0

import os, sys, pathlib, argparse, re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

filename=sys.argv[1]
kogefile=open(filename, 'r')
    #.stem+'-m'+str(args.missing_data)+'-DP'+str(args.readDepth_genotype)+'-P'+str(args.geno_percent)+'.geno'+ '.distrib'+'.txt','r')
   
dico = {}
for line in kogefile: 

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
        count = 1
        co = 1

        # comptage des caractères du référent
        for char in ref :
            count +=1

        #Comptage des caractères de l'alt (si il y'en a plusieurs, on prend en compte uniquement le premier)
        for char in alt :
            co += 1

        #Comparaison pour trouver le nombre de substitution, d'insertion et de délétion. 
        if int(count)-int(co) == 0 :
            sub +=1
        elif int(count)-int(co) <= 0 :
            ins += 1
        else :
            dell += 1


        ######## DICTIONNAIRE ##########
        
        if chrom in dico.keys():

            #if pos in dico.keys() :

            dico[chrom][pos] = (ref, alts)

            #else :
            #    dico[chrom][pos] = [ref, alt]
        else :
            dico[chrom] = {}
            dico[chrom][pos] = (ref, alts)

#print(dico)


print ('\n sub:' + str(sub) +', ins:' + str(ins) +', del:' + str(dell))

# Taux de mutation
tsub = (sub/ (sub+ins+dell)) * 100
tins = (ins/ (sub+ins+dell)) * 100
tdel = (dell/ (sub+ins+dell)) * 100

print('\n ' + str(tsub) + ' ' +str(tins) +' ' + str(tdel))

nb_pos = 1
#Comptages de toutes les positions
for keys in dico[chrom].items():
    #print(keys)
    nb_pos += 1

print(nb_pos)

# Comptage des mutations par chromosomes 
nb_mut = 1
liste_ch = []

for item in dico :
    #print(item)
    nb_mut = 1
    for posi in dico[item] :
        #print(posi)
        nb_mut +=1

    #print('\n chr:' + str(item) + ', mut:' + str(nb_mut))
    liste_ch.append(str(item))
    liste_ch.append(str(nb_mut))
    #print(nb_mut)
    #resu =(nb_mut/ nb_pos )*100
    #print(resu)

print(liste_ch)
