
notes = [('A',),
         ('Bb','A#'),
         ('B', 'Cb'),
         ('C', 'B#'),
         ('C#', 'Db'),
         ('D',),
         ('D#', 'Eb',),
         ('E', 'Fb'),
         ('F', 'E#'),
         ('F#', 'Gb'),
         ('G',),
         ('G#', 'Ab'),
         ]


def note_to_number(name):
    i = 0
    for n in notes:
        if name in n:
            return i
        i += 1
    return -1

def is_equal(lhs, rhs):
    return note_to_number(lhs) == note_to_number(rhs)

def number_to_note(n):
    return notes[n][0]

