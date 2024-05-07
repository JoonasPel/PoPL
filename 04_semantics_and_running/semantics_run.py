#!/usr/bin/env python3
#

from semantics_common import SymbolData, SemData

def run_program(tree, semdata):
  # Initialize all variables to zero
  for symdata in semdata.symtbl.values():
    if symdata.symtype == 'var':
      symdata.value = 0
  eval_node(tree, semdata) # Do the actual execution

def eval_node(node, semdata):
  symtbl = semdata.symtbl
  nodetype = node.nodetype
  if nodetype == 'program':
    # Execute each assignment in program
    for i in node.children_assigns:
      eval_node(i, semdata)
    return None
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
  elif nodetype == 'oper +':
    left_value = eval_node(node.child_left, semdata)
    right_value = eval_node(node.child_right, semdata)
    result = left_value + right_value
    return result
  elif nodetype == 'oper -':
    left_value = eval_node(node.child_left, semdata)
    right_value = eval_node(node.child_right, semdata)
    result = left_value - right_value
    return result
  elif nodetype == 'oper *':
    left_value = eval_node(node.child_left, semdata)
    right_value = eval_node(node.child_right, semdata)
    result = left_value * right_value
    return result
  elif nodetype == 'oper /':
    left_value = eval_node(node.child_left, semdata)
    right_value = eval_node(node.child_right, semdata)
    result = left_value / right_value
    return result
  else:
    print("Error, unknown node of type " + nodetype)
    return None


import sys
import lexer
import tree_generation
import tree_print
parser = tree_generation.parser

import symtbl_semantics_check

if __name__ == "__main__":
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument('--who', action='store_true', help='who wrote this' )
    arg_parser.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()
    if ns.who == True:
        print('H274830 Joonas Pelttari')
    if ns.file is None:
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        ast_tree = parser.parse(data, lexer=lexer.lexer, debug=False)
        semdata = SemData()
        symtbl_semantics_check.semantic_checks(ast_tree, semdata)
        tree_print.treeprint(ast_tree)
        print("Semantics ok.")
        print("Skipping program run for now")
        #run_program(ast_tree, semdata)
        #print("Program finished.")
        
        # Todo : Remove this. Debugging only
        symtbl_semantics_check.print_symbol_table(semdata, title="Symbols:")
