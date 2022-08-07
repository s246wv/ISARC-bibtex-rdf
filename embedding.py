from asyncio import QueueEmpty
from sentence_transformers import SentenceTransformer
from rdflib import Graph, URIRef

model = SentenceTransformer('all-MiniLM-L6-v2')

skosURI = "http://www.w3.org/2004/02/skos/core#"

graph = Graph()
graph.parse("acm_ccs2012-1626988337597.xml")
query = """
select ?label where {
    ?s <http://www.w3.org/2004/02/skos/core#prefLabel> ?label. 
}
"""
qres = graph.query(query)
words = []
for row in qres:
    words.append(row.label)

embs = model.encode(words)
for word, emb in zip(words, embs):
    print(word)
    print(emb)