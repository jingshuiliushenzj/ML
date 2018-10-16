#!/usr/bin/env python  
# encoding: utf-8 
import pandas as pd
def loaddata():
    #显示所有列
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width',200)
    data=pd.read_csv('data/data.csv')
    print(data.describe(percentiles=None, include=None, exclude=None))


if __name__ == '__main__':
    loaddata()