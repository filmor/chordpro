__all__ = ["parse", "dispatch", "show", "shorten", "lengthen"]

def my_partition(string, sep):
    a, b, c = string.partition(sep)
    return (a, b + c)

shorten_map = {
    "title": "t",
    "subtitle": "st",
    "comment": "c",
    "define": "d",
    "start_of_chorus": "soc",
    "end_of_chorus": "eoc",
    "start_of_tab": "sot",
    "end_of_tab": "eot"
}
shorten = lambda name: lengthen_map.get(name, name)

lengthen_map = dict((v, k) for k, v in shorten_map.iteritems())
lengthen = lambda name: lengthen_map.get(name, name)

def parse_line(string):
    line = ""
    chords = []
    string = string.strip()
    if string.startswith('#'):
        return ("comment", string[1:])
    if string.startswith('{'):
        s = string.strip('{} ').split(":", 1)
        directive = s[0]
        args = (s[1].strip("{} "),) if len(s) == 2 else ()
        directive = shorten_map.get(directive, directive)
        return ("directive", directive) + args
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
    return ("line", chords) if chords != [(None, '')] else ("directive", "nl",)

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
        if type == "directive":
            visit(val[0], *val[1:])
        else:
            visit(type, *val)

def show(parsed, visitor_class, *args):
    visitor = visitor_class(*args)
    dispatch(parsed, visitor)
    return visitor.result()

