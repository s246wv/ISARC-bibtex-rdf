from sentence_transformers import SentenceTransformer, util
from rdflib import BNode, Graph, Namespace, URIRef, Literal
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
# embeddingはembeddingで分けた方が良いかしら．

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

key_sims = {}

for emb, word in zip(embs, words):
    dicts = {}
    for key in acm_ccs_embs:
        acm_emb = np.array(acm_ccs_embs[key][1], dtype=np.float32)
        cos_sim = util.cos_sim(acm_emb, emb)
        dic = {acm_ccs_embs[key][0]: cos_sim.item()}
        dicts.update(dic)
    key_sim = {word: dicts}
    key_sims.update(key_sim)

with open("./acs_ccs_key_all.json", "w") as f:
    json.dump(key_sims, f)

key_sims_sorted = {}
for key in key_sims:
    key_sim_sorted = sorted(key_sims[key].items(), key=lambda x:x[1], reverse=True)
    top5 = key_sim_sorted[0:5]
    top5_dic = dict(top5)
    dic = {key: top5_dic}
    key_sims_sorted.update(dic)

with open("./acs_ccs_key_top5.json", "w") as f:
    json.dump(key_sims_sorted, f)

## グラフつくる
out_graph = Graph()
out_graph = graph
bibtex_base = Namespace("http://www.edutella.org/bibtex#") # これ使いまわしよくないわね．


for key in key_sims_sorted:
    bib_ids = out_graph.subjects(predicate=URIRef("http://www.edutella.org/bibtex#keyword"), object=Literal(key))
    for bib_id in bib_ids:
        blank = BNode()
        out_graph.add((URIRef(bib_id), bibtex_base.acmKeywordSimilarity, blank))
        out_graph.add((blank, bibtex_base.keyword, Literal(key)))
        # topNはリストの方がよかったかしら？
        acm_key_top1 = ""
        acm_key_top2 = ""
        acm_key_top3 = ""
        acm_key_top4 = ""
        acm_key_top5 = ""
        for acm_key in acm_ccs_embs:
            if(acm_ccs_embs[acm_key][0] == list(key_sims_sorted[key].keys())[0]):
                acm_key_top1 = acm_key
            elif(acm_ccs_embs[acm_key][0] == list(key_sims_sorted[key].keys())[1]):
                acm_key_top2 = acm_key
            elif(acm_ccs_embs[acm_key][0] == list(key_sims_sorted[key].keys())[2]):
                acm_key_top3 = acm_key
            elif(acm_ccs_embs[acm_key][0] == list(key_sims_sorted[key].keys())[3]):
                acm_key_top4 = acm_key
            elif(acm_ccs_embs[acm_key][0] == list(key_sims_sorted[key].keys())[4]):
                acm_key_top5 = acm_key

        out_graph.add((blank, bibtex_base.top1, URIRef(acm_key_top1)))
        out_graph.add((blank, bibtex_base.top2, URIRef(acm_key_top2)))
        out_graph.add((blank, bibtex_base.top3, URIRef(acm_key_top3)))
        out_graph.add((blank, bibtex_base.top4, URIRef(acm_key_top4)))
        out_graph.add((blank, bibtex_base.top5, URIRef(acm_key_top5)))
        
out_graph.serialize(destination="./hoge.ttl", format="ttl")

