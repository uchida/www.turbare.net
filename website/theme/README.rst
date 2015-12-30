Pelican theme
=============

a theme for pelican static web generator

Dependencies
------------

The assets_ Pelican plugin, which integrates the webassets_ package is required, 
install the assets_ plugin and activate it via your settings file and install webassets_ via::

   $ pip install webassets

Additionally, this theme uses the cssmin_ Python packages to reduce size of css
and the compass_ Ruby package to generate main css file via assets_ plugin,
these packages can be installed via::

   $ pip install cssmin
   $ gem install compass


Setting
-------

:`USE_MATHJAX = True`: use the MathJax Content Delivery Network to show math expressions

.. _assets: https://github.com/getpelican/pelican-plugins/tree/master/assets`
.. _webassets: https://pypi.python.org/pypi/webassets/
.. _cssmin: https://pypi.python.org/pypi/cssmin/
.. _compass: https://rubygems.org/gems/compass
