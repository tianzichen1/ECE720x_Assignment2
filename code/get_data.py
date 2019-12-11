from stackapi import StackAPI
import math
import pandas as pd

SITE = StackAPI('stackoverflow')
SITE.page_size = 100
SITE.max_pages= 500

questions = SITE.fetch('questions', tagged='javascript;php;jquery;html;ajax')

questions = str(questions)
with open('../data/questions.json', 'w') as f:
    f.write(questions)

with open('../data/questions.json', 'r') as f:
	questions = eval(f.read())['items']
qid = [q['question_id'] for q in questions]

times = math.ceil(len(qid) / 100.0)
ans = []
for i in range(times - 1):
	ans += SITE.fetch('/questions/{ids}/answers', ids=qid[i * 100: (i+1) * 100])['items']
ans += SITE.fetch('/questions/{ids}/answers', ids=qid[(i+1) * 100:])['items']
with open('../data/answers.json', 'w') as f:
	f.write(str(ans))

with open('../data/answers.json', 'r') as f:
	ans = eval(f.read())
aid = [a['answer_id'] for a in ans]
ids = qid + aid


times = math.ceil(len(ids) / 100.0)
posts = []
for i in range(times - 1):
	posts += SITE.fetch('/posts/{ids}', ids=ids[i * 100: (i+1) * 100])['items']
posts += SITE.fetch('/posts/{ids}', ids=ids[(i+1) * 100:])['items']
with open('../data/posts.json', 'w') as f:
	f.write(str(posts))

with open('../data/posts.json', 'r') as f:
	posts = eval(f.read())
df = pd.DataFrame(posts)
df[['owner']] = df[['owner']].astype(str)
df['owner'] = df['owner'].map(lambda x: x.replace('\t', ''))
df.to_csv("../data/allPosts.tsv", index=False, sep = '\t')

df = pd.DataFrame(posts)
df = df[['owner', 'post_type', 'post_id']]
df = df.dropna()
df['user_id'] = df['owner'].map(lambda x: x['user_id'])
df = df[['user_id', 'post_type', 'post_id']]
df.to_csv("../data/allPosts-metaData.tsv", index = False, sep = '\t')
