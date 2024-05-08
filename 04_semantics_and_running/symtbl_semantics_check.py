#!/usr/bin/env python3
#

import simple_semantics_check
import tree_print
import tree_generation
import lexer
from semantics_common import visit_tree, SymbolData, SemData

def add_symbol_to_symtbl(node, symbol_name, symbol_type, semdata, error_msg):
    if symbol_name in semdata.symtbl:
        definition_node = semdata.symtbl[symbol_name].defnode
        return f"Error, redefined {error_msg} {symbol_name} (earlier definition on line {str(definition_node.lineno)})"
    symdata = SymbolData(symbol_type, node)
    semdata.symtbl[symbol_name] = symdata
    node.symdata = symdata  # Add a link to the symbol data to AST node for execution

# Collect symbols to the symbol table. Returns None | error message
def add_symbols(node, semdata):
    result = None
    nodetype = node.nodetype
    if nodetype == "variable_def":
        result = add_symbol_to_symtbl(
            node,
            symbol_name=node.child_name.value,
            symbol_type=node.child_init_value.nodetype,
            semdata=semdata,
            error_msg="variable")
    elif nodetype == "procedure_def":
        result = add_symbol_to_symtbl(
            node,
            symbol_name=node.child_name.value,
            symbol_type=node.nodetype,
            semdata=semdata,
            error_msg="procedure")
    elif nodetype == "function_def":
        result = add_symbol_to_symtbl(
            node,
            symbol_name=node.child_name.value,
            symbol_type=node.nodetype,
            semdata=semdata,
            error_msg="function")
    elif nodetype == "formal_arg":
        result = add_symbol_to_symtbl(
            node,
            symbol_name=node.child_name.value,
            symbol_type=node.child_type.value,
            semdata=semdata,
            error_msg="formal arg")

    return result

# Check symbol use, add link to symbol data
def check_symbols(node, semdata):
    nodetype = node.nodetype
    if nodetype == 'id_name' and not semdata.formal_arg:
        name = node.value
        if name not in semdata.symtbl:
            return f"Error, undefined symbol {name} on line {str(node.lineno)}"
        node.symdata = semdata.symtbl[name]
    if nodetype == "formal_arg":
        semdata.formal_arg = True    

def check_symbols_after(node, semdata):
    if node.nodetype == "formal_arg":
        semdata.formal_arg = False

# todo : test function_call
# Check procedures and functions are used with correct parameters count
# todo rename. also check param types
def check_parameters_and_calling(node, semdata):
    nodetype = node.nodetype
    # Check param counts are correct
    if nodetype in ("procedure_call", "function_call"):
        call_params_count = len(node.children_args)
        name = node.child_name.value
        def_node = semdata.symtbl[name].defnode
        def_params_count = len(def_node.children_formal_args)
        if call_params_count != def_params_count:
            return (
                f"Error, {nodetype} with invalid number ({call_params_count}) "
                f"of parameters! {def_params_count} expected.")
        # Check param types are correct
        for i in range(0,call_params_count):
            call_type = node.children_args[i].nodetype
            def_type = def_node.children_formal_args[i].child_type.value
            if call_type == "id_name": # Find the var type from symbol table
                call_type = semdata.symtbl[node.children_args[i].value].defnode.child_init_value.nodetype
            if not (call_type == def_type or
                (call_type.startswith("int") and def_type == "int")):
                return f"Error, calling with type {call_type}. Expected {def_type}"

    if nodetype.endswith("_statement"):
        semdata.inside_statement = True
    # Todo add expression

def after_param_call_check(node, semdata):
    nodetype = node.nodetype
    if nodetype.endswith("_statement"):
        semdata.inside_statement = False

# Simple symbol table printer for debugging
def print_symbol_table(semdata, title):
    print(title)
    for name, data in semdata.symtbl.items():
        print(name, ":")
        for attr, value in vars(data).items():
            printvalue = value
            if hasattr(value, "nodetype"):
                printvalue = value.nodetype
                if hasattr(value, "lineno"):
                    printvalue = printvalue + ", line " + str(value.lineno)
            print("  ", attr, "=", printvalue)

def semantic_checks(tree, semdata):
    '''run all semantic checks'''
    # Run Phase 3 semantic checks
    simple_semantics_check.semantic_checks(tree, semdata)

    visit_tree(tree, add_symbols, None, semdata)

    semdata.formal_arg = False # Track if node is inside formal_arg
    visit_tree(tree, check_symbols, check_symbols_after, semdata)

    semdata.inside_statement = False # Track if inside statement
    semdata.inside_expression = False
    visit_tree(tree, check_parameters_and_calling, after_param_call_check, semdata)


parser = tree_generation.parser

if __name__ == "__main__":
    import argparse
    import codecs
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', '--file', help='filename to process')
    ns = arg_parser.parse_args()
    if ns.file is None:
        arg_parser.print_help()
    else:
        data = codecs.open(ns.file, encoding='utf-8').read()
        ast_tree = parser.parse(data, lexer=lexer.lexer, debug=False)
        tree_print.treeprint(ast_tree)
        semdata = SemData()
        semantic_checks(ast_tree, semdata)
        print_symbol_table(semdata, title="Symbol table:")
        print("Semantics ok:")
