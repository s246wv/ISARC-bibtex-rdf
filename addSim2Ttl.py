from rdflib import BNode, Graph, Namespace, URIRef, Literal
import json
import sys

# 第一引数が元となるttlファイル
input_ttl = sys.argv[1]
# 第二引数がcosine similarityのおさまったjsonファイル
input_json = sys.argv[2]
# 第三引数が出力するttlファイル名
output_ttl = sys.argv[3]

## jsonを読み込む
with open(input_json, "r") as f:
    key_sims_sorted = json.load(f)
with open('acm_ccs_emb.json') as f:
    acm_ccs_embs = json.load(f)

## グラフつくる
graph = Graph()
graph.parse(input_ttl)
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
            if(list(acm_ccs_embs[acm_key].keys())[0] == list(key_sims_sorted[key].keys())[0]):
                acm_key_top1 = acm_key
            elif(list(acm_ccs_embs[acm_key].keys())[0] == list(key_sims_sorted[key].keys())[1]):
                acm_key_top2 = acm_key
            elif(list(acm_ccs_embs[acm_key].keys())[0] == list(key_sims_sorted[key].keys())[2]):
                acm_key_top3 = acm_key
            elif(list(acm_ccs_embs[acm_key].keys())[0] == list(key_sims_sorted[key].keys())[3]):
                acm_key_top4 = acm_key
            elif(list(acm_ccs_embs[acm_key].keys())[0] == list(key_sims_sorted[key].keys())[4]):
                acm_key_top5 = acm_key

        out_graph.add((blank, bibtex_base.top1, URIRef(acm_key_top1)))
        out_graph.add((blank, bibtex_base.top2, URIRef(acm_key_top2)))
        out_graph.add((blank, bibtex_base.top3, URIRef(acm_key_top3)))
        out_graph.add((blank, bibtex_base.top4, URIRef(acm_key_top4)))
        out_graph.add((blank, bibtex_base.top5, URIRef(acm_key_top5)))
        
out_graph.serialize(destination=output_ttl + ".ttl", format="ttl")


