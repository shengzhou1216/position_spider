# -*- coding: utf-8 -*-
import os

from os import path
from wordcloud import WordCloud

text = open('lagou.txt').read()

wordcloud = WordCloud().generate(text)

