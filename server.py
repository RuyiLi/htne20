import csv
import re
from unidecode import unidecode
from typing import List, Dict
from math import log
from json import dumps
import pandas as pd
import numpy as np
import os
import pickle

# server imports
from bottle import get, post, run, request, static_file

data = pd.read_csv('books.csv', encoding="ISO-8859-1")
N = 16559  # number of books


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


# # collection of book numbers where the summary is too short for tf_idf
black_list = [False]*N

for i in range(N):
    temp_list = re.split(r'\W+', data["desc"][i].lower())
    if(len(temp_list) < 300):
        black_list[i] = True

# # precompute term frequencies to lower query time
# # note that the precompute time is like 4 min
# # list of dictionaries, each contains frequency of each word in desc O(NlogN)
# frequency_list = []
# for i in range(N):
#     if i % 100 == 0:
#         print(i)
#     temp_list = re.split(r'\W+', data["desc"][i].lower())
#     if(len(temp_list) < 300):
#         black_list[i] = True
#     temp_dict = {}
#     M = len(temp_list)
#     for j in range(M):
#         if temp_list[j] in temp_dict:
#             continue
#         cnt = 0
#         for k in range(j, M):
#             if temp_list[k] == temp_list[j]:
#                 cnt = cnt + 1
#         temp_dict[temp_list[j]] = cnt
#     frequency_list.append(temp_dict)

# # print(frequency_list[:10])
# with open('data', 'wb') as f:
#     pickle.dump(frequency_list, f)

# debug
# print(frequency_list)

f = open('data', 'rb')
frequency_list = pickle.load(f)
f.close()

print(frequency_list[:4])


def find_relevant(terms):
    weight = []
    for i in range(N):
        weight.append(-100000000)  # huge negative weight
    for term in terms:  # number of terms is too small to count
        term_frequency = 0
        # O(NlogN)
        for temp_dict in frequency_list:
            if term in temp_dict:
                term_frequency = term_frequency + temp_dict[term]
        idf = log(N / (term_frequency + 1))
        # debug
        #print(idf, " ", term_frequency)
        for i in range(N):  # iterate through books
            if black_list[i]:
                continue
            if weight[i] == -100000000:
                weight[i] = 0
            book_frequency = 0
            if term in frequency_list[i]:
                book_frequency = frequency_list[i][term]
            # debug
            # print(book_frequency)
            # print(idf)
            tf = log(1 + book_frequency)
            # debug
            # print(tf)
            tf_idf = (tf * idf)
            weight[i] = weight[i] + tf_idf
            # debug
            # print(tf_idf)
    result = []
    for i in range(N):
        result.append((weight[i], i))
    result.sort(reverse=True)
    result = result[0:min(N, 20)]
    # sort top 20 with LCS
    lcs_values = []
    for x in result:
        lcs_values.append(
            lcs(terms, re.split(r'\W+', unidecode(data["desc"][x[1]]).lower())))
    print(lcs_values)
    for i in range(min(N, 20)):
        result[i] = (lcs_values[i], result[i][1])
    result = sorted(result, key=lambda x: x[0], reverse=True)
    for i in range(min(N, 20)):
        result[i] = data["name"][result[i][1]]
    return result

    # debug
    """
    for i in range(N):
        print(weight[i])
    """
# server code

@post('/find')
def find():
    terms = request.body.read().decode('utf-8').split()
    reply = find_relevant(terms)
    return dumps(reply)

@get('/')
def index():
    return static_file('index.html', '.')


run(port=int(os.environ['PORT']), host='0.0.0.0')

"""
while True:
    x = input("Input: ").split(" ")
    print(find_relevant(x))
"""