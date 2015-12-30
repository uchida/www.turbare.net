MacBook のバッテリー充放電回数を CUI で取得
===========================================

:date: 2015-03-27 22:14
:author: Akihiro Uchida
:tags: osx
:category: memo
:slug: battery-cycle-count-for-macbook
:lang: ja

バッテリーの充放電回数は MacBook のバッテリー劣化を図る指標で
`Mac ノートブック：バッテリーの充放電回数を確認する <https://support.apple.com/ja-jp/HT201585>`_ には
:code:`/Applications/Utilities/System Information.app` による充放電回数の値の確認方法と、
各世代の MacBook 最大充放電回数の表が掲載されています。

いちいちアプリケーションを開いて確認するのも面倒なので CUI のスクリプトで取得してみました。

System Information.app で取得できる情報は `system_profiler(8)
<https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man8/system_profiler.8.html>`_
で取得できます。

手っ取り早く取得するならこんなワンライナー。

.. code-block:: bash

   $ system_profiler SPPowerDataType | awk -F: '/Cycle Count/ { print $2 }'

もう少しきちんと xml 出力して :code:`xpath` でパースすることも。

.. code-block:: bash

   $ system_profiler SPPowerDataType -xml | xpath '/plist/array/dict/key[.="_items"]/following-sibling::*[1]/dict/key[.="sppower_battery_health_info"]/following-sibling::*[1]/key[.="sppower_battery_cycle_count"]/following-sibling::*[1]/text()' 2>/dev/null

複雑すぎですね。plist xml の要素取り出しは :code:`plutil` で単純化できます。

.. code-block:: bash

   $ system_profiler SPPowerDataType -xml | plutil -extract '0._items.0.sppower_battery_health_info.sppower_battery_cycle_count' xml1 -o - - | xpath '/plist/integer/text()' 2>/dev/null

plist xml を :code:`plutil` で簡単に扱えます。まるで json を jq で扱うようです。

ちなみに私の環境だと MacBook Pro (Retina, 13-inch, Late 2013) で
購入後276日経過時点で396回でした。
このペースだと、だいたい2年程度で最大充放電回数とされる1000回に達しそう。

