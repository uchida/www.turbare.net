# -*- coding: utf-8 -*-
import unicodedata
import docutils.nodes
import docutils.transforms

def is_fullwidth(c):
    return c != '' and unicodedata.east_asian_width(c) in ['F', 'W', 'A']

def is_punctuation(c):
    return c != '' and unicodedata.category(c).startswith('P')

def to_be_joined(end_of_last_line, begin_of_line):
    if is_punctuation(end_of_last_line) and is_fullwidth(end_of_last_line):
        return True
    if is_fullwidth(end_of_last_line) and is_fullwidth(begin_of_line):
        return True
    return False

class JapaneseTextJoin(docutils.transforms.Transform):
    default_priority = 800

    def apply(self):
        for text in self.document.traverse(docutils.nodes.Text):
            if (isinstance(text.parent, docutils.nodes.literal_block) or
                isinstance(text.parent, docutils.nodes.raw)):
                continue
            lines = []
            end_of_last_line = ''
            for line in text.astext().splitlines():
                begin_of_line = line[0] if len(line) > 0 else ''
                if to_be_joined(end_of_last_line, begin_of_line):
                    lines[-1] += line
                else:
                    lines.append(line)
                end_of_last_line = line[-1] if len(line) > 0 else ''
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
