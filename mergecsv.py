__author__ = 'Sasa2905'

import pandas as pd
import sys
import csv

csv.field_size_limit(1000000)

withinscope = pd.read_csv("outputfile.csv", engine ="python")
withinscope['value_out'] = ""
outscope = pd.read_csv("outputfile2.csv", engine ="python")
for index,row in outscope.iterrows():
    key = row[0]
    value = row[1]
    samerow = withinscope.loc[withinscope["key"] == key].index
    if len(samerow) is 0:
        withinscope.loc[len(withinscope)] = [key,0,value]
    else:
        withinscope.loc[samerow,'value_out'] = value
withinscope.to_csv("mergedwithin.csv")