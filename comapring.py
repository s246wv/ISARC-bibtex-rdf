from sentence_transformers import SentenceTransformer, util
from rdflib import Graph
import json
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
graph = Graph()
graph.parse("./isarc/2022/isarc2022.bib.ttl")

# bibtexのkeywordsは配列．どうやってsimilarity計算するか？
# 出力rdfのスキーマを考えないといけなさそう．
# ID hoge:acmKeywordSimilarity [ bibtex:keyword "hogehoge";
#                                hoge:top1 acm:foobar;
#                                hoge:top2 acm:piyo
#                              ].
# こんなかんじ？

query = """
select ?id ?label where {
    ?id <http://www.edutella.org/bibtex#keyword> ?label. 
}
"""
qres = graph.query(query)
keys = []
words = []
for row in qres:
    keys.append(row.id)
    words.append(row.label)
embs = model.encode(words)
print(len(embs))

with open('acm_ccs_emb.json') as f:
    acm_ccs_embs = json.load(f)

# print(type(acm_ccs_embs['https://dl.acm.org/ccs/10011007.10010940.10010941.10010949.10010957.10011678'][1]))

for key in acm_ccs_embs:
    acm_emb = np.array(acm_ccs_embs[key][1], dtype=np.float32)
    for emb in embs:
        print(util.cos_sim(acm_emb, emb))