
class AsciiVisitor(object):
    def __init__(self):
        self._result = []
        self._title = ""
        self._subtitle = ""
        self._chorus_flag = False

    def _append_line(self, val, *args):
        self._result.append(val % tuple(args))

    def _append_lines(self, *args):
        for val in args:
            if isinstance(val, tuple):
                self._append_line(*val)
            else:
                self._append_line(val)

    def visit_nl(self):
        self._append_line("")

    def visit_c(self, val):
        lower = val.lower()
        if lower.startswith("chorus") or lower.startswith("refrain"):
            self._append_lines(val, "=" * len(val))
        else:
            self._append_lines(val, "-" * (len(val)))

    def visit_soc(self):
        self._append_lines("Chorus:", 7 * "=")
        self._chorus_flag = True

    def visit_eoc(self):
        self._append_lines(7 * "=")
        self._chorus_flag = False

    def visit_t(self, val):
        self._title = val

    def visit_st(self, val):
        self._subtitle = val

    def visit_line(self, chords):
        line = line_above = "  " if self._chorus_flag else ""
        for chord, text in chords:
            chord = chord if chord else ""
            just = len(line) - len(line_above) + len(chord)
            line_above += chord.rjust(max(just,0))

            # TODO: Skip for last chord
            line += text + (len(chord) - len(text) + 1) * \
                    (" " if len(text) == 0 or text[-1] == " " else "-")

        self._append_lines(line_above, line)

    def result(self):
        title = self._title + " - " + self._subtitle
        line = "+" + "-" * (len(title) + 2) + "+"

        res = [line, "| " + title + " |", line, ""]
        return "\n".join(res + self._result) + "\n"

