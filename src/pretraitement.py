import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import re

def pretraitement( title):
    PV_data_path = os.path.join("data/household_data/", title)
    df = pd.read_csv(PV_data_path, index_col=0, parse_dates=True, sep=';')

    df.fillna(0, inplace=True)
    acteurs = ['residential1', 'residential2', 'residential3', 'residential4', 'residential5', 'residential6', 'public1', 'public2', 'industrial1', 'industrial2', 'industrial3'];
    production = ['*_pv_1','*_pv_2','*_pv']
    stockage = ['*_storage_charge', '*_storage_decharge', '*_ev']

    dico = { 'date': [20141211] , 'hour': [18] , 'prod_r1': [0.0], 'stock_r1': [0.0],'conso_r1': [0.0], 'prod_r2': [0.0], 'stock_r2': [0.0],'conso_r2': [0.0], 'prod_r3': [0.002], 'stock_r3': [0.0],'conso_r3': [0.0], 'prod_r4': [0.0], 'stock_r4': [0.0],'conso_r4': [0.0], 'prod_r5': [0.0], 'stock_r5': [0.0],'conso_r5': [0.0], 'prod_r6': [0.0], 'stock_r6': [0.0],'conso_r6': [0.0], 'prod_i1': [0.0], 'stock_i1': [0.0],'conso_i1': [0.0], 'prod_i2': [0.0], 'stock_i2': [0.0],'conso_i2': [0.0] }
    new_df = pd.DataFrame(dico)

    for i in range(1, df.shape[0]):
        [d,h] = [0,0];
        [p_r1,s_r1,c_r1, p_r2,s_r2,c_r2, p_r3,s_r3,c_r3, p_r4,s_r4,c_r4, p_r5,s_r5,c_r5, p_r6,s_r6,c_r6, p_i1,s_i1,c_i1, p_i2,s_i2,c_i2]=[0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,0.0, 0.0,0.0,0.0];

        for j in list(df):
            if j == 'cet_cest_timestamp' :
                string = df[i][j];
                d = int(string[0:3] + string[5:6] + string[8:9]);
                h = int(string[11:12])
            elif df[i][j].match(re.compile('DE_KN_residential1\D*')) :
                if df[i][j].match(re.compile('\D*_pv\S*')) :
                    p_r1 = p_r1 + df[i][j]
                elif df[i][j].match(re.compile('\D*_storage\D*')) or df[i][j].match(re.compile('\D*_ev')) :
                    s_r1 = s_r1 + df[i][j]
                else :
                    c_r1 = c_r1 + df[i][j]
            elif df[i][j].match(re.compile('DE_KN_residential2\D*')) :
                if df[i][j].match(re.compile('\D*_pv\S*')) :
                    p_r2 = p_r2 + df[i][j]
                elif df[i][j].match(re.compile('\D*_storage\D*')) or df[i][j].match(re.compile('\D*_ev')) :
                    s_r2 = s_r2 + df[i][j]
                else :
                    c_r2 = c_r2 + df[i][j]
            elif df[i][j].match(re.compile('DE_KN_residential3\D*')) :
                if df[i][j].match(re.compile('\D*_pv\S*')) :
                    p_r3 = p_r3 + df[i][j]
                elif df[i][j].match(re.compile('\D*_storage\D*')) or df[i][j].match(re.compile('\D*_ev')) :
                    s_r3 = s_r3 + df[i][j]
                else :
                    c_r3 = c_r3 + df[i][j]
            elif df[i][j].match(re.compile('DE_KN_residential4\D*')) :
                if df[i][j].match(re.compile('\D*_pv\S*')) :
                    p_r4 = p_r4 + df[i][j]
                elif df[i][j].match(re.compile('\D*_storage\D*')) or df[i][j].match(re.compile('\D*_ev')) :
                    s_r4 = s_r4 + df[i][j]
                else :
                    c_r4 = c_r4 + df[i][j]
            elif df[i][j].match(re.compile('DE_KN_residential5\D*')) :
                if df[i][j].match(re.compile('\D*_pv\S*')) :
                    p_r5 = p_r5 + df[i][j]
                elif df[i][j].match(re.compile('\D*_storage\D*')) or df[i][j].match(re.compile('\D*_ev')) :
                    s_r5 = s_r5 + df[i][j]
                else :
                    c_r5 = c_r5 + df[i][j]
            elif df[i][j].match(re.compile('DE_KN_residential4\D*')) :
                if df[i][j].match(re.compile('\D*_pv\S*')) :
                    p_r6 = p_r6 + df[i][j]
                elif df[i][j].match(re.compile('\D*_storage\D*')) or df[i][j].match(re.compile('\D*_ev')) :
                    s_r6 = s_r6 + df[i][j]
                else :
                    c_r6 = c_r6 + df[i][j]
            elif df[i][j].match(re.compile('DE_KN_industrial1\D*')) :
                if df[i][j].match(re.compile('\D*_pv\S*')) :
                    p_i1 = p_i1 + df[i][j]
                elif df[i][j].match(re.compile('\D*_storage\D*')) or df[i][j].match(re.compile('\D*_ev')) :
                    s_i1 = s_i1 + df[i][j]
                else :
                    c_i1 = c_i1 + df[i][j]
            elif df[i][j].match(re.compile('DE_KN_industrial2\D*')) :
                if df[i][j].match(re.compile('\D*_pv\S*')) :
                    p_i2 = p_i2 + df[i][j]
                elif df[i][j].match(re.compile('\D*_storage\D*')) or df[i][j].match(re.compile('\D*_ev')) :
                    s_i2 = s_i2 + df[i][j]
                else :
                    c_i2 = c_i2 + df[i][j]
        dico = {'date': [d], 'hour': [h], 'prod_r1': [p_r1], 'stock_r1': [s_r1], 'conso_r1': [c_r1],
                'prod_r2': [p_r2], 'stock_r2': [s_r2], 'conso_r2': [c_r2], 'prod_r3': [p_r3], 'stock_r3': [s_r3],
                'conso_r3': [c_r3], 'prod_r4': [p_r4], 'stock_r4': [s_r4], 'conso_r4': [c_r4], 'prod_r5': [p_r5],
                'stock_r5': [s_r5], 'conso_r5': [c_r5], 'prod_r6': [p_r6], 'stock_r6': [s_r6], 'conso_r6': [c_r6],
                'prod_i1': [p_i1], 'stock_i1': [s_i1], 'conso_i1': [c_i1], 'prod_i2': [p_i2], 'stock_i2': [s_i2],
                'conso_i2': [c_i2]}
        new_df.append(np.DataFrame(dico), ignore_index = True)