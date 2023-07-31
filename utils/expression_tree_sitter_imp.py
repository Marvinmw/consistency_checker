from utils.buildASTG import ASTGraphCreator, make_graph
import networkx as nx
from utils.ExpressionVisitor import TypedVisitor
from utils.tree_sitter_utils import split_functions, remove_comments_and_docstrings, solidity_parser
from utils.tree_sitter_utils import tree_to_token_index, index_to_code_token, get_constructor
import collections
from operator import itemgetter
from utils import log
from utils.transform import transformAST

logger = log.setup_custom_logger("extractExpression")

def retyping(tokens_types, code):
    '''
    tree-sitter is not very accurate
    re-type identiifer with its parent node type
    A.h() -> h()
    '''
    new_toekns_types = []
    l = len(tokens_types)
    i = 0
    while i < l:
        t = tokens_types[i]
        if t[2] == 'identifier':
            if t[3] == 'member_expression':
                while i < len(tokens_types) and tokens_types[i][3] == 'member_expression':
                    i = i + 1
                #t1, t2, t3 = tokens_types[i], tokens_types[i+1], tokens_types[i+2]
                t3 = tokens_types[i-1]
                assert t3[3] == 'member_expression', f"{t3}"
                fnname = index_to_code_token(t3,code)
                if fnname in ['add', "sub", "mul", "div"]:
                    t1 = tokens_types[i-3]
                    t2 = tokens_types[i-2]
                    new_toekns_types.append( (t1[0], t1[1], f'identifier', 'call_expression' ) )
                    new_toekns_types.append( ( t2[0], t2[1], f'.', 'call_expression' ) )
                    new_toekns_types.append( ( t3[0], t3[1], f'call_method', 'call_expression' ) )
                else:
                    newt = (t3[0], t3[1], f'call_method', 'call_expression' )
                    new_toekns_types.append(newt)
            elif t[3] == 'call_expression':
                new_toekns_types.append((t[0], t[1], 'call_method', 'call_expression'))
                i = i+1
            elif t[3] == 'call_argument':
                new_toekns_types.append((t[0], t[1], 'identifier', 'call_argument'))
                i = i+1
            elif i+1 < l:  # a-f() f is identifier
                t_next = tokens_types[i+1]
                if t_next[3] == 'call_expression' and t_next[2] == "(":
                    new_toekns_types.append((t[0], t[1], 'call_method', 'call_expression'))
                else:
                    new_toekns_types.append(t)
                i = i + 1
            else:
                new_toekns_types.append(t)
                i = i+1
        else:
            new_toekns_types.append(t)
            i = i+1
    return new_toekns_types
            
def get_assignment_index(code_tokens):
    for i, c in enumerate(code_tokens):
        if c == "=":
            return i    
    return -1 


def class_state_definition_expression(contract_code, isAll = True ):
    '''
    int a = 10;
    int a;
    '''
    contract_code=remove_comments_and_docstrings(contract_code, lang='sol')
    tree = solidity_parser.parse(bytes(contract_code,'utf8')) 
    # rewrite add sub mul div
    modified_code, _ = transformAST(contract_code, tree.root_node)
    contract_code = modified_code
    tree = solidity_parser.parse(bytes(contract_code,'utf8')) 

    type_visitor = TypedVisitor()
    type_visitor.walk(tree)
    res_statment = collections.defaultdict(list)
    for ex in type_visitor.type_to_node['state_variable_declaration']:
        # if "buybackMultiplierLength" in ex.text.decode():
        #     print("debug")
        tokens_index=tree_to_token_index(ex)  
        code=contract_code.split('\n')   
        tokens_index = retyping(tokens_index, code)
        code_tokens=[ index_to_code_token(x,code) for x in tokens_index ]
        assgnindex = get_assignment_index(code_tokens)
        #assert assgnindex != -1
        if assgnindex == -1:
            if isAll:
                c=" ".join(code_tokens)
                c=c.replace("[", "")
                c=c.replace("]", "")
                c=c.replace("(", "")
                c=c.replace(")", "")
                c=c.replace(";", "")
                v_name=c.split()[-1]
                v_type=c.split()[0]
                res_statment[v_name].append({ "start":ex.start_point,  "code": "", "code_type":v_type, "raw_code":ex.text, "pos":(ex.start_point, ex.end_point)  } )
            continue
        token_types = [ x[2] for x in tokens_index ]
        c=" ".join(code_tokens)
        cs = c.split("=")
        vars_part = cs[0].strip()
        def_part = cs[1].strip()
        vars_part = vars_part.replace(")", "")
        vars_part = vars_part.replace("(", "")
        vars_part=vars_part.strip()
        if vars_part.endswith(","):
            vars_part = vars_part[:-1].strip()
        if ","  not in vars_part:
            tmpv = vars_part.split(" ")
            # print("======================")
            # print(tmpv)
            v_name = tmpv[-1] #code_tokens[assgnindex-1]
            if "[" in vars_part:
                v_name = vars_part
            v_type = tmpv[0]
            #print(f"{tokens_index}")
            res_statment[v_name].append({ "start":ex.start_point,  "code": " ".join(code_tokens[assgnindex+1:]), "code_type":v_type, "raw_code":ex.text, "pos":(ex.start_point, ex.end_point)  } )
        else:
            r=split_multiple_def(vars_part, def_part, ex, token_types, assgnindex)
            for k in r:
                res_statment[k].extend(r[k])
    return res_statment


def check_if_return_if(node):
    while( node.parent is not None ):
        if node.parent.type == "if_statement":
            condition_node = node.parent.children[2] # if ( condtion
            isElse = False
            #print(node.prev_sibling.text)
            while( node.prev_sibling is not None ):
                if(node.prev_sibling.type=='else'):
                    isElse = True
                node = node.prev_sibling
            return True, isElse, condition_node.text
        node = node.parent
    return False, False, None


def relace_fn_call(tokens_index, class_var_statment, fnc_code, fns, f_name):
    l = len(tokens_index)
    queue_return = []
    all_res = []
    init = True
    while len(queue_return) != 0 or init:
        init = False
        if len(queue_return) == 0:
            res = []
            i = 0
        else:
            (res,i) = queue_return.pop()
        while i < l:
            t = tokens_index[i]
            if t[2] == 'call_method':
                fn_name = index_to_code_token( t, fnc_code )
                #print("replace return call expression")
                if fn_name in fns:
                    if f_name != fn_name:
                        data=function_expressionReFormat(class_var_statment, fns[fn_name], fns, fn_name)
                        ###logger.info( fns[fn_name])
                        f_return = data['return']
                        if len(f_return):
                            rr = f_return[0]
                            for r in f_return:
                                # if len(r['code_type']) > len(rr['code_type']): 
                                #     rr = r
                                rr = r
                                res_copy = res.copy()
                                res_copy.append( "(" + rr['code'] + ")" )
                                tmp_i = i
                                search_stack = [ ]
                                assert tokens_index[tmp_i+1][2] == "("
                                while tmp_i<l: # and tokens_index[i][-1] == 'call_expression'
                                    tmp_i = tmp_i + 1
                                    if tokens_index[tmp_i][2] == "(":
                                        search_stack.append("(")
                                    if tokens_index[tmp_i][2] == ")":
                                        search_stack.pop()
                                    if len(search_stack) == 0:
                                        tmp_i = tmp_i + 1
                                        break
                                queue_return.append((res_copy, tmp_i))
                            (res,i) = queue_return.pop()
                        else:
                            res.append( index_to_code_token( t, fnc_code ) if len(t) ==4 else t[4])
                            i = i + 1
                    else:
                        res.append( index_to_code_token( t, fnc_code ) if len(t) ==4 else t[4])
                        i = i + 1
                else:
                    res.append( index_to_code_token( t, fnc_code ) if len(t) ==4 else t[4])
                    i = i + 1
            else:
                res.append( index_to_code_token( t, fnc_code ) if len(t) ==4 else t[4] )
                i = i + 1
        all_res.append(res)
    return all_res

def replace_var(tokens_index, var_list, code):
    l = len(tokens_index)
    i = 0
    new_tokens_index = []
    while i < l:
        t = tokens_index[i]
        v = index_to_code_token( t, code )
        if t[-2] == 'identifier':
            if index_to_code_token( t, code )  in var_list:
                ##logger.info(f"===========  { var_list[ index_to_code_token( t, code ) ][-1]}")
                if "_literal" in var_list[ index_to_code_token( t, code ) ][-1]['code_type'][0] or "string" in var_list[ index_to_code_token( t, code ) ][-1]['code_type'][0]:
                   new_tokens_index.append(t)
                else:
                    new_tokens_index.append( (t[0], t[1], t[2], t[3], "(" + var_list[ index_to_code_token( t, code ) ][-1]['code'] + ")" ) )
            else:
                new_tokens_index.append(t)    
        else:
            new_tokens_index.append(t)    
        i = i + 1
    return new_tokens_index

import re
def split_multiple_def(vars_part, def_part, ex, token_types, assgnindex):
    r=collections.defaultdict(list)
    vars_part = vars_part.replace(")", "")
    vars_part = vars_part.replace("(", "")
    vars_part=vars_part.strip()
    vp = vars_part.split(",")
    def_part =  def_part.strip()
    if def_part.startswith("("):
        def_part = def_part.replace(")", "")
        def_part = def_part.replace("(", "")
    dp = def_part.split(",")
    if len(vp) == len(dp):
        for i,v in enumerate(vp):
            v = v.strip()
            vv = v.split(" ")
            #print(vv)
            vname = vv[-1]
            r[vname].append( { "start":ex.start_point,   "code": dp[i], "code_type":token_types[assgnindex+1:], "raw_code":ex.text.decode(), "pos":(ex.start_point, ex.end_point)  } )
    return r



def function_expressionRaw(class_var_statment, fn_code, fns):
    tree = solidity_parser.parse(bytes(fn_code,'utf8')) 
    # rewrite add sub mul div
    modified_code, _ = transformAST(fn_code, tree.root_node)
    fn_code = modified_code

    tree = solidity_parser.parse(bytes(fn_code,'utf8')) 
    tokens_index = tree_to_token_index(tree.root_node) 
    type_visitor = TypedVisitor()
    type_visitor.walk(tree)
    return_statement = []
     #variable_declaration_statement
    declaration_statement = collections.defaultdict(list)
    code=fn_code.split('\n')
    for ex in type_visitor.type_to_node['variable_declaration_statement']:
        tokens_index=tree_to_token_index(ex)  
       # #logger.info(tokens_index) 
        code=fn_code.split('\n')
        code_tokens = [ index_to_code_token(x,code) for x in tokens_index ]
        assgnindex = get_assignment_index(code_tokens)
        # assert assgnindex != -1, f"{code_tokens}"
        if assgnindex == -1:
            continue
        token_types = [ x[2] for x in tokens_index ] 
        c=" ".join(code_tokens)
        cs = c.split("=")
        vars_part = cs[0].strip()
        def_part = cs[1].strip()
        vars_part = vars_part.replace(")", "")
        vars_part = vars_part.replace("(", "")
        vars_part=vars_part.strip()
        if vars_part.endswith(","):
            vars_part = vars_part[:-1].strip()
        if ","  not in vars_part:
            tmpv = vars_part.split(" ")
            # print("======================")
            # print(tmpv)
            v_name = tmpv[-1] #code_tokens[assgnindex-1]
            if "[" in vars_part:
                v_name = vars_part
            v_type = tmpv[0]
            #logger.info(f'variable_declaration_statement expression raw {ex.text} , remove = , { " ".join(code_tokens[assgnindex+1:])}')
            declaration_statement[v_name].append( { "start":ex.start_point,   "code": " ".join(code_tokens[assgnindex+1:]), "code_type":v_type, "raw_code":ex.text.decode(), "pos":(ex.start_point, ex.end_point)  } )
        else:
            r=split_multiple_def(vars_part, def_part, ex, token_types, assgnindex)
            for k in r:
                declaration_statement[k].extend(r[k])



    assign_statement =collections.defaultdict(list)
    for ex in  type_visitor.type_to_node['assignment_expression']:
        tokens_index=tree_to_token_index(ex)  
        code=fn_code.split('\n')
        code_tokens=[ index_to_code_token(x,code) for x in tokens_index ]
        assgnindex = get_assignment_index(code_tokens)
        assert assgnindex != -1
        token_types = [ x[2] for x in tokens_index ] 
        c=" ".join(code_tokens)
        cs = c.split("=")
        vars_part = cs[0].strip()
        vars_part = vars_part.replace(")", "")
        vars_part = vars_part.replace("(", "")
        vars_part=vars_part.strip()
        if vars_part.endswith(","):
            vars_part = vars_part[:-1].strip()
       
        def_part = cs[1].strip()
        if ","  not in vars_part:
            tmpv = vars_part.split(" ")
            v_name = tmpv[-1] #code_tokens[assgnindex-1]
            if "[" in vars_part:
                v_name = vars_part
            v_type = tmpv[0]
           # #logger.info(f'assignment_expression expression raw {ex.text}, remove = ,{ " ".join(code_tokens[assgnindex+1:])}')
            assign_statement[v_name].append( {"start":ex.start_point, "code": " ".join(code_tokens[assgnindex+1:]), "code_type":v_type, "raw_code":ex.text.decode(), "pos": (ex.start_point, ex.end_point)}  )
        else:
            r=split_multiple_def(vars_part, def_part, ex, token_types, assgnindex)
            for k in r:
                assign_statement[k].extend(r[k])

    expression_statement = collections.defaultdict(list)
   

    var_list = collections.defaultdict(list)
    local_var_list = collections.defaultdict(list)
    for var_statements in [ expression_statement, assign_statement, declaration_statement, class_var_statment]:
        for v in var_statements.keys():
            var_list[v].extend( var_statements[v] )
    
    for var_statements in [ expression_statement, assign_statement, declaration_statement]:
        for v in var_statements.keys():
            local_var_list[v].extend( var_statements[v] )
          
    for vv in var_list:
        var_list[vv] = sorted(var_list[vv], key=itemgetter('start')) 
    for ex in type_visitor.type_to_node['return_statement']:
        inIf, isBranch, condition = check_if_return_if(ex)
        tokens_index=tree_to_token_index(ex)
        code_tokens=[ index_to_code_token(x,code) for x in tokens_index ]
        tokens_index = retyping(tokens_index, code)
        code_tokens=[ index_to_code_token(x,code) for x in tokens_index ]
        tokens_index=tokens_index[1:]
        token_types = [ x[2] for x in tokens_index ]
       # ##logger.info(f'return_statement expression raw {ex.text} ')
        rcode = ex.text.decode('utf8').replace("return", "")
        rcode=rcode.replace(";", "")
        if len(rcode.strip()):
            return_statement.append( {  "code":rcode,  "code_type":token_types, "raw_code":ex.text.decode(), "pos":(ex.start_point, ex.end_point) , "if-else":(inIf, isBranch, condition) } )
    
 
    return {"return":return_statement, "var":local_var_list}

def function_expressionReFormat(class_var_statment, fn_code, fns, f_name):
    tree = solidity_parser.parse(bytes(fn_code,'utf8')) 
    # rewrite add sub mul div
    modified_code, _ = transformAST(fn_code, tree.root_node)
    fn_code = modified_code

    tree = solidity_parser.parse(bytes(fn_code,'utf8')) 
    tokens_index = tree_to_token_index(tree.root_node) 
    type_visitor = TypedVisitor()
    type_visitor.walk(tree)
    return_statement = []
     #variable_declaration_statement
    declaration_statement = collections.defaultdict(list)
    code=fn_code.split('\n')
    for ex in type_visitor.type_to_node['variable_declaration_statement']:
        tokens_index=tree_to_token_index(ex)  
       # ##logger.info(tokens_index) 
        tokens_index = retyping(tokens_index, code)  # relace_fn_call(tokens_index, class_var_statment, fnc_code, fns)
        code=fn_code.split('\n')
        code_tokens = [ index_to_code_token(x,code) for x in tokens_index ]
        # tokens_index=replace_var(tokens_index, var_list, code)
        code_tokens_all = relace_fn_call(tokens_index, class_var_statment, code, fns, f_name) 
        for code_tokens in code_tokens_all:
            assgnindex = get_assignment_index(code_tokens)
            #assert assgnindex != -1, f"{code_tokens}"
            if assgnindex == -1:
                continue
            token_types = [ x[2] for x in tokens_index ] 
            c=" ".join(code_tokens)
            cs = c.split("=")
            vars_part = cs[0].strip()
            vars_part = vars_part.replace(")", "")
            vars_part = vars_part.replace("(", "")
            vars_part=vars_part.strip()
            if vars_part.endswith(","):
                vars_part = vars_part[:-1].strip()
            def_part = cs[1].strip()
            if ","  not in vars_part:
                tmpv = vars_part.split(" ")
                v_name = tmpv[-1] #code_tokens[assgnindex-1]
                if "[" in vars_part:
                    v_name = vars_part
                v_type = tmpv[0]
                ##logger.info(f'variable_declaration_statement expression raw {ex.text} , remove = , { " ".join(code_tokens[assgnindex+1:])}')
                declaration_statement[v_name].append( { "start":ex.start_point,   "code": " ".join(code_tokens[assgnindex+1:]), "code_type":v_type, "raw_code":ex.text.decode(), "pos":(ex.start_point, ex.end_point)  } )
            else:
                r=split_multiple_def(vars_part, def_part, ex, token_types, assgnindex)
                for k in r:
                    declaration_statement[k].extend(r[k])

    assign_statement =collections.defaultdict(list)
    for ex in  type_visitor.type_to_node['assignment_expression']:
        tokens_index=tree_to_token_index(ex)  
       # ##logger.info(tokens_index) 
        tokens_index = retyping(tokens_index, code)     
        code=fn_code.split('\n')
        code_tokens=[ index_to_code_token(x,code) for x in tokens_index ]
        code_tokens_all = relace_fn_call(tokens_index, class_var_statment, code, fns, f_name)
        for code_tokens in code_tokens_all:
            assgnindex = get_assignment_index(code_tokens)
            assert assgnindex != -1
            token_types = [ x[2] for x in tokens_index ] 
            c=" ".join(code_tokens)
            cs = c.split("=")
            vars_part = cs[0].strip()
            vars_part = vars_part.replace(")", "")
            vars_part = vars_part.replace("(", "")
            vars_part=vars_part.strip()
            if vars_part.endswith(","):
                vars_part = vars_part[:-1].strip()
            def_part = cs[1].strip()
            if ","  not in vars_part:
                tmpv = vars_part.split(" ")
                v_name = tmpv[-1] #code_tokens[assgnindex-1]
                if "[" in vars_part:
                    v_name = vars_part
                v_type = tmpv[0]
                ##logger.info(f'assignment_expression expression raw {ex.text}, remove = ,{ " ".join(code_tokens[assgnindex+1:])}')
                assign_statement[v_name].append( {"start":ex.start_point, "code": " ".join(code_tokens[assgnindex+1:]), "code_type":v_type, "raw_code":ex.text.decode(), "pos": (ex.start_point, ex.end_point)}  )
            else:
                r=split_multiple_def(vars_part, def_part, ex, token_types, assgnindex)
                for k in r:
                    assign_statement[k].extend(r[k])
    expression_statement = collections.defaultdict(list)
    

    var_list = collections.defaultdict(list)
    local_var_list = collections.defaultdict(list)
    for var_statements in [ expression_statement, assign_statement, declaration_statement, class_var_statment]:
        for v in var_statements.keys():
            var_list[v].extend( var_statements[v] )
    
    for var_statements in [ expression_statement, assign_statement, declaration_statement]:
        for v in var_statements.keys():
            local_var_list[v].extend( var_statements[v] )
          
    for vv in var_list:
        var_list[vv] = sorted(var_list[vv], key=itemgetter('start')) 
    
    for ex in type_visitor.type_to_node['return_statement']:
        inIf, isBranch, condition = check_if_return_if(ex)
        tokens_index=tree_to_token_index(ex)
        code_tokens=[ index_to_code_token(x,code) for x in tokens_index ]
        tokens_index = retyping(tokens_index, code)
        code_tokens=[ index_to_code_token(x,code) for x in tokens_index ]
        tokens_index=tokens_index[1:]
        token_types = [ x[2] for x in tokens_index ]
        tokens_index=replace_var(tokens_index, var_list, code)
        res_all = relace_fn_call(tokens_index, class_var_statment, code, fns, f_name)
        ##logger.info(f'return_statement expression before {ex.text} , after { " ".join(res) }')
        for res in res_all:
            return_statement.append( {  "code":" ".join(res),  "code_type":token_types, "raw_code":ex.text, "pos":(ex.start_point, ex.end_point) , "if-else":(inIf, isBranch, condition) } )
    
    # 函数里的常量
    local_constant = get_all_constant(fn_code)
    # 根据 var 在代码里出现的最后位置确定 expression
    return {"return":return_statement, "var":local_var_list, "local_constant":local_constant}


def parse_methods(contract_code):
    '''
    # return code
    '''
    code=remove_comments_and_docstrings(contract_code, "solidity")
    res=split_functions(code)
    #print(res)
    return res

def get_all_expression(contract_code, expression_raw=True, keep_classtate=True):
    '''
    return all variables in the contract_code
    {'class_state':dict, func: {'return':list, 'var':{str:list}} }
    '''
    fns = parse_methods(contract_code)
   # print(contract_code)
    if not expression_raw:
        tree = solidity_parser.parse(bytes(contract_code,'utf8')) 
        # rewrite add sub mul div
        contract_code, _ = transformAST(contract_code, tree.root_node)
    class_var_statment = class_state_definition_expression(contract_code)
    res_fn = {}
    for f_name, f_code in fns.items():
       # ##logger.info(f_code)
        if expression_raw:
            a=function_expressionRaw(class_var_statment if not keep_classtate else {}, f_code, fns)
        else:
            a=function_expressionReFormat(class_var_statment if not keep_classtate else {}, f_code, fns, f_name)
        res_fn[f_name] = a
    res = {}
    res = {"class_state":class_var_statment, "function":res_fn}
    return res

def get_all_constant(contract_code, key_words=["state_variable_declaration", "assignment_expression", "variable_declaration_statement"]):
    contract_code = remove_comments_and_docstrings(contract_code, lang="sol")
    tree = solidity_parser.parse(bytes(contract_code,'utf8')) 
    type_visitor = TypedVisitor()
    type_visitor.walk(tree)
    res_statment = collections.defaultdict(list)
    node_list = [ n for k in key_words  for n in type_visitor.type_to_node[k] ]
    for ex in node_list:
        tokens_index=tree_to_token_index(ex)  
        c = ex.children[-1]
        if "_literal" in c.type:
            tokens_index=tree_to_token_index(ex)  
            code=contract_code.split('\n')   
            tokens_index = retyping(tokens_index, code)
            code_tokens=[ index_to_code_token(x,code) for x in tokens_index ]
            assgnindex = get_assignment_index(code_tokens)
            #assert assgnindex != -1
            if assgnindex == -1:
                continue
            token_types = [ x[2] for x in tokens_index ]
            c=" ".join(code_tokens)
            cs = c.split("=")
            vars_part = cs[0].strip()
            vars_part = vars_part.replace(")", "")
            vars_part = vars_part.replace("(", "")
            vars_part=vars_part.strip()
            if vars_part.endswith(","):
                vars_part = vars_part[:-1].strip()
            def_part = cs[1].strip()
            if ","  not in vars_part:
                tmpv = vars_part.split(" ")
                v_name = tmpv[-1] #code_tokens[assgnindex-1]
                if "[" in vars_part:
                    v_name = vars_part
                v_type = tmpv[0]
                #print(f"{tokens_index}")
                res_statment[v_name].append({ "start":ex.start_point,  "code": " ".join(code_tokens[assgnindex+1:]), "code_type":v_type, "raw_code":ex.text, "pos":(ex.start_point, ex.end_point)  } )
            else:
                r=split_multiple_def(vars_part, def_part, ex, token_types, assgnindex)
                for k in r:
                    res_statment[k].extend(r[k])
    return res_statment


def get_all_assignment(contract_code, key_words=["assignment_expression"]):
    contract_code = remove_comments_and_docstrings(contract_code, lang="sol")
    tree = solidity_parser.parse(bytes(contract_code,'utf8')) 
    type_visitor = TypedVisitor()
    type_visitor.walk(tree)
    res_statment = collections.defaultdict(list)
    node_list = [ n for k in key_words  for n in type_visitor.type_to_node[k] ]
    for ex in node_list:
        tokens_index=tree_to_token_index(ex)  
        # c = ex.children[-1]
        if True: #"_literal" in c.type:
            tokens_index=tree_to_token_index(ex)  
            code=contract_code.split('\n')   
            tokens_index = retyping(tokens_index, code)
            code_tokens=[ index_to_code_token(x,code) for x in tokens_index ]
            assgnindex = get_assignment_index(code_tokens)
            #assert assgnindex != -1
            if assgnindex == -1:
                continue
            token_types = [ x[2] for x in tokens_index ]
            c=" ".join(code_tokens)
            cs = c.split("=")
            vars_part = cs[0].strip()
            vars_part = vars_part.replace(")", "")
            vars_part = vars_part.replace("(", "")
            vars_part=vars_part.strip()
            if vars_part.endswith(","):
                vars_part = vars_part[:-1].strip()
            def_part = cs[1].strip()
            if ","  not in vars_part:
                tmpv = vars_part.split(" ")
                v_name = tmpv[-1] #code_tokens[assgnindex-1]
                if "[" in vars_part:
                    v_name = vars_part
                v_type = tmpv[0]
                #print(f"{tokens_index}")
                res_statment[v_name].append({ "start":ex.start_point,  "code": " ".join(code_tokens[assgnindex+1:]), "code_type":v_type, "raw_code":ex.text, "pos":(ex.start_point, ex.end_point)  } )
            else:
                r=split_multiple_def(vars_part, def_part, ex, token_types, assgnindex)
                for k in r:
                    res_statment[k].extend(r[k])
    return res_statment

def get_contract_ConstantStates(code):
    r0 = get_all_constant(code, key_words=["state_variable_declaration"] )
    r1 = get_constructor_ConstantStates(code)
    r0.update(r1)
    return r0

def get_constant_definedInfunction(contract_code, contractStates, constantState):
    
    contract_code = remove_comments_and_docstrings(contract_code, lang="sol")
    tree = solidity_parser.parse(bytes(contract_code,'utf8')) 
    contract_code, _ = transformAST(contract_code, tree.root_node)
    
    res = get_all_assignment(contract_code, key_words=["assignment_expression"])
    for c in contractStates:
        if c not in constantState:
            if c in res:
                for l in res[c]:
                    try:
                        if int(l["code"]) == 0:
                            continue
                        constantState[c] = [l]
                    except Exception as e:
                        continue
    
    for c,v in contractStates.items():
        if v[0]['code'].strip() == "":
            if c in res and len(res[c]) == 1:
                contractStates[c] = res[c]


    return contractStates, constantState

def get_constructor_ConstantStates(code):
    cleaned_code = remove_comments_and_docstrings(code, lang="sol")
    fn = get_constructor(cleaned_code)
    res = {}
    for f in fn:
        wrap_code = "contract A { " + fn[f] + "}"
        r = get_all_constant(wrap_code, key_words=["assignment_expression"] )
        res.update(r)
    return res

def get_contract_States(code):
    return class_state_definition_expression(code)

def get_contract_ConstantVar(code):
    fns = parse_methods(code)
    res = {}
    for f in fns:
        r = get_all_constant(fns[f])
        if len(r):
            res[f] = r
    return res
