import pandas as pd
import time

with open('../data/questions.json', 'r') as f:
    questions = eval(f.read())['items']
questions = pd.DataFrame(questions)[['owner', 'question_id', 'score', 'creation_date']].dropna()
questions['owner'] = questions['owner'].map(lambda x: x.get('user_id'))
questions = questions.dropna().reset_index(drop=True)

current = time.time()
interval = [current - t1 for t1 in questions['creation_date']]
upvotebytime = [ questions['score'][i] * 3600 * 24 / (current - questions['creation_date'][i]) for i in range(len(questions))]
questions['q_upvotebytime'] = upvotebytime
questions = questions[['owner', 'question_id', 'q_upvotebytime']]


with open('../data/answers.json', 'r') as f:
    ans = eval(f.read())
ans = pd.DataFrame(ans)[['owner', 'question_id', 'score', 'creation_date']].dropna()
ans['owner'] = ans['owner'].map(lambda x: x.get('user_id'))
ans = ans.dropna().reset_index(drop=True)

interval = [current - t1 for t1 in ans['creation_date']]
upvotebytime = [ ans['score'][i] * 3600 * 24 / (current - ans['creation_date'][i]) for i in range(len(ans))]
ans['a_upvotebytime'] = upvotebytime
ans = ans[['owner', 'question_id', 'a_upvotebytime']]

questions.columns = ['asker', 'question_id', 'q_upvotebytime']
ans.columns = ['answerer', 'question_id', 'a_upvotebytime']

df = pd.merge(questions, ans, how = 'left',on='question_id')
df = df.dropna().reset_index(drop=True)


#ARN
arn = df[['asker', 'answerer']]
arn.columns = ['from', 'to']
arn = arn.drop_duplicates()
arn.to_csv('../data/1-ARN.tsv', index=False, sep = '\t')

#ABAN
best_ans = {}
for i, row in df.iterrows():
    if row['asker'] not in best_ans or row['a_upvotebytime'] > best_ans[row['asker']][1]:
        best_ans[row['asker']] = [row['answerer'], row['a_upvotebytime']]

aban = {'from': list(best_ans.keys()), 'to': [x[0] for x in best_ans.values()]}
aban = pd.DataFrame(aban)
aban.to_csv('../data/2-ABAN.tsv', index=False, sep = '\t')

#CBEN
qs = set(df['question_id'])
cben = {'from': [], 'to':[]}

for q in qs:
    rows = df[df['question_id'] == q]
    if len(rows) > 1:
        besta = rows[rows['a_upvotebytime'] == max(rows['a_upvotebytime'])]
        if besta['a_upvotebytime'].values[0] > 0:
            besta = besta['answerer'].values[0]
            
            for i, row in rows.iterrows():
                if row['answerer'] != besta:
                    cben['from'].append(row['answerer'])
                    cben['to'].append(besta)

                    
cben = pd.DataFrame(cben)
cben.to_csv('../data/3-CBEN.tsv', index=False, sep = '\t')

#VBEN, VBEN2
qs = set(df['question_id'])
vben = {'from': [], 'to':[], 'weight': []}
vben2 = {'from': [], 'to':[], 'weight': []}

for q in qs:
    rows = df[df['question_id'] == q]
    if len(rows) > 1:
        for i, row in rows.iterrows():
            bigger = rows[rows['a_upvotebytime'] > row['a_upvotebytime']]
            for j, r in bigger.iterrows():
                vben['from'].append(row['answerer'])
                vben['to'].append(r['answerer'])
                vben['weight'].append(r['a_upvotebytime'] - row['a_upvotebytime'])

                vben2['from'].append(row['answerer'])
                vben2['to'].append(r['answerer'])
                vben2['weight'].append(r['a_upvotebytime'] - row['a_upvotebytime'])
                
            if row['a_upvotebytime'] > row['q_upvotebytime']:
                vben2['from'].append(row['asker'])
                vben2['to'].append(r['answerer'])
                vben2['weight'].append(r['a_upvotebytime'] - row['q_upvotebytime'])
    
vben = pd.DataFrame(vben)
vben.to_csv('../data/4-VBEN.tsv', index=False, sep = '\t')

vben2 = pd.DataFrame(vben2)
vben2.to_csv('../data/5-VBEN2.tsv', index=False, sep = '\t')


#Pruning
import networkx as nx

def pruning(df, n):
    users = set()
    G = nx.Graph()
    G.add_edges_from(df.values[:, :2])
    components = list(nx.connected_components(G))
    for c in components:
        if len(c) > n:
            for u in c:
                users.add(u)

    df = df[(df['from'].isin(users)) | (df['to'].isin(users))].reset_index(drop=True)
    return df

arn = pruning(arn, 6)
aban = pruning(aban, 6)
cben = pruning(cben, 6)
vben = pruning(vben, 6)
vben2 = pruning(vben2, 6)

arn.to_csv('../data/1-ARN.tsv', index=False, sep = '\t')
aban.to_csv('../data/2-ABAN.tsv', index=False, sep = '\t')
cben.to_csv('../data/3-CBEN.tsv', index=False, sep = '\t')
vben.to_csv('../data/4-VBEN.tsv', index=False, sep = '\t')
vben2.to_csv('../data/5-VBEN2.tsv', index=False, sep = '\t')

