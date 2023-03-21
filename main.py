import re
import turtle
from lexer import Token

# Definiendo la gramática del lenguaje DSL utilizando la notación BNF
GRAMMAR = '''
programa ::= instruccion*
instruccion ::= "adelante" valor
               | "atras" valor
               | "izquierda" valor
               | "derecha" valor
               | "levantar"
               | "bajar"
               | "color" COLORVAL
               | "limpiar"
               | "centro"
               | repetir
repetir ::= "repetir" valor "veces" "{" instruccion* "}"
valor ::= [0-9]+ | STRING

'''

# Implementando el analizador léxico utilizando expresiones regulares
TOKENS = [('ADELANTE', r'adelante'), ('ATRAS', r'atras'),
          ('IZQUIERDA', r'izquierda'), ('DERECHA', r'derecha'),
          ('LEVANTAR', r'levantar'), ('BAJAR', r'bajar'), ('COLOR', r'color'),('COLORVAL', r'red|green|blue|black|white'),('VECES', r'veces'),
('STRING', r'"[^"]*"'),
          ('LIMPIAR', r'limpiar'), ('CENTRO', r'centro'),
          ('REPETIR', r'repetir'), ('LBRACE', r'\{'), ('RBRACE', r'\}'),
          ('VALOR', r'[0-9]+'), ('ESPACIO', r'\s+')]

# Crear el analizador léxico a partir de las expresiones regulares
lexer = re.compile('|'.join('(?P<%s>%s)' % pair for pair in TOKENS))


# Implementar el parser utilizando el método de descenso recursivo
class Parser:

  def set_color(self, valor):
    if valor in self.colors:
      turtle.pencolor(self.colors[valor])
    else:
      raise ValueError(f'Error: valor de color desconocido {valor}')

  def __init__(self, tokens):
    self.tokens = tokens
    self.pos = 0
    self.colors = {
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255)
    }
    

  def programa(self):
    while self.pos < len(self.tokens):
      self.instruccion()

  def instruccion(self):
    token = self.tokens[self.pos]
    if token.type == 'ADELANTE':
      self.pos += 1
      valor = int(self.tokens[self.pos].value)
      self.pos += 1
      self.adelante(valor)
    elif token.type == 'COLOR':
      self.pos += 1
      valor = self.tokens[self.pos].value
      self.pos += 1
      self.color(valor)
    elif token.type == 'ATRAS':
      self.pos += 1
      valor = int(self.tokens[self.pos].value)
      self.pos += 1
      self.atras(valor)
    elif token.type == 'IZQUIERDA':
      self.pos += 1
      valor = int(self.tokens[self.pos].value)
      self.pos += 1
      self.izquierda(valor)
    elif token.type == 'DERECHA':
      self.pos += 1
      valor = int(self.tokens[self.pos].value)
      self.pos += 1
      self.derecha(valor)
    elif token.type == 'LEVANTAR':
      self.pos += 1
      self.levantar()
    elif token.type == 'BAJAR':
      self.pos += 1
      self.bajar()
    elif token.type == 'COLOR':
      self.pos += 1
      valor = int(self.tokens[self.pos].value)
      self.pos += 1
      self.color(valor)
    elif token.type == 'LIMPIAR':
      self.pos += 1
      self.limpiar()
    elif token.type == 'CENTRO':
      self.pos += 1
      self.centro()
    elif token.type == 'REPETIR':
      self.pos += 1
      veces = int(self.tokens[self.pos].value)
      self.pos += 1
      self.match('LBRACE')
      for i in range(veces):
        self.instruccion()
      self.match('RBRACE')

  def adelante(self, valor):
    turtle.forward(valor)

  def atras(self, valor):
    turtle.backward(valor)

  def izquierda(self, valor):
    turtle.left(valor)

  def derecha(self, valor):
    turtle.right(valor)

  def levantar(self):
    turtle.penup()

  def bajar(self):
    turtle.pendown()

  def color(self, valor):
    turtle.pencolor(valor)

  def limpiar(self):
    turtle.reset()

  def centro(self):
    turtle.home()

  def match(self, type):
    if self.tokens[self.pos].type == type:
      self.pos += 1
    else:
      raise SyntaxError(f'Error de sintaxis: se esperaba {type}')

  def parse(self):
    self.programa()
    return True

  


if __name__ == '__main__':
  # Pedir al usuario que ingrese el archivo que contiene el codigo a ingresar
  print("¿Cual es el nombre del archivo que desea que se lea?")
  archivo = input()
  with open(archivo, 'r') as file:
    codigo = file.read()
    parser = Parser(list(lexer.finditer(codigo)))

  # Se analiza léxicamente el código
  tokens = []
  for match in lexer.finditer(codigo):
    tipo = match.lastgroup
    valor = match.group()
    if tipo == 'ESPACIO':
      continue
    elif tipo == 'ADELANTE' or tipo == 'ATRAS' or tipo == 'IZQUIERDA' or tipo == 'DERECHA' or tipo == 'COLOR' or tipo == 'REPETIR':
      tokens.append(Token(tipo, valor))
    else:
      tokens.append(Token(tipo, valor))

  # Se analiza sintácticamente el código y se ejecuta
  parser = Parser(tokens)
  try:
    parser.parse()
  except SyntaxError as error:
    print(error)

  # Se muestra la ventana de turtle
  turtle.mainloop()
