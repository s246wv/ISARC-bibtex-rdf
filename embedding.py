from sentence_transformers import SentenceTransformer
from rdflib import Graph
import json

# You can choose the model here https://www.sbert.net/docs/pretrained_models.html 
model = SentenceTransformer('all-MiniLM-L6-v2')

graph = Graph()
# The 'publicID' is unofficial base URI. 
graph.parse("acm_ccs2012-1626988337597.xml", publicID="https://dl.acm.org/ccs/")
# Please modify this SPARQL query if you want to change the resource
query = """
select ?id ?label where {
    ?id <http://www.w3.org/2004/02/skos/core#prefLabel> ?label. 
}
"""
qres = graph.query(query)
keys = []
words = []
for row in qres:
    keys.append(row.id)
    words.append(row.label)
# Computing sentence embeddings. 
embs = model.encode(words)
dicts = {}
for key, word, emb in zip(keys, words, embs):
    dict = {key.toPython(): (word.toPython(), emb.tolist())}
    dicts.update(dict)
# Output the json file.
with open("./acm_ccs_emb.json", "w") as f:
    json.dump(dicts, f)
