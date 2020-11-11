#-*- coding: utf-8 -*-
import json
import os
from collections import Counter

import jieba
import pandas as pd
import matplotlib.pyplot as plt
#读取corpus文件夹下所有问题库，返回Q-A
from matplotlib.pyplot import MultipleLocator


def read_corpus():
    qlist= []
    alist= []
    corpus= []
    files = os.listdir('../corpus')
    #xinxicorpus = open('./corpus/xinxicorpus.txt',encoding='utf-8')
    for file in files:
        corpus.append(open('../corpus/'+file,encoding='utf-8'))
    for subcorpus in corpus:
        for line in subcorpus.readlines():
            s = json.loads(line)
            qlist.append(s['question'])
            alist.append(s['answer'])

    assert len(qlist) == len(alist)
    return qlist,alist

def picture(x,y):
    fig = plt.figure(num=1, figsize=(15, 8), dpi=80)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.legend(loc='upper left')
    y_major_locator = MultipleLocator(1)
    ax = plt.gca()
    ax.yaxis.set_major_locator(y_major_locator)
    plot1 = ax1.plot(x, y, marker='o', color='g', label='legend1')  # 点图：marker图标
    plot2 = ax1.plot(x, y, linestyle='--', alpha=0.5, color='r', label='legend2')
    plt.show()

if __name__ == '__main__':
    qlist, alist = read_corpus()
    qwords = pd.DataFrame({'comment': qlist})
    stop_list = []
    # 读取停用词数据
    stopwordsfile = open('../stopwordList/stopword.txt', encoding='gb18030', errors='ignore')
    for line in stopwordsfile.readlines():
        stop_list.append(line.rstrip("\n"))

    qwords['cut'] = qwords['comment'].apply(lambda x: [i for i in jieba.cut(x) if(i not in stop_list) and len(i.strip()) > 0 and (i.strip() not in stop_list)])

    words = []
    for content in qwords['cut']:
        words.extend(content)
    print(words)
    counter = Counter(words)
    x = list(counter.keys())
    y = list(counter.values())
    print(counter.keys())
    print(counter.values())