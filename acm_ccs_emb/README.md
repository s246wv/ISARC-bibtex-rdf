# ACM CCSを紐づける

## 概要
本作品は、ISARC bibtexRDFのキーワードにに対してACM Computing Classification System (ACM CCS)の語を対応づけるためのスクリプト及び生成されたrdfファイルです。

ISARC bibtexRDFでは、従来のbibtex2rdfで扱われていなかったキーワード情報をrdfファイルに付加する方法を示しました。しかし、キーワードは著者らが自由に記載できるため、文字列一致で文献検索に利用する場合、類似語であるにも関わらず検索結果から漏れる可能性があります。加えて、計算機科学分野に慣れ親しんだものが他分野の文献を検索する際に、適切なキーワードを選択できない可能性があります。
本作品では、その課題を解決するために、ACM CCSとの類似度を計算し、キーワードとの関連付けを行いました。具体的には、各キーワードをSentence-BERTを用いてベクトル空間に埋め込み、キーワード間のコサイン類似度を計算します。類似度をランキングし、トップ5までをrdfファイルに付加します。

本作品により、ACM CCSに反映された計算機科学の知見を利用して、計算機科学と他分野を横断するような分野の文献検索を容易にするLODを作成することができます。

## 必要なもの
`../requirements.txt`に書いているpythonのパッケージたち  
keywordが含まれたttlファイル  
`retrieveKeyword.rq`: このフォルダに入ってます．  
`acm_ccs2012-1626988337597.xml`: このフォルダに入ってます．[こちら](https://dl.acm.org/pb-assets/dl_ccs/acm_ccs2012-1626988337597.xml)から頂きました．  
`acm_ccs_emb.json`: このフォルダに入ってます．`embed4AcmCcs.py`を動かしても得られます． 

## 使い方
```bash
./runAll.sh hoge.ttl retrieveKeyword.rq
```
- `hoge.ttl`はkeywordsが含まれたものとしてください．
- 個別のpythonスクリプトの説明はおいおい整備します．


## できたもの
- 例えば，[isarc2022withACMCSS.bib.ttl](https://github.com/s246wv/ISARC-bibtex-rdf/blob/main/isarc/2022/isarc2022withACMCSS.bib.ttl)
- 下記のSPARQLクエリでキーワードに対して，ACM CCSの中からSentenceTransformersのall-MiniLM-L6-v2のモデルで計算したTensor同士のコサイン類似度の高いものtop 1を出力します．
```sparql
select ?id ?keyword ?acmlabel where {
    ?id <http://www.edutella.org/bibtex#acmKeywordSimilarity> ?o.
    ?o <http://www.edutella.org/bibtex#keyword> ?keyword;
       <http://www.edutella.org/bibtex#top1> ?acmid.
    ?acmid <http://www.w3.org/2004/02/skos/core#prefLabel> ?acmlabel.
}
```

## 寸劇
![寸劇](./bibtex2rdfWacmccs.gif)

## 謝辞
[Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://arxiv.org/abs/1908.10084):

```bibtex 
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

[ACM Computing Classification System](https://dl.acm.org/ccs)
