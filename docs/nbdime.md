nbdime(https://nbdime.readthedocs.io/en/latest/index.html)を導入しました。

標準的なdiffやmergeではipynb実行時の出力や実効回数を保持するためのメタデータを無視できず、conflictの解消が困難です。nbdimeはipynbのメタデータの部分を無視してdiffやmergeをするためのツールです。

先程の公式のページに使い方などのすべてが載っています。

公式のガイドではpipを使用しますが、もしuvを使用しているなら
```
uv tool install nbdime
```
とすればグローバルにインストールできます。

必要な設定は.gitattributesに書いておいたので、nbdimeがインストールできていれば使用することができるはずです。