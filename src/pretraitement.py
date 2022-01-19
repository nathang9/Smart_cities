import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import re


def pretraitement(title):
    pv_data_path = os.path.join("data/household_data/", title)
    df = pd.read_csv(pv_data_path, index_col=0, parse_dates=True, sep=';')
    df50 = dataframe_pourcent(df, 50)
    df60 = dataframe_pourcent(df, 60)
    df70 = dataframe_pourcent(df, 70)
    df75 = dataframe_pourcent(df, 75)

    df50.fillna(0, inplace=True)
    df60.fillna(0, inplace=True)
    df70.fillna(0, inplace=True)
    df75.fillna(0, inplace=True)

    df50 = create_df_correct(df50)
    df60 = create_df_correct(df60)
    df70 = create_df_correct(df70)
    df75 = create_df_correct(df75)

    tab50 = create_tab(df50)
    tab60 = create_tab(df60)
    tab70 = create_tab(df70)
    tab75 = create_tab(df75)

    return tab50, tab60, tab70, tab75


def dataframe_pourcent(df, prct):
    new_df = df.copy()
    for i in df.index:
        k = 0
        for j in list(df):
            if j != 'cet_cest_timestamp' and j != 'interpolated' and np.isnan(df[j][i]):
                k = k + 1
        kp = k * 100 / 68
        if kp > prct:
            new_df.drop([i], axis=0, inplace=True)
    return new_df


def create_df_correct(df):
    j = 0
    [d, h] = [0, 0]
    [p_r1, s_r1, c_r1, p_r2, s_r2, c_r2, p_r3, s_r3, c_r3, p_r4, s_r4, c_r4, p_r5, s_r5, c_r5, p_r6, s_r6, c_r6,
     p_i1, s_i1, c_i1, p_i2, s_i2, c_i2] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                            0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    for i in list(df):
        if i == 'cet_cest_timestamp':
            st = df[i][j]
            d = int(st[0:4] + st[5:7] + st[8:10])
            h = int(st[11:13])
        elif re.match(r'DE_KN_residential1\D*', i):
            [p_r1, s_r1, c_r1] = regex_valeurs(p_r1, s_r1, c_r1, df[i][j], i)
        elif re.match(r'DE_KN_residential2\D*', i):
            [p_r2, s_r2, c_r2] = regex_valeurs(p_r2, s_r2, c_r2, df[i][j], i)
        elif re.match(r'DE_KN_residential3\D*', i):
            [p_r3, s_r3, c_r3] = regex_valeurs(p_r3, s_r3, c_r3, df[i][j], i)
        elif re.match(r'DE_KN_residential4\D*', i):
            [p_r4, s_r4, c_r4] = regex_valeurs(p_r4, s_r4, c_r4, df[i][j], i)
        elif re.match(r'DE_KN_residential5\D*', i):
            [p_r5, s_r5, c_r5] = regex_valeurs(p_r5, s_r5, c_r5, df[i][j], i)
        elif re.match(r'DE_KN_residential6\D*', i):
            [p_r6, s_r6, c_r6] = regex_valeurs(p_r6, s_r6, c_r6, df[i][j], i)
        elif re.match(r'DE_KN_industrial1\D*', i):
            [p_i1, s_i1, c_i1] = regex_valeurs(p_i1, s_i1, c_i1, df[i][j], i)
        elif re.match(r'DE_KN_industrial2\D*', i):
            [p_i2, s_i2, c_i2] = regex_valeurs(p_i2, s_i2, c_i2, df[i][j], i)
    dico = {'date': [d], 'hour': [h], 'prod_r1': [p_r1], 'stock_r1': [s_r1], 'conso_r1': [c_r1],
            'prod_r2': [p_r2], 'stock_r2': [s_r2], 'conso_r2': [c_r2], 'prod_r3': [p_r3], 'stock_r3': [s_r3],
            'conso_r3': [c_r3], 'prod_r4': [p_r4], 'stock_r4': [s_r4], 'conso_r4': [c_r4], 'prod_r5': [p_r5],
            'stock_r5': [s_r5], 'conso_r5': [c_r5], 'prod_r6': [p_r6], 'stock_r6': [s_r6], 'conso_r6': [c_r6],
            'prod_i1': [p_i1], 'stock_i1': [s_i1], 'conso_i1': [c_i1], 'prod_i2': [p_i2], 'stock_i2': [s_i2],
            'conso_i2': [c_i2]}
    new_df = pd.DataFrame(dico)

    for j in range(1, 100):
        [d, h] = [0, 0]
        [p_r1, s_r1, c_r1, p_r2, s_r2, c_r2, p_r3, s_r3, c_r3, p_r4, s_r4, c_r4, p_r5, s_r5, c_r5, p_r6, s_r6, c_r6,
         p_i1, s_i1, c_i1, p_i2, s_i2, c_i2] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        for i in list(df):
            if i == 'cet_cest_timestamp':
                st = df[i][j]
                d = int(st[0:4] + st[5:7] + st[8:10])
                h = int(st[11:13])
            elif re.match(r'DE_KN_residential1\D*', i):
                [p_r1, s_r1, c_r1] = regex_valeurs(p_r1, s_r1, c_r1, df[i][j], i)
            elif re.match(r'DE_KN_residential2\D*', i):
                [p_r2, s_r2, c_r2] = regex_valeurs(p_r2, s_r2, c_r2, df[i][j], i)
            elif re.match(r'DE_KN_residential3\D*', i):
                [p_r3, s_r3, c_r3] = regex_valeurs(p_r3, s_r3, c_r3, df[i][j], i)
            elif re.match(r'DE_KN_residential4\D*', i):
                [p_r4, s_r4, c_r4] = regex_valeurs(p_r4, s_r4, c_r4, df[i][j], i)
            elif re.match(r'DE_KN_residential5\D*', i):
                [p_r5, s_r5, c_r5] = regex_valeurs(p_r5, s_r5, c_r5, df[i][j], i)
            elif re.match(r'DE_KN_residential6\D*', i):
                [p_r6, s_r6, c_r6] = regex_valeurs(p_r6, s_r6, c_r6, df[i][j], i)
            elif re.match(r'DE_KN_industrial1\D*', i):
                [p_i1, s_i1, c_i1] = regex_valeurs(p_i1, s_i1, c_i1, df[i][j], i)
            elif re.match(r'DE_KN_industrial2\D*', i):
                [p_i2, s_i2, c_i2] = regex_valeurs(p_i2, s_i2, c_i2, df[i][j], i)
        dico = {'date': [d], 'hour': [h], 'prod_r1': [p_r1], 'stock_r1': [s_r1], 'conso_r1': [c_r1],
                'prod_r2': [p_r2], 'stock_r2': [s_r2], 'conso_r2': [c_r2], 'prod_r3': [p_r3], 'stock_r3': [s_r3],
                'conso_r3': [c_r3], 'prod_r4': [p_r4], 'stock_r4': [s_r4], 'conso_r4': [c_r4], 'prod_r5': [p_r5],
                'stock_r5': [s_r5], 'conso_r5': [c_r5], 'prod_r6': [p_r6], 'stock_r6': [s_r6], 'conso_r6': [c_r6],
                'prod_i1': [p_i1], 'stock_i1': [s_i1], 'conso_i1': [c_i1], 'prod_i2': [p_i2], 'stock_i2': [s_i2],
                'conso_i2': [c_i2]}
        new_df = new_df.append(pd.DataFrame(dico), ignore_index=True)

    return new_df


def regex_valeurs(p, s, c, val, i):
    if re.match(r'[^ \t\n\r\f\v]*pv[^ \t\n\r\f\v]*', i):
        p = p + val
        print(i, " a de la production")
    elif re.match(r'[^ \t\n\r\f\v]*_storage[^ \t\n\r\f\v]*', i) or re.match(r'[^ \t\n\r\f\v]*_ev', i):
        s = s + val
        print(i, " a du stockage")
    elif not re.match(r'[^ \t\n\r\f\v]*_export[^ \t\n\r\f\v]*', i):
        c = c + val
        print(i, " a de la consommation")
    return (p, s, c)


def create_tab(df):
    tab = []
    for i in range (0, df.shape[0]):
        tab_hour = [ [df['prod_r1'][i], df['conso_r1'][i]],
                     [df['prod_r2'][i], df['conso_r2'][i]],
                     [df['prod_r3'][i], df['conso_r3'][i]],
                     [df['prod_r4'][i], df['conso_r4'][i]],
                     [df['prod_r5'][i], df['conso_r5'][i]],
                     [df['prod_r6'][i], df['conso_r6'][i]],
                     [df['prod_i1'][i], df['conso_i1'][i]],
                     [df['prod_i2'][i], df['conso_i2'][i]]]
        ligne = [df['hour'][i], tab_hour]
        tab.append(ligne)
    return tab
