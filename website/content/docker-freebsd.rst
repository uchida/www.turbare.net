簡単 FreeBSD Docker イメージの作り方
====================================

:date: 2016-03-05 20:29
:author: Akihiro Uchida
:tags: freebsd docker
:category: memo
:slug: simple-freebsd-docker-image
:lang: ja

FreeBSD が Docker の Experimental support をサポートしていることに気づいたので試してみました。
jail + ZFS + 64bit Linux compatibility layer を使って、既存の Linux イメージなどを動かせるようです。

2015年6月の 11-CURRENT ぐらいからサポートされてた模様。

FreeBSD 上で動かす方法は `Docker on FreeBSD - FreeBSD Wiki <https://wiki.freebsd.org/Docker>`_ や
`FreeBSDでDockerを試す - Keep It Simle, Stupid <http://yskwkzhr.blogspot.jp/2016/01/trying-docker-on-freebsd.html>`_ に譲るとして
FreeBSD 上で FreeBSD の Docker イメージを作ってみました。

Docker といいつつ実態はもちろん jail なので FreeBSD のイメージを作って FreeBSD 上で FreeBSD を動かしてもいいわけです。
実際 `lexaguskov/freebsd <https://hub.docker.com/r/lexaguskov/freebsd/>`_ や 
`kazuyoshi/freebsd-minimal <https://hub.docker.com/r/kazuyoshi/freebsd-minimal/>`_ といった
イメージが Docker Hub 上に既に上がっています。
ただ、これらのイメージ作成方法を探しても見つからなかったので、用意してみました。

FreeBSD 上で FreeBSD 動かすなら jail でいいのではという気がしたりしますが、
docker-compose や docker-swarm とかと組み合わせられる点は割とメリットがあると思います。

基本的には jail なので kernel は不要で FreeBSD でのユーザランド相当、
base.txz や lib32.txz とかがあれば動きそうなので、これらを展開して
(展開までに bsdinstall jail とか使う方法とかもあります)
tar で固め直して docker import したら動くイメージが作れるようになりました。

.. code-block:: console

   $ mkdir docker-freebsd-10.2
   $ fetch http://ftp.freebsd.org/pub/FreeBSD/releases/amd64/10.2-RELEASE/base.txz
   $ tar xf base.txz -C docker-freebsd-10.2
   $ fetch http://ftp.freebsd.org/pub/FreeBSD/releases/amd64/10.2-RELEASE/lib32.txz
   $ tar xf lib32.txz -C docker-freebsd-10.2
   $ tar -C docker-freebsd-10.2 -czpf docker-freebsd-10.2.tgz .
   $ cat docker-freebsd-10.2.tgz | docker import - freebsd
   $ docker run -it freebsd /bin/sh
   % freebsd-version

あと展開したファイルに schg フラグがついていたりして削除が面倒、という側面もあります。

あと根本的にはこの方法だと Dockerfile を作って Automated build できないし、作り方を明示的に共有できない。
ということで公式イメージとかがよく使う手を使って Dockerfile 化。

.. code-block:: console

   $ fetch http://ftp.freebsd.org/pub/FreeBSD/releases/amd64/10.2-RELEASE/base.txz
   $ fetch http://ftp.freebsd.org/pub/FreeBSD/releases/amd64/10.2-RELEASE/lib32.txz
   $ cat Dockerfile
   FROM scratch
   ADD base.txz /
   ADD lib32.txz /
   CMD ["/bin/sh"]
   $ docker build -t freebsd .
   $ docker run -it freebsd /bin/sh
   # freebsd-version
   10.2-RELEASE

この方法で Dockerfile を github に公開して `uchida/docker-freebsd <https://github.com/uchida/docker-freebsd>`_
Docker Hub にも `auchida/freebsd <https://hub.docker.com/r/auchida/freebsd/>`_ で上げてみました。

ただ `kazuyoshi/freebsd-minimal <https://hub.docker.com/r/kazuyoshi/freebsd-minimal/>` はサイズ 4MB 程度なので、
もっと中身を削ってサイズは縮められそう。

