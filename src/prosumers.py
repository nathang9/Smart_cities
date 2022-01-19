from scipy.optimize import minimize
import numpy as np

# main grid price
MAIN_GRID = [1,1,1,1]
MAIN_GRID_SELL = MAIN_GRID
MAIN_GRID_BUY = MAIN_GRID

def compute_operational_cost(x,  time,usage_cost,prod_cost):
    """
    compute the operational cost for a single prosumers

    :param x: variable that contains the detail of power variation [power_buy, power_sell, power_charge, power_discharge, power_prod]
    :param int time: time of the transaction
    :param float usage_cost: cost for using the battery
    :param float prod_cost: cost for producing energy by the prosumers
    :return: operational cost
    """

    power_buy, power_sell, power_charge, power_discharge, power_prod = x

    transaction_cost = MAIN_GRID_BUY[time] * power_buy - MAIN_GRID_SELL[time] * power_sell
    battery_cost = usage_cost * (power_charge + power_discharge)
    operational_cost = transaction_cost + battery_cost + prod_cost * power_prod
    return operational_cost

def constraint(x, power_needed = 100):
    power_buy, power_sell, power_charge, power_discharge, power_prod = x
    return power_needed - power_buy + power_sell - power_charge + power_discharge - power_prod

class prosumer:

    def __init__(self, id=None):
        self.id = id                # identifier of each prosumer
        self.consume = 0            # how much is consumed
        self.produce = 0            # how much is produced
        self.balance = 0            # balance between consumption and production
        self.isProducer = False     # role
        self.isConsumer = False     # role
        self.delta = 0              # requested price for energy
#        self.charge = 0             # battery current charge (in % ?)
#        self.max_charge = 0         # battery max charge

    def update(self, consume, produce):
        """
        Update a prosumer consumption and production

        :param float consume: how much is consumed
        :param float produce: how much is produced
        :return: None
        """
        self.consume = consume
        self.produce = produce
        self.compute_balance()

    def compute_balance(self):
        self.balance = self.produce - self.consume
        if self.balance > 0:
            self.isProducer = True
            self.isConsumer = False
        elif self.balance < 0:
            self.isProducer = False
            self.isConsumer = True
        else:
            self.isProducer = False
            self.isConsumer = False

    def compute_delta(self, total_consumption, total_production, param = 0):
        """
        comute delta for bargaining power and update delta of prosumer

        :param float total_consumption: The total consumption of all the prosumers
        :param float total_production: The total production of all the prosumers
        :param float param: parameter to make deltas converge
        :return: delta
        """
        if self.isProducer:
            ratio = self.balance / total_production
            delta_prod = min(ratio + 0.5, 1) / param
        elif self.isConsumer:
            ratio = self.balance / total_consumption
            delta_prod = 1 - min(max(ratio - 0.5, 0) * param, 1)
        print("ratio", ratio)
        self.delta = int(delta_prod*10)/10
        print("delta", self.delta)
        print("------------------------------------------")
        return int(delta_prod*10)/10

def create(tab):
    prosumers = []
    for i in range(len(tab[0][1])):
        name = "prosumer" + str(i)
        pro = Prosumer(name)
        pro.update(tab[0][1][1], tab[0][1][0])
        prosumers.append(pro)
    return prosumers

def update_ALL(tab, iter, prosumers):
    for i in range(len(tab[iter][1])):
        prosumers[i].update(tab[iter][1][1], tab[iter][1][0])

#################################################################################
# main grid price 0,1558 €/kWh # sell for 0,1873 €/kWh
# été : [hc, hc, hc, hc, hc, hc, hc, hm, hm, hm, hm, hp, hp, hp, hp, hp, hp, hm, hm, hc, hc, hc, hc, hc]
# hiver : [hc, hc, hc, hc, hc, hc, hc, hp, hp, hp, hp, hm, hm, hm, hm, hm, hm, hp, hp, hc, hc, hc, hc, hc]
# week-end : [hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc]
hc, hm, hp = 0.5 * 0.1558, 0.75 * 0.1558, 1.25 * 0.1558
MAIN_GRID = [hc, hc, hc, hc, hc, hc, hc, hm, hm, hm, hm, hp, hp, hp, hp, hp, hp, hm, hm, hc, hc, hc, hc, hc]
MAIN_GRID_SELL = [element * 0.9 for element in MAIN_GRID]
MAIN_GRID_BUY = [element * 1.1 for element in MAIN_GRID]

# price of using a solar pannel : 0.20 €/kWh --> ((4000 + (2000*(year/10)))/year)/1000 --> 0.2
# https://mypower.engie.fr/energie-solaire/conseils/cout-panneau-solaire.html

# price of using a battery between 0.12 €/kWh and 0.20 €/kWh
# https://selectra.info/energie/actualites/expert/batterie-domestique-autoconsommation


def compute_operational_cost(x,  time,usage_cost,prod_cost,main_grid_buy,main_grid_sell):
    """
    compute the operational cost for a single prosumers

    :param x: variable that contains the detail of power variation [power_buy, power_sell, power_charge, power_discharge, power_prod]
    :param int time: time of the transaction
    :param float usage_cost: cost for using the battery
    :param float prod_cost: cost for producing energy by the prosumers
    :return: an FLOAT operational cost
    """

    power_buy, power_sell, power_charge, power_discharge, power_prod = x

    if power_prod > power_buy:
        power_buy = 0
        power_sell = power_prod - power_buy
    elif power_prod > 0:
        power_buy -= power_prod
        power_sell = 0

    transaction_cost = main_grid_buy[time] * power_buy - main_grid_sell[time] * power_sell
    battery_cost = usage_cost * (power_charge + power_discharge)
    operational_cost = transaction_cost + battery_cost + prod_cost * power_prod
    return operational_cost

def constraint(x, power_needed = None):
    power_buy, power_sell, power_charge, power_discharge, power_prod = x
    if power_needed is None:
        power_needed = power_buy
    return power_needed - power_buy + power_sell - power_charge + power_discharge - power_prod

def constraint1(x):
    power_buy, power_sell, power_charge, power_discharge, power_prod = x
    return power_prod - power_sell

def worst_case(power_buy=0, power_sell=0, power_charge=0, power_discharge=0, power_produce=0, prices_power=(0,0), main_grid_buy=MAIN_GRID_BUY, main_grid_sell=MAIN_GRID_SELL, time=0):
    """
    Compute the worst price for a prosumers resulting an exchange with the main grid

    :param float power_buy: amount of power to buy
    :param float power_sell: amount of power to sell
    :param float power_charge: amount of power to charge in the battery
    :param float power_discharge: amount of power to discharge in the battery
    :param power_produce: price of using the battery and price of producing energy
    :param main_grid_buy: price of buying energy to the main grid
    :param main_grid_sell: price of selling energy to the main grid
    :param float time: time of the transaction
    :return: an FLOAT price of consumption (can be positive if it costs money or negative if prosumer gains money)
    """

    if power_sell == 0 and power_produce != 0:
        power_sell = power_produce

    # bounds for buy, sell, charge, discharge, produce
    bnds = [(power_buy, power_buy*100), (power_sell, power_produce), (0, power_charge), (0, power_discharge), (0, power_produce)]
    con = {'type': 'ineq', 'fun': constraint}
    con1 = {'type': 'ineq', 'fun': constraint1}
    cons = [con, con1]
    x0 = [power_buy, 0, power_charge, power_discharge, power_produce]
    mini = minimize(compute_operational_cost, x0, args=(time, prices_power[0], prices_power[1], main_grid_buy, main_grid_sell), bounds = bnds, constraints = cons)
    return mini.fun, mini.x

'''
# bounds for buy, sell, charge, discharge, produce
bnds = [(10,20), (0,50), (0,0), (0,0), (0,50)]
con = {'type': 'ineq', 'fun': constraint}
con1 = {'type': 'ineq', 'fun': constraint1}
cons = [con, con1]
#sol = minimize(objective, x0, method='SLSQP', bounds = bnds, constraints = cons)
x0 = [0,0,0,0,0]
for i in range(0,23):
    print(i)
    mini = minimize(compute_operational_cost, x0, args=(i,0.2,0.1,MAIN_GRID_BUY,MAIN_GRID_SELL), bounds = bnds, constraints = cons)
    print(mini.fun)
    print(mini.x)
'''

#print(worst_case())
