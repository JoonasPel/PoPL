#!/usr/bin/env python3

import ply.yacc
import ply.lex
import lexer
import tree_print
import semantics_check

# Class for syntax tree nodes
class ASTnode:
    def __init__(self, typestr):
        self.nodetype = typestr

tokens = lexer.tokens

# Creates an ASTnode for terminal token. Used in multiple places for creating
# nodes "id_name" and "id_type"
def create_node(name, value, lineno):
    node = ASTnode(name)
    node.value = value
    node.lineno = lineno
    return node


def p_program(p):
    '''program : opt_definitions statement_list'''
    p[0] = ASTnode("program")
    p[0].children_definitions = p[1]
    p[0].children_statements = p[2]
    p[0].lineno = p.lineno(0)

def p_empty(p):
    '''empty : '''
    p[0] = None

def p_statement_list1(p):
    '''statement_list : statement'''
    p[0] = [p[1]]

def p_statement_list2(p):
    '''statement_list : statement COMMA statement_list'''
    p[0] = p[3]
    p[0].append(p[1])

def p_definitions1(p):
    '''definitions : function_definition'''
    p[0] = p[1]

def p_definitions2(p):
    '''definitions : procedure_definition'''
    p[0] = p[1]

def p_definitions3(p):
    '''definitions : variable_definition'''
    p[0] = p[1]

def p_opt_definitions1(p):
    '''opt_definitions : empty'''
    p[0] = []

def p_opt_definitions2(p):
    '''opt_definitions : opt_definitions definitions'''
    p[0] = p[1]
    p[0].append(p[2])

def p_variable_definition(p):
    '''variable_definition : VAR IDENT EQ expression'''
    p[0] = ASTnode("variable_def")
    p[0].child_name = create_node("id_name", p[2], p.lineno(2))
    p[0].child_init_value = p[4]
    p[0].lineno = p.lineno(1)

def p_opt_var_defs1(p):
    '''opt_var_defs : var_def_list'''
    p[0] = p[1]

def p_opt_var_defs2(p):
    '''opt_var_defs : empty'''
    p[0] = []

def p_var_def_list1(p):
    '''var_def_list : var_def_list variable_definition'''
    p[0] = p[1]
    p[0].append(p[2])

def p_var_def_list2(p):
    '''var_def_list : variable_definition'''
    p[0] = [p[1]]

def p_function_definition(p):
    '''function_definition : FUNCTION FUNC_IDENT LCURLY opt_formals RCURLY RETURN IDENT opt_var_defs IS rvalue END FUNCTION'''
    p[0] = ASTnode("function_def")
    p[0].child_name = create_node("id_name", p[2], p.lineno(2))
    p[0].child_returntype = create_node("id_type", p[7], p.lineno(7))
    p[0].children_var_defs = p[8]
    p[0].children_formal_args = p[4]
    p[0].child_body = p[10]
    p[0].lineno = p.lineno(1)

def p_procedure_definition(p):
    '''procedure_definition : PROCEDURE PROC_IDENT LCURLY opt_formals RCURLY opt_return_type opt_var_defs IS statement_list END PROCEDURE'''
    p[0] = ASTnode("procedure_def")
    p[0].child_name = create_node("id_name", p[2], p.lineno(2))
    p[0].child_returntype = p[6]
    p[0].children_var_defs = p[7]
    p[0].children_formal_args = p[4]
    p[0].children_stmts = p[9]
    p[0].lineno = p.lineno(1)

# not tested
def p_opt_return_type1(p):
    '''opt_return_type : RETURN IDENT'''
    p[0] = create_node("id_type", p[2], p.lineno(2))

# not tested
def p_opt_return_type2(p):
    '''opt_return_type : empty'''
    p[0] = p[1]

def p_formals1(p):
    '''formals : formals COMMA formal_arg'''
    p[0] = p[1]
    p[0].append(p[3])

def p_formals2(p):
    '''formals : formal_arg'''
    p[0] = [p[1]]

def p_opt_formals1(p):
    '''opt_formals : formals'''
    p[0] = p[1]

def p_opt_formals2(p):
    '''opt_formals : empty'''
    p[0] = p[1]

def p_formal_arg(p):
    '''formal_arg : IDENT LSQUARE IDENT RSQUARE'''
    p[0] = ASTnode("formal_arg")
    p[0].child_name = create_node("id_name", p[1], p.lineno(1))
    p[0].child_type = create_node("id_type", p[3], p.lineno(3))
    p[0].lineno = p.lineno(1)

def p_args1(p):
    '''args : expression'''
    p[0] = [p[1]]

def p_args2(p):
    '''args : args COMMA expression'''
    p[0] = p[1]
    p[0].append(p[3])

def p_opt_args1(p):
    '''opt_args : args'''
    p[0] = p[1]

def p_opt_args2(p):
    '''opt_args : empty'''
    p[0] = []

def p_assignment1(p):
    '''assignment : lvalue EQ rvalue'''
    p[0] = ASTnode("assignment")
    p[0].child_lvalue = p[1]
    p[0].child_rvalue = p[3]
    p[0].lineno = p.lineno(2)

def p_assignment2(p):
    '''assignment : IDENT DOT IDENT'''

def p_lvalue1(p):
    '''lvalue : IDENT'''
    p[0] = ASTnode("var_lvalue")
    p[0].value = p[1]
    p[0].lineno = p.lineno(1)

def p_lvalue2(p):
    '''lvalue : IDENT DOT IDENT'''

def p_rvalue1(p):
    '''rvalue : expression'''
    p[0] = p[1]

def p_rvalue2(p):
    '''rvalue : unless_expression'''
    p[0] = p[1]

def p_print_statement(p):
    '''print_statement : PRINT printlist'''
    p[0] = ASTnode("print_statement")
    p[0].children_printitems = p[2]
    p[0].lineno = p.lineno(1)

def p_printlist1(p):
    '''printlist : printitem'''
    p[0] = [p[1]]

def p_printlist2(p):
    '''printlist : printlist AMPERSAND printitem'''
    p[0] = p[1]
    p[0].append(p[3])

def p_printitem1(p):
    '''printitem : expression'''
    p[0] = p[1]

def p_printitem2(p):
    '''printitem : STRING'''
    p[0] = ASTnode("string_literal")
    p[0].value = p[1]
    p[0].lineno = p.lineno(1)

def p_statement1(p):
    '''statement : unless_statement
                 | RETURN expression'''

def p_statement2(p):
    '''statement : loop_statement'''
    p[0] = p[1]

def p_statement3(p):
    '''statement : print_statement'''
    p[0] = p[1]

def p_statement4(p):
    '''statement : assignment'''
    p[0] = p[1]

def p_statement5(p):
    '''statement : procedure_call'''
    p[0] = p[1]

def p_loop_statement(p):
    '''loop_statement : DO statement_list UNTIL expression'''
    p[0] = ASTnode("loop_statement")
    p[0].child_condition = p[4]
    p[0].children_stmts = p[2]
    p[0].lineno = p.lineno(1)

def p_unless_statement(p):
    '''unless_statement : DO statement_list UNLESS expression opt_otherwise DONE'''

def p_opt_otherwise(p):
    '''opt_otherwise : OTHERWISE statement_list
                     | empty'''

def p_expression1(p):
    '''expression : simple_expr'''
    p[0] = p[1]

def p_expression2(p):
    '''expression : expression relation_op simple_expr'''
    p[0] = p[2]
    p[0].child_left_expr = p[1]
    p[0].child_right_expr = p[3]

def p_relation_op1(p):
    '''relation_op : EQ'''
    p[0] = ASTnode("=_op")
    p[0].lineno = p.lineno(1)

def p_relation_op2(p):
    '''relation_op : LT'''
    p[0] = ASTnode("<_op")
    p[0].lineno = p.lineno(1)

def p_simple_expr1(p):
    '''simple_expr : term'''
    p[0] = p[1]

def p_simple_expr2(p):
    '''simple_expr : simple_expr add_or_minus term'''
    p[0] = p[2]
    p[0].child_left_expr = p[1]
    p[0].child_right_expr = p[3]

def p_add_or_minus1(p):
    '''add_or_minus : PLUS'''
    p[0] = ASTnode("+_op")
    p[0].lineno = p.lineno(1)

def p_add_or_minus2(p):
    '''add_or_minus : MINUS'''
    p[0] = ASTnode("-_op")
    p[0].lineno = p.lineno(1)

def p_mult_or_div1(p):
    '''mult_or_div : MULT'''
    p[0] = ASTnode("*_op")
    p[0].lineno = p.lineno(1)

def p_mult_or_div2(p):
    '''mult_or_div : DIV'''
    p[0] = ASTnode("/_op")
    p[0].lineno = p.lineno(1)

def p_term1(p):
    '''term : factor'''
    p[0] = p[1]

def p_term2(p):
    '''term : term mult_or_div factor'''
    p[0] = p[2]
    p[0].child_left_expr = p[1]
    p[0].child_right_expr = p[3]

def p_factor1(p):
    '''factor : atom'''
    p[0] = p[1]

def p_factor2(p):
    '''factor : PLUS atom'''

def p_factor3(p):
    '''factor : MINUS atom'''

def p_atom1(p):
    '''atom : IDENT APOSTROPHE IDENT
            | DATE_LITERAL'''

def p_atom2(p):
    '''atom : INT_LITERAL'''
    p[0] = ASTnode("int_literal")
    p[0].value = p[1]
    p[0].lineno = p.lineno(1)

def p_atom3(p):
    '''atom : IDENT'''
    p[0] = create_node("id_name", p[1], p.lineno(1))

def p_atom4(p):
    '''atom : function_call'''
    p[0] = p[1]

def p_atom5(p):
    '''atom : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_atom6(p):
    '''atom : procedure_call'''
    p[0] = p[1]

def p_function_call(p):
    '''function_call : FUNC_IDENT LPAREN opt_args RPAREN'''
    p[0] = ASTnode("function_call")
    p[0].child_name = create_node("id_name", p[1], p.lineno(1))
    p[0].children_args = p[3]
    p[0].lineno = p.lineno(1)

def p_procedure_call(p):
    '''procedure_call : PROC_IDENT LPAREN opt_args RPAREN'''
    p[0] = ASTnode("procedure_call")
    p[0].child_name = create_node("id_name", p[1], p.lineno(1))
    p[0].children_args = p[3]
    p[0].lineno = p.lineno(1)

def p_unless_expression(p):
    '''unless_expression : DO expression UNLESS expression OTHERWISE expression DONE'''

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
        ast_tree = parser.parse(data, lexer=lexer.lexer, debug=False)
        tree_print.treeprint(ast_tree, outformat)
        semantics_check.semantic_checks(ast_tree)
