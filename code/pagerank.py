import numpy as np
import pandas as pd

def top10(df):
    nodes = []

    for i, row in df.iterrows():
        if row['from'] not in nodes:
            nodes.append(row['from'])
        if row['to'] not in nodes:
            nodes.append(row['to'])

    node2num = {}
    for i in range(len(nodes)):
        node2num[nodes[i]] = i

    mat = [[0] * len(nodes) for _ in nodes]
    for i, row in df.iterrows():
        mat[node2num[row['from']]][node2num[row['to']]] = 1
        
    scores = pagerank(np.array(mat))
    scores = list(scores)
    for i in range(len(scores)):
        scores[i] = [nodes[i], scores[i]]
    tops = sorted(scores, key = lambda x: x[1], reverse=True)[:10]
    res = {}
    for i in range(10):
        res[tops[i][0]] = i + 1
    
    return res


def pagerank(S):
    N = len(S)

    for j in range(N):
        sum_of_col = sum(S[:,j])
        for i in range(N):
            if sum_of_col == 0:
                S[i, j] = 0
            else:
                S[i, j] /= sum_of_col

    alpha = 0.85
    A = alpha*S + (1-alpha) / N * np.ones([N, N])

    P_n = np.ones(N) / N
    P_n1 = np.zeros(N)

    e = 100000
    k = 0

    while e > 0.00000001:
        P_n1 = np.dot(A, P_n)
        e = P_n1-P_n
        e = max(map(abs, e))
        P_n = P_n1
        k += 1
    
    return P_n

arn = pd.read_csv('../data/1-ARN.tsv', sep = '\t')
aban = pd.read_csv('../data/2-ABAN.tsv', sep = '\t')
cben = pd.read_csv('../data/3-CBEN.tsv', sep = '\t')
vben = pd.read_csv('../data/4-VBEN.tsv', sep = '\t')
vben2 = pd.read_csv('../data/5-VBEN2.tsv', sep = '\t')


tarn = top10(arn)
taban = top10(aban)
tcben = top10(cben)
tvben = top10(vben)
tvben2 = top10(vben2)

tops = set(list(tarn.keys()) + list(taban.keys()) + list(tcben.keys()) + list(tvben.keys()) + list(tvben2.keys()))

ranks = {'userId':[], 'displayName': [], 'ProfileLink': [], 'Rank1ARN': [],
         'Rank2ABAN':[], 'Rank3CBEN':[], 'Rank4VBEN':[], 'Rank5VBEN2': []}

with open('../data/questions.json', 'r') as f:
    uq = eval(f.read())['items']

for i in range(len(uq)):
    uq[i] = uq[i]['owner']

with open('../data/answers.json', 'r') as f:
    ua = eval(f.read())
for i in range(len(ua)):
    ua[i] = ua[i]['owner']

us = ua + uq

for d in tops:
    ranks['userId'].append(int(d))
    for u in us:
        if 'user_id' in u and u['user_id'] == int(d):
            ranks['displayName'].append(u['display_name'])
            ranks['ProfileLink'].append(u['link'])
            break

    ranks['Rank1ARN'].append(tarn[d] if d in tarn else 0)
    ranks['Rank2ABAN'].append(taban[d] if d in taban else 0)
    ranks['Rank3CBEN'].append(tcben[d] if d in tcben else 0)
    ranks['Rank4VBEN'].append(tvben[d] if d in tvben else 0)
    ranks['Rank5VBEN2'].append(tvben2[d] if d in tvben2 else 0)

ranks = pd.DataFrame(ranks)
ranks.to_csv('../data/RANKS.tsv', index=False, sep = '\t')