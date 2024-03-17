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
    '''function_definition : FUNCTION FUNC_IDENT LCURLY RCURLY
                           | FUNCTION FUNC_IDENT LCURLY formals RCURLY
                           | RETURN IDENT opt_variable_definition IS
                           | rvalue END FUNCTION'''
    debug_syntax(p)


def p_procedure_definition(p):
    '''procedure_definition : PROCEDURE PROC_IDENT LCURLY RCURLY
                            | PROCEDURE PROC_IDENT LCURLY formals RCURLY
                            | RETURN IDENT opt_variable_definition IS
                            | opt_variable_definition IS
                            | statement_list END PROCEDURE'''
    debug_syntax(p)

def p_formals(p):
    '''formals : formal_arg
               | formals COMMA formal_arg'''
    debug_syntax(p)

def p_formal_arg(p):
    '''formal_arg : IDENT LSQUARE IDENT RSQUARE'''
    debug_syntax(p)

def p_procedure_call(p):
    '''procedure_call : PROC_IDENT LPAREN RPAREN
                      | PROC_IDENT LPAREN arguments RPAREN'''
    debug_syntax(p)

def p_arguments(p):
    '''arguments : expression
                 | arguments COMMA expression'''
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
    '''print_statement : PRINT print_item opt_print_statement'''
    debug_syntax(p)

def p_opt_print_statement(p):
    '''opt_print_statement : opt_print_statement AMPERSAND print_item
                           | empty'''
    debug_syntax(p)

def p_print_item(p):
    '''print_item : STRING
                  | expression'''
    debug_syntax(p)

def p_statement(p):
    '''statement : procedure_call
                 | assignment
                 | print_statement
                 | DO statement_list UNTIL expression
                 | DO statement_list UNLESS expression OTHERWISE statement_list DONE
                 | DO statement_list UNLESS expression DONE
                 | RETURN expression'''
    debug_syntax(p)

def p_expression(p):
    '''expression : simple_expr
                  | expression EQ simple_expr
                  | expression LT simple_expr'''
    debug_syntax(p)

def p_simple_expr(p):
    '''simple_expr : term
                   | simple_expr PLUS term
                   | simple_expr MINUS term'''
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
    '''function_call : FUNC_IDENT LPAREN RPAREN
                     | FUNC_IDENT LPAREN arguments RPAREN'''
    debug_syntax(p)

def p_unless_expression(p):
    '''unless_expression : DO expression UNLESS expression OTHERWISE expression DONE'''
    debug_syntax(p)

# error token is generated by PLY if the automation enters error state
# (cannot continue reducing or shifting)
def p_error(p):
    print( 'syntax error @', p )
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

