from argparse import Namespace
import requests
import bs4
import re
from rdflib import Graph, Literal, URIRef, Namespace
import sys

# webサイトの情報をもらってきます．
# url = "https://www.iaarc.org/publications/search.php?query=&publication=42"
url = sys.argv[1]
r = requests.get(url)

# keywordsとDOIのペアをもらいます．
html = bs4.BeautifulSoup(r.text, 'lxml')
articles = html.find_all("div", class_="article compact")
pairs = {}  #doiをキーにしてキーワードたちをバリューにもつ辞書
for article in articles:
    doi_tag = article.find("div", class_="doi")
    doi = doi_tag.find("a").get_text()
    keyword_tag = article.find("div", class_="keywords")
    keywords_temp = keyword_tag.get_text().split(";")
    keywords = []
    for keyword in keywords_temp:
        temp = re.sub("^ ", "", keyword)
        temp = re.sub("^Keywords: ", "", temp)
        keywords.append(temp)
    pairs[doi] = keywords
# print(pairs)
# RDFにします．
# RDFを読み込みます．
# fileName = "isarc2021.bib.ttl"
# outfile = "isarc2021_2.bib.ttl"
fileName = sys.argv[2]+".bib.ttl"
outfile = sys.argv[2]+"_2.bib.ttl"
g = Graph()
g.parse(fileName)
bibtex_base = Namespace("http://www.edutella.org/bibtex#")
for key in pairs.keys():
    for keyword in pairs[key]:
        # keywordをdoiに対応付けます．
        g.add((URIRef(key), bibtex_base.keyword, Literal(keyword)))
g.serialize(destination=outfile, format="ttl")
# 終わり