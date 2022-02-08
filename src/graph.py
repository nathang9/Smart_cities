import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

from prosumers import *
from market import *



def plot_prosumers(tab):
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