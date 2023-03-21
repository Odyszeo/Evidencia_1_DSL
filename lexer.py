import re
from collections import namedtuple

# Definir una clase Token para representar un token
Token = namedtuple('Token', ['type', 'value'])

# Implementar el analizador léxico utilizando expresiones regulares
TOKENS = [
    ('ADELANTE', r'adelante'),
    ('ATRAS', r'atras'),
    ('IZQUIERDA', r'izquierda'),
    ('DERECHA', r'derecha'),
    ('LEVANTAR', r'levantar'),
    ('BAJAR', r'bajar'),
    ('COLOR', r'color'),
    ('LIMPIAR', r'limpiar'),
    ('CENTRO', r'centro'),
    ('REPETIR', r'repetir'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('VECES', r'veces'),
    ('VALOR', r'[0-9]+'),
    ('ESPACIO', r'\s+'),
    ('VARIABLE', r'[a-zA-Z][a-zA-Z0-9_]*')
]

# Crear el analizador léxico a partir de las expresiones regulares
lexer = re.compile('|'.join('(?P<%s>%s)' % pair for pair in TOKENS))

def tokenize(code):
    tokens = []
    for match in lexer.finditer(code):
        tipo = match.lastgroup
        valor = match.group()
        if tipo == 'ESPACIO':
            continue
        elif tipo == 'ADELANTE' or tipo == 'ATRAS' or tipo == 'IZQUIERDA' or tipo == 'DERECHA' or tipo == 'COLOR' or tipo == 'REPETIR':
            tokens.append(Token(type(valor.upper()), valor))
        elif tipo == 'VALOR':
            tokens.append(Token(tipo, int(valor)))
        else:
            tokens.append(Token(tipo, valor))
    return tokens