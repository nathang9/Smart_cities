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

    dico = {'date': [20141211], 'hour': [18], 'prod_r1': [0.0], 'stock_r1': [0.0], 'conso_r1': [0.0], 'prod_r2': [0.0],
            'stock_r2': [0.0], 'conso_r2': [0.0], 'prod_r3': [0.002], 'stock_r3': [0.0], 'conso_r3': [0.0],
            'prod_r4': [0.0], 'stock_r4': [0.0], 'conso_r4': [0.0], 'prod_r5': [0.0], 'stock_r5': [0.0],
            'conso_r5': [0.0], 'prod_r6': [0.0], 'stock_r6': [0.0], 'conso_r6': [0.0], 'prod_i1': [0.0],
            'stock_i1': [0.0], 'conso_i1': [0.0], 'prod_i2': [0.0], 'stock_i2': [0.0], 'conso_i2': [0.0]}
    new_df = pd.DataFrame(dico)

    for j in range(1, 100):
        [d, h] = [0, 0];
        [p_r1, s_r1, c_r1, p_r2, s_r2, c_r2, p_r3, s_r3, c_r3, p_r4, s_r4, c_r4, p_r5, s_r5, c_r5, p_r6, s_r6, c_r6,
         p_i1, s_i1, c_i1, p_i2, s_i2, c_i2] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];

        for i in list(df):
            if i == 'cet_cest_timestamp':
                st = df[i][j];
                d = int(st[0:4] + st[5:7] + st[8:10]);
                h = int(st[11:13])
            elif re.match(r'DE_KN_residential1\D*', i):
                if re.match(r'\D*_pv\S*', i):
                    p_r1 = p_r1 + df[i][j]
                elif re.match(r'\D*_storage\D*', i) or re.match(r'\D*_ev', i):
                    s_r1 = s_r1 + df[i][j]
                else:
                    c_r1 = c_r1 + df[i][j]
            elif re.match(r'DE_KN_residential2\D*', i):
                if re.match(r'\D*_pv\S*', i):
                    p_r2 = p_r2 + df[i][j]
                elif re.match(r'\D*_storage\D*', i) or re.match(r'\D*_ev', i):
                    s_r2 = s_r2 + df[i][j]
                else:
                    c_r2 = c_r2 + df[i][j]
            elif re.match(r'DE_KN_residential3\D*', i):
                if re.match(r'\D*_pv\S*', i):
                    p_r3 = p_r3 + df[i][j]
                elif re.match(r'\D*_storage\D*', i) or re.match(r'\D*_ev', i):
                    s_r3 = s_r3 + df[i][j]
                else:
                    c_r3 = c_r3 + df[i][j]
            elif re.match(r'DE_KN_residential4\D*', i):
                if re.match(r'\D*_pv\S*', i):
                    p_r4 = p_r4 + df[i][j]
                elif re.match(r'\D*_storage\D*', i) or re.match(r'\D*_ev', i):
                    s_r4 = s_r4 + df[i][j]
                else:
                    c_r4 = c_r4 + df[i][j]
            elif re.match(r'DE_KN_residential5\D*', i):
                if re.match(r'\D*_pv\S*', i):
                    p_r5 = p_r5 + df[i][j]
                elif re.match(r'\D*_storage\D*', i) or re.match(r'\D*_ev', i):
                    s_r5 = s_r5 + df[i][j]
                else:
                    c_r5 = c_r5 + df[i][j]
            elif re.match(r'DE_KN_residential6\D*', i):
                if re.match(r'\D*_pv\S*', i):
                    p_r6 = p_r6 + df[i][j]
                elif re.match(r'\D*_storage\D*', i) or re.match(r'\D*_ev', i):
                    s_r6 = s_r6 + df[i][j]
                else:
                    c_r6 = c_r6 + df[i][j]
            elif re.match(r'DE_KN_industrial1\D*', i):
                if re.match(r'\D*_pv\S*', i):
                    p_i1 = p_i1 + df[i][j]
                elif re.match(r'\D*_storage\D*', i) or re.match(r'\D*_ev', i):
                    s_i1 = s_i1 + df[i][j]
                else:
                    c_i1 = c_i1 + df[i][j]
            elif re.match(r'DE_KN_industrial2\D*', i):
                if re.match(r'\D*_pv\S*', i):
                    p_i2 = p_i2 + df[i][j]
                elif re.match(r'\D*_storage\D*', i) or re.match(r'\D*_ev', i):
                    s_i2 = s_i2 + df[i][j]
                else:
                    c_i2 = c_i2 + df[i][j]
        dico = {'date': [d], 'hour': [h], 'prod_r1': [p_r1], 'stock_r1': [s_r1], 'conso_r1': [c_r1],
                'prod_r2': [p_r2], 'stock_r2': [s_r2], 'conso_r2': [c_r2], 'prod_r3': [p_r3], 'stock_r3': [s_r3],
                'conso_r3': [c_r3], 'prod_r4': [p_r4], 'stock_r4': [s_r4], 'conso_r4': [c_r4], 'prod_r5': [p_r5],
                'stock_r5': [s_r5], 'conso_r5': [c_r5], 'prod_r6': [p_r6], 'stock_r6': [s_r6], 'conso_r6': [c_r6],
                'prod_i1': [p_i1], 'stock_i1': [s_i1], 'conso_i1': [c_i1], 'prod_i2': [p_i2], 'stock_i2': [s_i2],
                'conso_i2': [c_i2]}
        new_df = new_df.append(pd.DataFrame(dico), ignore_index=True)