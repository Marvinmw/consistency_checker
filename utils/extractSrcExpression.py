from utils.expression_tree_sitter_imp import get_all_expression
from parser_imp_js.code2jsonTree import getTreeJson
from parser_imp_js.tree_matcher import match_graphs, build_express_tree, match_expressions,build_SingleNode
import collections
import argparse
import pickle
import os
import glob
import re
from utils import log

logger = log.setup_custom_logger("extractExpression")

def clean_array_symbol(expression):
   # print(expression)
    result1 = re.findall(r'(\w+\s*(\[\s*(\w|\(|\)|\s)+\s*\]\s*)+)', expression)
    for r in result1:
        h = r[0]
        e = re.sub(r'[^\w]+', "_", h)
        es = "".join(e.split())
        expression = expression.replace(h, es)
    return expression

def clean_contract_code(contract_code):
    contract_code = contract_code.replace('.fromUInt()', '')
    contract_code = contract_code.replace('.toUInt()', '')
    contract_code = contract_code.replace('Math.', '')
    contract_code = contract_code.replace('SignedMath.', '')

    # WadMath
    # contract_code = contract_code.replace('.wadMul', '+')
    # contract_code = contract_code.replace('.wadDiv', '*')
    # contract_code = contract_code.replace('.wadAdd', '/')

    # contract_code = contract_code.replace('.rayMul', '+')
    # contract_code = contract_code.replace('.rayDiv', '*')
    # contract_code = contract_code.replace('.rayAdd', '/')


    contract_code = contract_code.replace('.wadMul', '.mul')
    contract_code = contract_code.replace('.wadDiv', '.div')
    contract_code = contract_code.replace('.wadSub', '.sub')
    contract_code = contract_code.replace('.wadAdd', '.add')

    contract_code = contract_code.replace('.rayMul', '.mul')
    contract_code = contract_code.replace('.rayDiv', '.div')
    contract_code = contract_code.replace('.rayAdd', '.add')
    contract_code = contract_code.replace('.raySub', '.sub')
  
    # replace a.b.c.d -> c.d
    # (\w+\.){2,}
    #logger.info(f"replace long funciotn call a.b.c.d -> c.d")
    result1 = re.findall(r'\w+(?:\.\w+)+\(', contract_code)
    for r in result1:
        r=r.replace("(", "")
        rs = r.split(".")[-2:]
        newr=".".join(rs)
        ##logger.info(f"======== {r} {rs}")
        contract_code = contract_code.replace(r, newr)

    result2 = re.findall(r'(sub|add|div|mul)\s*\(.*?\s*\"(.*?)\"\)', contract_code)
    # pattern = re.compile(r'(sub|add|div|mul)\(.*?,\s*\"(.*?)\"\)')   # 只匹配 "sub(" 开头的函数调用中的字符串
    for r in result2:
        ##logger.info(f"======== {r} {rs}")
        sc = r[-1]
        contract_code = re.sub(rf',*\s*\"{sc}\"', ' ', contract_code)
    return contract_code


# def process_expression(exp):
#     expression=getTreeJson(exp)
#     G=build_express_tree(expression)
#     fn_g['return'].append((G, r['code'], expression, r))

def process_code(code_file, isCleanCode=True, imp="tree-sitter"):
    #logger.info("process_code")
    contract_code = None
    with open(code_file) as f:
       contract_code = f.read()
    if isCleanCode:
        contract_code = clean_contract_code(contract_code)
    if imp == 'tree-sitter':
        varInCode = get_all_expression(contract_code)
    elif imp == 'slither':
        assert False, "No implementation"
    # {'class_state':dict, func: {'return':list, 'var':{str:list}} }
    
    # convert expression to expression tree in networkx Graph format
    class_statements = varInCode['class_state']
    res_fns = collections.defaultdict(list)
    functions = varInCode['function'] 
    for fn_name in functions:
        fn_g = collections.defaultdict(list)
        fn_g['var'] = collections.defaultdict(list)
        return_statements = functions[fn_name]['return']
        var_statements = functions[fn_name]['var']
        for r in return_statements:
            if len(r['code_type'])!=1:
                try:
                    expression=getTreeJson(r['code'])
                    G=build_express_tree(expression)
                    fn_g['return'].append((G, r['code'], expression, r))
                except Exception as e:
                    pass
                #     #logger.info(e)
                #    #logger.info(f"{e} == {r['code']}")
                    #logger.info(f" Exception {e} == {v['code']}")
            else:
                G = build_SingleNode(r['code'], r['code_type'][0], r['code'])
                fn_g['return'].append((G, r['code'], {}, r))

        for vname, vlist in var_statements.items():
            vg_list = []
            for v in vlist:
                if len(v['code_type'])!=1:
                    try:
                        expression=getTreeJson(v['code'])
                        G=build_express_tree(expression)
                        vg_list.append((G, v['code'], expression, v))
                    except Exception as e:
                        pass
                        #raise  Exception(f"{e} == {v['code']}")
                        #logger.info(f" Exception {e} == {v['code']}")
                else:
                    G = build_SingleNode(v['code'], v['code_type'][0], v['code'])
                    vg_list.append((G, v['code'], {},v))
            fn_g['var'][vname].extend(vg_list)
        res_fns[fn_name] = fn_g
    res_class = {}
    for class_variable in class_statements:
        c = class_statements[class_variable][0]
        if len(c['code_type'])!=1:
            try:
                expression=getTreeJson(class_statements[class_variable][0]['code'])
                G=build_express_tree(expression)
                res_class[class_variable] = (G, class_statements[class_variable][0]['code'], expression, class_statements[class_variable][0])
            except Exception as e:
                pass
                        #logger.info(f"Exception {e} == {class_statements[class_variable][0]['code']}")
        else:
            G = build_SingleNode(v['code'], v['code_type'][0], v['code'])
            res_class[class_variable] = (G, v['code'], {},class_statements[class_variable][0]) 
    return ( res_class, res_fns )



def getSolidityFiles(input_dir):
    sol_list = {}
    for sol_file in glob.glob(f"{input_dir}/***.sol", recursive=True):
        #logger.info(sol_file)
        fname = os.path.basename(sol_file)
        sol_list[fname] = sol_file
    return sol_list

def process_projects(project_dir, whitepaper_imp_file, isCleanCode=True):
    sol_list = getSolidityFiles(project_dir )
    project_data = { }
    for sol_file in sol_list:
        project_data[sol_file] = process_code( sol_list[sol_file] , isCleanCode)
    whitepaper_data = process_code( whitepaper_imp_file , isCleanCode)
    return project_data, whitepaper_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="solidity file")
    parser.add_argument("-o", "--output", type=str, help="pickle file with Graph Type")    
    parser.add_argument("-b", "--backend", type=str, default="tree-sitter", help="processing backend")    
    args = parser.parse_args()
    data = process_code(args.input, args.backend)
    pickle.dump(data, open(args.output, "wb"))


