# VCF-project: KOFI (toolKit fOr vcF analysIs) ....
==========================

KOFI is a software performing vcf analyses for you. The main goal of this tool is to facilitate the understanding of all the vcf data. 
After loading your file, we perform data filtration according to the following criteria : 
- Quality of the read is over 30
- General DP is at least ten times highter than the number of individuals
- Missing data is below 5%
- Genotype DP is over 10
- Percentage of genotype is over 95%

The third last values can be changed manually. 

There are three out-coming files : 
... 

Users can choose beetwen 2 programs : 
kofi.py wich can be lunched with python3 by giving the name of the vcf file as an argument on your terminal.
cgi.py can be lunched with python3 without any argument. All the steps are performed with an graphic interface simple to use.

*[Installation manual](https://github.com/emiracherif/VCF-project/blob/master/INSTALLmd)

## Manual

Command

Arguments

Si le vcf de départ est phasé le fichier geno respectera l'ordre du phasage meme si le genotype est noté "/"


## Required

Please make sure you own the latest version of those packages : 
- system packages : os, sys, pathlib, argparse, re
- dataframe and graphic packages : numpy, pandas, seaborn, matplotlib.pyplot 

## Running KOFI

##Contributing

* Licencied under CeCill-C (http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html) and GPLv3 
* Intellectual property belongs to ... 
* Written by Magali Arhainx and  Emira Cherif
* Copyright 2014-5000

## Contact 

For bug tracking purpose you can use the GitHub questions or you can contact the developers at
xxx@xxx.fr](mailto:xxx@xxx.fr)

.
.
.

