#!/usr/bin/env python
"""ChordPro Parser"""

from ascii_visitor import *
from chordpro_visitor import *
from transpose_visitor import *
from xml_visitor import *

def my_partition(string, sep):
    a, b, c = string.partition(sep)
    return (a, b + c)

def parse_line(string):
    line = ""
    chords = []
    string = string.strip()
    if string.startswith('#'):
        return ("comment", string[1:])
    if string.startswith('{'):
        return ("command",) + tuple(string.strip('{} ').split(":", 1))
    if not string.startswith('['):
        start, string = my_partition(string, '[')
        chords.append((None, start))
    while string:
        before, _, after = string.partition(']')
        if not before.startswith('['):
            raise Exception("Aye")
        _, _, chord = before.partition('[')
        line, string = my_partition(after, '[')
        chords.append((chord, line))
    return ("line", chords) if chords != [(None, '')] else ("command", "nl",)

def parse(stream):
    res = []
    for i in stream.readlines():
        parsed = parse_line(i.rstrip())
        if parsed:
            res.append(parsed)
    return res

def dispatch(parsed, visitor):
    def visit(flag, *args):
        f = lambda *args2: None
        if hasattr(visitor, "visit_" + flag):
            f = getattr(visitor, "visit_" + flag)
        elif hasattr(visitor, "visit"):
            f = lambda *args2: visitor.visit(flag, *args2)
        return f(*args)

    for el in parsed:
        type = el[0]
        val = el[1:]
        if type == "command":
            visit(val[0], *val[1:])
        elif type == "comment":
            visit("comment", *val)
        elif type == "line":
            visit("line", *val)
        else:
            visit(type, *val)

def show(parsed, visitor_class, *args):
    visitor = visitor_class(*args)
    dispatch(parsed, visitor)
    return visitor.result()

if __name__ == '__main__':
    import codecs, argparse

    parser = argparse.ArgumentParser(description="Chordpro converter")

    parser.add_argument('filename')
    parser.add_argument('--type', default="ascii")

    args = parser.parse_args()

    file = codecs.open(args.filename, encoding='utf-8')

    visitor = {
            "ascii": AsciiVisitor,
            "chordpro": ChordproVisitor,
            "xml": XmlVisitor
        }

    parsed = parse(file)

    print show(parsed, visitor[args.type])
