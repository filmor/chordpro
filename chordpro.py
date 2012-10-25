#!/usr/bin/env python
"""ChordPro Parser"""

from parser import *
from ascii_visitor import *
from chordpro_visitor import *
from transpose_visitor import *
from tex_visitor import *
from xml_visitor import *

if __name__ == '__main__':
    import codecs, argparse, sys

    parser = argparse.ArgumentParser(description="Chordpro converter")

    parser.add_argument('filename')
    parser.add_argument('--format', default="ascii")
    parser.add_argument('--output', default="-")

    args = parser.parse_args()

    file = codecs.open(args.filename, encoding='utf-8')
    out = open(args.output, "w") if args.output != "-" else sys.stdout

    visitor = {
            "ascii": AsciiVisitor,
            "chordpro": ChordproVisitor,
            "xml": XmlVisitor,
            "tex": TexVisitor
        }

    parsed = parse(file)

    out.write(show(parsed, visitor[args.format]))
