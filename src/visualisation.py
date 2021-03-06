import matplotlib.pyplot as plt
import matplotlib as matplotlib
import tkinter as tk

# Visus nécessaires: courbe de gain par personne, courbe de participation d'heure en heure, les gains avec moyenne/max/min
# Conso et prod d'heure en heure pour chaque prosumer

def visualisation_generale():
    matplotlib.use('TkAgg')
    h = courbe_prix(0.1)
    plt.legend(handles=h)
    plt.show()
    return ('yeah!')


# Permet de voir la différence de prix entre l'achat/vente sur la main grid et le prix sur le marché
def courbe_prix(delta):
    hc, hm, hp = 0.5 * 0.1558, 0.75 * 0.1558, 1.25 * 0.1558
    MAIN_GRID = [hc, hc, hc, hc, hc, hc, hc, hm, hm, hm, hm, hp, hp, hp, hp, hp, hp, hm, hm, hc, hc, hc, hc, hc]
    MAIN_GRID_SELL = [element * 0.9 for element in MAIN_GRID]
    MAIN_GRID_BUY = [element * 1.1 for element in MAIN_GRID]
    MARKET_PRICE = []
    for i in range(0, 24):
        MARKET_PRICE.append(MAIN_GRID_BUY[i] - delta * (MAIN_GRID_BUY[i] - MAIN_GRID_SELL[i]))
    # x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    # psell, = plt.plot(x, MAIN_GRID_SELL, label="sell")
    # pbuy, = plt.plot(x, MAIN_GRID_BUY, label="buy")
    # pmarket, = plt.plot(x, MARKET_PRICE, label="market")

    # plt.legend(handles=[psell, pbuy, pmarket])
    # plt.show()

    # handles = [psell, pbuy, pmarket]
    return MAIN_GRID_BUY, MAIN_GRID_SELL, MARKET_PRICE


# Argent gagné par une personne en choisissant le fonctionnement marché plutôt que la main grid
def gain_par_personne(tab_temoin, tab_market):
    diff = []
    for i in range(0, len(tab_temoin)):
        diff.append(tab_market[i] - tab_temoin[i])
    return diff


# Argent gagné en moyenne, argent gagné au maximum et au minimum à chaque itération
def mean_min_max(tabs_gain):
    mini, maxi, moy = [], [], []
    for i in range(0, len(tabs_gain)):
        mini.append(min(tabs_gain[i]))
        maxi.append(max(tabs_gain[i]))
        moy.append(sum(tabs_gain[i]) / len(tabs_gain[i]))
    pmin, = plt.plot(mini, label="Gain minimum")
    pmax, = plt.plot(maxi, label="Gain maximum")
    pmoy, = plt.plot(moy, label="Gain moyen")
    handles = [pmin, pmax, pmoy]
    return handles

# Récupération de la production et la consommation heure par heure d'une résidence 'resi' en particulier
def cons_prod_one(tab, resi):
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
    [c,p] = doub
    if c != 0 or p != 0:
        fig, axs = plt.subplots(2, 4)
        for i in range(0, 4):
            hours, prod, cons = cons_prod_one(tab, i * 2)
            hours1, prod1, cons1 = cons_prod_one(tab, i * 2 + 1)
            if p==1 :
                axs[0, i].plot(hours, prod, 'r')
                axs[1, i].plot(hours1, prod1, 'r')
            if c==1 :
                axs[0, i].plot(hours, cons, 'b')
                axs[1, i].plot(hours1, cons1, 'b')

            axs[0, i].set_title('Résidence n° ' + str(i * 2 + 1))
            axs[1, i].set_title('Résidence n° ' + str(i * 2 + 2))
        plt.show()
    else:
        print("Rien n'est demandé.")
