# -*- coding: utf-8 -*-
import unicodedata
import docutils.nodes
import docutils.transforms

def is_fullwidth(c):
    return c != '' and unicodedata.east_asian_width(c) in ['F', 'W', 'A']

def is_punctuation(c):
    return c != '' and unicodedata.category(c).startswith('P')

def to_be_joined(tail, head):
    if is_punctuation(tail) and is_fullwidth(head):
        return True
    if is_fullwidth(tail) and is_fullwidth(head):
        return True
    return False

class JapaneseTextJoin(docutils.transforms.Transform):
    default_priority = 800

    def apply(self):
        for text in self.document.traverse(docutils.nodes.Text):
            if (isinstance(text.parent, docutils.nodes.literal_block) or
                isinstance(text.parent, docutils.nodes.raw)):
                continue
            tail, lines = '', []
            for line in text.astext().splitlines():
                head = line[0] if len(line) > 0 else ''
                if to_be_joined(tail, head):
                    lines[-1] += line
                else:
                    lines.append(line)
                tail = line[-1] if len(line) > 0 else ''
            if text.astext()[-1] == '\n':
                lines.append('\n')
            joined_text = docutils.nodes.Text('\n'.join(lines), text.rawsource)
            text.parent.replace(text, joined_text)

def register():
    import docutils.parsers.rst
    origparser = docutils.parsers.rst.Parser
    class Parser(origparser):
        def get_transforms(self):
            return origparser.get_transforms(self) + [JapaneseTextJoin]
    docutils.parsers.rst.Parser = Parser
