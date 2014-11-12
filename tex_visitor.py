# -*- encoding: utf-8

from string import Template
from _texcaller import escape_latex

def indicate_last(iterable):
    i = 0
    l = len(iterable)
    for x in iterable:
        i += 1
        yield i == l, x

class _MyTemplate(Template):
    delimiter = "§"

class TexVisitor(object):
    def __init__(self, template=None):

        if not template:
            template = open("template.tex").read()
        self._result = []
        self._template = _MyTemplate(template)
        self._title = ""
        self._subtitle = ""

    def visit_t(self, title):
        self._title = title

    def visit_st(self, subtitle):
        self._subtitle = subtitle

    def visit_c(self, comment):
        self._result.append("\\textbf{%s}" % escape_latex(comment))
    
    def visit_ci(self, comment):
        self._result.append("\\textit{%s}" % escape_latex(comment))

    def visit_soc(self):
        self._result.append("\\textbf{Chorus}\\begin{textit}")

    def visit_eoc(self):
        self._result.append("\\end{textit}\\textbf{End of Chorus}")

    def visit_nl(self):
        self._result.append("")

    def visit_line(self, chords):
        line = []
        for last, (chord, text) in indicate_last(chords):
            text = escape_latex(text)
            if chord is None:
                line.append(text)
            else:
                if text.isspace() or len(text) == 0:
                    line.append("\guitarChord{%s}%s" %
                            (chord + "|", "{ }" if last else " ")
                            )
                else:
                    if len(chord) >= len(text.strip()):
                        if not text[-1].isspace():
                            if not last:
                                chord += "_"
                                text = "{%s}" % text
                        else:
                            chord += "|"
                            text = "{%s}" % text

                    line.append("\guitarChord{%s}%s" % (chord, text))

        self._result.append("".join(line))

    def result(self):
       return self._template.substitute(
               block="\n".join(self._result),
               title=escape_latex(self._title),
               subtitle=escape_latex(self._subtitle),
               diagrams="",
               )

