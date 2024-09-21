import torch
import torch 
import torch.nn.functional as F
from transformers import BertTokenizer, BertModel
import collections
import torch
from transformers import AutoModel, AutoTokenizer
from scipy.spatial.distance import cosine



tokenizer = AutoTokenizer.from_pretrained("Muennighoff/SGPT-125M-weightedmean-nli-bitfit")
model = AutoModel.from_pretrained("Muennighoff/SGPT-125M-weightedmean-nli-bitfit")

device = torch.device("cpu")
model.to(device)
model.eval()
import re

import re

def split_camel_case(str):
    return re.findall(r'[A-Za-z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))', str)

def to_camel_case(s):
    if "_" in s:
        parts = s.split("_")
        v = ""
        
        for p in parts:
            if p.strip():
                v += p[0].upper()+p[1:] if len(p) > 1 else p[0].upper()
        return v
    else:
        return s

def get_embedding(v, preprocess=True):
    
    if preprocess:
        v = to_camel_case(v)
        v = split_camel_case(v)
    
    texts = [ " ".join(v).lower() ]
    batch_tokens = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

    
    with torch.no_grad():
        
        last_hidden_state = model(**batch_tokens, output_hidden_states=True, return_dict=True).last_hidden_state

    
    weights = (
        torch.arange(start=1, end=last_hidden_state.shape[1] + 1)
        .unsqueeze(0)
        .unsqueeze(-1)
        .expand(last_hidden_state.size())
        .float().to(last_hidden_state.device)
    )

    
    input_mask_expanded = (
        batch_tokens["attention_mask"]
        .unsqueeze(-1)
        .expand(last_hidden_state.size())
        .float()
    )

    
    sum_embeddings = torch.sum(last_hidden_state * input_mask_expanded * weights, dim=1)
    sum_mask = torch.sum(input_mask_expanded * weights, dim=1)

    embeddings = sum_embeddings / sum_mask

    
    
    
    
    

    
    
    
    return embeddings[0]

def distance_2Names(name1, name2):
    v1_emb = get_embedding(name1, preprocess=True) if name1.isidentifier() else get_embedding(name1, preprocess=False)
    v2_emb = get_embedding(name2, preprocess=True) if name2.isidentifier() else get_embedding(name2, preprocess=False)
    dis = 1-F.cosine_similarity(v1_emb, v2_emb, dim=0)
    return dis

def find_similarName(v1, candidate_list):
    v1_emb = get_embedding(v1)
    best_var = ""
    best_sim = -1
    res = []
    for v in candidate_list:
        ve = get_embedding(v)
        sim = F.cosine_similarity(v1_emb, ve, dim=0)
        
        
        
        
        res.append([v, sim])
    sorted_by_second = sorted(res, key=lambda tup: tup[1], reverse=True)
    
    return sorted_by_second

def match_var_names(var_names_chatgpt, ConstantStates, top_K=1):
    res = collections.defaultdict(list)
    res_best = collections.defaultdict(list)
    for k, term in var_names_chatgpt.items():
        vars_candidates = term[0]
        best_var = ""
        best_sim = -1
        top_vars = []
        for vc in vars_candidates:
            code_var_name_list =  list(ConstantStates.keys())
            
            tmp_varlist = find_similarName(vc, code_var_name_list)
            res[k].extend( tmp_varlist )
            
            
            
            top_vars.extend( tmp_varlist )
        
        
        top_vars_tmp = {}
        for t in top_vars:
            if t[0] not in top_vars_tmp:
                top_vars_tmp[t[0]] = t
            elif t[1] > top_vars_tmp[t[0]][1]:
                top_vars_tmp[t[0]] = t
            else:
                continue
        top_vars = list(top_vars_tmp.values())
        sorted_by_second = sorted(top_vars, key=lambda tup: tup[1], reverse=True)
        res_best[k] = sorted_by_second[:top_K] 
    return res, res_best



def match_twoVarList(var1_list, var2_list):
    tripple_sim = []
    short_var_list = var1_list
    long_var_list = var2_list
    if len(var1_list) > len(var2_list):
        short_var_list = var2_list
        long_var_list = var1_list
    for v1 in short_var_list:
        for v2 in long_var_list:
                v1e = get_embedding(v1)
                v2e = get_embedding(v2)
                # scipy.spatial.distance.consine return the distance
                sim = 1 - cosine(v1e, v2e) 
                
                tripple_sim.append((v1, v2, sim))
    sorted_triples = sorted(tripple_sim, key=lambda x: x[2], reverse=True)
    best_matches = {}
    used_var = []
    for t in sorted_triples:
        if t[0] not in best_matches:
            if t[1] in used_var:
                continue
            best_matches[t[0]] = t[1] 
            used_var.append(t[1])
    
    
    
    return best_matches

