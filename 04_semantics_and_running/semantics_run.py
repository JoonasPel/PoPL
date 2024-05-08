#!/usr/bin/env python3
#

import symtbl_semantics_check
import tree_print
import tree_generation
import lexer
import sys
from semantics_common import SymbolData, SemData


def run_program(tree, semdata):
    # Initialize all int_literals to zero
    for symdata in semdata.symtbl.values():
        if symdata.symtype == "int_literal":
            symdata.value = 0
    eval_node(tree, semdata)


def eval_node(node, semdata):
    symtbl = semdata.symtbl
    nodetype = node.nodetype
    if nodetype == "program":
        for i in node.children_definitions:
            eval_node(i, semdata)
        for i in node.children_statements:
            eval_node(i, semdata)
    
    elif nodetype == "variable_def":
        value = eval_node(node.child_init_value, semdata)
        node.symdata.value = value
    elif nodetype == "int_literal":
        return node.value
    elif nodetype == "date_literal":
        return node.value
    elif nodetype == "string_literal":
        return node.value
    elif nodetype == "id_name":
        return node.symdata.value
    elif nodetype.endswith("_op"):
        left_value = eval_node(node.child_left_expr, semdata)
        right_value = eval_node(node.child_right_expr, semdata)
        oper = nodetype[0]
        if oper == "*":
            return left_value * right_value
        if oper == "/":
            return left_value / right_value
        if oper == "+":
            return left_value + right_value
        if oper == "-":
            return left_value - right_value
        
    elif nodetype == "print_statement":
        for printitem in node.children_printitems:
            print(eval_node(printitem, semdata), end=" ")
        print()


    elif nodetype == 'assign':
        # Execute the expression
        expr_value = eval_node(node.child_expr, semdata)
        # Change the value of the variable in symbol data
        node.symdata.value = expr_value
        # Print out the assignment
        print(node.value, "=", expr_value)
        return None

    elif nodetype == 'number':
        # Return the value of the number as result
        return node.value

    elif nodetype == 'variable':
        # Return the value of the variable in symboldata as result
        return node.symdata.value


    else:
        print("Error, unknown node of type " + nodetype)
        return None


parser = tree_generation.parser

if __name__ == "__main__":
    import argparse
    import codecs
    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this')
    arg_parser.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()
    if ns.who == True:
        print('H274830 Joonas Pelttari')
    if ns.file is None:
        arg_parser.print_help()
    else:
        data = codecs.open(ns.file, encoding='utf-8').read()
        ast_tree = parser.parse(data, lexer=lexer.lexer, debug=False)
        semdata = SemData()
        symtbl_semantics_check.semantic_checks(ast_tree, semdata)
        tree_print.treeprint(ast_tree)
        print("Semantics ok.")
        run_program(ast_tree, semdata)
        print("Program finished.")

        # Todo : Remove this. Debugging only
        symtbl_semantics_check.print_symbol_table(semdata, title="Symbols:")
