# -*- coding: utf-8 -*-
import os

from os import path
from wordcloud import WordCloud
import jieba

text = open('lagou.txt').read()

# seg_list = jieba.cut(text)

stopwords = []

with open('stopwords.txt',encoding='utf-8') as f:
    for l in f.readlines():
        # l = l.strip('\n').replace('/','').replace('，','').replace(',','').replace('.','').replace('、','').replace(';','').replace('；','').replace('。','').replace(':','').replace('：','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('10','').replace('0','')
        stopwords.append(l.strip('\n'))

with open('custom_stopwords.txt',encoding='utf-8') as f:
    for l in f.readlines():
        # l = l.strip('\n').replace('/','').replace('，','').replace(',','').replace('.','').replace('、','').replace(';','').replace('；','').replace('。','').replace(':','').replace('：','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('10','').replace('0','')
        stopwords.append(l.strip('\n'))

chtext = ''
with open('lagou.txt',encoding='utf-8') as f:
    for l in f.readlines():
        # l = l.strip('\n').replace('/','').replace('，','').replace(',','').replace('.','').replace('、','').replace(';','').replace('；','').replace('。','').replace(':','').replace('：','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','').replace('10','').replace('0','')
        chtext += ' '.join([word for word in jieba.cut(l) if word not in stopwords])

# Generate a word cloud image
# lower max_font_size
font = 'SimHei.ttf'
wordcloud = WordCloud(max_font_size=40,font_path=font).generate(chtext)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.figure()

wordcloud.to_file('lagou.jpg')


