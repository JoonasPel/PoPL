import sys, ply.lex

STUDENTNAME = "Joonas Pelttari"
STUDENTID = 274830
HELPMESSAGE = '''
usage: main.py [-h] [--who | -f FILE]
  -h, --help            show this help message and exit
  --who                 print out student IDs and NAMEs of authors
  -f FILE, --file FILE  filename to process
'''

tokens = [
    'LPAREN','RPAREN','LSQUARE','RSQUARE','LCURLY',
    'RCURLY','APOSTROPHE','AMPERSAND','COMMA','DOT',
    'EQ','LT','PLUS','MINUS','MULT','DIV','INT_LITERAL',
    'STRING', 'COMMENT'
]+['VAR', 'IS', 'UNLESS', 'OTHERWISE', 'UNTIL', 'DO', 'DONE',
   'PROCEDURE', 'FUNCTION', 'RETURN', 'PRINT', 'END']

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

# keywords. \b is used to get boundaries so i.e. printed doesnt trigger print
t_VAR = r'\bvar\b'
t_IS = r'\bis\b'
t_UNLESS = r'\bunless\b'
t_OTHERWISE = r'\botherwise\b'
t_UNTIL = r'\buntil\b'
t_DO = r'\bdo\b'
t_DONE = r'\bdone\b'
t_PROCEDURE = r'\bprocedure\b'
t_FUNCTION = r'\bfunction\b'
t_RETURN = r'\breturn\b'
t_PRINT = r'\bprint\b'
t_END = r'\bend\b'

# longer tokens
t_STRING = r'"([^"]*)"'

# todo thousand separator
def t_INT_LITERAL(t):
    r'-?[0-9]+'
    t.value = int(t.value)
    if abs(t.value) >= 1_000_000_000_000:
        print("ERROR! INT_LITERAL TOO LARGE OR SMALL. Line:", t.lexer.lineno)
        sys.exit(1)
    return t

# todo: fix newlines and line counting 
def t_COMMENT(t):
    r'%[^%]*%'
    pass

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
    print("Starting to process file:", fileName)
    with open(fileName, 'r', encoding='utf-8') as file:
        data = file.read()
    lexer.input(data)
    token = lexer.token()
    while token:
        print(token)
        token = lexer.token()












    
