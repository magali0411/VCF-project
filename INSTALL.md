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

![](images/KOFIFinterface.png)

La séléction du fichier VCF se fait grâce à un explorateur de fichier. 

#### Etape 2 : Choix des options

![](images/KOFIFAna.png)

Les valeurs des données manquantes, de la profondeur de read et du pourcentage de génotype peuvent être séléctionnées ou écrites dans les cases.
Les boutons d'aides [?] donnent des informations les valeurs à entrer. 

#### Etape 3 : Resultat

![](images/KOFIResul.png)

Avant d'ouvrir les fichiers d'analyses il est conseillé de fermer KOFI.


