import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime

def pretraitement( title):
    PV_data_path = os.path.join("data/household_data/", title)
    df = pd.read_csv(PV_data_path, index_col=0, parse_dates=True, sep=';')

    df.fillna(0, inplace=True)
    df.drop('cet_cest_timestamp', inplace=True)
    acteurs = ['residential1', 'residential2', 'residential3', 'residential4', 'residential5', 'residential6', 'public1', 'public2', 'industrial1', 'industrial2', 'industrial3'];
    production = ['*_pv_1','*_pv_2','*_pv']
    stockage = []

