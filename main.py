#!/usr/bin/env python3
# coding: utf-8


# import
import os, logging
from logging import warning, info, debug
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib
sns.set()
# # filepath
# os.getcwd()
# s = [i for i in os.listdir("data/Eur/raw/") if "minimum" in i][0]
# # data
# data = pd.read_csv(f'data/Eur/raw/{s}', sep="\t", index_col=0)
# # first transfo
# data = data.T
# data.index = [  i.replace("S1", "-06-30").replace("S2", "-12-31").strip()
#                 for  i in data.index]
# data.index = [pd.Timestamp(i) for i in data.index]
# data = data.iloc[:-1, :]
# # sanity checks
# data.head()
# data.dtypes.head()
# data.iloc[0, 0]
# # type casting
# for col in data.columns :
#     try :
#         data[col] = data[col].astype(np.float32)
#     except TypeError :
#         data[col] = np.nan
#     except ValueError :
#         data[col] = np.nan
# # sanity checks
# data.dtypes.head()
# data.head()
# # got to csv
# data.to_csv(f"data/Eur/df/{s}")
#

# filepath
s = [i for i in os.listdir("data/Eur/raw/") if "empty" in i][0]
s
# data
data = pd.read_csv(f'data/Eur/raw/{s}', sep="\t", index_col=0)
# first transfo
data = data.T
data.index = [  i.replace("Q1", "-03-31").replace("Q2", "-06-30")\
                .replace("Q3", "-09-30").replace("Q4", "-12-31").strip()
                for i in data.index]
data.index = [pd.Timestamp(i) for i in data.index]
data = data.iloc[:-1, :]
# sanity checks
data.head()
data.dtypes.head()
data.iloc[0, 0]


cols = [ i for i in  data.columns if "fr" in i.lower()]
_data = data.loc[:, cols]
_data = _data.iloc[:-6, :]

for col in _data.columns :
    _data[col] = _data[col].apply(lambda i : i.replace("p", "").strip())
    try :
        _data[col] = _data[col].astype(np.float32)
    except :
        print(col)


_data

cols = [i for i in _data.columns if (_data[i].mean() > 50)]


#
# col = _data.columns[0]
# col
#
# _data[col].mean()

_data.plot()
