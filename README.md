# bibtexからrdfを作る

## 必要なもの
java
[bibtex2rdf](http://bibtex2rdf.sourceforge.net/)  
python  
requirements.txtに書いているpythonのパッケージたち  

## 使い方

```
java -jar bibtex2rdf -schema config.txt -baseuri "https://doi.org/" -enc UTF-8 [bibtex_file] [output_rdf_file]
python conversion.py [xml/rdf_file] [extension]
python scrape.py [url] [rdf_file]
```

### 補足
- *[ISARC](https://www.iaarc.org/publications/search.php?series=1&query=&publication=0)のProc.からrdfを作るためのスクリプトです．他に適用するためには少し修正が必要です．*
- *conversion.pyでいったんrdf/xmlをttlに変換していますが，特に必要はないですが，現状のスクリプトは一度変換することを前提にしています．*

## 謝辞
[bibtex2rdf - A configurable BibTeX to RDF Converter](http://bibtex2rdf.sourceforge.net/)  






## 追加機能の設計メモ
- キーワードを単語埋め込みしてacmのCCSと比較して類似キーワードを紐づけする．acm ccsから検索出来るように．
  - embeddingはqueryを読み込むようにしてembeddingしたvectorファイルを出力する人にしてしまおうかしら．
  - comparingはcos_simを計算するだけにしましょうか．vectorファイルを二つ読み込む．