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
    parser.add_argument('--format', '-f', default="ascii")
    parser.add_argument('--output', '-o', default="-")
    parser.add_argument('--transpose', '-t', default=0, type=int)

    args = parser.parse_args()

    file = codecs.open(args.filename, encoding='utf-8') \
            if args.filename != "-" else sys.stdin
    out = open(args.output, "w") if args.output != "-" else sys.stdout

    visitor = {
            "ascii": AsciiVisitor,
            "chordpro": ChordproVisitor,
            "xml": XmlVisitor,
            "tex": TexVisitor
        }

    parsed = parse(file)

    if args.transpose != 0:
        parsed = show(parsed, TransposeVisitor, args.transpose)

    out.write(show(parsed, visitor[args.format]))
