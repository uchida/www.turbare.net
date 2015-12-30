#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pelican import signals

def add_modified_on_article(generator):
    import os
    from datetime import datetime
    for article in generator.articles:
        mtime = os.path.getmtime(article.source_path)
        article.modified = datetime.fromtimestamp(mtime)

def add_modified_on_page(generator):
    import os
    from datetime import datetime
    for page in generator.pages:
        mtime = os.path.getmtime(page.source_path)
        page.modified = datetime.fromtimestamp(mtime)

def register():
    signals.article_generator_finalized.connect(add_modified_on_article)
    signals.page_generator_finalized.connect(add_modified_on_page)
