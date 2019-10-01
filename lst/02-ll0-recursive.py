# coding: utf-8

#+begin_src python

from collections import namedtuple

class ParserError(RuntimeError):
    pass

class Stream:
    """Eine (ineffiziente) Abstraktion fuer einen Eingabestrom aus Tokens,
       die es erlaubt ein einzelnes Zeichen in die Zukunft zu blicken
       (look-ahead).
    """
    def __init__(self, data):
        self.data = list(data)

    def peek(self):
        """Returns the type of the current token."""
        if len(self.data) > 0:
            return self.data[0][0]

    def read(self, expected=None):
        """Consumes the first token and returns it. If `expected' is given
           the token type is checked and a ParserError is thrown in case."""
        token = self.data.pop(0)
        if expected is not None and token[0] != expected:
            raise ParserError("Expected type: " + str(expected))
        return token[1]

TOK_INT = 0
TOK_PLUS = 1
TOK_EOF = 2

#parser0
def addInt(token_stream):
    # Nur eine Regel: addInt -> Int addIntTail
    ## 'Int': Das erste Token muss ein INT sein
    int_load  = token_stream.read(expected=TOK_INT)
    ## 'addIntTail': Rekursiver Abstieg
    tail_tree = addIntTail(token_stream)
    # Baumstruktur als geschachtelte Listen
    return ("head", int_load, tail_tree) #parser1

#parser2
def addIntTail(token_stream):
    # Verwende Look-Ahead zur Regelauswahl
    if token_stream.peek() == TOK_PLUS:
        # addIntTail -> '+' Int addIntTail
        ## '+': consume the PLUS
        _         = token_stream.read(expected=TOK_PLUS)
        ## 'Int': capture the integer
        int_load  = token_stream.read(expected=TOK_INT)
        ## 'addIntTail': Rekursiver Abstieg!
        tail_tree = addIntTail(token_stream)
        # Baumstruktur zurückgeben
        return ("tail", int_load, tail_tree)
    elif token_stream.peek() == TOK_EOF: #... #parser3
        return None
    else:
        raise ParserError("Expected + or $.")

token_stream = Stream([
    [TOK_INT, 1],
    [TOK_PLUS, None],
    [TOK_INT, 2],
    [TOK_PLUS, None],
    [TOK_INT, 3],
    [TOK_EOF, None]
])

print(addInt(token_stream))
#+end_src
