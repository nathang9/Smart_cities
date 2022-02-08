import matplotlib.pyplot as plt
import pandas as pd

from src.pretraitement import *
from src.prosumers import *
from src.market import *
from graph import *

# Formate the data for use
tab50 = pretraitement("Copie.csv", 50);

# plot production for all prosumers
plot_prod_cons(tab50, [0, 1])
# plot consumption for all prosumers
plot_prod_cons(tab50, [1, 0])


# plot both the cost for a given prosumer with and without market exchanges
plot_market_VS_worst(tab50, 5)
plot_market_VS_worst(tab50, 7)

# plot the impact of the delta for a given prosumer
plot_prosumer_gain_delta(5)
plot_prosumer_gain_delta(7)

plt.show()