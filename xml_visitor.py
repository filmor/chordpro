import lxml.etree as et
from datetime import datetime

_dt_format = "%Y-%m-%dT%H:%M:%S+00:00"

class XmlVisitor(object):
    def __init__(self, transpose=0):
        self._root = et.Element(
                "song",
                attrib={
                    "xmlns": "http://openlyrics.info/namespace/2009/song",
                    "version": "0.8",
                    "createdIn": "chordpro.py 0.1",
                    "modifiedDate": datetime.utcnow().strftime(_dt_format)
                    })

        prop = et.SubElement(self._root, "properties")
        self._titles_node = et.SubElement(prop, "titles")
        self._authors_node = et.SubElement(prop, "authors")
        self._lyrics_node = et.SubElement(self._root, "lyrics")
        if transpose != 0:
            et.SubElement(prop, "transposition").text = transpose

        self._verse = None
        self._lines = None
        self._last_node = None
        self._verse_count = 0
        self._chorus_count = 0

    def _fix_last_lines(self):
        if not self._lines is None:
            for el in reversed(self._lines):
                if el.tail is None:
                    if el.tag == "chord":
                        el.tail = " "
                        break
                    elif el.tag == "br":
                        self._lines.remove(el)
                else:
                    break

    def _new_verse(self, name=None):
        if name is None:
            self._verse_count += 1
            name = "v%d" % self._verse_count

        self._fix_last_lines()

        self._verse = et.SubElement(self._lyrics_node, "verse", {"name": name})
        self._lines = et.SubElement(self._verse, "lines")
        self._last_node = None

    def _append_node(self, *args, **kwargs):
        if self._lines is None:
            self._new_verse()
        self._last_node = et.SubElement(self._lines, *args, **kwargs)
        return self._last_node

    def visit_t(self, val):
        et.SubElement(self._titles_node, "title").text = val

    def visit_st(self, val):
        et.SubElement(self._authors_node, "author").text = val

    def visit_c(self, val):
        if self._lines is None:
            self._new_verse()
        # subelement!
        self._lines.attrib["part"] = val

    def visit_nl(self):
        if self._lines is None:
            self._new_verse()
        if not (self._lines.text is None and len(self._lines) == 0):
            # self._lines = et.SubElement(self._verse, "lines")
            self._append_node("br")

    def visit_comment(self, val):
        pass

    def visit_soc(self):
        self._chorus_count += 1
        self._new_verse("c%d" % self._chorus_count)

    def visit_eoc(self):
        self._new_verse()

    def visit_line(self, chords):
        for chord, text in chords:
            if chord:
                self._append_node("chord", {"name": chord})
            if not self._last_node is None:
                self._last_node.tail = text
            else:
                self._lines.text = text
        self._append_node("br")

    def result(self):
        self._fix_last_lines()
        return et.tostring(self._root, encoding="utf-8", pretty_print="True",
                           xml_declaration=True)

