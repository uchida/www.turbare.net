# -*- coding: utf-8 -*-
from pelican import signals
from pelican.contents import Article
from HTMLParser import HTMLParser
from typogrify.filters import typogrify

def disable_typogrify(pelican):
    pelican.settings['TYPOGRIFY'] = None

class FilterParser(HTMLParser):
    def __init__(self, excludes):
        HTMLParser.__init__(self)
        self.content = ''
        self.excludes = excludes
        self.is_applicable = False
        self.targets = []

    def handle_starttag(self, tag, attrs):
        if tag in self.excludes:
            self.is_applicable = False
        self.content = ''

    def handle_endtag(self, tag):
        if self.is_applicable:
            new_content = typogrify(self.content)
            if self.content != new_content:
                self.targets.append((self.content, new_content))
        self.is_applicable = True

    def handle_data(self, data):
        if self.is_applicable:
            self.content += data

def run_typogrify(article_generator):
    articles = []
    excludes = article_generator.settings.get("TYPOGRIFY_EXCLUDE_TAGS", [])
    parser = FilterParser(excludes)
    for article in article_generator.articles:
        parser.feed(article.content)
        parser.close()
        content = article.content
        for old, new in parser.targets:
            content = content.replace(old, new)
        new_article = Article(content, article.metadata, article.settings,
                              article.filename, article._context)
        articles.append(new_article)
    article_generator.articles = articles

def register():
    signals.initialized.connect(disable_typogrify)
    signals.article_generator_finalized.connect(run_typogrify)
