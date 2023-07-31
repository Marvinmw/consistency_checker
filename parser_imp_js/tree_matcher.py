import networkx as nx
from parser_imp_js.code2jsonTree import getTreeJson
from utils import log
logger = log.setup_custom_logger("extractExpression")

def _abstract_node(node):
    n = node.copy()
    if n['type'] == 'SymbolNode':
        n['value'] = 'identifier'
    if n['type'] == 'ConstantNode':
        n['value'] = 'constant'
    return n


def _node_match(node1, node2):
    n1 = _abstract_node(node1)
    n2 = _abstract_node(node2)
    
    v1 = n1['value']
    t1 = n1['type']

    v2 = n2['value']
    t2 = n2['type']
    if v1 == v2 and t1 == t2:
        return True
    else:
        return False


def getNodes(node):
     # add nodes
    res = [ ]
    if node['mathjs'] == "FunctionNode":
        value = "FCall" #node['fn']['name'] if "name" in node['fn'] else "FCall"
        text = node['text']
        type = node['mathjs']
    elif node['mathjs'] == 'OperatorNode':
        value = node['op']
        text = node['text']
        type = node['mathjs']
    elif node['mathjs'] == 'ConstantNode':
        value = node['value']
        text = node['text']
        type = node['mathjs']
    elif node['mathjs'] == 'SymbolNode':
        value = node['name']
        text = node['text']
        type = node['mathjs']
    elif node['mathjs'] == 'ParenthesisNode':
        value = '()'
        text = node['text']
        type = node['mathjs']
    elif node['mathjs'] == 'AssignmentNode':
        value = '='
        text = node['text']
        type = node['mathjs']
    elif node['mathjs']=="AccessorNode":
        #assert False, f"unhandle the type {node['mathjs']} {node}"
        #logger.warning(f"unhandle the type {node['mathjs']} {node}")
        value = 'array'
        text = node['text']
        type = node['mathjs']
    elif  node['mathjs']=="IndexNode":
        value = '[]'
        text = node['text']
        type = node['mathjs']
    elif node['mathjs']=="ConditionalNode":
        value = 'condition'
        text = node['text']
        type = node['mathjs']
    elif node['mathjs']=="BlockNode":
        print(node)
        for n in node['blocks']:
            res+=getNodes(n)
        return res
    else:
        raise Exception(f"unhandle the type {node['mathjs']}, {node}")
    res.append( (value, text, type, node['parent_id']) )
    return res

def build_express_tree(data_json_format):
    '''
    node attribute: value, type, text
    '''
    G = nx.DiGraph()
    nodes = data_json_format['nodes']

    #function_name_nodes_ignore = []
    # add nodes
    for id, node in nodes.items():
        res = getNodes(node)
        for ( value, text, type, parent_id ) in res:
            # if str(parent_id) != '-1' and type == 'SymbolNode' and nodes[ str(parent_id) ]['mathjs'] == 'FunctionNode' :
            #     function_name = nodes[ str(node['parent_id']) ]['fn']['name'] if 'name' in nodes[ str(node['parent_id']) ]['fn']
            #     if value == function_name:
            #         function_name_nodes_ignore.append( id )
            #         continue
            G.add_node(int(id), text = text, type = type, value=value)
            
    # add edges
    edges = [ ]
    for id, node in nodes.items():
        res = getNodes(node)
        for ( value, text, type, parent_id ) in res:
            if int(parent_id) == -1:
                continue
            edges.append( ( int(node['parent_id']), int(id) ) )

    G.add_edges_from( edges )
    # clean nodes, merge tow nodes with () and ()
    e_list = list(G.edges)
    n_dict = { i:i for i in list(G.nodes) }
    G.in_degree()

    # case () -> ()
    for (e1, e2) in e_list:
        if G.nodes[n_dict[e1]]["value"] == "()" and  G.nodes[n_dict[e2]]["value"] == "()":
            G=nx.contracted_nodes(G, n_dict[e1], n_dict[e2], self_loops=False)
            n_dict[e2] = n_dict[e1]

    # case root is ()  
    root = []
    for n, indegree in list(G.in_degree(list(G.nodes) )):
        if indegree == 0:
            root.append(n)
    assert len(root) == 1
    if G.nodes[root[0]]["value"] == "()":
        G.remove_node(root[0])

    # case non () -> ()
    for n in list(G.nodes):
        if n not in G.nodes:
            continue
        for v in G.successors(n):
            if G.nodes[v]["value"] == "()":
                G=nx.contracted_nodes(G, n, v, self_loops=False)

    return G



def build_SingleNode(text, type, value):
    '''
    node attribute: value, type, text
    '''
    G = nx.DiGraph()
    id = 0

    G.add_node(int(id), text = text, type = type, value=value)


    return G

def match_graphs(G1, G2):
    dist = nx.graph_edit_distance(G1, G2, node_match=_node_match)
    return dist


def match_expressions(expression1, expression2):
    ex1_json = getTreeJson(expression1)
    G1 = build_express_tree(ex1_json)
    ex2_json = getTreeJson(expression2)
    G2 = build_express_tree(ex2_json)
    return match_graphs(G1, G2)


