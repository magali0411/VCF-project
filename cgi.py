#! src\bin\env python3
# -*- coding: utf-8 -*-

#Importation des modules

import os, sys, pathlib, argparse, re

from pathlib import Path

from tkinter import * 

from tkinter.messagebox import *

from tkinter.filedialog import *



#Définition des couleurs
orange = '#fde3d9'
orangedark = '#f47645'
blue = '#7acfdf'
bluedark = '#61a5b2'
grey = "#E3E2E1"

#Procédure de fermeture
def Exit():
    if askyesno("Exit", "Êtes-vous sûr de vouloir quitter?"):
        showwarning('Exit', "Fermeture de kofi")
        main.destroy()

    else:
        showinfo('Exit', 'Welcome back on kofi')

#Initailisation de la fenêtre principale
main = Tk()
main.title("Kofi")
#main.geometry("%dx%d%+d%+d" % (500, 500, 0, 0))
main.resizable(0,0)
main.configure(bg = "white")
#main.attributes("-fullscreen", 2)
ws = main.winfo_screenwidth()
hs = main.winfo_screenheight()
#calcul la position de la fenetre
x = (ws/2) - (ws/2)
y = (hs/2) - (hs/2)
#applique la taille et la position
main.geometry('%dx%d+%d+%d' % (ws, hs, x, y))
#intercepte l'evenement quit, appel Exit
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

# Inactivation du main quand il existe une autre fenêtre


# Ouverture du fichier!
def open_vcf() : 
    main.configure(bg = grey)
    filepath = askopenfilename(title="Open vcf file",filetypes=[('vcf files','.vcf'),('all files','.*')])
    # Etape d'ouverture du fichier ici 

    waiting_opening()

# Fichier de progression des vérifications 


def waiting_opening() :
    
    loading = Toplevel(main, cursor = "watch")
    loading.geometry( "300x200+30+30") 
    loading.title =("Kofi")
    loading.resizable(0,0)
    lab=Label(loading, text="Loading file...")
    lab.grid(row = 5, column = 5)
    filtre()

# Mise en place des filtres 

a = "val"

DP_GE = StringVar()
DP_GE.set("999")

def filtre() :
    #loading.withdray()
    main.configure(bg="white")
    back.destroy()
    back2.destroy()
    load.destroy()
    info = Label(main, text = "VCF file is load. Please select .... blablabla", bg = "white")
    info.place(relwidth = 0.9,rely = 0.15, relx= 0.015)
    
    # Création des deux cadres
    cadre_qual = LabelFrame(main, bd=1, text = "Quality", font = "Helevtica 14", bg = orange)
    cadre_dp = LabelFrame(main, bd=1, text = "DP (deep lenght)",  bg = orange, font = "Helevtica 14")
    
    #Placement des deux cadres
    cadre_qual.place(relwidth = 0.9,rely = 0.2, relx= 0.05)
    cadre_dp.place(relwidth = 0.9,rely = 0.4, relx = 0.05)

    #Ecritures au sein des cadres
    l1 = Label(cadre_qual, text = "Veuillez selectionner la qualité minimale", bg = orange)
    l1.pack(side = LEFT)
    l2 = Label(cadre_dp, text = "La valeur de base du génotype est de \a \n  Souhaitez vous la changer?", bg = orange)
    l2.pack(side = LEFT)

    #Choix du changement ou non de la DP de base
   
    r1 = Radiobutton(cadre_dp, text="Oui", bg = orange)
    r1.pack(side = LEFT)
    r2 = Radiobutton(cadre_dp, text="Non", bg = orange)
    r2.pack(side = LEFT)
    e1 = Entry(cadre_dp, bg = "white", text = "DP / genotype", state='disabled', textvariable = DP_GE )
    e1.pack()
 
    #Choix de la qualité
    choix_qual = Spinbox(cadre_qual, from_=0, to=10000, increment=250, bg="white" )
    choix_qual.pack()

    #Choix de la DP activée uniquement si l'utilisateur le souhaite (boucle)
    choix_dpgen = Spinbox(cadre_dp)

    
    #state = 'readonly','disabled'



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