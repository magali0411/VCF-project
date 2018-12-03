
DicoID = {}
liste = []

#Un ou plusieurs dico ? 

i = 0
for ligne in fd :
	DicoID[i] = () # Liste vide à remplir avec les infos importantes (REGEX)

	##Numéro de chromosome
	s_chr = re.search("LG([0-9]*)", ligne)
	if s_chr : 
		chr = str(s_chr.group(0))
                DicoID[i] = list.append(chr)
        else :
                #Comment gérer des variants qui n'ont pas beaucoup d'info? Tri au préalable?            
		
	##Position
	s_pos = re.search("LG[0-9]*.([0-9]*)", ligne)
	if s_pos :
		pos = str(s_pos.group(0))

	##Nucléotides
	s_nucl = re.search ("\s([A-Z]*)\s([A-Z]*)", ligne)
	if s_nucl :
		nucl1 = str(s_nucl.group(0))
		nucl2 = str(s_nucl.group(1))
	# groupe 1 : nucléotide(s) référence
	# groupe 2 : nucléotide(s) variants

	##Qualité 
	s_qual = re.search ("s[A-Z]*\s[A-Z]*\s([0-9]*\.[0-9]*)")
		if s_qual :
			qual = str(s_qual)


        i = i +1

