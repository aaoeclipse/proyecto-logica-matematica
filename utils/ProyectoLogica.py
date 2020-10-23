from ply import lex
import ply.yacc as yacc
import json

tokens = ('NEGATE', 'OR', 'AND', 'THEN', 'DOUBLEIF', 'LPAREN', 'RPAREN', 'LETTER')

t_ignore = ' \t'

t_NEGATE   = r'~'
t_OR    = r'o'
t_AND   = r'\^'
t_THEN   = r'=>'
t_DOUBLEIF   = r'<=>'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_LETTER( t ) :
    r'[p, q, r, s, t, u, v, w, x, y, z]+'
    return t

def t_newline( t ):
  r'\n+'
  t.lexer.lineno += len( t.value )

def t_error( t ):
  print("Invalid Token:",t.value[0])
  t.lexer.skip( 1 )

lexer = lex.lex()

precedence = (
    ( 'left', 'OR', 'AND' ),
    ( 'left', 'THEN', 'DOUBLEIF' ),
    ( 'nonassoc', 'UNEGATE' )
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

def p_DOUBLEIF(p) :
    'expr : expr DOUBLEIF expr'
    p[0] = {p[2]:{0:p[1], 1:p[3]}}

def p_expr2uNEGATE(p) :
    'expr : NEGATE expr %prec UNEGATE'
    p[0] = {p[1]:p[2]}


def p_parens(p) :
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Syntax error in input!")

def p_expr2NUM(p) :
    'expr : LETTER'
    p[0] = p[1]

parser = yacc.yacc()

def parse(expresion):
    res = parser.parse(expresion)
    js = json.dumps(res, indent=3)
    return js