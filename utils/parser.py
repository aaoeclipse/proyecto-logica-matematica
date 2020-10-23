# Grafo
import networkx as nx

# Lexical Analyzer
import ply.lex as lex

# Grafo
G = nx.DiGraph()

# List of token names.   This is always required
tokens = (
    'BOOLEAN','LETTER',
    'NEGATIVE','OR','BOTHARROW','RIGHTARROW',
    'BIGO', 'LEFTBRACE', 'RIGHTBRACE'
    )


# Regular expression rules for simple tokens
t_BOTHARROW   = r'\<\=\>'
t_RIGHTARROW  = r'\=\>'
t_LEFTBRACE= r'\('
t_RIGHTBRACE= r'\)'
t_BIGO  = r'o'
t_OR  = r'\^'
t_NEGATIVE  = r'\~'
t_BOOLEAN    = r'[0-1][0-1]*'
t_LETTER = r'[p,q,r,s,t,u,v,w,x,y,z]'

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Give the lexer some input
# lexer.input()

# Tokenize
# for tok in lexer:
#     print(tok)

# Syntax Analyzer
import ply.yacc as yacc

# Precedence rules for the arithmetic operators
precedence = (
    ('left','BOTHARROW','RIGHTARROW', 'OR', 'BIGO'),
    ('right','UNEGATIVE'),
    )

# dictionary of names (for storing variables)
names = { }

def p_expr_unegative(p):
    'expression : NEGATIVE expression %prec UNEGATIVE'
    G.add_node('~')
    G.add_node(p[2])
    # old_node = search_for_node(p[2])
    G.add_edge('~', p[2])
    p[0] = '~{}'.format(p[2])

def p_statement_expr(p):
    'statement : expression'
    print(p[1])

def p_expression_binop(p):
    '''expression : expression OR expression
                  | expression BIGO expression
                  | expression BOTHARROW expression
                  | expression RIGHTARROW expression'''
    global G
    if p[2] == '^'  : 
        G.add_node(p[1])
        G.add_node('^')
        G.add_node(p[3])
        G.add_edge(p[1], '^')
        G.add_edge('^', p[3])
        p[0] = '{}{}{}'.format(p[1],'^',p[3])
    elif p[2] == 'o': 
        G.add_node(p[1])
        G.add_node('o')
        G.add_node(p[3])
        G.add_edge(p[1], 'o')
        G.add_edge('o', p[3])
        p[0] = '{}{}{}'.format(p[1],'o',p[3])
    elif p[2] == '<=>': 
        G.add_node(p[1])
        G.add_node('<=>')
        G.add_node(p[3])
        G.add_edge(p[1], '<=>')
        G.add_edge('<=>', p[3])
        p[0] = '{}{}{}'.format(p[1],'<=>',p[3])
    elif p[2] == '=>': 
        G.add_node(p[1])
        G.add_node('=>')
        G.add_node(p[3])
        G.add_edge(p[1], '=>')
        G.add_edge('=>', p[3])
        p[0] = '{}{}{}'.format(p[1],'=>',p[3])

def p_expression_group(p):
    'expression : LEFTBRACE expression RIGHTBRACE'
    G.add_node('(')
    G.add_node(p[2])
    G.add_node(')')
    G.add_edge('(', p[2])
    G.add_edge(p[2], ')')
    p[0] = '({})'.format(p[2])

def p_expression_letter(p):
    'expression : LETTER'
    p[0] = p[1]

def p_expression_boolean(p):
    'expression : BOOLEAN'
    p[0] = p[1]

def p_error(p):
    print("Syntax error at {}".format(p))

data = '''
p^z
z <=> a
'''
parser = yacc.yacc()

def parse_string(s):
    """
    docstring
    """
    global G
    G = nx.Graph()
    parser.parse(s)

    return G

def search_for_node(s):
    ''' asdfsa '''
    global G
    G = nx.DiGraph()
    # get initial s
    initial_value = s[0]
    print('init: {}'.format(initial_value))
    for node in G.nodes:
        print(node)
        if initial_value == node:
            print(node)
            return node

def show_g():
    global G
    print(G)