from sympy import *
from utils.bert_varname_match import match_var_names, match_twoVarList
from utils.expression_tree_sitter_imp import  get_constant_definedInfunction, get_contract_ConstantStates, get_all_expression, get_contract_States
from utils.extractSrcExpression import clean_contract_code, clean_array_symbol
from sympy import symbols, simplify
import collections
import re
# from dataclasses import dataclass
from pprint import pprint

def dict_to_markdown(data_dict, ouputfile):
    markdown = ""
    
    for section, subsections in data_dict.items():
        markdown += f"## {section}\n\n"
        
        for subsection, subsection_data in subsections.items():
            if isinstance(subsection_data, list):
                markdown += f"### {subsection}\n\n"
                value_str = ', \n '.join(subsection_data)
                markdown += f"  &ensp;** Possible Values **:\n {value_str}\n\n"
            else:
                markdown += f"### Item {subsection}\n\n"
                for key, value in subsection_data.items():
                    if isinstance(value, tuple):
                        value_str = f"  &emsp; \n- Description: {value[-1]} \n   - Possible Var Names from ChatGPT: {value[0]} \n   - Expression:  {value[1]} \n" #f"({', '.join(value)})"
                    elif isinstance(value, list):
                        value_str = ', \n '.join(value)
                    else:
                        value_str = "   "+str(value)
                    markdown += f"   &ensp;**{key}**\n {value_str}\n\n"
            
        
        markdown += "\n"
    
    with open(ouputfile, "w") as f:
        f.write(markdown)
    return markdown

def isclose(a, b, rel_tol=1e-13, abs_tol=0.0):
    # print(Abs(a - b))
    # print(max(rel_tol * max(Abs(a), Abs(b)), abs_tol))
    return Abs(a - b) <= max(rel_tol * max(Abs(a), Abs(b)), abs_tol)

def is_number(expression):
    expr = sympify(expression)
    return expr.is_number

def replace_constantInExp(constant_list, exp):
    for c in constant_list:
        exp = re.sub(rf'\b({c})\b', constant_list[c], exp)
    return exp

def replace_logic_timeUnit(exp):
    exp = exp.replace("||", "|")
    exp = exp.replace("&&", "&")
    exp = exp.replace("!", "~")
    exp = re.sub(r"\b(minutes)\b", " ", exp)
    exp = re.sub(r"\b(days)\b", " ", exp)
    exp = re.sub(r"\b(hours)\b", " ", exp)
    exp = re.sub(r"\b(months)\b", " ", exp)
    exp = re.sub(r"\b(years)\b", " ", exp)
    return exp

def ternary_statement(exp):
    pattern = r"(.*)\s*\?\s*(.*)\s*:\s*(.*)"
    matches = re.findall(pattern, exp)
    if matches:
        condition = matches[0][0].strip()
        expression_true = matches[0][1].strip()
        expression_false = matches[0][2].strip()
        return True, (expression_true, expression_false)
    else:
        return False, (exp, )

import os

def checkRevenueModel(var_names_whitepaper, contract_code=None, file_list=None, top_K=3):
    assert contract_code is not None or file_list is not None,  f"{contract_code} {file_list}"
    if file_list is None:
        ContractStates=get_contract_States(contract_code)
        ConstantStates=get_contract_ConstantStates(contract_code)
        ContractStates, ConstantStates = get_constant_definedInfunction(contract_code, ContractStates, ConstantStates)
    else:
        ContractStates = {}
        ConstantStates = {}
        for fn in file_list:
            assert os.path.isfile(fn)
            with open(fn) as f:
                contract_code = f.read()
                s=get_contract_States(contract_code)
                c=get_contract_ConstantStates(contract_code)
                ContractStates.update(s)
                ConstantStates.update(c)
        ContractStates, ConstantStates = get_constant_definedInfunction(contract_code, ContractStates, ConstantStates)
    ContractStates.update(ConstantStates)
    # match whitepaper and developer's code
    res_list, res_best_tops = match_var_names(var_names_whitepaper, ContractStates, top_K)
    reports_whitepaper = collections.defaultdict()
    recored_found = []
    for k in res_best_tops:
        check_result = [ ]
        for res_best in res_best_tops[k]:
            best_mached = res_best[0]
            best_sim = res_best[1]
            # if best_sim < 0.5:
            #     check_result.append( { "info":var_names_whitepaper[k], "matched_var":"Not Found", "isEq":False} )
            #     continue
            print(best_mached)
            print(ContractStates[best_mached])
            i=ContractStates[best_mached][0]
            exp_states = i['code']
            # remove time units
            exp_states = re.sub(r'(days|minutes|years|ether)', '', exp_states)
            dev_raw = exp_states
            whitepaper_states = var_names_whitepaper[k][1]
            if whitepaper_states is None:
                check_result.append( { "info":var_names_whitepaper[k], "claim":"not defined the value in the whitepaper", "matched_var_name":best_mached, "matched_var_exp":best_mached+" = "+dev_raw, "isEq":False} )
                continue
            conversion = var_names_whitepaper[k][2]
            if best_mached not in ConstantStates: # expression 
                wparts = whitepaper_states.split()
                white_var_list = [ n for n in wparts if n.isidentifier() ]
                dparts = exp_states.split()
                dev_var_list = [ n for n in dparts if n.isidentifier() ]
                matched_vars = match_twoVarList(white_var_list, dev_var_list) # match the variables in the two expressions if they are expressions.
                for v1 in matched_vars:
                    whitepaper_states = re.sub(rf'\b({v1})\b', matched_vars[v1], whitepaper_states)
                    exp_states = re.sub(rf'\b({v1})\b', matched_vars[v1], exp_states)
           # print(exp_states)   
            try:  
                dev_exp = simplify(exp_states)
                white_exp = simplify(whitepaper_states) * conversion
                if is_number(dev_exp) and is_number(white_exp):
                    eq = isclose(dev_exp, white_exp)
                else:
                    eq = Eq(dev_exp, white_exp )
                #if eq:
                check_result.append( { "info":var_names_whitepaper[k], "Is the fee found": "Yes" if eq == True else "No", "matched_var_name":best_mached, "matched_var_exp":best_mached+" = "+dev_raw, "isEq":eq} )
            except:
                print(f"Skip No-expression Var {exp_states}")
                pass 
            # print(f"{eq}, {k}={best_mached},{best_sim}, {whitepaper_states} - {exp_states}, {dev_exp} {white_exp}")
        for c in check_result:
            if c['isEq'] == True:
                reports_whitepaper[k] = c
                print( ', '.join("{!s}={!r}".format(key,val) for (key,val) in c.items()) )
                break
        if k not in reports_whitepaper:
            print(check_result)
            reports_whitepaper[k] = check_result[0]
            print( ', '.join("{!s}={!r}".format(key,val) for (key,val) in check_result[0].items()) )
        recored_found.append(reports_whitepaper[k]['matched_var_name'])
    
    # find hidden revenue fee
    code_clean = clean_contract_code(contract_code)
    all_expression=get_all_expression(code_clean, expression_raw=False, keep_classtate = True)
    reveune_hidden_return = collections.defaultdict(list)
    revenue_hidden_var = collections.defaultdict(list)
    global_constant = { g:ConstantStates[g][0]['code'] for g in ConstantStates }
    for function_name, f in all_expression["function"].items():
        # print(f"{function_name}++++++++++++++")
        # if function_name == "takeFee":
        #     print("debug")
        local_constant = {c_name:c_v[0]['code'] for c_name, c_v in f["local_constant"].items()}
        if "fee" in function_name.lower() or "rate" in function_name.lower():
           # print(f"{function_name}===========")
            for returned_value in f["return"]:
                #print(f"return {clean_array_symbol(v['code'])}")
               # print(f"return {returned_value['code']}")
                if not returned_value['code'].strip():
                    continue
                rexp = clean_array_symbol(returned_value['code'])
                rexp = replace_constantInExp(local_constant, rexp)
                rexp = replace_constantInExp(global_constant, rexp)
                rexp = replace_logic_timeUnit(rexp)
                isTernary, parts = ternary_statement(rexp)
                for tmp_exp in parts:
                    reveune_hidden_return[function_name].append( str(simplify(tmp_exp) ))
                    #print(f"{function_name} return = {returned_value['code']} ##### {simplify(tmp_exp)}")
                

        for var_name in f['var']:
            if "fee" in var_name.lower() or "rate" in var_name.lower() and var_name not in recored_found:
                #print(f"{function_name}=========== {var_name}")
                for var_value in f['var'][var_name]:
                    vexp = clean_array_symbol(var_value['code'])
                    vexp = replace_constantInExp(local_constant, vexp)
                    vexp = replace_constantInExp(global_constant, vexp)
                    var_name_array_rep = clean_array_symbol(var_name)
                    vexp = replace_logic_timeUnit(vexp)
                    isTernary, parts = ternary_statement(vexp)
                    if not isTernary:
                       # print(parts)
                       # print(f"{var_name_array_rep} = {var_value['code']} ##### {simplify(vexp)}")
                        revenue_hidden_var[var_name_array_rep].append( str(simplify(vexp)) )
                    else:
                        for j, tmp_exmp in enumerate(parts):
                         #   print(f"{var_name_array_rep} = {var_value['code']} #####   {simplify(tmp_exmp)}")
                            revenue_hidden_var[f"{var_name_array_rep}_{j}"].append( str(simplify(tmp_exmp)) )
    

    return {"whitepaper":reports_whitepaper, "hidden_fee_function":reveune_hidden_return, "hidden_fee_var":revenue_hidden_var}

