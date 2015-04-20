import sys
import random

loopVar = 0

tokens = (
    'NAME','NUMBER', 'STRING', 'COMMA', 'SC',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN', 'LBRACKET', 'RBRACKET',
    'LSBRACKET', 'RSBRACKET',
    'PRINT', 'READ', 'RETURN',
    'ITER', 'IF', 'ELSE', 'FOR',
    'LT', 'GT', 'LEQ', 'GEQ', 'DE', 'NE',
    'AND', 'OR', 'NOT',
    'NUM', 'TEXT',
    )

# Tokens

t_COMMA    = r','
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET  = r'\{'
t_RBRACKET  = r'\}'
t_LSBRACKET  = r'\['
t_RSBRACKET  = r'\]'
t_SC  = r';'
t_LT  = r'<'
t_GT  = r'>'
t_LEQ  = r'<='
t_GEQ  = r'>='
t_DE  = r'=='
t_NE  = r'!='
t_NAME    = r'[a-zA-Z_][a-zA-Z0-9_]*'

def getVar():
    global loopVar
    loopVar += 1
    return "loopVar_%s"%loopVar
    

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_RETURN(t):
    r'return'    
    return t

def t_NUM(t):
    r'num'    
    return t

def t_READ(t):
    r'read'    
    return t

def t_AND(t):
    r'and'    
    return t

def t_OR(t):
    r'or'    
    return t

def t_NOT(t):
    r'not'    
    return t

def t_TEXT(t):
    r'text'    
    return t

def t_IF(t):
    r'if'    
    return t

def t_ELSE(t):
    r'else'    
    return t

def t_STRING(t):
    r'"[^"]+"'
    return t
    
def t_PRINT(t):
    r'print'
    return t

def t_FOR(t):
    r'loop'
    return t

def t_ITER(t):
    r'iter'
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lex.lex()

precedence = (
    ('left','AND', 'OR', 'NOT'),
    ('left','LT', 'GT', 'LEQ', 'GEQ', 'DE', 'NE'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    )

# dictionary of names
varTypes = { }

header = ""
functions = ""

def p_start(t):
    'start : statement'
    global body
    body = t[1]

def p_statement_conc(t):
    'statement : statement statement'
    t[0] = "%s\n %s"%(t[1],t[2])

def p_statement_value(t):
    'statement : value'
    t[0] = "%s;"%t[1]

def p_value(t):
    '''value : STRING
              | NUMBER
              | NAME
              | NAME dim'''
    t[0] = t[1]

#arr[3] = 2

############################### COMPARISONS

def p_value_lt(t):
    '''value : value LT value'''
    t[0] = "((%s < %s) ? 1 : 0)"%(t[1], t[3])

def p_value_gt(t):
    '''value : value GT value'''
    t[0] = "((%s > %s) ? 1 : 0)"%(t[1], t[3])

def p_value_leq(t):
    '''value : value LEQ value'''
    t[0] = "((%s <= %s) ? 1 : 0)"%(t[1], t[3])

def p_value_geq(t):
    '''value : value GEQ value'''
    t[0] = "((%s >= %s) ? 1 : 0)"%(t[1], t[3])

def p_value_de(t):
    '''value : value DE value'''
    t[0] = "((%s == %s) ? 1 : 0)"%(t[1], t[3])

def p_value_ne(t):
    '''value : value NE value'''
    t[0] = "((%s != %s) ? 1 : 0)"%(t[1], t[3])

############################### LOPS

def p_value_and(t):
    '''value : value AND value'''
    t[0] = "(((%s != 0) && (%s != 0)) ? 1 : 0)"%(t[1], t[3])

def p_value_or(t):
    '''value : value OR value'''
    t[0] = "(((%s != 0) || (%s != 0)) ? 1 : 0)"%(t[1], t[3])

def p_value_not(t):
    '''value : NOT value'''
    t[0] = "((%s != 0) ? 0 : 1)"%(t[2])

############################### ARITHMETICS

def sumMethod(a, b, ta, tb):
    if ta == "double" and tb == "double":
        return ("%s + %s"%(a,b), "num")
    if ta == "String" or tb == "String":
        return ('%s + %s'%(a,b), "text")

def p_value_plus(t):
    '''value : value PLUS value'''
    """if not isinstance(t[1],tuple):
        a = t[1]
        va = varTypes[t[1]]
    else: (a, va) = t[1]
    if not isinstance(t[3],tuple):
        b = t[3]
        vb = varTypes[t[3]]
    else: (b, vb) = t[3]"""
    #t[0] = sumMethod(a,b,va,vb)
    t[0] = "%s + %s"%(t[1],t[3])

def p_value_minus(t):
    '''value : value MINUS value'''
    t[0] = "%s - %s"%(t[1], t[3])

def p_value_times(t):
    '''value : value TIMES value'''
    t[0] = "%s * %s"%(t[1], t[3])

def p_value_divide(t):
    '''value : value DIVIDE value'''
    t[0] = "%s / %s"%(t[1], t[3])

############################### READ

def p_value_read(t):
    '''value : READ'''
    global header
    header += "import java.io.*;\n"
    t[0] = "(new BufferedReader(new InputStreamReader(System.in))).readLine()"

############################### ASSIGNMENTS

def p_declr(t):
    'statement : typename'
    t[0] = "%s;"%t[1]

def p_type_name(t):
    'typename : type NAME'
    global varTypes
    varTypes[t[2]] = t[1]
    t[0] = "%s %s"%(t[1],t[2])

def p_declr_assign(t):
    'statement : type NAME EQUALS value'
    global varTypes
    varTypes[t[2]] = t[1]
    if isinstance(t[4],tuple): t[4] = t[4][0]
    t[0] = "%s %s = %s;"%(t[1],t[2],t[4])

def p_assign(t):
    'statement : NAME EQUALS value'
    t[0] = "%s = %s;"%(t[1],t[3])


############################### FUNCTIONS

def p_func(t):
    'statement : typename LPAREN rev_params RPAREN LBRACKET statement RBRACKET'
    global functions
    functions += "public static %s ( %s ) { %s }\n"%(t[1],t[3],t[6])
    t[0] = ""

def p_func_no_return(t):
    'statement : NAME LPAREN rev_params RPAREN LBRACKET statement RBRACKET'
    global functions
    functions += "public static void %s ( %s ) { %s }\n"%(t[1],t[3],t[6])
    t[0] = ""

def p_func_call(t):
    'value : NAME LPAREN snd_params RPAREN'
    t[0] = "%s ( %s )"%(t[1],t[3])

def p_params_rev(t):
    '''rev_params : rev_params rev_params
                  | typename
                  | '''
    if len(t) == 1: t[0] = ""
    elif len(t) == 2: t[0] = t[1]
    else: t[0] = "%s, %s"%(t[1],t[2])

def p_params_snd(t):
    '''snd_params : snd_params snd_params
                  | value
                  | '''
    if len(t) == 1: t[0] = ""
    elif len(t) == 2: t[0] = t[1]
    else: t[0] = "%s, %s"%(t[1],t[2])

def p_return(t):
    'statement : RETURN value'
    t[0] = "return %s;"%t[2]

############################### TYPES

def p_typecast(t):
    'value : LPAREN type RPAREN value'
    if t[2] == "double": t[0] = 'Double.parseDouble(%s)'%t[4]
    elif t[2] == "String": t[0] = '"" + %s'%t[4]

def p_type_num(t):
    'type : NUM'
    t[0] = 'double'

def p_type_text(t):
    'type : TEXT'
    t[0] = 'String'

############################### PRINT

def p_statement_print(t):
    'statement : PRINT value'
    t[0] = "System.out.println(%s);"%t[2]

############################### IF

def p_statement_if(t):
    'statement : IF LPAREN value RPAREN LBRACKET statement RBRACKET'
    t[0] = "if((%s) != 0) { %s }"%(t[3],t[6])

def p_statement_else(t):
    'statement : ELSE LBRACKET statement RBRACKET'
    t[0] = "else { %s }"%t[3]

############################### LOOPS

def p_statement_iter(t):
    'statement : ITER LPAREN NUMBER RPAREN LBRACKET statement RBRACKET'
    v = getVar()
    t[0] = "for(int %s = 0; %s < %s; %s++) { %s }"%(v,v,t[3],v,t[6])

def p_statement_for1(t):
    'statement : FOR LPAREN statement COMMA value COMMA statement RPAREN LBRACKET statement RBRACKET'
    v = getVar()
    t[0] = "%s for(; (%s) != 0;) { %s %s}"%(t[3],t[5],t[10],t[7])

def p_statement_for2(t):
    'statement : FOR LPAREN COMMA value COMMA statement RPAREN LBRACKET statement RBRACKET'
    v = getVar()
    t[0] = "for(; (%s) != 0;) { %s %s}"%(t[4],t[9],t[6])

def p_statement_for3(t):
    'statement : FOR LPAREN COMMA value COMMA RPAREN LBRACKET statement RBRACKET'
    v = getVar()
    t[0] = "for(; (%s) != 0;) { %s}"%(t[4],t[8])

def p_statement_for4(t):
    'statement : FOR LPAREN statement COMMA value COMMA RPAREN LBRACKET statement RBRACKET'
    v = getVar()
    t[0] = "%s for(; (%s) != 0;) { %s}"%(t[3],t[5],t[9])

def p_error(t):
    print("Syntax error at '%s'" % t.value)


######################### ARRAYS
#int[ ][ ] aryNumbers = new int[2][3]
def p_array(t):
    '''statement : type dim NAME'''
    dimension = '[]' * t[2].count('[')
    t[0] = "%s %s %s = new %s %s"%(t[1],dimension,t[3],t[1],t[2]) 

def p_multidim(t):
    '''dim : dim dim'''
    t[0] = "%s %s"%(t[1],t[2]) 

def p_dim(t):
    '''dim : LSBRACKET NUMBER RSBRACKET'''
    t[0] = "[%s]"%t[2] 


#num[3] = 2

#multidimention?
#statement?

######################### TABLES

######################### GRAPHS

















import ply.yacc as yacc
yacc.yacc()

input = open(sys.argv[1],"r")

code = ""

for line in input.readlines():
    line = line.replace("\n","")
    line = line.replace(";","")
    if line == "": continue
    if line[:2] == "//": continue
    code += " %s "%line

yacc.parse(code)

print header
print "public class Output {"
print functions
print "public static void main(String[] args) throws Exception {"
print body
print "}}"
