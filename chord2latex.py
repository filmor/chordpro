#!/usr/bin/python3

from string import Template
from functools import wraps
import re
import sys
from note import *
from optparse import OptionParser

directive=r"\{((?P<name>\w*):)?(?P<val>[^\}]*)\}"
regex = re.compile(directive)

class MyTemplate(Template):
    delimiter = "§"

template = MyTemplate(open("template.tex").read())

title = ""
subtitle = ""
transpose = 0

def subs_decorator(func):
    def my_func(match):
        return func(**match.groupdict())
    return my_func

@subs_decorator
def transpose_chord(chord):
    chord_regex = re.compile(r"([A-G](?:b|#)?)")
    def do_transpose(matches):
        
        return number_to_note(((note_to_number(match.group(0)) + transpose) % 12))
    return chord_regex.sub(do_transpose, chord)

last_chord = None
@subs_decorator
def simplify_chord(chord):
    # Remove slash
    global last_chord
    # chord = re.sub(r"(\([^)]*\)|(?<=[^A-Z])(b5|#|5|7)|[^A-Z/mb75#]|maj|dim|/.*)", "", chord)
    if last_chord == chord:
        return ""
    else:
        last_chord = chord
        return chord

@subs_decorator
def retex_chord(chord):
    # TODO
    return chord

@subs_decorator
def adjust_chordname(chord, syl):
    ins = ""
    if chord == "":
        return syl
    if len(chord) > len(syl):
        ins = "_"
    return "[%s%s]%s" % (chord, ins, syl, )

chord_regex = r"\[(?P<chord>[^\]]*)\]"
subs = [
        # Correct latex characters
        (r"_", r"\_"),
        # Simplify chords
        (chord_regex, lambda m : '[' + simplify_chord(m) + ']'),
        # Transpose chords
        (chord_regex, lambda m : '[' + transpose_chord(m) + ']'),
        # ReTeX chords
        (chord_regex, lambda m : '[' + retex_chord(m) + ']'),
        # Fix chord positioning
        (chord_regex + r"([^\\\s\[]{1,3})", r"[\1]{\2}"),
        # Add a _ if the chord is longer than the syllable
        (chord_regex + r"(?P<syl>[^ \[]+)", adjust_chordname),
        # Fix chords at line endings
        (r"_?\]\s*$", "]{ }\n"),
        # Fix consecutive chords
        (r"\] *\[", r" ] ["),
        (chord_regex + r" +", r"[\1|] "),
        ]

subs = [ (re.compile(a), b) for a,b in subs ]

def apply_subs(line):
    for regex, val in subs:
        line = regex.sub(val, line)
    return line

def process_line(line):
    global title
    global subtitle
    global last_chord
    last_chord = None
    if line.startswith('#'):
        return '%' + line[1:]
    else:
        match = regex.match(line)
        if match is None:
            return apply_subs(line)
        name, val = match.group('name'), match.group('val')

        if name == 't' or name == 'title':
            title = val
        elif name == 'st' or name == 'subtitle':
            subtitle = val
        elif name == 'c' or name == 'comment':
            return "\n\\textbf{%s}\n" % val
        elif name == 'ci' or name == 'comment_italic':
            return "\n\\textit{%s}\n" % val
        elif val == "soc" or val == "start_of_chorus":
            return "\n\\textbf{Refrain}\\begin{textit}\n"
        elif val == "eoc" or val == "end_of_chorus":
            return "\n\\end{textit}\n"
        else:
            raise "Bla"

if __name__ == '__main__':
    op = OptionParser()
    add = op.add_option
    add("-t", "--transpose", type="int", default=0)
    (options, args) = op.parse_args()
    transpose = options.transpose
    in_file = None
    out_file = None
    if len(args) > 2:
        sys.exit(1)
    if len(args) < 2 or args[1] == "-":
        out_file = sys.stdout
    else:
        out_file = open(args[1], "w")

    if len(args) == 0 or args[0] == "-":
        in_file = sys.stdin
    else:
        in_file = open(args[0], "r")

    guitarblock = ""
    for line in in_file.readlines():
        guitarblock += process_line(line) or ""
    res = template.substitute(block=guitarblock, title=title, subtitle=subtitle)
    print(res, file=out_file)
