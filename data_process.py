#encoding : utf-8
'''
@author: Nicolas
@project: QAonMilitaryKG
@file: data_process.py
@time: 2020/7/11 9:36
@desc:
'''
import csv
import json
import sys
import codecs
import numpy as np
import os
import pandas as pd


def trans(path):
    # jsonData = codecs.open(path + '.json', 'r', encoding='utf-8')
    # csvfile = open(path+'.csv', 'w') # 此处这样写会导致写出来的文件会有空行
    # csvfile = open(path+'.csv', 'wb') # python2下
    df1 = pd.read_csv(path+'.csv',encoding='utf-8',error_bad_lines=False)
    print(df1.head())
    df2 = df1[['_id']]
    x = 1
    # df.shape[0],df.shape[1],len(df) 行。列。行
    for x in range(df1.shape[0]):
        df2['_id'] = x

    print(df1.head(2))

def trans1():
    # basePath = os.path.dirname(os.path.abspath(__file__))
    # print('base:',basePath)
    # json_data = pd.read_json(basePath+'/new_data/military_data.json', lines=True)
    json_data = pd.read_json('new_data/data.json' ,lines=True)
    # print(json_data)
    print(json_data.head())
    # json_data.head()
    new_data = json_data[['_id', '名称', '产国', '大类', '类型']]
    leixing = json_data[['类型']]
    leixing = leixing.drop_duplicates(subset=['类型'],keep='first')
    x = 1
    for indexs in new_data.index:
        new_data.loc[indexs].values[0] = x
        x = x + 1
    #new_data['_id'] = lambda x,y:x+y
    new_data.to_csv('new_data/new_military_b.csv',index=False,encoding='utf-8')
    leixing.to_csv('new_data/leixing.csv',index=False,encoding='utf-8')

def trans2():
    new_data = pd.read_csv('new_data/new_military_b.csv', encoding='utf-8')
    # print(json_data)
    print(new_data.head())
    relation1 = new_data[['类型','产国','大类']]
    relation1 = relation1.drop_duplicates(subset=['类型'],keep='first')
    relation1['产国'] = 'SubclassOf'
    relation1.to_csv('new_data/relation1.csv',index=False,encoding='utf-8')

    relation2 = new_data[['名称', '产国', '类型']]
    # relation2 = relation2.drop_duplicates(subset=['类型'],keep='first')
    relation2['产国'] = 'InstanceOf'
    relation2.to_csv('new_data/relation2.csv', index=False, encoding='utf-8')

    leibie = new_data[['大类']]
    leibie = leibie.drop_duplicates(subset=['大类'],keep='first')
    leibie.to_csv('new_data/leibie.csv',index=False,encoding='utf-8')

def csv2json(path):
    _csv = []
    _json = []
    with open(path+'.csv', mode='r', encoding='utf-8')as csv_file_name:
        read_object = csv.reader(csv_file_name)  # 用csv模块自带的函数来完成读写操作
        with open("csv2json.json", mode='w', encoding='utf-8')as json_file_name:
            for i in read_object:
                _csv.append(i)
            key = _csv[0]
            for i in range(1, len(_csv)):
                _json_temp = []
                for j in zip(key, _csv[i]):
                    k = ":".join(j)
                    _json_temp.append(k)
                _json.append(_json_temp)
            json.dump(_json, json_file_name)

if __name__ == '__main__':
    #path = str(sys.argv[1])  # 获取path参数
    path = 'new_data/data'
    path1 = 'new_data/military_data'
    # print(path)
    # trans(path)
    # trans1()
    trans2()
    # csv2json(path)



    '''
    exp1: exception raised: 'gbk' codec can't encode character u'\xa0' in position 73: illegal multibyte sequence
方案1：
在对unicode字符编码时，添加ignore参数，忽略无法无法编码的字符，这样就可以正常编码为GBK了。
对应代码为：
print myUnWebItems.encode(“GBK“, ‘ignore’);
方案2：
或者，将其转换为GBK编码的超集GB18030 （即，GBK是GB18030的子集）：
print myUnWebItems.encode(“GB18030“);
对应的得到的字符是GB18030的编码。


    '''