from utils.ASTVisitor import ASTVisitor
import collections 
class TypedVisitor(ASTVisitor):
    def __init__(self):
        self.type_to_node = collections.defaultdict(list)
        self.type_node_keys = collections.defaultdict(dict)
        self.function_tree = collections.defaultdict(dict)
     
    def visit_function_definition(self, node):
        self.type_to_node["function_definition"].append(node)
        if node.children[1].text not in self.function_tree:
            self.function_tree[node.children[1].text]  = node
        return True

    def visit_identifier(self, node):
        self.type_to_node["identifier"].append(node)
        return True

    def visit_parameter(self, node):
        self.type_to_node["parameter"].append(node)
        return True
    
    def visit_expression_statement(self, node):
        '''
        a = b + 1;
        '''
        self.type_to_node["expression_statement"].append(node)
        return True
    
    def visit_binary_expression(self, node):
        '''
        b + 1;
        '''
        self.type_to_node["binary_expression"].append(node)
        return True
    
    def visit_call_expression(self, node):
        '''
        '_createStake(amount, term)'
        '''
        self.type_to_node["call_expression"].append(node)
        return True
    
    def visit_call_struct_argument(self, node):
        self.type_to_node['call_struct_argument'].append(node)
        return True
    
    def visit_update_expression(self, node):
        self.type_to_node["update_expression"].append(node)
        return True

    def visit_number_literal(self, node):
        self.type_to_node['number_literal'].append(node)
        return True
    
    def visit_variable_declaration_statement(self, node):
        '''
        int a = b + 1;
        '''
        #assert node.children[0].type == 'variable_declaration', f'{node.children[0]}'
        #assert node.children[0].children[1].type == 'identifier', f'{node.children[0].children[1].type}'
        variable_declaration = node.children[0].children[1].text
        self.type_to_node['variable_declaration_statement'].append(node)
        return True
    
    def visit_string_literal(self, node):
        self.type_to_node['string_literal'].append(node)
        return True
    
    def visit_return_statement(self, node):
        self.type_to_node['return_statement'].append(node)
        return True

    def visit_assignment_expression(self, node):
        '''
        'a = b'
        '''
        #assert node.children[0].type == "identifier", f'{node.children[0].type} {node.text}'
        varaible_def = node.children[0].text
        self.type_to_node['assignment_expression'].append(node)
        return True
 
    def visit_state_variable_declaration(self, node):
        '''
        contract state variable
        '''
        # for n in node.children:
        #     if n.type == 'identifier':
        #         state_variable = n.text
        #         break
        self.type_to_node['state_variable_declaration'].append(node)
        return True
    
