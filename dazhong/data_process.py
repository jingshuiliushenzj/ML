#!/usr/bin/env python  
# encoding: utf-8 
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
import jieba
import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(current_dir)
sys.path.append("..")
import smote 
import numpy as np
def getLabel(score): 
    if score > 3: 
        return 1 
    elif score < 3:
        return 0 
    else: 
        return None 

#从csv中加载数据  
def loaddata():
    #显示所有列
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width',200)
    data=pd.read_csv('data/data.csv')
    return data

#产生标签值
def createLabel(data):
    data['target'] = data['stars'].map(lambda x:getLabel(x))
    dataSelect=data[['cus_comment','target']]#选择评论列和类别列。 
    return dataSelect.dropna()#删除掉中评的数据

#数据预处理
def preprocess(data):
    data=createLabel(data)
    return data


#载入停用词
def load_stopwords():
    stop_file=open("data/stopwords.txt", encoding='utf-8')
    stopwords_list=stop_file.readlines()
    stopwords=[x.strip() for x in stopwords_list]
    return stopwords

#结巴分词
def fenci(data):
    data=data.apply(lambda x:' '.join(jieba.cut(x)))
    return data

#文本特征提取   
def feature_extraction(data,stopwords):
    #TF-IDF构建文本向量    sklearn库中可以指定stopwords
    tf = TfidfVectorizer(stop_words=stopwords, max_features=3000)
    tf.fit(data)
    return tf

#模型训练--贝叶斯分类器
def train_model(x_train,y_train,x_test,y_test):
    classifier=MultinomialNB()
    classifier.fit(x_train,y_train)
    #print(classifier.score(x_test,y_test))
    return classifier #返回模型

#预测
def predict(model,comment,tf):
    return model.predict_proba(tf.transform(fenci((comment))))# 返回预测属于某标签的概率
    
if __name__ == '__main__':
    data=loaddata()
    data=preprocess(data)
    x_train,x_test,y_train,y_test=train_test_split(data['cus_comment'],data['target'],random_state=3,test_size=0.25)
    
    stopwords=load_stopwords()
    x_train_fenci=fenci(x_train)
    tf=feature_extraction(x_train_fenci, stopwords)
    
    x_train_tf=tf.transform(x_train_fenci).toarray()
    samples0=[]
    for i, label in enumerate(y_train):
        if label==0:
            samples0.append(x_train_tf[i])
    s=smote.Smote(np.array(samples0),N=100)
    over_samplings_x=s.over_sampling()
    total_samplings_x=np.row_stack((x_train_tf,over_samplings_x))
    total_samplings_y=np.row_stack((y_train,np.zeros((len(over_samplings_x),1))))
    print(total_samplings_x.shape)
    print(total_samplings_y.shape)
#     model=train_model(x_train_tf, y_train,tf.transform(fenci(x_test)),y_test)
#     y_predict=model.predict(tf.transform(fenci((x_test))))
#     comment1="一如既往的好。已经快成了陆家嘴上班的我的食堂了。满减活动非常给力，上次叫了八样东西，折扣下来居然就六十左右，吃得好爽好爽。南瓜吃过几次，就一次不够酥烂，其他几次都很好。烤麸非常入味，适合上海人。鱼香肉丝有点辣，下饭刚好。那个蔬菜每次都点。总体很好吃。"
#     comment2="糯米外皮不绵滑，豆沙馅粗躁，没有香甜味。12元一碗不值。"
#     print(predict(model,pd.Series([comment1]) , tf))
#     print(predict(model,pd.Series([comment2]), tf))