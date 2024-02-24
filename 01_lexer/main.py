import sys, ply.lex, datetime

STUDENTNAME = "Joonas Pelttari"
STUDENTID = 274830
HELPMESSAGE = '''
usage: main.py [-h] [--who | -f FILE]
  -h, --help            show this help message and exit
  --who                 print out student IDs and NAMEs of authors
  -f FILE, --file FILE  filename to process
'''

reserved = {
    'var': 'VAR',
    'is': 'IS',
    'unless': 'UNLESS',
    'otherwise': 'OTHERWISE',
    'until': 'UNTIL',
    'do': 'DO',
    'done': 'DONE',
    'procedure': 'PROCEDURE',
    'function': 'FUNCTION',
    'return': 'RETURN',
    'print': 'PRINT',
    'end': 'END',
}

tokens = [
    'LPAREN','RPAREN','LSQUARE','RSQUARE','LCURLY',
    'RCURLY','APOSTROPHE','AMPERSAND','COMMA','DOT',
    'EQ','LT','PLUS','MINUS','MULT','DIV','INT_LITERAL',
    'STRING', 'COMMENT', 'IDENT', 'DATE_LITERAL',
    'FUNC_IDENT', 'PROC_IDENT',
    ]
tokens += reserved.values()

# one and two letter tokens:
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'

t_APOSTROPHE = r'\''
t_AMPERSAND = r"\&"
t_COMMA = r','
t_DOT = r'\.'
t_EQ = r'\='
t_LT = r'\<'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'

# longer tokens


def t_STRING(t):
    r'"([^"]*)"'
    t.value = t.value.replace('"', '')
    return t

def t_DATE_LITERAL(t):
    r'\d{4}-\d{2}-\d{2}'
    try:
        t.value = datetime.date(
            int(t.value[0:4]), int(t.value[5:7]), int(t.value[8:10]))
    except ValueError:
        print(f"line {t.lexer.lineno}: Invalid Date")
        sys.exit(1)
    return t

def t_INT_LITERAL(t):
    r'-?\d{1,3}(\'\d{3})*'
    t.value = t.value.replace("'", "")
    t.value = int(t.value)
    if abs(t.value) >= 1_000_000_000_000:
        print(f"line {t.lexer.lineno}: INT_LITERAL too large")
        sys.exit(1)
    return t

def t_COMMENT(t):
    r'\(%[^%]*%\)'
    # comments can span to multiple lines. This keeps count of correct line num
    t.lexer.lineno += t.value.count("\n")
    pass

def t_IDENT(t):
    r'[a-z][a-zA-Z0-9_]{1,}'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_FUNC_IDENT(t):
    r'[A-Z][a-z0-9_]{1,}'
    return t

def t_PROC_IDENT(t):
    r'[A-Z]{2}[A-Z0-9_]*'
    return t

t_ignore = " "

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    raise Exception("Illegal character '{}' at line {}".format( 
        t.value[0], t.lexer.lineno ) )

lexer = ply.lex.lex()


def handleArguments(args):
    if '-h' in args or '--help' in args:
        print(HELPMESSAGE)
    if '--who' in args:
        print(STUDENTNAME, STUDENTID)
    if '-f' in args or '--file' in args:
        return args[-1]
    else:
        print(HELPMESSAGE)
    sys.exit(0)

if __name__ == "__main__":
    fileName = handleArguments(sys.argv)
    with open(fileName, 'r', encoding='utf-8') as file:
        data = file.read()
    lexer.input(data)
    token = lexer.token()
    while token:
        print(token)
        token = lexer.token()
