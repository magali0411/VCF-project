
# Petites stats #

#Initialisation des variables
ins = 0
dell = 0
sub = 0

kogefile=open(filename.stem+'-m'+str(args.missing_data)+'-DP'+str(args.readDepth_genotype)+'-P'+str(args.geno_percent)+'.geno'+ '.distrib'+'.txt','r')
   
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

        #Comptage des caract-res de l'alt
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
            dico[chrom][pos] = [ref, alts]

print(dico)
print ('\n sub:' + str(sub) +', ins:' + str(ins) +', del:' + str(dell))
# Taux de mutation
tsub = (sub/ (sub+ins+dell)) * 100
tins = (ins/ (sub+ins+dell)) * 100
tdel = (dell/ (sub+ins+dell)) * 100
print('\n ' + str(tsub) + ' ' +str(tins) +' ' + str(tdel))