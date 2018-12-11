#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 10:01:25 2018

@author: echerif
"""


import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
# Create a dataset (fake)
data = pd.read_table('all-phoenix-dattier-LG15-17-m5-DP10-P95.geno.distrib.txt', delimiter="\t")
#df=pd.DataFrame(data[['POS','G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G1_Total','G1_Total','G2_Total','G3_Total','G4_Total','G5_Total','G6_Total','G7_Total','G8_Total','G9_Total','G10_Total']])

df=pd.DataFrame(data[['POS','G1_Total','G2_Total','G3_Total','G4_Total','G5_Total','G6_Total','G7_Total','G8_Total','G9_Total','GG_Total']])
#print(df.columns)
#exit()
#print(df)
#df = pd.DataFrame(np.random.random((5,5)), columns=["a","b","c","d","e"])
 
# Default heatmap: just a visualization of this square matrix
df = df.pivot_table(index=data[['POS']],
                        values=data[['G1_Total','G2_Total','G3_Total','G4_Total','G5_Total','G6_Total','G7_Total','G8_Total','G9_Total','GG_Total']])
#                        columns=data[['G1','G2','G3','G4','G5','G6','G7','G8','G9','G10']])
#print(data)
#exit()
p1 = sns.heatmap(df,vmin=0,cmap="RdBu_r")
sns.palplot(sns.diverging_palette(220, 20, n=7))
plt.show()
#print()