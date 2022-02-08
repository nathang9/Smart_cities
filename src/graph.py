import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

from prosumers import *
from market import *
from visualisation import *

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
    plt.show()

def plot_worst_case(tab, prosumer_rank):
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
    plt.show()

def plot_market_VS_worst(tab, prosumer_rank):

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
        if liste_participants[prosumer_rank].isProducer:
            prix = liste_participants[prosumer_rank].balance * MAIN_GRID_SELL[tab[i][0]]
        else:
            prix = liste_participants[prosumer_rank].balance * MAIN_GRID_BUY[tab[i][0]]
        market_graph.append(prix - dict_rep[name])
        update_ALL(tab,i, liste_participants)

        cons = tab[i][1][prosumer_rank][1]
        prod = tab[i][1][prosumer_rank][0]
        w, _ = worst_case(power_buy=cons, power_produce=prod, prices_power=(0.2, 0.2), time=tab[i][0])
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
    plt.show()

def plot_prod_cons(tab):
    fig, axs = plt.subplots(2, 4)
    for i in range(0, 4):
        hours, prod, cons = cons_prod_one(tab, i * 2);
        hours1, prod1, cons1 = cons_prod_one(tab, i * 2 + 1)
        axs[0, i].plot(hours, prod, 'r')
        axs[0, i].plot(hours, cons, 'b')
        axs[0, i].set_title('Résidence n° ' + str(i * 2))
        axs[1, i].plot(hours1, prod1, 'r')
        axs[1, i].plot(hours1, cons1, 'b')
        axs[1, i].set_title('Résidence n° ' + str(i * 2 + 1))
    plt.show()
