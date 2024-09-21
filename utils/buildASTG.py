
import networkx as nx
from matplotlib import pyplot as plt
import warnings
from utils.tree_sitter_utils import index_to_code_token


def make_graph(code, root_node, function_tree, strict=True):
    visitor = ASTGraphCreator(code, function_tree, strict=strict)
    visitor.visit(root_node, parent_id=None)
    return visitor


class ASTGraphCreator( ):
    """
    AST visitor which creates a CFG.
    After traversing the AST by calling visit() on the root, self.cfg has a complete CFG.
    """

    def __init__(self, code, function_tree, strict):
        super(ASTGraphCreator).__init__()
        self.ast = nx.DiGraph()
        self.node_id = 0
        self.strict = strict
        self.code = code
        self.function_tree = function_tree
        self.node_type = []

    def visit_children(self, n, **kwargs):
        for i, c in enumerate(n.children):
            self.visit(c, child_idx=i, **kwargs)
            

    def visit(self, n, parent_id, **kwargs):
        code = n.text.decode()
        my_id = self.node_id
        self.node_type.append( n.type )
        self.node_id += 1
        if parent_id is None:
            self.ast.graph["root_node"] = my_id
        
        def attr_to_label(node_type, index_code_node, numchid):
            if numchid == 0:
                trimmed_code = index_to_code_token(index_code_node, self.code.split("\n"))
            else:
                trimmed_code = ""
           
            return node_type + ":" + trimmed_code
        sp = n.start_point
        ep = n.end_point 

        self.ast.add_node(
            my_id,
            n=n,
            label=attr_to_label(n.type, (sp, ep), len(n.children) or n.type=="string"),
            code=code,
            node_type=n.type,
            start=n.start_point,
            end=n.end_point,
            **kwargs
        )
        if parent_id is not None:
            self.ast.add_edge(parent_id, my_id)
        self.visit_children(n, parent_id=my_id)


