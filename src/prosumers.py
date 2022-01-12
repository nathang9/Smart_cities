from scipy.optimize import minimize
import numpy as np

class Prosumer:


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



    '''
    def requested_price(self, total_consumption, total_production, time, usage_cost, prod_cost):
        """
        compute and return the requested price to sell/buy

        :param float total_consumption: The total consumption of all the prosumers
        :param float total_production: The total production of all the prosumers
        :param int time: The time for the transaction
        :param float usage_cost: cost for using the battery
        :param float prod_cost: cost for producing energy by the prosumers
        :return: requested price
        """

        min = minimize(compute_operational_cost, [0,0,0,0,0], args=(time,usage_cost,prod_cost))
        operational_cost = min.fun
        power_buy, power_sell, power_charge, power_discharge, power_prod = min.x


        bargaining_power = 0
        ratio = 0.5
        if self.isProducer:
            ratio = self.balance / total_production
            delta = min(ratio+0.5, 1)
        elif self.isConsumer:
            ratio = self.balance / total_consumption
            delta = max(ratio-0.5, 0)

        return delta
    '''

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
            delta_prod = min(ratio + 0.5, 1) / (param+1)
        elif self.isConsumer:
            ratio = -self.balance / total_consumption
            delta_prod = 1 - min(max(ratio - 0.5, 0) * param, 1)
        print("ratio", ratio)
        self.delta = int(delta_prod*10)/10
        print("delta", self.delta)
        print("------------------------------------------")
        return int(delta_prod*10)/10


################################################################################"
# main grid price 0,1558 €/kWh
# été : [hc, hc, hc, hc, hc, hc, hc, hm, hm, hm, hm, hp, hp, hp, hp, hp, hp, hm, hm, hc, hc, hc, hc, hc]
# hiver : [hc, hc, hc, hc, hc, hc, hc, hp, hp, hp, hp, hm, hm, hm, hm, hm, hm, hp, hp, hc, hc, hc, hc, hc]
# week-end : [hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc, hc]
hc, hm, hp = 0.5 * 0.1558, 0.75 * 0.1558, 1.25 * 0.1558
MAIN_GRID = [hc, hc, hc, hc, hc, hc, hc, hm, hm, hm, hm, hp, hp, hp, hp, hp, hp, hm, hm, hc, hc, hc, hc, hc]
MAIN_GRID_SELL = [element * 0.9 for element in MAIN_GRID]
MAIN_GRID_BUY = [element * 1.1 for element in MAIN_GRID]


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
    battery_cost = 0 #usage_cost * (power_charge + power_discharge)
    operational_cost = transaction_cost + battery_cost + prod_cost * power_prod
    return operational_cost

def constraint(x, power_needed = 100):
    power_buy, power_sell, power_charge, power_discharge, power_prod = x
    return power_needed - power_buy + power_sell - power_charge + power_discharge - power_prod

def constraint1(x):
    power_buy, power_sell, power_charge, power_discharge, power_prod = x
    return power_prod - power_sell


'''
# bounds for buy, sell, charge, discharge, produce
bnds = [(100,200), (0,50), (0,100), (0,100), (0,50)]
con = {'type': 'ineq', 'fun': constraint}
con1 = {'type': 'ineq', 'fun': constraint1}
cons = [con, con1]
#sol = minimize(objective, x0, method='SLSQP', bounds = bnds, constraints = cons)
x0 = [0,0,0,0,0]
for i in range(0,23):
    print(i)
    mini = minimize(compute_operational_cost, x0, args=(i,0.2,0.1), bounds = bnds, constraints = cons)
    print(mini.fun)
    print(mini.x)
'''
