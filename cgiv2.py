#! src\bin\env python3
# -*- coding: utf-8 -*-

#Importation des modules

import os, sys, pathlib, argparse, re, time, threading
from pathlib import Path

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
    if askyesno("Exit", "Êtes-vous sûr de vouloir quitter?"):
        showwarning('Exit', "Fermeture de kofi")
        main.destroy()

    else:
        showinfo('Exit', 'Welcome back on kofi')

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

#w = main.winfo_reqwidth
#h = main.winfo_reqheight

# Création d'un menu sur la fenêtre
menubar = Menu(main)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Quitter", command=Exit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="A propos")
menubar.add_cascade(label="Aide", menu=menu2)

#Attribution du menu au main
main.config(menu=menubar)


################ Ouverture du fichier! ################


#Récupération du chemin du fichier selectionné
def open_vcf() : 
    #main.configure(bg = grey)
    filepath = askopenfilename(title="Open vcf file",filetypes=[('vcf files','.vcf')])
    # On lance la suite du programme avec le chemin récupéré 
    verif_opening(filepath)
    #return filepath

compteur = 0 
#filename = Path(filepath)
#print(filename)

def verif_opening(filepath) :

    ######### Initatilisation de la toplevel ##########
    loading = Toplevel(main, cursor = "watch", bg = orange)
    cpt = Toplevel(loading, bg = blue)
    #loading.geometry( "200x150") 
    loading.geometry("%dx%d%+d%+d" % (ws//7,hs//6,ws//3,hs//3))  
    loading.title =("Kofi")
    loading.resizable(0,0)
    lab=Label(loading, text="Loading file...", font = ("Helvetica", 18, "bold"), bg = orange)
    lab.grid(sticky='ew')
    #padx=120, pady=20)

    # On récupère le chemin du fichier dans une variable gloable
    filename = Path(filepath)

    # Vérifie que l'utilisateur a bien choisi un fichier
    if not Path.is_file(filename):
        return showwarning("Warning", "Please select a file!")
    prog = Label(loading, bg = orange, text = "Path OK!", font = ("Helvetica", 10))
    prog.grid(sticky='ew')

    ########### Création d'un compteur du temps d'analyse #####
    #compteur = 0 
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


    compteur_sec()
    ################################################################################
    # Normalement l'utilisteur choisi forcément un fichier de type VCF
    # des doubles vérifications sont tout de même effectuées
    ###########################################################################""

    #Si le fichier séléctionné n'existe pas 
    if not filename.exists():

        #Exit de la fonction de chargement, affichage d'une erreur
        return showerror("Error", "Oops, this file dosn't exist!")

    #Sinon, affichage que c'est ok!
    prog.configure(text = "Path OK! \n File OK!")

    ################# Ouverture et vérification à l'intérieur du fichier ####################
    def next() :
        prog.configure(text = "")
        deeper.destroy()
        fileformat = re.findall("##fileformat=VCFv4",fd)    
        chrom = re.findall("#CHROM",fd)

        # Fonction de passage à l'étape suivante
        def ex() :
            filtre(filename)
            loading.destroy()

        # Analyse dans le fichier 
        if not chrom or not fileformat :
            #main.configure(bg = "white")
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
        deeper.grid(sticky = 'n') #Affiche le bouton qui lance l'analyse à l'intérieur
    else:
        #main.configure(bg = "white")
        # On quitte la fonction et donc la toplevel avec un message d'erreur 
        return showerror("Error", "Oops, wrong extention!")

############# Mise en place des filtres ##################

#Initialisation des variables
m = DoubleVar() 
DP = IntVar()
P = DoubleVar()


def filtre(filename) :
    main.configure(bg="white")
    back.destroy()
    back2.destroy()
    load.destroy()
    info = Label(main, text = "VCF file is load.", font = "Helevtica 14 bold" , bg = "white" )
    info2 = Label(main, font = "Helevtica 12", text ="By default, we only kept data when : \n -quality score was over 30 \n -DP (read depth) was at least 10 time highter than individual" , bg = "white")
    info.place(relwidth = 0.9,rely = 0.15)
    info2.place(relwidth = 0.9, rely = 0.20)

    # Création des cadres
    cadre_data = LabelFrame(main, bd=1, text = "Missing data", font = "Helevtica 14", bg = orange)
    cadre_dp = LabelFrame(main, bd=1, text = "DP (deep lenght)",  bg = orange, font = "Helevtica 14")
    cadre_gen = LabelFrame(main, bd=1, text = "Génotype",  bg = orange, font = "Helevtica 14")

    #Placement des deux cadres
    cadre_data.place(relwidth = 0.9, relx= 0.05, rely = 0.3)
    cadre_dp.place(relwidth = 0.9,relx = 0.05, rely = 0.5)
    cadre_gen.place(relwidth = 0.9,relx = 0.05, rely= 0.7 )

    #Création des logos d'informations pour chaque valeur
    def info_data() :

        showinfo(title = 'Data', message = 'Les données manquantes...')
    def info_dp() :
        showinfo(title = 'DP', message = 'La DP ...')

    def info_gen() :
        showinfo(title = 'Génotype', message = 'Le génotype...')

    #Ecritures au sein des cadres
    l1 = Label(cadre_data, text = "Veuillez selectionner la qualité minimale (valeur numérique attendue)", bg = orange)
    b1 = Button(cadre_data,bitmap = 'question',fg="black", command = info_data).pack(side = RIGHT)
    l1.pack(side = LEFT)
    l2 = Label(cadre_dp, text = "Veuillez selectionner la DP minimale (valeur numérique attendue", bg = orange)
    b2 = Button(cadre_dp,bitmap = 'question', fg = "black", command = info_dp).pack(side = RIGHT)
    l2.pack(side = LEFT)
    l3 = Label(cadre_gen, text = "Veuillez selectionner le % de génotype (valeur numérique attendue)", bg = orange)
    b3 = Button(cadre_gen,bitmap = 'question',fg="black", command= info_gen).pack(side = RIGHT)
    l3.pack(side = LEFT)

    #Choix des données manquantes
    choix_data = Spinbox(cadre_data, from_=0, to=100, increment=10, bg="white")
    choix_data.pack()

    #Choix de la DP 
    choix_DP = Spinbox(cadre_dp, from_=0, to=30, increment=5, bg="white")
    choix_DP.pack()

    #Choix du % de génotype
    choix_gen = Spinbox(cadre_gen, from_= 0, to=100, increment = 5, bg = "white")
    choix_gen.pack()

    #Validation des valeurs 
    def val() :
        #Affectation ou non des de la valeur de la DP
        try : 
            DP = choix_DP.get()
            #Desactivation de la séléction
            choix_DP.configure(state = 'disabled')

        except :

            return showerror(title = "Error", message = "Numeric value expecter for DP")
            


        #Affectation ou non des de la valeur de la data
        try :
            m = choix_data.get()
            #Desactivation de la séléction
            choix_data.configure(state='disabled')

        except :

            return showerror(title = "Error", message = "Numeric value expecter for missing data")
    


        #Affectation ou non des de la valeur du génotype

        try :
            P = choix_gen.get()
            #Desactivation de la séléction
            choix_gen.configure(state='disabled')
        except :
            return showerror(title = "Error", message = "Numeric value expecter for genotpye")

        #Passage au nettoyage
        nettoyage(filename)

    #Création et placement du bouton de validation    
    valide = Button(main, relief = 'groove', bg = bluedark, fg = "white",font = "Helevtica 12", text = "Bloquer les valeurs", command = val)
    valide.place(relx = 0.8, rely= 0.8 )



def nettoyage(filename) :
    nettoyage = Toplevel(main, cursor = "watch", bg = blue)
    nettoyage.geometry("%dx%d%+d%+d" % (ws//3,hs//3,ws//3,hs//3))  
    nettoyage.title =("Kofi")
    lab=Label(nettoyage, text="Création d'un nouveau fichier vcf \n et d'un nouveau \n fichier de genotypage",fg = "white", font = ("Helvetica", 18, "bold"), bg = blue)
    lab.pack()
     ####### Etape 1.1 nettoyage & filtres   ####### 

    nb_indiv = 0
    #Creation d'un nouveau fichier vcf
    kofile = open(filename.stem+'-m'+str(m)+'-DP'+str(DP)+'-P'+str(P)+'.vcf','a')

    #Creation du nouveau fichier de genotypage (conversion du vcf)
    konvfile=open(filename.stem+'-m'+str(m)+'-DP'+str(DP)+'-P'+str(P)+'.geno'+'.txt','a')

    #Ecriture de l'entête dans le nouveau vcf kofile
    from re import finditer
    fd = open(filename,"r")
    print(filename)
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

                # Condition sur le pourcentage de de données manquantes tolérées choisi par l'utilisateur ou celle par défaut
                if float((missing_count*100)/nb_indiv)<=float(m):
                #float((missing_count*100)/nb_indiv)<=float(m):

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


#Chargement interface 
back = Button(main, bg = orange, bd = 0 )
back2 = Button(main, bg = orange, bd = 0)
load = Button(main, text ='Load VCF', font = "Helevtica 16 bold", cursor="circle",command = open_vcf, bg = orangedark, fg = "white", bd = 0.2 , pady = 4, padx = 5)
label2 = Label(main, bg=bluedark, font = "helevtica 10 italic")
label = Label(main, text="Welcome on Kofi V1", bg = blue, font = "helevtica 10 italic") 

#PLacement de l'interface
back.place(rely = 0.33, relx = 0.36 , height = 200, width = 200 )    
back2.place(rely = 0.4, relx = 0.4 , height = 200, width = 200 ) 
load.place(rely = 0.4, relx = 0.4 , height = 150, width = 150 )
#Entête du programme
label2.place(relheight = 0.05,relwidth = 1,rely = 0)

label.place(relwidth = 1, rely = 0  )

main.mainloop()
