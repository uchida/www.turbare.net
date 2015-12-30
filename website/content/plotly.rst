Plotly + iPython Notebook を試す
================================

:date: 2013-11-05 16:38
:author: Akihiro Uchida
:tags: python
:category: memo
:slug: plotly-and-ipython-notebook
:lang: ja

iPython Notebook は対話的に操作でき、メモを書けて、作業を記録に残すことができる。
とても便利。

ただ、現状 iPython notebook でグラフを対話的に拡大、縮小するには
matplotlib と qtconsole を使う方法がある。
ただ、qtconsole を利用するには当然 Qt を入れる必要があり、
virtualenv を利用していたりするとインストールに一手間かかる。

そこで `Plotly <https://plot.ly/>`_ という Web サービスと iPython notebook を
組み合わせると比較的手軽にグラフ操作ができるので紹介。
(matplotlib は version 1.3 で WebAgg が導入されたので、
そのうち iPython notebook と WebAgg を組み合わせれば plotly と同様の操作が
できるようになるはず。)

Plotly は Web 上でデータ分析や可視化ができる Web サービス。
さらに、以下の言語用の API が提供されていてるので、グラフ用のライブラリとしても利用できる。

- Python
- MATLAB
- Julia
- R
- Perl
- Arduino

REST API も用意されているので、それを使えば他の言語からも利用できるはずです。
特に Python は iPython Notebook で plotly の出力する HTML を埋め込むことで、
拡大や縮小等を対話的に操作できます。

ただ、以下に示す方法では plotly 自体にアクセス制御機能があるにも関わらず、
現状デフォルトでは public に設定されてしまうようです、注意。

インストール、ユーザ登録
------------------------

pip からインストールできる。

.. code-block:: console

   $ pip install plotly

さらにユーザ登録して API キーを取得しておきます。

iPython Notebook から利用する
-----------------------------

iPython notebook を起動

.. code-block:: console

   $ ipython notebook

plotly を import

.. code-block:: python
   
   import plotly
   py = plotly.plotly(username='<your-username>', key='<your-api-key>')   

とりあえずデータを作ってみました。

.. code-block:: python
   
   import numpy as np
   
   N = 10000
   K = 1.0
   twopi = 2 * np.pi
   
   q, p = np.zeros(N), np.zeros(N)
   q[0], p[0] = [0.1, 0.1]
   for i in range(1,N):
       q[i] = q[i-1] + p[i-1]
       q[i] = q[i] - np.floor(q[i] / twopi) * twopi
       p[i] = p[i-1] + K * np.sin(q[i])
       p[i] = p[i] - np.floor(p[i] / twopi) * twopi

プロットするため、データを plotly 用に json の中に用意します。

.. code-block:: python

   data = {'x': q, 'y': p, 'type': 'scatter', 'mode': 'markers', 'marker': {'size': 2}}   

plotly にプロットさせてみます。

filename の部分は元データが Standard Map なので stdmap としました。
これは plotly 上でデータセットを認識するための名前に利用されます。

.. code-block:: python
   
   response = py.plot(data, filename='stdmap', fileopt='overwrite')

下記のように表示されました、成功したようです::
   
   High five! You successfuly sent some data to your account on plotly. View your plot in your browser at https://plot.ly/~<your-username>/0 or inside your plot.ly account where it is named 'stdmap'

iPython notebook 上に表示させます。

.. code-block:: python

   from IPython.display import HTML
   src = '<iframe src="{}/600/600" width="650" height="650"></iframe>'.format(response['url'])
   html = HTML(src)
   html

こうすると iPython notebook 上でグラフが表示され、
ドラッグして拡大、ダブルクリックで戻るなど、対話的に操作ができます。

こんな感じです。

.. raw:: html

   <iframe src="https://plot.ly/~uchida/2/600/600/" width="650" height="650"></iframe>

参考

- `7105191 - nbviewer.ipython.org <http://nbviewer.ipython.org/7105191>`_
- `Plotly API <https://plot.ly/API/>`_

