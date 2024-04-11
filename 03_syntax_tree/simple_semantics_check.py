#!/usr/bin/env python3
#

from semantics_common import visit_tree, SymbolData, SemData

# Define semantic check functions


# Stupid check, make sure all numbers are < 10
def check_literals(node, semdata):
  nodetype = node.nodetype
  if nodetype == 'number':
    if node.value >= 10:
      return "Number "+str(node.value)+" on line " + str(node.lineno) + " too large!"
  else:
    return None

# Another stupid check, only allow less than 4 nested + operations
def check_plus_level_before(node, semdata):
  nodetype = node.nodetype
  if nodetype == 'oper +':
    # We are entering a plus node, increase level
    semdata.plus_level = semdata.plus_level + 1
    if semdata.plus_level > 3:
      return "Error, more than 3 nested plus operations, line " + str(node.lineno)
    else:
      return None

# Another stupid check, only allow less than 4 nested + operations
def check_plus_level_after(node, semdata):
  nodetype = node.nodetype
  if nodetype == 'oper +':
    # We are leaving the plus node, decrease level
    semdata.plus_level = semdata.plus_level - 1
  else:
    return None

def semantic_checks(tree, semdata):
  '''run simple semantic checks'''
  # Initialize 'oper +' level count to 0
  semdata.plus_level = 0
  # Check stupid things
  visit_tree(tree, check_literals, None, semdata)
  visit_tree(tree, check_plus_level_before, check_plus_level_after, semdata)


import lexer
import tree_generation2
import tree_print
parser = tree_generation2.parser

if __name__ == "__main__":
    import argparse, codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file', help='filename to process')

    ns = arg_parser.parse_args()

    if ns.file is None:
        arg_parser.print_help()
    else:
        data = codecs.open( ns.file, encoding='utf-8' ).read()
        ast_tree = parser.parse(data, lexer=lexer.lexer, debug=False)
        tree_print.treeprint(ast_tree) # Just for debugging

        semdata = SemData()
        semantic_checks(ast_tree, semdata)
        print("Semantics ok:")
