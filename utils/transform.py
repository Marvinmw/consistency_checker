# transform SafeMath
from treelib import Node, Tree
from utils.tree_sitter_utils import index_to_code_token
from utils import log
logger = log.setup_custom_logger("extractExpression")
class ASTTree( ):
    def __init__(self, code, function_tree):
        super(ASTTree).__init__()
        self.ast =  Tree()
        self.node_id = 0
        self.code = code
        self.function_tree = function_tree
        self.node_type = []

    def visit_children(self, n, parent_id):
        for i, c in enumerate(n.children):
            self.visit(c, parent_id)
            
    def visit(self, n, parent_id):
        my_id = self.node_id
        self.node_type.append( n.type )
        self.node_id += 1
        trimmed_code = index_to_code_token((n.start_point, n.end_point), self.code.split("\n"))
        # if n.type == "string":
        #     print(n)
        #     print(trimmed_code)
        if parent_id is not None:
            self.ast.create_node(
                n.type,
                my_id,
                parent=parent_id,
                data={"type":n.type, "start_point":n.start_point, "end_point":n.end_point, "code":trimmed_code, "text":n.text.decode()}
            )
        else:
            self.ast.create_node(  # root node
                n.type,
                my_id,
                data={"type":n.type, "start_point":n.start_point, "end_point":n.end_point, "code":trimmed_code, "text":n.text.decode()}
            )
       
        self.visit_children(n, parent_id=my_id)


def copySitterTree(code, root):
    ast_visitor = ASTTree(code, root)
    ast_visitor.visit(root, parent_id=None)
    return ast_visitor.ast


operators={"add":"+", "sub":"-", "div":"/", "mul":"*", "divCeil":"/"}
def rewriteMathFunction(tree, root):
    '''
    To do
    add sub div mul
    '''
    queue = [root]
    while len(queue) > 0:
        current_node = queue[0]
        queue = queue[1:]
        if current_node.tag == "call_expression":
            cur_node_children = tree.children(current_node.identifier)
            curdata = current_node.data
            first_child = cur_node_children[0]
            if first_child.tag == "identifier":  
                # case: add(a, b)
                operation_name = first_child.data["code"]
                # if "sub" in operation_name:
                #     print("debug")
                if operation_name in ["add", "sub", "div", "mul", "divCeil"]: 
                    # 把操作上移动到当前节点
                    tree.remove_node( first_child.identifier )
                    curdata["type"]="call_expression"
                    curdata["code"]=operators[operation_name]
                    tree.update_node( current_node.identifier, data = curdata)

                    # 更新 siblings
                    # update comma node to operator node
                    comma_node = cur_node_children[3]
                    comma_data = comma_node.data
                    comma_data['type']=operators[operation_name]
                    comma_data['code']=operators[operation_name]
                    comma_data['text']=operators[operation_name]
                    tree.update_node( comma_node.identifier, tag=comma_data['type'], data = comma_data)

                    # 检查 call arguments
                    call_argument_node_left_operand = cur_node_children[2]
                    call_argument_node_right_operand = cur_node_children[4]
                    left_operand_children = tree.children(call_argument_node_left_operand.identifier)
                    right_operand_children = tree.children(call_argument_node_right_operand.identifier)
                    
                    if left_operand_children[0].is_leaf():
                        # 如果直接是变量
                        left_operand_node = left_operand_children[0]
                        tree.update_node( call_argument_node_left_operand.identifier, tag=left_operand_node.tag, data=left_operand_node.data)
                        tree.remove_node(left_operand_node.identifier)
                    else:
                        # inserted_parentheses_left = Node(
                        #         "(",
                        #         get_id(),
                        #         data={"type":"(", "start_point":None, "end_point":None, "code":"(", "text":"("}
                        # )
                        # inserted_parentheses_right = Node(
                        #         ")",
                        #         get_id(),
                        #         data={"type":")", "start_point":None, "end_point":None, "code":")", "text":")"}
                        # )
                        # insert_before( tree, current_node, call_argument_node_left_operand,  inserted_parentheses_left)
                        # insert_after( tree, current_node, call_argument_node_left_operand,  inserted_parentheses_right)
                        pass
                        #rewriteMathFunction(tree, left_operand_children[0])
                    
                    if right_operand_children[0].is_leaf():
                        # 如果直接是变量
                        right_operand_node = right_operand_children[0]
                        tree.update_node( call_argument_node_right_operand.identifier, tag=right_operand_node.tag, data=right_operand_node.data)
                        tree.remove_node(right_operand_node.identifier)
                    else:
                        # inserted_parentheses_left = Node(
                        #         "(",
                        #         get_id(),
                        #         data={"type":"(", "start_point":None, "end_point":None, "code":"(", "text":"("}
                        # )
                        # inserted_parentheses_right = Node(
                        #         ")",
                        #         get_id(),
                        #         data={"type":")", "start_point":None, "end_point":None, "code":")", "text":")"}
                        # )
                        # insert_before( tree, current_node, call_argument_node_right_operand,  inserted_parentheses_left)
                        # insert_after( tree, current_node, call_argument_node_right_operand,  inserted_parentheses_right)
                        pass
                        #rewriteMathFunction(tree, right_operand_children[0])
            elif first_child.tag == "member_expression": 
                # case: a.add(c)
                member_children = tree.children(first_child.identifier)
                caller_node = member_children[0]
                point_node = member_children[1]
                operator_node = member_children[2]
                operation_name = operator_node.data['code']
                if operation_name in ["add", "sub", "div", "mul"]: 
                    parentheses_left_node = cur_node_children[1]
                    second_call_argument = cur_node_children[2]
                    parentheses_righ_node = cur_node_children[3]
                    # 把操作上移动到当前节点
                    tree.remove_node( operator_node.identifier )
                    curdata["type"]="binary_expression"
                    curdata["code"]=operators[operation_name]
                    tree.update_node( current_node.identifier, data = curdata)

                    # 删掉 point node 
                    tree.remove_node( point_node.identifier )

                    # 改变 first_child -> call_arguments
                    fdata = first_child.data
                    fdata['type'] = "call_argument"
                    tree.update_node( first_child.identifier, tag="call_argument", data=fdata )
                    # switch current node "call_expression children" the first and the second nodes  ( a  c )
                    
                    switch_positions(current_node, first_child, parentheses_left_node)
                    inserted_operator_node = Node(
                                    operators[operation_name],
                                    get_id(),
                                    data={"type":"(", "start_point":None, "end_point":None, "code":operators[operation_name], "text":operators[operation_name]}
                            )
                    insert_after( tree, current_node, first_child, inserted_operator_node) # ( a + c )
                    # inserted_parentheses_left = Node(
                    #                 "(",
                    #                 get_id(),
                    #                 data={"type":"(", "start_point":None, "end_point":None, "code":"(", "text":"("}
                    #         )
                    # inserted_parentheses_right = Node(
                    #                 ")",
                    #                 get_id(),
                    #                 data={"type":")", "start_point":None, "end_point":None, "code":")", "text":")"}
                    #         )
                    # insert_after( tree, current_node, inserted_operator_node,  inserted_parentheses_left) # ( a + ( c )
                    # insert_before( tree, current_node, inserted_operator_node,  inserted_parentheses_right) # ( a ) + ( c )
                    pass
                    #rewriteMathFunction(tree, first_child)
                    #rewriteMathFunction(tree, second_call_argument)
                else:
                    #logger.info(f"{operator_node.tag} is not add, sub, div and mul")
                    pass
                
            elif first_child.tag in [ "binary_expression", "ternary_expression"]: 
                first_child_node_children = tree.children(first_child.identifier)
                call_node = first_child_node_children[-1]
                if call_node.tag == "identifier":
                    operation_name = call_node.data["code"]
                    if operation_name in ["add", "sub", "div", "mul"]: 
                        # 把操作上移动到当前节点
                        tree.remove_node( call_node.identifier )
                        curdata["type"]="call_expression"
                        curdata["code"]=operators[operation_name]
                        tree.update_node( current_node.identifier, data = curdata)

                        # 更新 siblings
                        # update comma node to operator node
                        comma_node = cur_node_children[3]
                        comma_data = comma_node.data
                        comma_data['type']=operators[operation_name]
                        comma_data['code']=operators[operation_name]
                        comma_data['text']=operators[operation_name]
                        tree.update_node( comma_node.identifier, tag=comma_data['type'], data = comma_data)

                        # 检查 call arguments
                        call_argument_node_left_operand = cur_node_children[2]
                        call_argument_node_right_operand = cur_node_children[4]
                        left_operand_children = tree.children(call_argument_node_left_operand.identifier)
                        right_operand_children = tree.children(call_argument_node_right_operand.identifier)
                        
                        if left_operand_children[0].is_leaf():
                            # 如果直接是变量
                            left_operand_node = left_operand_children[0]
                            tree.update_node( call_argument_node_left_operand.identifier, tag=left_operand_node.tag, data=left_operand_node.data)
                            tree.remove_node(left_operand_node.identifier)
                        else:
                            # inserted_parentheses_left = Node(
                            #         "(",
                            #         get_id(),
                            #         data={"type":"(", "start_point":None, "end_point":None, "code":"(", "text":"("}
                            # )
                            # inserted_parentheses_right = Node(
                            #         ")",
                            #         get_id(),
                            #         data={"type":")", "start_point":None, "end_point":None, "code":")", "text":")"}
                            # )
                            # insert_before( tree, current_node, call_argument_node_left_operand,  inserted_parentheses_left)
                            # insert_after( tree, current_node, call_argument_node_left_operand,  inserted_parentheses_right)
                            pass
                            #rewriteMathFunction(tree, left_operand_children[0])
                    
                        if right_operand_children[0].is_leaf():
                            # 如果直接是变量
                            right_operand_node = right_operand_children[0]
                            tree.update_node( call_argument_node_right_operand.identifier, tag=right_operand_node.tag, data=right_operand_node.data)
                            tree.remove_node(right_operand_node.identifier)
                        else:
                            # inserted_parentheses_left = Node(
                            #         "(",
                            #         get_id(),
                            #         data={"type":"(", "start_point":None, "end_point":None, "code":"(", "text":"("}
                            # )
                            # inserted_parentheses_right = Node(
                            #         ")",
                            #         get_id(),
                            #         data={"type":")", "start_point":None, "end_point":None, "code":")", "text":")"}
                            # )
                            # insert_before( tree, current_node, call_argument_node_right_operand,  inserted_parentheses_left)
                            # insert_after( tree, current_node, call_argument_node_right_operand,  inserted_parentheses_right)
                            pass
                            #rewriteMathFunction(tree, right_operand_children[0])

                elif call_node.tag == "member_expression":
                     # case: a.add(c)
                    member_children = tree.children(call_node.identifier)
                    caller_node = member_children[0]
                    point_node = member_children[1]
                    operator_node = member_children[2]
                    operation_name = operator_node.data['code']
                    if operation_name in ["add", "sub", "div", "mul"]: 
                        parentheses_left_node = cur_node_children[1]
                        second_call_argument = cur_node_children[2]
                        parentheses_righ_node = cur_node_children[3]
                        # 把操作上移动到当前节点
                        tree.remove_node( operator_node.identifier )
                        curdata["type"]="call_expression"
                        curdata["code"]=operators[operation_name]
                        tree.update_node( current_node.identifier, data = curdata)

                         # 删掉 point node 
                        tree.remove_node( point_node.identifier )
                        # 改变 call_node -> call_arguments
                        fdata = call_node.data
                        fdata['type'] = "call_argument"
                        tree.update_node( call_node.identifier, tag="call_argument", data=fdata )

                        # top - up call node
                        move_toAfter(tree, call_node, current_node, first_child)
                        
                        # switch current node "call_expression children" the first and the second nodes  ( a  c )
                        switch_positions(current_node, call_node, parentheses_left_node)

                        # 插入操作符
                        inserted_operator_node = Node(
                                        operators[operation_name],
                                        get_id(),
                                        data={"type":"(", "start_point":None, "end_point":None, "code":operators[operation_name], "text":operators[operation_name]}
                                )
                        insert_after( tree, current_node, call_node, inserted_operator_node) # ( a + c )

                        # inserted_parentheses_left = Node(
                        #                 "(",
                        #                 get_id(),
                        #                 data={"type":"(", "start_point":None, "end_point":None, "code":"(", "text":"("}
                        #         )
                        # inserted_parentheses_right = Node(
                        #                 ")",
                        #                 get_id(),
                        #                 data={"type":")", "start_point":None, "end_point":None, "code":")", "text":")"}
                        #         )
                        # insert_after( tree, current_node, inserted_operator_node,  inserted_parentheses_left) # ( a + ( c )
                        # insert_before( tree, current_node, inserted_operator_node,  inserted_parentheses_right) # ( a ) + ( c )
                        pass
            else:
               # logger.info(f"{first_child.tag } is not considered")
               pass

        cur_children = tree.children(current_node.identifier)
        for child in cur_children:
            queue.append(child)

    return tree 

def getLeavesFromLeftToRight(tree):
    # base case
    root_id = tree.root
    if root_id is None:
        return
    # implement iterative preorder traversal and start
    # storing leaf nodes.
    st = []
    st.append(root_id)
    tokens = []
    while len(st) > 0:
        root_id = st.pop()
        root = tree.get_node(root_id)
        # if node is leafnode, print its data
        if root.is_leaf() or root.tag == "string" or root.tag == "number_literal":
            #print(root.data, end=" ")
            if root.tag == "number_literal": # xx days, xxx minutes
                tokens.append(root.data['code'].split()[0])
            else:
                tokens.append(root.data['code'])

        children = [ c.identifier for c in tree.children(  root_id )] if root.tag != "string" or root.tag != "number_literal"else []
        st += children[::-1]
    
    return " ".join(tokens), tokens
                
def addStatementSeparator(tree):
    def filter_sta(node):
        if node.tag in ["return_statement", "variable_declaration_statement", "expression_statement", "state_variable_declaration"]:
            return True
        else:
            return False
    
    def filter_func(node):
        if node.tag == "function_definition":
            return True
        else:
            return False
    
    def filter_bracket(node):
        if node.tag.endswith("{") or node.tag.endswith("}"):
            return True
        else:
            return False
    
    def filter_directive(node):
       # print(node.tag)
        if node.tag=="import_directive" or node.tag=="pragma_directive" or node.tag == "using_directive":
            return True
        else:
            return False
        
    stnode_list = list(tree.filter_nodes(filter_sta))   
    for n in stnode_list:
        separator_node = Node(";", get_id(),data={"type":";", "start_point":None, "end_point":None, "code":";\n", "text":";"} )
        tree.add_node( separator_node, n) 
    
    stnode_list = list(tree.filter_nodes(filter_func))   
    for n in stnode_list:
        separator_node = Node("\n", get_id(),data={"type":"\n", "start_point":None, "end_point":None, "code":"\n", "text":"\n"} )
        tree.add_node( separator_node, n)     
    


    stnode_list = list(tree.filter_nodes(filter_bracket))   
    for n in stnode_list:
        ndata = n.data
        ndata["code"] = ndata["code"]+"\n"
        tree.update_node( n.identifier, data = ndata)
    
    stnode_list = list(tree.filter_nodes(filter_directive))   
    for n in stnode_list:
        separator_node = Node(";\n", get_id(),data={"type":"\n", "start_point":None, "end_point":None, "code":";\n", "text":"\n"} )
        tree.add_node( separator_node, n)  

def move_toAfter(tree, source_node, destination_node, pos_node):
    snid = source_node.identifier
    dnid = destination_node.identifier
    #parent = self[source].predecessor(self._identifier)
    parent = tree[snid].predecessor(tree._identifier)
    # self[nid].update_successors(child_id, mode, tree_id=self._identifier)
    tree[parent].update_successors(snid, tree.node_class.DELETE, tree_id=tree._identifier)
    # tree.__update_fpointer(dnid, snid, tree.node_class.ADD)
    insert_after(tree, destination_node, pos_node, source_node)

                
def switch_positions(node, child_node1, child_node2):
    node_tree_id = node._initial_tree_id
    nid1 = child_node1.identifier
    nid2 = child_node2.identifier
    ind1 = node.successors(node_tree_id).index(nid1)
    ind2 = node.successors(node_tree_id).index(nid2)
    node.successors(node_tree_id)[ind1] = nid2
    node.successors(node_tree_id)[ind2] = nid1

def insert_before(tree, parent_node, child_node, insertednode):
    #self._nodes.update({node.identifier: node})
    tree._nodes.update({insertednode.identifier: insertednode}) 
    #self.__update_fpointer(pid, node.identifier, self.node_class.ADD)
    ptree_id = parent_node._initial_tree_id
    ind = parent_node.successors(ptree_id).index(child_node.identifier) 
    parent_node.successors(ptree_id).insert(ind, insertednode.identifier)
    #self.__update_bpointer(node.identifier, pid)
    tree[insertednode.identifier].set_predecessor(parent_node.identifier, tree._identifier)
    insertednode.set_initial_tree_id(tree._identifier)

def insert_after(tree, parent_node, child_node, insertednode):
    #self._nodes.update({node.identifier: node})
    tree._nodes.update({insertednode.identifier: insertednode}) 
    #self.__update_fpointer(pid, node.identifier, self.node_class.ADD)
    ptree_id = parent_node._initial_tree_id
    ind = parent_node.successors(ptree_id).index(child_node.identifier) 
    parent_node.successors(ptree_id).insert(ind+1, insertednode.identifier)
    #self.__update_bpointer(node.identifier, pid)
    tree[insertednode.identifier].set_predecessor(parent_node.identifier, tree._identifier)
    insertednode.set_initial_tree_id(tree._identifier)

                 
counter=None
def get_id():
    global counter
    id = counter
    counter += 1
    return id


def transformAST(code, root):
    global counter
    ast = copySitterTree(code, root)
   # ast.show()
    # nn, n = getLeavesFromLeftToRight(ast)
    # print("===========")
    # print(nn)
    # print("===========")
    counter = len(ast.nodes)
    root_node = ast.get_node( ast.root )
    modified_tree = rewriteMathFunction(ast, root_node)
    addStatementSeparator(modified_tree)
    modified_code, tokens = getLeavesFromLeftToRight(modified_tree)
    return modified_code, tokens