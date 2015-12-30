FreeBSD periodic(8) の出力を調整する
====================================

:date: 2015-04-06
:author: Akihiro Uchida
:tags: FreeBSD
:category: memo
:slug: configure-output-for-periodic-in-freebsd
:lang: ja

FreeBSD では cron から periodic(8) で定期実行タスクが実行され、
その結果が root 宛にメールされます。

各 jail 上でのメールを ssmtp でメールサーバに relay するよう設定していましたが、
jail の数が多くなるにつれ、煩わしくなり periodic の設定を調整しました。

`man 8 periodic`_ や `man 5 periodic.conf`_ をみると、
``/etc/periodic.conf`` で以下の変数を設定することで出力を調整できるようです。

* ``<basedir>_show_success``
* ``<basedir>_show_info``
* ``<basedir>_show_badconfig``

``<basedir>`` の部分は ``daily`` ``weekly`` ``monthly`` ``security`` のいずれかです。
要は ``/etc/periodic`` 以下のディレクトリですね。

periodic から呼び出される ``{,/usr/local}/etc/periodic/{daily,weekly,monthly,security}/`` 以下のスクリプトは notable infomation が無い場合は終了コード 0 となるはずです。

ということで ``/etc/periodic.conf`` で以下のように ``show_success`` を無効とする設定をいれるようにしました。

.. code-block:: sh

   daily_show_success="NO"
   weekly_show_success="NO"
   monthly_show_success="NO"
   security_show_success="NO"

``periodic`` コマンドを直接実行し、その出力を見ることで設定結果を確認できます。

.. _man 8 periodic: https://www.freebsd.org/cgi/man.cgi?query=periodic%288%29
.. _man 5 periodic.conf: https://www.freebsd.org/cgi/man.cgi?query=periodic.conf
