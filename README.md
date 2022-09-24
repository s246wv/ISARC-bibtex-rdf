# bibtexからrdfを作る

## 概要
本作品は、Sibersjkiによるbibtex2rdfで生成したrdfに対して、The International Association for Automation and Robotics in Construction (ISARC)のウェブサイトから取得したキーワード情報を追加するスクリプト及び生成されたrdfファイルです。  

bibtexファイルにはキーワード情報が含まれていないことが多く、bibtex2rdfで生成したrdfファイルでは、キーワード情報を活用することが容易ではありません。本作品では、会議録のウェブサイトから文献情報をスクレイピングすることで、彼らの提供するbibtexファイルに含まれる情報に対して，キーワード情報を付加しています。これにより、個人レベルでの文献情報のLOD的な使い方の幅を広げることが期待できます。  

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

