# word_network
## 概要
- できること
  - 検索単語を入力すると一緒に呟かれた単語がわかる
  - その単語をグラフで見ることができる
  - 単語ごとの関係性がわかる
  - 自分が気になってること・もの・人について他人がどう考えているのかがわかる
  - 次数中心性、近接中心性、媒介中心性での指数がわかる
  - PageRankがわかる
  
- 使い方
  - word_network.pyをダウンロードし、コマンドライン上で起動(開発環境と同じものが必要です)
  - 検索したい単語を入力する 
  
- 開発環境
  - mac Os Mojave
  - Python3
  - networkx
  - MeCab0.996(mecab-ipadic-NEologdの辞書を使用)
- 補足
  - 取ってきた単語は「単語リスト.txt」というテキストファイルに保存されますが、プログラムを起動するごとに上書きされます。
  - 辞書に載っていない単語をTwitterから拾ってしまった場合にエラーが出て終了します。ご容赦ください。
## 実行例
