from parser import shorten, lengthen

class ChordproVisitor(object):
    def __init__(self, short_directives=False):
        self._result = []
        self._transform = shorten if short_directives else lengthen

    def visit(self, command, *args):
        self._result.append(
                "{%s}" % (":".join((self._transform(command),) + args)))

    def visit_comment(self, text):
        self._result.append("# %s" % text)

    def visit_nl(self):
        self._result.append("")

    def visit_line(self, chords):
        line = ""
        for chord, text in chords:
            if chord:
                line += "[%s]" % chord
            line += text
        self._result.append(line)

    def result(self):
        return "\n".join(self._result)

