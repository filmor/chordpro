#!/usr/bin/env python
"""ChordPro Parser"""

from parser import *
from ascii_visitor import *
from chordpro_visitor import *
from transpose_visitor import *
from xml_visitor import *

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
