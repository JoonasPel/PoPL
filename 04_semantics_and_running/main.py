#!/usr/bin/env python3
#

from datetime import datetime
import sys
import symtbl_semantics_check
import tree_print
import tree_generation
import lexer
from semantics_common import SymbolData, SemData


def run_program(tree, semdata):
    # Initialize all int_literals to zero
    for symdata in semdata.symtbl.values():
        if symdata.symtype == "int_literal":
            symdata.value = 0
    eval_node(tree, semdata)


def eval_node(node, semdata):
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
        if oper == "=":
            return left_value == right_value
        if oper == "<":
            return left_value < right_value
        print(f"Error, unknown operator type: {oper}")

    elif nodetype == "attr_read":
        date = eval_node(node.child_var, semdata)
        attr = eval_node(node.child_attr, semdata)
        if attr == "day":
            return date.day
        if attr == "month":
            return date.month
        if attr == "year":
            return date.year
        print(f"Error, unknown date attr type: {attr}")
    elif nodetype == "attr_assign":
        date = eval_node(node.child_var, semdata)
        attr = eval_node(node.child_attr, semdata)
        return date, attr
    elif nodetype == "attr":
        return node.value

    elif nodetype == "assignment":
        l_value = node.child_lvalue
        r_value = eval_node(node.child_rvalue, semdata)
        nodetype = l_value.nodetype
        if nodetype == "id_name":
            l_value.symdata.value = r_value
        elif nodetype == "attr_assign":
            date, attr = eval_node(l_value, semdata)
            if attr == "day":
                l_value.child_var.symdata.value = date.replace(day=r_value)
            elif attr == "month":
                l_value.child_var.symdata.value = date.replace(month=r_value)
            elif attr == "year":
                l_value.child_var.symdata.value = date.replace(year=r_value)
            else:
                print(f"Error, unknown date attr type: {attr}")
        else:
            print(f"Error, unknown assingment type: {nodetype}")

    elif nodetype == "print_statement":
        for printitem in node.children_printitems:
            print(eval_node(printitem, semdata), end=" ")
        print()
    elif nodetype == "loop_statement":
        while True:
            for i in node.children_stmts:
                eval_node(i, semdata)
            if eval_node(node.child_condition, semdata):
                break
    elif nodetype == "unless_stmt":
        if not eval_node(node.child_unless, semdata):
            for i in node.children_stmts:
                eval_node(i, semdata)
        else:
            for i in node.children_otherwise:
                eval_node(i, semdata)
    
    elif nodetype == "unless_expr":
        if not eval_node(node.child_unless, semdata):
            return eval_node(node.child_do, semdata)
        return eval_node(node.child_otherwise, semdata)

    elif nodetype == "function_def":
        pass
    elif nodetype == "function_call":
        func_name = node.child_name.value
        func_node = semdata.symtbl[func_name].defnode
        # Initialize formal args to the value given to them in function call
        for idx, formal_arg in enumerate(func_node.children_formal_args):
            calling_value = eval_node(node.children_args[idx], semdata)
            formal_arg.symdata.value = calling_value
        # Execute body
        return eval_node(func_node.child_body, semdata)

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
        run_program(ast_tree, semdata)
        # Uncomment to print symbol table:
        #symtbl_semantics_check.print_symbol_table(semdata, title="Symbols:")
