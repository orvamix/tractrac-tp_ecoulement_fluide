# -*-coding:Utf-8 -*

#########################################################################
#
#Programme en python permettant d'exploiter les résultats d'analyse
#d'un écoulement de liquide dans une conduite grâce au programme TracTrac
#exploité sur Matlab. La matrice 'Pts' fut exportée en .csv
#
##########################################################################


#-- importation des bibliothèques --

import numpy as np
import csv
import matplotlib.pyplot as plt

#-- Variables --

#largeur de la conduite en pixel et subdivision en intervalles de cette largeur
largeur=1000
subdi=20
fichier_entree="resultats-matlab/tractrac120.csv"
fichier_sortie="resultats-python/res120-max.csv"

#-- Programme --


#Creation d'une matrice "results" à partir du fichier .csv
#Chaque ligne correspond à une particule à un certain moment
results = []
with open(fichier_entree) as csvfile:
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    for row in reader:
        results.append(row)


inter=largeur//subdi

#Matrice 'réduction' de 2 colonnes et n lignes correspondants à la matrice résults
reduction = np.zeros(shape=(len(results),2))

#Matrice 'somme' de 2 lignes et n colonnes correspondants aux intervalles
somme = np.zeros(shape=(2,inter))

#Matrice finale
final = np.zeros(shape=(inter))

#On réduit la matrice résults de 11 colonnes pour n'en faire plus que 2
#Ces deux colonnes restantes correspondent à la position verticale et la vitesse
i=0
for x in results:
    reduction[i][0]=x[3]
    reduction[i][1]=x[4]
    i+=1

#On calcule la variable position qui correspond à la postion de la particule en pixel divisé
#par la subdivision en intervalles.
#Ainsi, la ligne 0 de la matrice correspond aux nombres de particules détectées pour toutes les images pour chaque intervalle
#La ligne 1 correspond à la somme des vitesses pour les particules d'un intervalle donné.
i=0
for x in reduction:
    position=reduction[i][0]//subdi
    position=int(position)
    somme[1][position-1]+=reduction[i][1]
    somme[0][position-1]+=1
    i+=1

#La matrice finale correspond à la moyenne des vitesses. On fait la somme totale des vitesses divisé par le nombre de particules
#pour chaque intervalle. On vérifie qu'il n'y a pas de division par 0 (s'il y a 0 particules détectées).
i=0
for i in range(inter):
    if float(somme[0][i])==0.0:
        continue
    
    final[i]=abs(float(somme[1][i])/float(somme[0][i]))
    i+=1


print(final)

#On sauvegarde la matrice finale dans un .csv
np.savetxt(fichier_sortie, final, delimiter=",", fmt='%1.4f')

#On affiche le résultat
plt.plot(final)
plt.show()