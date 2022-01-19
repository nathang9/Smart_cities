import pandas as pd

from pretraitement import *
from prosumers import *

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

tab = []
time = []
for i in range(len(tab50)):
    time = []
    print(i)
    for j in range(len(tab50[i][1])):
        cons = tab50[i][1][j][1]
        prod = tab50[i][1][j][0]
        w = worst_case(power_buy=cons, power_produce=prod, prices_power=(0.1, 0.1), time=tab50[i][0])
        time.append(w)
        print(w)
    tab.append(time)
print("----------------------------------------------------------------")
print(tab)