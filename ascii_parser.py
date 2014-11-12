#!/usr/bin/env python

from re import compile

_chord_re = compile(r"([A-G](?:b|#)?(?:\w|/)*)")

def parse_verse(s):
    lines = s.split("\n")

    result = []

    k = 0
    for chords, lyrics in zip(lines, lines[1:]):
        k += 1
        if k % 2 == 0:
            continue

        res = []
        
        matches = [ i for i in _chord_re.finditer(chords) ]

        if len(matches) == 0:
            res.append((None, lyrics))
            continue

        if matches[0].start() != 0:
            res.append((None, lyrics[:matches[0].start()]))

        for m, n in zip(matches, matches[1:]):
            res.append((m.group(), lyrics[m.start():n.start()]))

        res.append((matches[-1].group(), lyrics[matches[-1].start():]))

        result.append(("line", res))
    return result

if __name__ == '__main__':
    from chordpro_visitor import ChordproVisitor
    from parser import show
    from sys import stdin, stdout
    from io import TextIOWrapper

    inp = TextIOWrapper(stdin.buffer, encoding="utf-8").read()
    out = show(parse_verse(inp), ChordproVisitor) #.encode("utf-8")

    stdout.write(out)
