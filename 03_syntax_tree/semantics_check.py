#!/usr/bin/env python3
#
from semantics_common import visit_tree, SymbolData, SemData


# Check that we are reading only allowed attrs from a date. e.g somedate'month
def check_date_attr_read(node, semdata):
    allowed = ["day", "month",  "year", "weekday", "weeknum"]
    nodetype = node.nodetype
    if nodetype == "attr_read":
        if node.child_attr.value not in allowed:
            return "Error, reading invalid attribute from a date, line " + str(node.lineno)
        return None

# Check that we are modifying only allowed attrs from a date. e.g somedate.month
def check_date_attr_assign(node, semdata):
    allowed = ["day", "month",  "year"]
    nodetype = node.nodetype
    if nodetype == "attr_assign":
        if node.child_attr.value not in allowed:
            return "Error, modifying invalid attribute from a date, line " + str(node.lineno)
        return None

# Check that function and procedure definitions have return type of int or date
# Notice that procedure is allowed to have no return value at all by the lang
def check_func_proc_returntypes(node, semdata):
    allowed = ["int", "date_literal"]
    nodetype = node.nodetype
    if nodetype == "function_def":
        type = node.child_returntype.value
        if type not in allowed:
            return f"Error, function returns not allowed type ({type}), line {str(node.lineno)}"
        return None 
    if nodetype == "procedure_def":
        if node.child_returntype != None and node.child_returntype.value not in allowed:
            type = node.child_returntype.value
            return f"Error, procedure returns not allowed type ({type}), line {str(node.lineno)}"
        return None

# Check that function definitions do NOT have procedure calls inside them.
def check_no_nested_proc_call_before(node, semdata):
    nodetype = node.nodetype
    if nodetype == "function_def":
        semdata.inside_function_def = True
    if nodetype == "procedure_call" and semdata.inside_function_def:
        return f"Error, procedure call not allowed inside function def, line {str(node.lineno)}"

def check_no_nested_proc_call_after(node, semdata):
    nodetype = node.nodetype
    if nodetype == "function_def":
        semdata.inside_function_def = False
   
def check_date_literal_usage_after(node, semdata):
    nodetype = node.nodetype
    if nodetype == "date_literal":
        semdata.date_literal_found = True
    # If we are leaving a node that is not date_literal but directly earlier WAS!
    elif semdata.date_literal_found:
        semdata.date_literal_found = False
        # Check different possibilities if date_literal was used in correct place
        if nodetype == "variable_def" and node.child_init_value.nodetype == "date_literal":
            return None
        if nodetype == "assignment" and node.child_rvalue.nodetype == "date_literal":
            return None
        return f"Error, date_literal in a wrong place, line {str(node.lineno)}"

# Check that a procedure has a return statement only if it returns anything
# Basically find out if return type and return stmt exist and after leaving
# the proc def, check if there is a problem (stmt exists, return type not)
def check_return_stms_allowed_before(node, semdata):
    nodetype = node.nodetype
    if nodetype == "procedure_def":
        semdata.inside_proc_def = True
        if node.child_returntype is not None:
            semdata.return_exists = True
    elif semdata.inside_proc_def and nodetype == "return_stmt":
        semdata.return_stmt_exists = True

def check_return_stms_allowed_after(node, semdata):
    nodetype = node.nodetype
    if nodetype == "procedure_def":
        semdata.inside_proc_def = False
        if semdata.return_stmt_exists and not semdata.return_exists:
            return f"Error, procedure has return stmt but returns nothing, line {str(node.lineno)}"
        # init values to False again for possible another proc defs
        semdata.return_exists = False
        semdata.return_stmt_exists = False

def semantic_checks(tree):
    semdata = SemData()

    visit_tree(tree, check_date_attr_read, None, semdata)
    visit_tree(tree, check_func_proc_returntypes, None, semdata)

    semdata.inside_function_def = False
    visit_tree(tree, check_no_nested_proc_call_before,
               check_no_nested_proc_call_after, semdata)
    
    semdata.date_literal_found = False
    visit_tree(tree, None, check_date_literal_usage_after, semdata)

    semdata.inside_proc_def = False
    semdata.return_exists = False
    semdata.return_stmt_exists = False
    visit_tree(tree, check_return_stms_allowed_before, check_return_stms_allowed_after, semdata)
    print("Semantics ok:")
