
class ChordproVisitor(object):
    def __init__(self):
        self._result = []

    def visit(self, command, *args):
        self._result.append("{%s}" % (":".join((command,) + args)))

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

