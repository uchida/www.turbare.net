# -*- coding: utf-8 -*-

def register():
    from docutils.writers.html_plain import HTMLTranslator
    class Translator(HTMLTranslator):
    
        def visit_abbreviation(self, node):
            attrs = {}
            if node.hasattr('explanation'):
                attrs['title'] = node['explanation']
            self.body.append(self.starttag(node, 'abbr', '', **attrs))
    
        def visit_image(self, node):
            # set an empty alt if alt is not specified
            # avoids that alt is taken from src
            node['alt'] = node.get('alt', '')
            return HTMLTranslator.visit_image(self, node)

    import pelican.readers
    pelican.readers.PelicanHTMLTranslator = Translator
