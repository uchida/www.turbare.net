A document transltion process with sphinx and gettext
=====================================================

:date: 2013-09-17 21:05
:author: Akihiro Uchida
:tags: transl, sphinx, transifex
:category: memo
:slug: workflow-with-transifex-and-sphinx
:lang: en
:translation: true

I'll show an example document (e.g scipy-lecture-notes) translation process with sphinx and gettext.

Get document
------------

.. code-block:: console

   $ git clone https://github.com/scipy-lectures/scipy-lecture-notes.git
   ...
   $ cd scipy-lecture-notes

All command-line operations after this are done in the directory scipy-lecture-notes.

We decide release version to translate and cut a branch from release commit

.. code-block:: console

   $ git checkout -b 2013.1-transl 2013.1

Make gettext 
------------

Add gettext target in Makefile and set ``gettext_compact = False`` and ``locale_dirs = ['locale/']``.
With ``gettext_compact = False``, indivisual pot files will corresponds each rst files
i.e. create lots of small pot files instead of some large pot files.
``locale_dirs = ['locale/']`` is required to build translated documents.

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

Make gettext!

.. code-block:: console

   $ make gettext
   ...

Register with Transifex
-----------------------

Create an acount, your organization, and then creates your projects on Transifex.
A free organization plan is available for open-source projects.

Install ``transifex_client`` and ``sphinx-intl`` for collaboration with transifex.

.. code-block:: console

   $ pip install transifex_client
   ...
   $ pip install sphinx-intl
   ...

Type ``tx init`` to generate ``~/.transifexrc`` and ``.tx/config``.

.. note::

   plain password are writen in ~/.transifexrc

Input username and password for transifex.

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
   $ cat ~/.transifexrc
   [https://www.transifex.com]
   hostname = https://www.transifex.com
   password = <transifex-password>
   username = <transifex-username>
   token =
   $ cat .tx/config
   [main]
   host = https://www.transifex.com

Use ``sphinx-intl`` command to put all the entries of tranlsation file together into .tx/config,
and then use ``tx push`` to register entries on .tx/config with transifex resources.

.. code-block:: console

   $ sphinx-intl update-txconfig-resources --pot-dir build/locale --transifex-project-name="<project-name>"
   Updating source for resource <project-name>.AUTHORS ( en -> locale/pot/AUTHORS.pot ).
   Setting source file for resource <project-name>.AUTHORS ( en -> locale/pot/AUTHORS.pot ).
   Updating file expression for resource <project-name>.AUTHORS ( locale/<lang>/LC_MESSAGES/AUTHORS.po ).
   ...
   $ cat .tx/config
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

On the Web UI of your transifex project, push "Create language" and add language.

Translate in Web UI or download po files and edit them and upload.

Build Translation
-----------------

To get tranlatied files, type ``tx pull`` with your language code, for example 'ja' for Japanese:

.. code-block:: console

   $ tx pull -l ja
   ...

To build translated files:

.. code-block:: console

   $ sphinx-intl build
   $ make -e SPHINXOPTS="-D language='ja'" html
   ...


References
----------

* `Using Transifex service for team translation - Sphinx documentation <http://sphinx-doc.org/latest/intl.html#using-transifex-service-for-team-translation>`_

