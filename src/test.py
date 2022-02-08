import pandas as pd
import matplotlib.pyplot as plt

from src.graph import plot_prosumer_gain_delta
from src.pretraitement import *
from src.prosumers import *
from src.market import *

tab50 = pretraitement("Copie.csv")
print(tab50)
liste_teta = []
liste_gain = []
nb_valeur_teta = 1000
for teta in range(nb_valeur_teta):
    print('Creation de la liste des participants -------------------------------------------------------------------------------')
    liste_participants = create(tab50)
    teta = teta/nb_valeur_teta
    print('teta : ' +str(teta))
    print('Création du marché')
    marche = market(liste_participants,teta,0.1558*(2-teta)*0.75,0.1558*teta*0.75)
    marche.resolve()
    print('marché résolu')
    dict_rep = marche.getDictionnaireGain()
    print(dict_rep)
    liste_teta.append(teta)
    liste_gain.append(dict_rep['prosumer1'])

#plt.plot(liste_teta, liste_gain)
#plt.show()
print('here------------------------------------------------------------------------------------')
plot_prosumer_gain_delta('prosumer1')
