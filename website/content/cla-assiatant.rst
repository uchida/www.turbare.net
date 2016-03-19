.. -*- coding: utf-8; -*-

CLA assistant
=============

:date: 2016-03-19
:author: Akihiro Uchida
:tags: license
:category: memo
:slug: cla-assiatant
:lang: ja

OSS に contribution を投げていると CLA というやつを求められることがある。
CLA は Contributor License Agreement の略で contribution をプロジェクトが使う権利を明示的にもらうための同意書。

`著作権の保有と譲渡 - オープンソースソフトウェアの育て方 <http://producingoss.com/ja/copyright-assignment.html>`_
あたりがわかりやすい。

重要な仕組みだと思う一方、個人で導入するのは大変そう。
いっそサービスでもあれば、作るかと思い数ヶ月、
ある日 `CLA Assistant <http://cla-assistant.io>`_ を見つけた。

`SAP の github チーム <https://github.com/sap/>`_ が作ったとのこと、
大きい企業に CLA 管理が必要というのは納得だが、
サービスにする気風は素晴らしい。

このサービスは github の pull request から webhook に反応して CLA 署名の状況を表示したり、
署名を求める bot として動く。
CLA は gist で管理されるので、どのバージョンに署名したのかもわかる。
集めた CLA の管理は普通に考えると annoying だが、これは github アカウントで署名される、
バランスがいい。
CLA の準備についての手間は残るが、そこは止むを得ないところ。そこさえ越えれば個人でもできそう。

ということで取らぬ狸の皮算用、導入して数ヶ月し、導入したのも忘れたところで
`pull request <https://github.com/uchida/ansible-mock-role/pull/1>`_ が来た。

また同じような仕組みで `CLAHub <https://clahub.com>`_ というのもあるよう。

