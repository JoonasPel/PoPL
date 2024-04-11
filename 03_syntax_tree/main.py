#!/usr/bin/env python3

import ply.yacc
import ply.lex
import lexer
import tree_print

# Class for syntax tree nodes
class ASTnode:
    def __init__(self, typestr):
        self.nodetype = typestr

def debug_syntax(p):
    pass

# tokens are defined in lex-module, but needed here also in syntax rules
tokens = lexer.tokens

# any function starting with 'p_' is PLY yacc rule
# first definition is the target we want to reduce
# in other words: after processing all input tokens, if this start-symbol
# is the only one left, we do not have any syntax errors
def p_program(p):
    '''program : opt_definitions statement_list'''
    p[0] = ASTnode("program")
    p[0].children_definitions = p[1]
    p[0].children_statements = p[2]
    p[0].lineno = p.lineno(0)
    debug_syntax(p)

def p_empty(p):
    '''empty : '''
    debug_syntax(p)

def p_statement_list1(p):
    '''statement_list : statement'''
    p[0] = [p[1]]
    debug_syntax(p)

def p_statement_list2(p):
    '''statement_list : statement COMMA statement_list'''
    p[0] = p[3]
    p[0].append(p[1])
    debug_syntax(p)

def p_definitions1(p):
    '''definitions : function_definition'''
    debug_syntax(p)

def p_definitions2(p):
    '''definitions : procedure_definition'''
    debug_syntax(p)

def p_definitions3(p):
    '''definitions : variable_definition'''
    p[0] = p[1]
    debug_syntax(p)

def p_opt_definitions1(p):
    '''opt_definitions : empty'''
    p[0] = []
    debug_syntax(p)

def p_opt_definitions2(p):
    '''opt_definitions : opt_definitions definitions'''
    p[0] = p[1]
    p[0].append(p[2])
    debug_syntax(p)

def p_variable_definition(p):
    '''variable_definition : VAR IDENT EQ expression'''
    p[0] = ASTnode("variable_def")
    p[0].child_name = ASTnode("id_name")
    p[0].child_name.value = p[2]
    p[0].child_name.lineno = p.lineno(2)
    p[0].child_init_value = p[4]
    p[0].lineno = p.lineno(1)
    debug_syntax(p)

def p_opt_var_defs(p):
    '''opt_var_defs : var_def_list
                    | empty'''
    debug_syntax(p)

def p_var_def_list(p):
    '''var_def_list : var_def_list variable_definition
                    | variable_definition'''
    debug_syntax(p)

def p_function_definition(p):
    '''function_definition : FUNCTION FUNC_IDENT LCURLY opt_formals RCURLY RETURN IDENT opt_var_defs IS rvalue END FUNCTION'''
    debug_syntax(p)

def p_procedure_definition(p):
    '''procedure_definition : PROCEDURE PROC_IDENT LCURLY opt_formals RCURLY opt_return_type opt_var_defs IS statement_list END PROCEDURE'''
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

def p_args(p):
    '''args : expression
            | args COMMA expression'''
    debug_syntax(p)

def p_opt_args(p):
    '''opt_args : args
                | empty'''
    debug_syntax(p)

def p_assignment1(p):
    '''assignment : lvalue EQ rvalue'''
    p[0] = ASTnode("assignment")
    p[0].child_lvalue = p[1]
    p[0].child_rvalue = p[3]
    p[0].lineno = p.lineno(2)
    debug_syntax(p)

def p_assignment2(p):
    '''assignment : IDENT DOT IDENT'''
    debug_syntax(p)

def p_lvalue1(p):
    '''lvalue : IDENT'''
    p[0] = ASTnode("var_lvalue")
    p[0].value = p[1]
    p[0].lineno = p.lineno(1)
    debug_syntax(p)

def p_lvalue2(p):
    '''lvalue : IDENT DOT IDENT'''
    debug_syntax(p)

def p_rvalue1(p):
    '''rvalue : expression'''
    p[0] = p[1]
    debug_syntax(p)

def p_rvalue2(p):
    '''rvalue : unless_expression'''
    p[0] = p[1]
    debug_syntax(p)

def p_print_statement(p):
    '''print_statement : PRINT printlist'''
    p[0] = ASTnode("print_statement")
    p[0].children_printitems = p[2]
    p[0].lineno = p.lineno(1)
    debug_syntax(p)

def p_printlist1(p):
    '''printlist : printitem'''
    p[0] = [p[1]]
    debug_syntax(p)

def p_printlist2(p):
    '''printlist : printlist AMPERSAND printitem'''
    p[0] = p[1]
    p[0].append(p[3])
    debug_syntax(p)

def p_printitem1(p):
    '''printitem : expression'''
    p[0] = p[1]
    debug_syntax(p)

def p_printitem2(p):
    '''printitem : STRING'''
    p[0] = p[1]
    p[0].lineno = p.lineno(1)
    debug_syntax(p)

def p_statement1(p):
    '''statement : procedure_call
                 | unless_statement
                 | RETURN expression'''
    debug_syntax(p)

def p_statement2(p):
    '''statement : loop_statement'''
    p[0] = p[1]
    debug_syntax(p)

def p_statement3(p):
    '''statement : print_statement'''
    p[0] = p[1]
    debug_syntax(p)

def p_statement4(p):
    '''statement : assignment'''
    p[0] = p[1]
    debug_syntax(p)

def p_loop_statement(p):
    '''loop_statement : DO statement_list UNTIL expression'''
    p[0] = ASTnode("loop_statement")
    p[0].child_condition = p[4]
    p[0].children_stmts = p[2]
    p[0].lineno = p.lineno(1)
    debug_syntax(p)

def p_unless_statement(p):
    '''unless_statement : DO statement_list UNLESS expression opt_otherwise DONE'''
    debug_syntax(p)

def p_opt_otherwise(p):
    '''opt_otherwise : OTHERWISE statement_list
                     | empty'''
    debug_syntax(p)

def p_expression1(p):
    '''expression : simple_expr'''
    p[0] = p[1]
    debug_syntax(p)

def p_expression2(p):
    '''expression : expression relation_op simple_expr'''
    p[0] = p[2]
    p[0].child_left_expr = p[1]
    p[0].child_right_expr = p[3]
    debug_syntax(p)

def p_relation_op1(p):
    '''relation_op : EQ'''
    p[0] = ASTnode("=_op")
    p[0].lineno = p.lineno(1)
    debug_syntax(p)

def p_relation_op2(p):
    '''relation_op : LT'''
    p[0] = ASTnode("<_op")
    p[0].lineno = p.lineno(1)
    debug_syntax(p)

def p_simple_expr1(p):
    '''simple_expr : term'''
    p[0] = p[1]
    debug_syntax(p)

def p_simple_expr2(p):
    '''simple_expr : simple_expr add_or_minus term'''
    p[0] = p[2]
    p[0].child_left_expr = p[1]
    p[0].child_right_expr = p[3]
    debug_syntax(p)

def p_add_or_minus1(p):
    '''add_or_minus : PLUS'''
    p[0] = ASTnode("+_op")
    p[0].lineno = p.lineno(1)
    debug_syntax(p)

def p_add_or_minus2(p):
    '''add_or_minus : MINUS'''
    p[0] = ASTnode("-_op")
    debug_syntax(p)

def p_mult_or_div(p):
    '''mult_or_div : MULT
                   | DIV'''
    debug_syntax(p)

def p_term1(p):
    '''term : factor'''
    p[0] = p[1]
    debug_syntax(p)

# TODO DIV MYÖS
def p_term2(p):
    '''term : term mult_or_div factor'''
    p[0] = ASTnode("*_op")
    p[0].child_left_expr = p[1]
    p[0].child_right_expr = p[3]
    debug_syntax(p)

def p_factor1(p):
    '''factor : atom'''
    p[0] = p[1]
    debug_syntax(p)

def p_factor2(p):
    '''factor : PLUS atom'''
    debug_syntax(p)

def p_factor3(p):
    '''factor : MINUS atom'''
    debug_syntax(p)

def p_atom1(p):
    '''atom : IDENT APOSTROPHE IDENT
            | DATE_LITERAL
            | function_call
            | procedure_call
            | LPAREN expression RPAREN'''
    debug_syntax(p)

def p_atom2(p):
    '''atom : INT_LITERAL'''
    p[0] = ASTnode("int_literal")
    p[0].value = p[1]
    p[0].lineno = p.lineno(1)
    debug_syntax(p)

def p_atom3(p):
    '''atom : IDENT'''
    p[0] = ASTnode("id_name")
    p[0].value = p[1]
    p[0].lineno = p.lineno(1)
    debug_syntax(p)

def p_function_call(p):
    '''function_call : FUNC_IDENT LPAREN opt_args RPAREN'''
    debug_syntax(p)

def p_unless_expression(p):
    '''unless_expression : DO expression UNLESS expression OTHERWISE expression DONE'''
    debug_syntax(p)

def p_error(p):
    if (p):
        print( f"{p.lineno}:Syntax Error (token: '{p.value}')" )
    else:
        print("Unexpected end of input")
    raise SystemExit

parser = ply.yacc.yacc()

if __name__ == '__main__':
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-t', '--treetype', help='type of output tree (unicode/ascii/dot)')
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    group.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()
    outformat="unicode"
    if ns.treetype:
      outformat = ns.treetype
    if ns.who == True:
        print('H274830 Joonas Pelttari')
    elif ns.file is None:
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        result = parser.parse(data, lexer=lexer.lexer, debug=False)
        tree_print.treeprint(result, outformat)
