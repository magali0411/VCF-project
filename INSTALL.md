# Requis

## La version 3 et plus de Python est recommandée 
Librairies Python
> os
> sys
> re
> pathlib
> argparse
> re

Système d'exploitation 
> Linux / ubuntu 
> Windows (l'installation d'anaconda est recommandée) 

## Softwares/Modules
> python3-tk
> pandas 0.23.4
> numpy
> seaborn
> matplotlibe.pylot
> webbrowser
> math

Pour installer les modules nécessaires au bon fonctionnnement de KOFI:
```
pip install --upgrade *module name*
```
## Installation
Pour installer KOFI :
Créer le dossier où KOFI sera installer puis:
```
git clone https://github.com/emiracherif/VCF-project.git
```
Deux fichiers vcf test sont fournis (https://github.com/emiracherif/VCF-project/tree/master/datatest).
## Utilisation
### Version 1: Ligne de commande
Pour lancer KOFI avec les options par défaut:
```
python kofi.py file.vcf
```

Pour lancer KOFI avec des options personalisées:
```
python kofi.py file.vcf -m <int> -dp <int> -p <int>
```
- -m  
Entier correspondant au pourcentage de données manquantes tolérées . 
- -dp  
Entier correspondant à la profondeur (DP) minimale de "reads"/ génotype.
- --p  
Entier correspondant au pourcentage de génotypes ayant la DP minimale

### Version 2: Interface cgi
Pour lancer l'interface KOFI:
```
python koficgi.py
```
#### Etape 1 : Selection du VCF

![](images/1.png |width=100)

Une fois arrivé sur l'interface KOFI, cliquer sur le bouton central "load vcf".

![](images/2.png|width=100)

Un explorateur de fichier permettra la séléction du fichier voulu. 

![](images/3.png|width=100)

Il suffit ensuite de suivre les étapes annoncées par KOFI

![](images/4.png|width=100)

Finalement, il est possible de selectionner les valeurs des données manquantes, de profondeur minimale de "reads' par génotype et le pourcentage de génotpyes ayant la DP minimale. 

Kofi s'occupe ensuite de créer les 4 fichiers de sortis ainsi que l'affichage de l'heatmap. 



