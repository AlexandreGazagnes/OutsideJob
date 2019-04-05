#!/usr/bin/env python3
# coding: utf-8


# import
import os, logging
from logging import warning, info, debug
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# plot
%matplotlib
sns.set()


# min revenue
#####################

# data
s = [i for i in os.listdir("data/Eur/raw/") if "minimum" in i][0]
df = pd.read_csv(f'data/Eur/raw/{s}', sep="\t", index_col=0)
# first transfo
df = df.T
df.index = [  i.replace("S1", "-06-30").replace("S2", "-12-31").strip()
                for  i in df.index]
df.index = [pd.Timestamp(i) for i in df.index]
df = df.iloc[:-1, :]
for col in df.columns : # type casting
    try : df[col] = df[col].astype(np.float32)
    except TypeError : df[col] = np.nan
    except ValueError : df[col] = np.nan
# df.to_csv(f"data/Eur/df/{s}") # go to csv
# just selec Fr revenues
cols = [i for i in df.columns if ("eur" in i.lower() and "fr" in i.lower())]
min_revenue = df.loc[:, cols]


# house prices
#####################

# data
s = [i for i in os.listdir("data/Eur/raw/") if "empty" in i][0]
df = pd.read_csv(f'data/Eur/raw/{s}', sep="\t", index_col=0)
# first transfo
df = df.T
df.index = [  i.replace("Q1", "-03-31").replace("Q2", "-06-30")\
                .replace("Q3", "-09-30").replace("Q4", "-12-31").strip()
                for i in df.index]
df.index = [pd.Timestamp(i) for i in df.index]
df = df.iloc[:-1, :]
# select fr only
cols = [ i for i in  df.columns if "fr" in i.lower()]
_df = df.loc[:, cols].iloc[:-8, :]
# cast
_df = _df.apply(lambda i : i.apply(lambda j : j.replace("p", "").strip()), axis=1)
for col in _df.columns :
    try : _df[col] = _df[col].astype(np.float32)
    except : print(col)
# select indice not % of var
cols = [i for i in _df.columns if (_df[i].mean() > 50)]
cols = [i for i in cols if (("total" in i.lower()) and ("fr" in i.lower()))]
house_prices = _df.loc[:, cols]
house_prices


# mix
#####################

min_revenue["date"] = min_revenue.index
house_prices["date"] = house_prices.index
data = pd.merge(house_prices, min_revenue, on="date")
data.head(7)
data.set_index("date", drop=True, inplace=True)
data.columns = ["house_prices", "min_revenue"]
data["house_prices"] = data["house_prices"] * 100 / data["house_prices"].iloc[5]
data["min_revenue"] = data["min_revenue"] * 100 / data["min_revenue"].iloc[5]
data.head()
# data["indice"] = data.iloc[:, 0] /data.iloc[:, 1]
data.plot()
