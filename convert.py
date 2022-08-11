## ntを選ぶときは警告が出ます．要修正？
from rdflib import Graph
import sys
import os

g = Graph()
## 第一引数でファイル名を渡します．
fileName = sys.argv[1]
g.parse(fileName)
## 第二引数でタイプを指定します．
ext = sys.argv[2]
outName = os.path.splitext(fileName)[0] + "." + ext
g.serialize(destination=outName, format=ext)
