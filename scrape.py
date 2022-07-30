from sqlite3 import paramstyle
import requests
import bs4
import re
from rdflib import Graph, URIRef

# webサイトの情報をもらってきます．
url = "https://www.iaarc.org/publications/search.php?query=&publication=42"
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
fileName = "isarc2021.bib.ttl"
g = Graph()
g.parse(fileName)
for key in pairs.keys():
    if(URIRef(key), None, None) in g:
        print("aru")