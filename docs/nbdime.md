nbdime(https://nbdime.readthedocs.io/en/latest/index.html)を導入しました。

標準的なdiffやmergeではipynb実行時の出力や実効回数を保持するためのメタデータを無視できず、conflictの解消が困難です。nbdimeはipynbのメタデータの部分を無視してdiffやmergeをするためのツールです。

先程の公式のページに使い方などのすべてが載っています。

公式のガイドではpipを使用しますが、もしuvを使用しているなら
```
uv tool install nbdime
```
とすればグローバルにインストールできます。

gitとの連携に必要な設定をするには.gitがあるフォルダで
```
nbdime config-git --enable
```
とすれば良いです。

もしグローバルに設定する必要があれば
```
nbdime config-git --enable --global
```
とします。