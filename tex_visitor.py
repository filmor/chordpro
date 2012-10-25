# -*- encoding: utf-8

from string import Template

class _MyTemplate(Template):
    delimiter = "§"

class TexVisitor(object):
    def __init__(self, template=open("template.tex").read()):
        self._result = []
        self._template = _MyTemplate(template)

    def visit_t(self, title):
        self._title = title

    def visit_st(self, subtitle):
        self._subtitle = subtitle

    def visit_c(self, comment):
        self._result.append("\\textbf{%s}" % comment)
    
    def visit_ci(self, comment):
        self._result.append("\\textit{%s}" % comment)

    def visit_soc(self):
        self._result.append("\\textbf{Chorus}\\begin{textit}")

    def visit_eoc(self):
        self._result.append("\\end{textit}")

    def visit_line(self, chords):
        line = []
        for chord, text in chords:
            if chord is None:
                line.append(text)
            else:
                # Heuristics
                if len(chord) >= len(text):
                    chord += "_"

                line.append("[%s]{%s}" % (chord, text if len(text) else " "))

        self._result.append("".join(line))

    def result(self):
       return self._template.substitute(
               block="\n".join(self._result),
               title=self._title,
               subtitle=self._subtitle
               )

