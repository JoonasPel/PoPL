#!/usr/bin/env python3

import ply.yacc
import ply.lex
import lexer # previous phase example snippet code

# Simple debuggin function to call from syntax rules
symbolnum=0
def debug_syntax(p):
  global symbolnum
  symbolnum=symbolnum+1
  p[0] = symbolnum
  msg = ""
  for i,s in enumerate(p.slice):
    if s is not None:
      if type(s) is ply.lex.LexToken:
        msg = msg + str(s.type)+"<" + str(s.value) + "> "
      else:
        msg = msg + str(s)+"("+str(p[i])+")" + " "
    else:
      msg = msg + "?? "
    if i == 0:
      msg = msg + ":: "
  print(msg)

# tokens are defined in lex-module, but needed here also in syntax rules
tokens = lexer.tokens

# any function starting with 'p_' is PLY yacc rule
# first definition is the target we want to reduce
# in other words: after processing all input tokens, if this start-symbol
# is the only one left, we do not have any syntax errors
def p_program(p):
    '''program : statement_list
               | opt_definitions statement_list'''
    debug_syntax(p)

def p_empty(p):
    '''empty : '''
    debug_syntax(p)


def p_statement_list(p):
    '''statement_list : statement
                      | statement_list COMMA statement'''
    debug_syntax(p)

def p_definitions(p):
    '''definitions : function_definition
                   | procedure_definition
                   | variable_definition'''
    debug_syntax(p)

def p_opt_definitions(p):
    '''opt_definitions : opt_definitions definitions
                       | empty'''
    debug_syntax(p)

def p_variable_definition(p):
    '''variable_definition : VAR IDENT EQ expression'''
    debug_syntax(p)

def p_opt_variable_definition(p):
    '''opt_variable_definition : opt_variable_definition variable_definition
                               | empty'''
    debug_syntax(p)

def p_function_definition(p):
    '''function_definition : FUNCTION FUNC_IDENT LCURLY opt_formals RCURLY RETURN IDENT opt_variable_definition IS rvalue END FUNCTION'''
    debug_syntax(p)


def p_procedure_definition(p):
    '''procedure_definition : PROCEDURE PROC_IDENT LCURLY opt_formals RCURLY opt_return_type opt_variable_definition IS statement_list END PROCEDURE'''
    debug_syntax(p)

def p_opt_return_type(p):
    '''opt_return_type : RETURN IDENT
                       | empty'''
    debug_syntax(p)

def p_formals(p):
    '''formals : formal_arg
               | formals COMMA formal_arg'''
    debug_syntax(p)

def p_opt_formals(p):
    '''opt_formals : formals
                   | empty'''
    debug_syntax(p)

def p_formal_arg(p):
    '''formal_arg : IDENT LSQUARE IDENT RSQUARE'''
    debug_syntax(p)

def p_procedure_call(p):
    '''procedure_call : PROC_IDENT LPAREN opt_args RPAREN'''
    debug_syntax(p)

def p_arguments(p):
    '''arguments : expression
                 | arguments COMMA expression'''
    debug_syntax(p)

def p_opt_args(p):
    '''opt_args : arguments
                | empty'''
    debug_syntax(p)

def p_assignment(p):
    '''assignment : lvalue EQ rvalue
                  | IDENT DOT IDENT'''
    debug_syntax(p)

def p_lvalue(p):
    '''lvalue : IDENT
              | IDENT DOT IDENT'''
    debug_syntax(p)

def p_rvalue(p):
    '''rvalue : expression
              | unless_expression'''
    debug_syntax(p)

def p_print_statement(p):
    '''print_statement : PRINT printlist'''
    debug_syntax(p)

def p_printlist(p):
    '''printlist : printitem
                 | printlist AMPERSAND printitem'''
    debug_syntax(p)

def p_printitem(p):
    '''printitem : STRING
                  | expression'''
    debug_syntax(p)

def p_statement(p):
    '''statement : procedure_call
                 | assignment
                 | print_statement
                 | unless_statement
                 | DO statement_list UNTIL expression
                 | RETURN expression'''
    debug_syntax(p)

def p_unless_statement(p):
    '''unless_statement : DO statement_list UNLESS expression opt_otherwise DONE'''
    debug_syntax(p)

def p_opt_otherwise(p):
    '''opt_otherwise : OTHERWISE statement_list
                     | empty'''
    debug_syntax(p)

def p_expression(p):
    '''expression : simple_expr
                  | expression relation_op simple_expr'''
    debug_syntax(p)

def p_relation_op(p):
    '''relation_op : EQ
                   | LT'''
    debug_syntax(p)

def p_simple_expr(p):
    '''simple_expr : term
                   | simple_expr add_or_minus term'''
    debug_syntax(p)

def p_add_or_minus(p):
    '''add_or_minus : PLUS
                    | MINUS'''
    debug_syntax(p)

def p_term(p):
    '''term : factor
            | term MULT factor
            | term DIV factor'''
    debug_syntax(p)

def p_factor(p):
    '''factor : atom
              | PLUS atom  
              | MINUS atom'''
    debug_syntax(p)

def p_atom(p):
    '''atom : IDENT
            | IDENT APOSTROPHE IDENT
            | INT_LITERAL
            | DATE_LITERAL
            | function_call
            | procedure_call
            | LPAREN expression RPAREN'''
    debug_syntax(p)

def p_function_call(p):
    '''function_call : FUNC_IDENT LPAREN opt_args RPAREN'''
    debug_syntax(p)

def p_unless_expression(p):
    '''unless_expression : DO expression UNLESS expression OTHERWISE expression DONE'''
    debug_syntax(p)

def p_error(p):
    #6:Syntax Error (token: 'something')
    print( f"{p.lineno}:Syntax Error (token: '{p.value}')" )
    raise SystemExit

parser = ply.yacc.yacc()

if __name__ == '__main__':
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-d', '--debug', action='store_true', help='debug?' )
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()
    Debug = True if ns.debug else False
    if ns.who == True:
        # identify who wrote this
        print( 'H274830 Joonas Pelttari' )
    elif ns.file is None:
        # user didn't provide input filename
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        result = parser.parse(data, lexer=lexer.lexer, debug=Debug )
        print( 'syntax OK' )

