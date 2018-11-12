#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, pathlib, argparse, re

#Vérification du format à l'intérieur du fichier (ne marche pas)
fileformat = re.search("##fileformat=VCFv4",fd)
chrom = re.search("#CHROM",fd)

     if (chrom != true || fileformat != true):
     	print ("Oops, file format doesn't match with vcf type")
     	exit()


## Donner un ID pour chaque locus variant:
## + création d'un dictionnaire de liste propre à chaque mutation

DicoID = {}
i = 0
for ligne in fd :
	DicoID[i] = () # Liste vide à remplir avec les infos importantes (REGEX)
	i = i +1


