#note: merge this with server.js so we have one time startup
import csv
import re
from typing import List, Dict
from collections import Counter
from math import log

from unidecode import unidecode

import pandas as pd
import numpy as np

data = pd.read_csv("movies.csv", encoding="ansi")
N = 596426 #number of movies - 1

def lcs(a, b):
    l = max(len(a), len(b))+1
    dp = [[0]*l for i in range(l)]
    for i in range(len(a)+1):
        for j in range(len(b)+1):
            if((not i) or (not j)):
                continue
            if(a[i-1] == b[j-1]):
                dp[i][j] = dp[i-1][j-1]+1
            else:
                dp[i][j] = max(dp[i][j-1], dp[i-1][j])
    return dp[len(a)][len(b)]

#precompute term frequencies to lower query time
#note that the precompute time is like 6 min
frequency_list = [] #list of dictionaries, each contains frequency of each word in desc O(NlogN)
for i in range(N):
    print(i)
    temp_list = re.split(r'\W+', unidecode(data["desc"][i]).lower())
    temp_dict = {}
    M = len(temp_list)
    for j in range(M):
        if temp_list[j] in temp_dict:
            continue
        cnt = 0
        for k in range(j, M):
            if temp_list[k] == temp_list[j]:
                cnt = cnt + 1
        temp_dict[temp_list[j]] = cnt
    frequency_list.append(temp_dict)

#debug
#print(frequency_list)

def find_relevant(terms):
    weight = []
    for i in range(N):
        weight.append(0)
    for term in terms: #number of terms is too small to count
        term_frequency = 0
        #O(NlogN)
        for temp_dict in frequency_list:
            if term in temp_dict:
                term_frequency = term_frequency + temp_dict[term]
        idf = log(N / (term_frequency + 1))
        #debug
        #print(idf, " ", term_frequency)
        for i in range(N): #iterate through movies
            movie_frequency = 0
            if term in frequency_list[i]:
                movie_frequency = frequency_list[i][term]
            #debug
            #print(movie_frequency)
            #print(idf)
            tf = log(1 + movie_frequency)
            #debug
            #print(tf)
            tf_idf = (tf * idf)
            weight[i] = weight[i] + tf_idf
            #debug
            #print(tf_idf)
    result = []
    for i in range(N):
        result.append((weight[i], i))
    result.sort(reverse=True)
    result = result[0:min(N, 10)]
    #sort top 10 with LCS
    lcs_values = []
    for x in result:
        lcs_values.append(lcs(terms, re.split(r'\W+', unidecode(data["desc"][x[1]]).lower())))
    for i in range(min(N, 10)):
        result[i] = (lcs_values[i], result[i][1])
    result = sorted(result, key=lambda x: x[0], reverse=True)
    return result

    #debug
    """
    for i in range(N):
        print(weight[i])
    """

#10 queries you can try
for i in range(10):
    x = input("Input: ")
    result = find_relevant(x.split(" "))
    for movie in result:
        print(data["name"][movie[1]])