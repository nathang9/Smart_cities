import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

from src.prosumers import *
from src.market import *
from src.visualisation import *

from src.market import market
from src.pretraitement import pretraitement
from src.prosumers import create

# All the prices are the current (2021 / 2022) french prices with EDF
# main grid price 0,1558 €/kWh # sell for 0,1873 €/kWh
# Price variation depending of the hour of the day, the day of the week and the season
# été : [hc, hc, hc, hc, hc, hc, hc, hm, hm, hm, hm, hp, hp, hp, hp, hp, hp, hm, hm, hc, hc, hc, hc, hc]
# hiver : [hc, hc, hc, hc, hc, hc, hc, hp, hp, hp, hp, hm, hm, hm, hm, hm, hm, hp, hp, hc, hc, hc, hc, hc]
# week-end : [hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc]
# hc : heure creuse ; hm : heure moyenne ; hp : heure pleine
# coefficients are chosen arbitrarily
hc, hm, hp = 0.5 * 0.1558, 0.75 * 0.1558, 1.25 * 0.1558
# summer prices are chosen for this simulation
MAIN_GRID = [hc, hc, hc, hc, hc, hc, hc, hm, hm, hm, hm, hp, hp, hp, hp, hp, hp, hm, hm, hc, hc, hc, hc, hc]
# Coefficients for buying prices and selling prices are chosen arbitrarily : 1.1 for buying and 0.9 for selling
MAIN_GRID_SELL = [element * 0.9 for element in MAIN_GRID]
MAIN_GRID_BUY = [element * 1.1 for element in MAIN_GRID]


def plot_worst_case_ALL(tab):
    """both the cost for a given prosumer with and without market exchanges

    Plot the cost for all the prosumers without market
    :param tab: table provided by pretraitement.py
    """
    temp = []
    graph = [[] for i in range(len(tab[0][1]))]
    time = []
    day = 1
    for i in range(len(tab)):
        print(i)
        if (i > 0 and tab[i - 1][0] > tab[i][0]):
            day += 1
        time.append(datetime.datetime(year=1, month=1, day=day, hour=tab[i][0], minute=0, second=0))
        for j in range(len(tab[i][1])):
            cons = tab[i][1][j][1]
            prod = tab[i][1][j][0]
            w, _ = worst_case(power_buy=cons, power_produce=prod, prices_power=(0.1, 0.0), time=tab[i][0])
            graph[j].append(w)
            print(w)
        temp.append(graph)
    print(time)
    for i in range(len(graph)):
        plt.figure()
        plt.plot(time, graph[i])
        # beautify the x-labels
        plt.gcf().autofmt_xdate()
        myFmt = mdates.DateFormatter('%H:%M')
        plt.gca().xaxis.set_major_formatter(myFmt)
    #plt.show()


def plot_worst_case(tab, prosumer_rank):
    """
    Plot the cost without market for one prosumer

    :param tab: table provided by pretraitement.py
    :param prosumer_rank: number of the prosumer
    """
    graph = []
    time = []
    day = 1
    for i in range(len(tab)):
        print(i)
        if (i > 0 and tab[i - 1][0] > tab[i][0]):
            day += 1
        time.append(datetime.datetime(year=1, month=1, day=day, hour=tab[i][0], minute=0, second=0))
        cons = tab[i][1][prosumer_rank][1]
        prod = tab[i][1][prosumer_rank][0]
        w, _ = worst_case(power_buy=cons, power_produce=prod, prices_power=(0.1, 0.0), time=tab[i][0])
        graph.append(w)
        print(w)
    print(time)
    plt.figure()
    plt.plot(time, graph)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    #plt.show()


def plot_market_VS_worst(tab, prosumer_rank):
    """
    Plot both the cost for a given prosumer with and without market exchanges

    :param tab: table provided by pretraitement.py
    :param prosumer_rank: number of the prosumer
    """
    graph = []
    market_graph = []
    time = []
    day = 1

    liste_participants = create(tab)
    name = "prosumer" + str(prosumer_rank)

    for i in range(len(tab)):
        print(i)

        if (i > 0 and tab[i - 1][0] > tab[i][0]):
            day += 1
        time.append(datetime.datetime(year=1, month=1, day=day, hour=tab[i][0], minute=0, second=0))

        marche = market(liste_participants, 0.9, MAIN_GRID_BUY[tab[i][0]], MAIN_GRID_SELL[tab[i][0]])
        marche.resolve()
        dict_rep = marche.getDictionnaireGain()
        if liste_participants[prosumer_rank].balance > 0:
            prix = - liste_participants[prosumer_rank].balance * MAIN_GRID_SELL[tab[i][0]] - dict_rep[name]
        else:
            prix = - liste_participants[prosumer_rank].balance * MAIN_GRID_BUY[tab[i][0]] - dict_rep[name]
        market_graph.append(prix)
        update_ALL(tab, i, liste_participants)

        cons = tab[i][1][prosumer_rank][1]
        prod = tab[i][1][prosumer_rank][0]
        w, _ = worst_case(power_buy=cons, power_produce=prod, prices_power=(0.0, 0.0), time=tab[i][0])
        graph.append(w)
        print(w)

    print(time)
    plt.figure()
    plt.plot(time, graph)
    plt.plot(time, market_graph)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    #plt.show()

# Récupération de la production et la consommation heure par heure d'une résidence 'resi' en particulier
def cons_prod_one(tab, resi):
    """
    Gather the production and the consumption for a household

    :param tab: table provided by pretraitement.py
    :param resi: household number
    :return: hours, production, consumption
    """
    cons = []
    prod = []
    hours = []
    for i in range(0, len(tab)):
        prod.append(tab[i][1][resi][0])
        cons.append(tab[i][1][resi][1])
        hours.append(str(i))
    return hours, prod, cons


# Courbe de consommation et production de chaque résident au cours du temps
# doub=[c,p] permet de préciser ce qu'on veut voir:
# [1,1]=consommation et production
# [1,0]=seulement la consommation
# [0,1]=seulement la production
def plot_prod_cons(tab, doub):
    """
    Plot the consumption and/or the production of all prosumers

    :param tab: table provided by pretraitement.py
    :param doub: array for plotting consumption and/or production [1 if plot consumption else 0, 1 if plot production else 0]
    """
    plt.figure()
    [c, p] = doub
    if c != 0 or p != 0:
        fig, axs = plt.subplots(2, 4)
        for i in range(0, 4):
            hours, prod, cons = cons_prod_one(tab, i * 2)
            hours1, prod1, cons1 = cons_prod_one(tab, i * 2 + 1)
            if p == 1:
                axs[0, i].plot(hours, prod, 'r')
                axs[1, i].plot(hours1, prod1, 'r')
            if c == 1:
                axs[0, i].plot(hours, cons, 'b')
                axs[1, i].plot(hours1, cons1, 'b')

            axs[0, i].set_title('Résidence n° ' + str(i * 2 + 1))
            axs[1, i].set_title('Résidence n° ' + str(i * 2 + 2))
        #plt.show()
    else:
        print("Rien n'est demandé.")


def plot_prosumer_gain_delta(prosumer_rank):
    """
    Plot the variation of gain with respect to the delta parameter

    :param prosumer_rank:
    """
    plt.figure()
    prosumer_name = "prosumer" + str(prosumer_rank)
    tab50 = pretraitement("Copie.csv", 50)
    liste_teta = []
    liste_gain = []
    nb_valeur_teta = 100
    for teta in range(nb_valeur_teta):
        print(
            'Creation de la liste des participants -------------------------------------------------------------------------------')
        liste_participants = create(tab50)
        teta = teta / nb_valeur_teta
        print('Création du marché')
        marche = market(liste_participants, teta, 0.1558 * (2 - teta) * 0.75, 0.1558 * teta * 0.75)
        marche.resolve()
        print('marché résolu')
        dict_rep = marche.getDictionnaireGain()
        liste_teta.append(teta)
        liste_gain.append(dict_rep[prosumer_name])

    plt.plot(liste_teta, liste_gain)
    #plt.show()
