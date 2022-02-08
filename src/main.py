import pandas as pd

from src.pretraitement import *
from src.prosumers import *
from src.market import *

tab50,tab60,tab70,tab75 = pretraitement("Copie.csv");
# print(tab50)
# print(tab50[0][1][0][1])

#print(len(tab50))
#print((len(tab50[0])))
#print((len(tab50[0][0])))
#print((len(tab50[0][0][0])))
#print((len(tab50[0][0][0][0])))

#df = pd.read_csv("../data/household_data/75pourcent.csv")
#tab50 = create_tab(df)

#tab = []
#time = []
#for i in range(len(tab50)):
#    time = []
#    print(i)
#    for j in range(len(tab50[i][1])):
#        cons = tab50[i][1][j][1]
#        prod = tab50[i][1][j][0]
#        w = worst_case(power_buy=cons, power_produce=prod, prices_power=(0.1, 0.1), time=tab50[i][0])
#        time.append(w)
#        print(w)
#    tab.append(time)
#print("----------------------------------------------------------------")
#print(tab)
print('Creation de la liste des participants -------------------------------------------------------------------------------')
liste_participants = create(tab50)
print('Création du marché')
marche = market(liste_participants,0.9,0.1558*1.1*0.75,0.1558*0.9*0.75)
marche.resolve()
print('marché résolu')
dict_rep = marche.getDictionnaireGain()

for personne in dict_rep:
    print('Personne : ' + personne + ' , gain : ' + str(dict_rep[personne])+ '\n')