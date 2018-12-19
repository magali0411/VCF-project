#! src\bin\env python3
# -*- coding: utf-8 -*-

#Importation des modules

import os, sys, pathlib, argparse, re, time, threading
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
import webbrowser
from math import * 

#Installation de Tkinter selon les différentes versions
try:
    try : 
        import tkinter as Tk
        from tkinter import * 
        from tkinter.messagebox import *
        from tkinter.filedialog import *
    except:
        import Tkinter as Tk
        from tKinter import * 
        from tKinter.messagebox import *
        from tKinter.filedialog import *
except:
    raise ImportError('Tkinter non disponible')

#Définition des couleurs
orange = '#fde3d9'
orangedark = '#f47645'
blue = '#7acfdf'
bluedark = '#61a5b2'
grey = "#E3E2E1"


#Procédure de fermeture de le fenêtre princiaple
def Exit():
    if askyesno("Exit", "Do you really want to exit kofi :'( ?"):
        showwarning('Exit', "Exiting...see you soon") 
        main.destroy()

    else:
        showinfo('Exit', 'Welcome back on kofi!')

#Initailisation de la fenêtre principale
main = Tk()
main.title("Kofi")
main.configure(bg = "white")
main.resizable(0,0)
#main.attributes("-fullscreen", 2)
#On récupère la largeur (ws) et la hauteur (hs) de la fenêtre
ws = main.winfo_screenwidth()
hs = main.winfo_screenheight()
#calcul la position de la fenetre adaptée à l'écra,
x = (ws/2) - (ws/2)
y = (hs/2) - (hs/2)
#applique la taille et la position
main.geometry('%dx%d+%d+%d' % (ws, hs, 0, 0))

#intercepte l'evenement quit pour informer l'utilisateur, appel la fonction Exit
main.protocol("WM_DELETE_WINDOW", Exit)


# Fonction d'affichage de l'heure

time1 = ''
time2 = ''

def hour():

    global time1
    # Heure actuelle du PC
    time2 = time.strftime('%H:%M:%S')
    # Si le temps récupéré est différent
    if time2 != time1:
        time1 = time2
        clock.config(text=time2)
    # Toute les 200ms la fonction s'appelle (récursivité) pour s'actualiser 
    clock.after(200, hour)

# Fonction pour ouvrir le manuel
new = 1
url = "https://github.com/emiracherif/VCF-project/blob/master/README.md"
url2 = "https://github.com/emiracherif/VCF-project/blob/master/INSTALL.md"

def openweb():
    webbrowser.open(url,new=new)

def openweb2() :
    webbrowser.open(url2, new= new)

#######################################################
################ Ouverture du fichier! ################
#######################################################

#Récupération du chemin du fichier selectionné
def open_vcf() : 
    #main.configure(bg = grey)
    filepath = askopenfilename(title="Open vcf file",filetypes=[('vcf files','.vcf')])
    # On lance la suite du programme avec le chemin récupéré 
    verif_opening(filepath)


# Fonction de vérification sur le fichier sélectionnée


compteur = 0 

def verif_opening(filepath) :

    ######### Initatilisation de la toplevel ##########
    loading = Toplevel(main, cursor = "watch", bg = orange)
    cpt = Toplevel(loading, bg = blue)
    loading.geometry("%dx%d%+d%+d" % (ws//7,hs//6,ws//3,hs//3))  
    loading.title =("Kofi")
    loading.resizable(0,0)
    lab=Label(loading, text="Loading file...", font = ("Helvetica", 18, "bold"), bg = orange)
    lab.grid(sticky='ew')

    
    ########### Création d'un compteur du temps d'analyse #####
    def compteur_sec() :

        #Initialisation du compteur
        # On ne peut pas quitter le compteur manuellement 
        cpt.overrideredirect(TRUE) 
        cpt.title =("waiting time")
        cpt.resizable(0,0)
        cpt.geometry('%dx%d+%d+%d' % (ws//5,hs//5,ws//7,hs//6))
        
        compteur = 0
        text = Label(cpt, text="Waiting time :", font =("", 14), bg = blue, fg = "white")
        coff = Label(cpt, text= "Go make yourself some coffe...",font =("", 8), bg = blue, fg = "white" )
        compteur_lbl = Label(cpt, text= str(compteur), font=("", 20), bg = blue, fg = "white")
        def incremente():
        #Incrémentation 
            global compteur
            compteur += 1 
            compteur_lbl['text'] = str(compteur) + str("sec")
            cpt.after(1000, incremente)
        incremente()
        # appel récursif (compteur infini)

        #Placement des widgets sur la fenêtre
        text.pack(pady = 25)
        compteur_lbl.pack()
        coff.pack(side = BOTTOM)
        
    # On récupère le chemin du fichier dans une variable si le fichier existe 

    try : 
        filename = Path(filepath)
    except :
        loading.destroy()
        return showwarning("Warning", "Please select a file!")

    # Vérifie que l'utilisateur a bien choisi un fichier
    if not Path.is_file(filename):
        loading.destroy()
        return showwarning("Warning", "Please select a file!")

    if showwarning :
        loading.destroy

    prog = Label(loading, bg = orange, text = "Path OK!", font = ("Helvetica", 10))
    prog.grid(sticky='ew')

    ################################################################################
    # Normalement l'utilisteur choisi forcément un fichier de type VCF
    # des doubles vérifications sont tout de même effectuées
    ###########################################################################

    #Si le fichier séléctionné n'existe pas, ou plus 
    if not filename.exists():

        #Exit de la fonction de chargement, affichage d'une erreur
        return showerror("Error", "Oops, this file dosn't exist anymore!")

    #Sinon, affichage que c'est ok!
    prog.configure(text = "Path OK! \n File OK!")

    # Appel du compteur 
    compteur_sec()

    ################# Ouverture et vérification à l'intérieur du fichier ####################

    def next() :
        prog.configure(text = "")
        deeper.destroy()
        fileformat = re.findall("##fileformat=VCFv4",fd)    
        chrom = re.findall("#CHROM",fd)

        # Fonction de passage à l'étape de filtration du vcf
        def ex() :
            filtre(filename)
            loading.destroy()

        # Analyse des entêtes dans le fichier 
        if not chrom or not fileformat :
            #Si on ne trouve pas ces deux entêtes, on exit la fonction et on renvoit une erreur
            return showerror("Error", "Oops, mandatory header line doesn't match with vcf type")
        else : 
            # Retour positif sur le fichier
            prog.configure(text = "We opened it and ... \n you're file is perfectly fine! ")
            # Affichage du bouton pour passer à l'étape suivante!
            yeah = Button(loading, text="Next step", relief = 'groove', command = ex,fg = "white", bg = orangedark, cursor='hand2')
            yeah.grid(sticky='n')

    ### Vérifie que c'est bien un vcf
    if filename.suffix==".vcf":

        #Ouverture du fichier dans la variable fd
        fd=filename.read_text()

        # Retour positif
        prog.configure(text = "Path OK! \n File OK! \n .vcf OK!")

        # Affichage du bouton pour vérifier l'intérieur du fichier
        deeper = Button(loading, relief = 'groove', text="Let's go deeper", command = next,fg = "white", cursor='hand2', bg = orangedark)
        deeper.grid(sticky = 'n') #Affiche le bouton qui lance l'analyse à l'intérieur du fichier
    
    else:
        # On quitte la fonction et donc la toplevel avec un message d'erreur 
        return showerror("Error", "Oops, wrong extention!")

##########################################################
############# Mise en place des filtres ##################
##########################################################

m = ""
DP = ""
P = ""

def filtre(filename) :

    # Chargement de l'interface
    main.configure(bg="white")
    back.destroy()
    load.destroy()
    info = Label(main, text = "{} is loaded.".format(filename.name), font = "Helevtica 14 bold" , bg = "white" )
    info.place(relwidth = 0.9,rely = 0.15)

    # Création des cadres de séléctions
    cadre_data = LabelFrame(main, bd=1, text = "Missing data", font = "Helevtica 14", bg = orange)
    cadre_dp = LabelFrame(main, bd=1, text = "DP (Read Depth)",  bg = orange, font = "Helevtica 14")
    cadre_gen = LabelFrame(main, bd=1, text =  "Genotype percentage",  bg = orange, font = "Helevtica 14")

    #Placement des cadres
    cadre_data.place(relwidth = 0.9, relx= 0.05, rely = 0.3)
    cadre_dp.place(relwidth = 0.9,relx = 0.05, rely = 0.5)
    cadre_gen.place(relwidth = 0.9,relx = 0.05, rely= 0.7 )

    #Création des logos d'informations pour chaque valeur
    def info_data() :
        showinfo(title = 'Missing data', message = "KOFI missing data corresponds to missing genotypes specified with two dots separated by a slash './.'")
        
    def info_dp() :
        showinfo(title = 'DP', message = 'KOFI DP corresponds to the minimum percentage of read depth per genotype')

    def info_gen() :
        showinfo(title = 'Genotype percentage', message = 'KOFI Genotype percentage corresponds to the minimum percentage of genotype required with the predefined DP')

    #Ecritures au sein des cadres
    l1 = Label(cadre_data, text = " Please choose the percentage of tolerated missing data shall fall within 0-100 interval", bg = orange)
    b1 = Button(cadre_data,bitmap = 'question',fg="black", command = info_data).pack(side = RIGHT)
    l1.pack(side = LEFT)
    l2 = Label(cadre_dp, text = "Please choose the minimum Depth of coverage (DP) per genotype (numeric value expected)", bg = orange)
    b2 = Button(cadre_dp,bitmap = 'question', fg = "black", command = info_dp).pack(side = RIGHT)
    l2.pack(side = LEFT)
    l3 = Label(cadre_gen, text = "Please choose the minimum percentage of genotype required harboring the defined DP (numeric value expected)", bg = orange)
    b3 = Button(cadre_gen,bitmap = 'question',fg="black", command= info_gen).pack(side = RIGHT)
    l3.pack(side = LEFT)

    #Choix des données manquantes avec attribution d'une valeur par défaut

    def1 = StringVar(main)
    def1.set(5)
    choix_data = Spinbox(cadre_data, from_=0, to=50, increment=5, bg="white", textvariable = def1)
    choix_data.pack()

    #Choix de la DP 
    def2 = StringVar(main)
    def2.set(10)
    choix_DP = Spinbox(cadre_dp, from_=0, to=30, increment=5, bg="white", textvariable = def2)
    choix_DP.pack()

    #Choix du % de genotype
    def3 = StringVar(main)
    def3.set(95)
    choix_gen = Spinbox(cadre_gen, from_= 0, to=100, increment = 5, bg = "white", textvariable = def3 )
    choix_gen.pack()

    #Validation des valeurs 
    def val() :

        #Affectation ou non des de la valeur de la DP
        try : 
            DP = int(choix_DP.get())
            #Desactivation de la séléction
            choix_DP.configure(state = 'disabled')
        except :
            return showerror(title = "Error", message = "Numeric value expected for DP")

        #Affectation ou non des de la valeur de la data
        try :
            m = float(choix_data.get())
            #Desactivation de la séléction
            choix_data.configure(state='disabled')
        except :
            return showerror(title = "Error", message = "Numeric value expected for missing data")
            
        #Affectation ou non des de la valeur du genotype
        try :
            P = float(choix_gen.get())
            #Desactivation de la séléction
            choix_gen.configure(state='disabled')
        except :
            return showerror(title = "Error", message = "Numeric value expected for genotpye")

        #Passage au nettoyage du fichier
        nettoyage(filename,m,P,DP)

    #Création et placement du bouton de validation    
    valide = Button(main, relief = 'groove', bg = bluedark, fg = "white",font = "Helevtica 12", text = "Validate", command = val)
    valide.place(relx = 0.8, rely= 0.8 )

####################################################################
#############      ETAPE DE NETTOYAGE DU PREMIER VCF        ########
############# CREATION DE 4 NOUVEAUX FICHIERS PLUS LISIBLES ########
####################################################################

def nettoyage(filename, m, P, DP) :

    # Creation d'une toplevel de chargement
    nettoyage = Toplevel(main, cursor = "watch", bg = blue)
    nettoyage.geometry("%dx%d%+d%+d" % (ws//3,hs//3,ws//3,hs//3))  
    nettoyage.title =("Kofi")
    lab=Label(nettoyage, text="\n Creating a new filtred vcf file with the choosen filtred. \n \n Conversion of the filtred vcf in tabular genotyping file.\n \n Creating a genotype distribution file.",fg = "white", font = ("Helvetica", 18, "bold"), bg = blue)
    lab.pack()

    ####### Etape 1.1 nettoyage & filtres   ####### 

    nb_indiv = 0

    #Creation d'un nouveau fichier vcf et on récupère son nom
    kofile = open(filename.stem+'-m'+str(m)+'-DP'+str(DP)+'-P'+str(P)+'.vcf','a')
    nameko = filename.stem+'-m'+str(m)+'-DP'+str(DP)+'-P'+str(P)+'.vcf'

    #Creation du nouveau fichier de genotypage (conversion du vcf) + son nom
    konvfile=open(filename.stem+'-m'+str(m)+'-DP'+str(DP)+'-P'+str(P)+'.geno'+'.txt','a')
    namekonv = filename.stem+'-m'+str(m)+'-DP'+str(DP)+'-P'+str(P)+'.geno'+'.txt'

    #Creation du nouveau fichier de genotypage distrib + son nom 
    kogefile=open(filename.stem+'-m'+str(m)+'-DP'+str(DP)+'-P'+str(P)+'.geno'+ '.distrib'+'.txt','a')
    namekoge = filename.stem+'-m'+str(m)+'-DP'+str(DP)+'-P'+str(P)+'.geno'+ '.distrib'+'.txt'

    #Ecriture de l'entête dans le nouveau vcf kofile
    from re import finditer
    fd = open(filename,"r")

    for line in fd : 
    
        headline = re.search("^##.+",line)
    
        if headline :
    
            kofile.write("\n"+ headline.group(0))
        
        chromline = re.search("#CHROM.+",line)
        if chromline : 
            kofile.write("\n"+chromline.group(0))
            # Comptage du nombre d'individus dans le vcf
            liste = chromline.group(0).split("\t")
            nb_indiv = len(liste[9:])
            
            #Ecriture de l'entete du fichier de conversion konvfile
            konvfile.write("\n"+"SNP_ID"+"\t"+"CHROM"+"\t"+"POS"+"\t"+"REF"+"\t"+"ALT")
            liste_ind=liste[9:]
            for i in liste_ind:
                konvfile.write("\t"+i)

            #Ecriture de l'entete du fichier de geno distrib kogefile
            kogefile.write("\n"+"SNP_ID"+"\t"+"CHROM"+"\t"+"POS"+"\t"+"REF"+"\t"+"ALT"+
                           "\t"+"Ho1"+"\t"+"aHo1_Total"+"\t"+"Ho2"+"\t"+"aHo2_Total"+"\t"+"Ho3"+
                           "\t"+"aHo3_Total"+"\t"+"He1"+"\t"+"bHe1_Total"+"\t"+"He2"+"\t"+"bHe2_Total"+
                           "\t"+"He3"+"\t"+"bHe3_Total"+"\t"+"MD"+"\t"+"mD_Total"
                           )


    #Extraction des qualités et DP générales
        qual = re.search("\s(\d+\.\d+)\s",line)
        dp_g = re.search(";(DP=)(\d+);",line)
    
        if qual and dp_g:
           
            #Filtre sur la qualité et la DP générale
            if (float(qual.group(0)) > 30 and int(dp_g.group(2))>= (int(nb_indiv)*10)) :

                
                #Filtre sur un pourcentage max de données manquantes tolérées 
                missing_iterator = finditer("\.\/\.", line)
                missing_count = 0
                for match in missing_iterator:
                    missing_count +=1

                # Condition sur le pourcentage de de données manquantes tolérées choisi par l'utilisateur ou celle par défaut
                if float((missing_count*100)/nb_indiv)<=float(m):

                    dp_geno_it=finditer(":(\d+):", line)
                    dp_geno_count=0
                    
                    # Condition sur la DP/genotype minimale choisie par l'utilisateur ou celle par défaut
                    for mat in dp_geno_it:
                        if(int(mat.group(1))>=int(DP)):
                            dp_geno_count+=1

                    # Condition sur le pourcentage minimal d'individus choisi par l'utilisateur ayant la DP/genotype minimale  ou par défaut
                    if float((dp_geno_count*100)/nb_indiv)>=float(P):
                        # Ecriture du nouveau vcf filtré kofile
                        kofile.write("\n"+line)
    fd.close()
    kofile.close()

    ####### Etape 1.2 VCF2genofile #######

    # Ouverture du nouveau fichier vcf
    ko = open(filename.stem+'-m'+str(m)+'-DP'+str(DP)+'-P'+str(P)+'.vcf',"r").readlines()        

    # Remplissage du geno file 
    for line in ko :

        geno = re.search("(^[a-zA-Z]+\d+)\s+(\d+)\s+.+\s+([a-zA-Z]+)\s+([a-zA-Z]),*([a-zA-Z]*)\s",line)
    
        # Si la ligne n'est pas dans l'entête
        if not line.startswith('\n') and not line.startswith('#')  :
            head=line.split("\t")
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
            gg=1


            for mag in geno_iterator:


                if mag.group(0)=="0/0" or mag.group(0)=="0|0":
                    konvfile.write("\t"+ref+"/"+ref)
                    g1+=1
                 
                elif mag.group(0)=="1/1"or mag.group(0)=="1|1":
                    g2+=1
                    konvfile.write("\t"+alt+"/"+alt)
            
                elif mag.group(0)=="2/2"or mag.group(0)=="2|2":
                    g3+=1
                    konvfile.write("\t"+alts+"/"+alts)

                elif mag.group(0) in ('0/1','0|1', '1/0','1|0'):
                    g4+=1
                    konvfile.write("\t"+ref+"/"+alt)

                elif mag.group(0) in ('0/2','0|2', '2/0','2|0'):
                    g5+=1
                    konvfile.write("\t"+ref+"/"+alts)

                elif mag.group(0) in ('1/2','1|2', '2/1','2|1'):
                    g6+=1
                    konvfile.write("\t"+alt+"/"+alts)

                else:
                    gg+=1
                    konvfile.write("\t"+mag.group(0))
                

        
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
    kogefile=open(filename.stem+'-m'+str(m)+'-DP'+str(DP)+'-P'+str(P)+'.geno'+ '.distrib'+'.txt','r')

    # Ouverture d'un nouveau fichier stat
    kostatfile=open(filename.stem+'-m'+str(m)+'-DP'+str(DP)+'-P'+str(P)+'.stat'+'.txt','a')
    namekostat = str(filename.stem+'-m'+str(m)+'-DP'+str(DP)+'-P'+str(P)+'.stat'+'.txt')
    
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

    kostatfile.write('Chromosome \t' + 'Nombre de mutations \t' + 'Taux \n')

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

    showinfo(title="files created", message = "Created on your working directory : \n{}".format('-'+nameko+'\n'+'-'+namekonv +'\n'+'-'+namekoge) + '\n'+'-'+namekostat)
    
    if showinfo :
        # On efface les widget de la fenêtre pour passer aux stats...
        for chose in main.winfo_children():
            chose.destroy() 
        # ... mais on garde le menu et l'entête du programme 
        label2 = Label(main, bg=bluedark, font = "helevtica 10 italic")
        label = Label(main, text="Welcome on Kofi.dev", bg = blue, font = "helevtica 10 italic") 
        label2.place(relheight = 0.05,relwidth = 1,rely = 0)
        label.place(relwidth = 1, rely = 0  )
        thend = Label(main, text = "Thanks for using KOFI!", bg = "white", fg = bluedark, font = 'helevtica 32 bold')
        thend.place(rely = 0.4, relx = 0.4)

        # Création d'un menu sur la fenêtre
        menubar = Menu(main)
        menu1 = Menu(menubar, tearoff=0)
        #menu1.add_command(label="About kofi")
        menu1.add_command(label="About kofi", command = openweb)
        menu1.add_command(label="User guide", command = openweb2)
        menubar.add_cascade(label="Help", menu=menu1)
        #Attribution du menu au main
        main.config(menu=menubar)
        return heat(m,DP,P, filename)

################################################
########### Affichage de l'heatmap #############
################################################

def heat(m, DP, P,filename) : 

    #Utilisation de pandas pour réaliser un dataframe 
    data = pd.read_table(filename.stem+'-m'+str(m)+'-DP'+str(DP)+'-P'+str(P)+'.geno'+ '.distrib'+'.txt', delimiter="\t")

    df=pd.DataFrame(data[['POS','CHROM','aHo1_Total','aHo2_Total','aHo3_Total','bHe1_Total','bHe2_Total','bHe3_Total','mD_Total']])
 
    # Default heatmap: just a visualization of this square matrix

    df = df.pivot_table(index=data[['POS']],
                        values=data[['POS','aHo1_Total','aHo2_Total','aHo3_Total','bHe1_Total','bHe2_Total','bHe3_Total','mD_Total']])


    p1 = sns.heatmap(df,vmin=0,vmax=250,cmap="RdBu_r")

    plt.show()


#############################################################################
################# INTERFACE FENETRE PRINCIPALE ##############################
#############################################################################

#Chargement interface 
back = Button(main, bg = orange, bd = 0 )
#back2 = Button(main, bg = orange, bd = 0)
load = Button(main, text ='Load VCF', font = "Helevtica 16 bold", cursor="circle",command = open_vcf, bg = orangedark, fg = "white", bd = 0.2 , pady = 4, padx = 5)
label2 = Label(main, bg=bluedark, font = "helevtica 10 italic")
label = Label(main, text="Welcome on Kofi.dev", bg = blue, font = "helevtica 10 italic") 

#PLacement de l'interface
back.place(rely = 0.4, relx = 0.4 , height = 300, width = 300 )    
#back2.place(rely = 0.4, relx = 0.4 , height = 200, width = 200 ) 
load.place(rely = 0.4, relx = 0.4 , height = 150, width = 150 )
#Entête du programme
label2.place(relheight = 0.05,relwidth = 1,rely = 0)
label.place(relwidth = 1, rely = 0  )

# Création d'un menu sur la fenêtre

menubar = Menu(main)
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="About kofi", command = openweb)
menu1.add_command(label="User guide", command = openweb2)
menubar.add_cascade(label="Help", menu=menu1)

#Attribution du menu au main
main.config(menu=menubar)

# Placement de l'horloge
clock = Label(main, font=('times', 20, 'bold'), bg='white', fg= bluedark)
clock.place(rely = 0.85, relx = 0.85)
hour()


main.mainloop()
