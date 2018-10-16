#!/usr/bin/env python  
# encoding: utf-8 
import pandas as pd
def getLabel(score): 
    if score > 3: 
        return 1 
    elif score < 3:
        return 0 
    else: 
        return None 
    
def loaddata():
    #显示所有列
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width',200)
    data=pd.read_csv('data/data.csv')
    return data
def createLabel(data):
    data['target'] = data['stars'].map(lambda x:getLabel(x))
    return data.dropna()
def preprocess(data):
    data=createLabel(data)
    return data
if __name__ == '__main__':
    data=loaddata()
    data=preprocess(data)
    print(data.info())