from stackapi import StackAPI
import pandas as pd

ranks = pd.read_csv('../data/RANKS.tsv', sep = '\t')
tops = list(map(int, ranks['userId']))

SITE = StackAPI('stackoverflow')
SITE.page_size = 50
SITE.max_pages= 1

reputations = SITE.fetch('/users/{ids}', ids = tops)
reputations = reputations['items']
reputation_val = []
for r in reputations:
    reputation_val.append([r['user_id'], r['reputation']])

reputation_val = sorted(reputation_val, key = lambda x: x[1], reverse = True)
repu_top10 = [reputation_val[i][0] for i in range(10)]

arn = ranks[ranks['Rank1ARN'] > 0]['userId'].values
aban = ranks[ranks['Rank2ABAN'] > 0]['userId'].values
cben = ranks[ranks['Rank3CBEN'] > 0]['userId'].values
vben = ranks[ranks['Rank4VBEN'] > 0]['userId'].values
vben2 = ranks[ranks['Rank5VBEN2'] > 0]['userId'].values

n1 = n2 = n3 = n4 = n5 = 0
for i in range(10):
    n1 += 1 if arn[i] in repu_top10 else 0
    n2 += 1 if aban[i] in repu_top10 else 0
    n3 += 1 if cben[i] in repu_top10 else 0
    n4 += 1 if vben[i] in repu_top10 else 0
    n5 += 1 if vben2[i] in repu_top10 else 0

print(n1, n2, n3, n4, n5)
    
