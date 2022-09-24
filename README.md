# bibtexからrdfを作る

## 必要なもの
java  
[bibtex2rdf](http://bibtex2rdf.sourceforge.net/)  
python  
requirements.txtに書いているpythonのパッケージたち  

## 使い方

```bash
java -jar bibtex2rdf.jar -schema config.txt -baseuri "https://doi.org/" -enc UTF-8 [bibtex_file] [output_rdf_file]
python conversion.py [xml/rdf_file] [extension]
python scrape.py [url] [rdf_file]
```

### 補足
- bibtexからrdfを作る主要機能はbibtex2rdf.jarが担ってくださっています．
- scrape.pyは[ISARC](https://www.iaarc.org/publications/search.php?series=1&query=&publication=0)のProc.からキーワードを取得して，rdfに反映するためのスクリプトです．
- 汎用的なツールとしてはkeywordsタグを含むbibtexからrdfを作るものがあった方が良いかもしれません．

## できたもの
- [isarc](https://github.com/s246wv/ISARC-bibtex-rdf/tree/main/isarc)に入っています．例えば，[isarc2022.bib.ttl](https://github.com/s246wv/ISARC-bibtex-rdf/blob/main/isarc/2022/isarc2022.bib.ttl)  
下記のようなSPARQLクエリでpaperに対するキーワードを取得します．
```sparql
select ?id ?label where {
    ?id <http://www.edutella.org/bibtex#keyword> ?label. 
}
```

## 謝辞
[bibtex2rdf - A configurable BibTeX to RDF Converter](http://bibtex2rdf.sourceforge.net/)  

