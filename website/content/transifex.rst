Sphinx と transifex を活用した翻訳手順
======================================

:date: 2013-09-15 0:13
:author: Akihiro Uchida
:tags: transl, sphinx, transifex
:category: memo
:slug: workflow-with-transifex-and-sphinx
:lang: ja

2年程前から放置していた
`scipy-lecture-notes の翻訳 <http://www.ike-dyn.ritsumei.ac.jp/~uchida/scipy-lecture-notes/>`_
を再開した。
いまや Sphinx は gettext を利用して翻訳できるようになり、
さらに transifex という割と使いやすい翻訳サイトもあらわれ、
翻訳元が更新されたときの差分翻訳がしやすくなったので、
いろいろ試して翻訳手順が確立してきたので載せてみた。

書いてから気づいたが `Using Transifex service for team translation - Sphinx document
<http://sphinx-doc.org/latest/intl.html#using-transifex-service-for-team-translation>`_
にだいたい書いてある、そっちを見た方が早い。

ドキュメントの取得
------------------

まずは、翻訳元の Sphinx ドキュメントを取得

.. code-block:: console

   $ git clone https://github.com/scipy-lectures/scipy-lecture-notes.git
   ...
   $ cd scipy-lecture-notes

以降の操作は scipy-lecture-notes ディレクトリ以下で。

ついでに翻訳元のドキュメントが git で管理されている場合は、
どのバージョンを翻訳するか決めておくこと。
(翻訳途中にファイル名変更や削除など構造が変わるとつらいことになる)
以下のようにして tag: 2013.1 のコミットからブランチを切り、
そこで作業するとかした方がいい。

.. code-block:: console

   $ git checkout -b 2013.1-transl 2013.1

gettext の生成
--------------

make のターゲットに gettext が無かったので追加し、
conf.py で :code:`gettext_compact` を :code:`False` に設定。
gettext の出力先は他のターゲットに合わせて build 以下にした。
また、翻訳した内容で build するために conf.py で 
:code:`locale_dirs = ['locale/']` も設定

.. code-block:: diff

   diff --git a/Makefile b/Makefile
   index e59b398..d949399 100644
   --- a/Makefile
   +++ b/Makefile
   @@ -11,9 +11,10 @@ PYTHON        = python
    PAPEROPT_a4     = -D latex_paper_size=a4
    PAPEROPT_letter = -D latex_paper_size=letter
    ALLSPHINXOPTS   = -d build/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
   +I18NSPHINXOPTS  = $(SPHINXOPTS) .
   
   
   -.PHONY: help clean html web pickle htmlhelp latex changes linkcheck zip
   +.PHONY: help clean html web pickle htmlhelp latex changes linkcheck zip gettext
   
    help:
           @echo "Please use \`make <target>' where <target> is one of"
   @@ -103,3 +104,8 @@ install: pdf html
           git commit -a -m 'Make install' && \
           git push
   
   +gettext:
   +       $(SPHINXBUILD) -b gettext $(I18NSPHINXOPTS) build/locale
   +       @echo
   +       @echo "Build finished. The message catalogs are in build/locale."
   diff --git a/conf.py b/conf.py
   index efb63a9..19b99c5 100644
   --- a/conf.py
   +++ b/conf.py
   @@ -304,3 +304,6 @@ extlinks = {
   
    pngmath_dvipng_args = ['-gamma 1.5', '-D 180', '-bg', 'Transparent']
    pngmath_use_preview = True
   +
   +gettext_compact = False
   +
   +locale_dirs = ['locale/']

:code:`make gettext` して pot ファイルを作成し、

.. code-block:: console

   $ make gettext
   ...

transifex への追加
------------------

transifex のアカウント、組織、プロジェクトを作成。
オープンソースプロジェクトに関しては Free Plan で組織を作れる。

:code:`transifex_client` と :code:`sphinx-intl` をインストール。

.. code-block:: console

   $ pip install transifex_client
   ...
   $ pip install sphinx-intl
   ...

:code:`tx init` コマンドで ~/.transifexrc と .tx/config を生成。
途中で transifex のユーザ名とパスワードを聞かれるので入力。
~/.transifexrc にパスワードがべた書きされているのがとても気持ち悪い。

.. code-block:: console

   $ tx init
   Creating .tx folder...
   Transifex instance [https://www.transifex.com]:
   Creating skeleton...
   Creating config file...
   /path/to/home/.transifexrc not found.
   No entry found for host https://www.transifex.com. Creating...
   Please enter your transifex username: <transifex-username>
   Password: 
   Updating /path/to/home/.transifexrc file...
   Done.
   $ cat ~/.transifexrc # 生成された ~/transifexrc を確認
   [https://www.transifex.com]
   hostname = https://www.transifex.com
   password = <transifex-password>
   username = <transifex-username>
   token =
   $ cat .tx/config # 生成された .tx/config を確認
   [main]
   host = https://www.transifex.com

:code:`sphinx-intl` コマンドで .tx/config に各 po ファイルの内容について書き加え、
:code:`tx` コマンドでリソースの登録。

.. code-block:: console

   $ sphinx-intl update-txconfig-resources --pot-dir build/locale --transifex-project-name="<project-name>"
   Updating source for resource <project-name>.AUTHORS ( en -> locale/pot/AUTHORS.pot ).
   Setting source file for resource <project-name>.AUTHORS ( en -> locale/pot/AUTHORS.pot ).
   Updating file expression for resource <project-name>.AUTHORS ( locale/<lang>/LC_MESSAGES/AUTHORS.po ).
   ...
   $ cat .tx/config # .tx/config の更新を確認
   [main]
   host = https://www.transifex.com
   type = PO
   ...
   [<project-name>.intro--summary-exercises--auto_examples--plot_sprog_annual_maxima]
   file_filter = locale/<lang>/LC_MESSAGES/intro/summary-exercises/auto_examples/plot_sprog_annual_maxima.po
   source_file = locale/pot/intro/summary-exercises/auto_examples/plot_sprog_annual_maxima.pot
   source_lang = en
   $ tx push -s
   Pushing translations for resource <project-name>.AUTHORS:
   Pushing source file (locale/pot/AUTHORS.pot)
   Resource does not exist.  Creating...
   ...

transifex にソースとなる言語のリソースが追加されているので、
言語を追加で日本語を追加します。

あとはひたすら翻訳。transifex の web UI 上でも翻訳できるし、
ダウンロードしてエディタで翻訳もできる。

翻訳後にドキュメントを確認する場合は以下のようにして
po ファイルを取得してビルド。

.. code-block:: console

   $ tx pull -l ja
   ...
   $ sphinx-intl build
   ...
   $ make -e SPHINXOPTS="-D language='ja'" html
   ...

バージョン管理
--------------

transifex には Release というバージョン機能のようなものがありますが、
今のところ Web API が提供されていないので Web 上追加していくしかありません。
ファイルが多いと追加も面倒なので、現状ではバージョン毎にプロジェクトを分けた方がよさそうです。

複数プロジェクトの場合でも翻訳メモリが共有されるので、近い原文の訳文を候補として提示してくれます。

参考
----

* `2013/03/31 Sphinx の i18n 機能を使った翻訳手順 - 清水川 Web <http://www.freia.jp/taka/blog/sphinx-i18n-translation-procedure-with-transifex-amazon-s3/index.html>`_ 
* `Using Transifex service for team translation - Sphinx document <http://sphinx-doc.org/latest/intl.html#using-transifex-service-for-team-translation>`_


