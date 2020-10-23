'''
        Lógica mátematica proyecto 3

        PRUEBA DANIELA VILLAMAR

'''

from ply import lex
import ply.yacc as yacc
import json

# Operadores lógicos
tokens = ('MINUS', 'OR', 'AND', 'THEN', 'IFIF', 'LPAREN', 'RPAREN', 'PROP')

t_ignore = ' \t'

t_MINUS   = r'~'
t_OR    = r'o'
t_AND   = r'\^'
t_THEN   = r'=>'
t_IFIF   = r'<=>'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_PROP( t ) :
    r'[p, q, r, s, t, u, v, w, x, y, z]+' # Variables proposicionales de nuestro alfabeto
    return t

def t_newline( t ):
  r'\n+'
  t.lexer.lineno += len( t.value )

def t_error( t ):
  print("Invalid Token:",t.value[0])
  t.lexer.skip( 1 )

#atributo necesario
lexer = lex.lex()

precedence = (
    ( 'left', 'OR', 'AND' ),
    ( 'left', 'THEN', 'IFIF' ),
    ( 'nonassoc', 'UMINUS' )
)

def p_OR(p) :
    'expr : expr OR expr'
    p[0] = {p[2]:{0:p[1], 1:p[3]}}

def p_AND(p) :
    'expr : expr AND expr'
    p[0] = {p[2]:{0:p[1], 1:p[3]}}


def p_THEN(p) :
    'expr : expr THEN expr'
    p[0] = {p[2]:{0:p[1], 1:p[3]}}

def p_IFIF(p) :
    'expr : expr IFIF expr'
    p[0] = {p[2]:{0:p[1], 1:p[3]}}

def p_expr2uminus(p) :
    'expr : MINUS expr %prec UMINUS'
    p[0] = {p[1]:p[2]}


def p_parens(p) :
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Syntax error in input!")

def p_expr2NUM(p) :
    'expr : PROP'
    p[0] = p[1]

parser = yacc.yacc()

def parse(expresion):
    res = parser.parse(expresion)
    js = json.dumps(res, indent=3)
    return js


# expresion = input("Ingrese la expresion a evaluar: ")
# res = parser.parse(expresion)
# js = json.dumps(res, indent=3)
# print('Resultado: ', expresion)
# print(js)
