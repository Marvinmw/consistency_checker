import torch
import torch 
import torch.nn.functional as F
from transformers import BertTokenizer, BertModel
import collections

# tokenizer = AutoTokenizer.from_pretrained('xlm-roberta-large')
# model = AutoModelForMaskedLM.from_pretrained("xlm-roberta-large")

# # tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')  #bert-large-uncased bert-base-uncased
# # model = BertModel.from_pretrained("bert-base-multilingual-cased")
# device = torch.device("cpu")
# model.to(device)
# import re
# def get_embedding(v1):
#     v1=re.sub('[^A-Za-z0-9.]+', ' ',v1)
#     encoded_input=tokenizer(v1, return_tensors='pt')
#     context_embeddings=model(**encoded_input)#[0][:,0,:].squeeze()
#    # print(context_embeddings[0].shape)
#     context_embeddings = context_embeddings[0][:,0,:].squeeze()
#     #print(context_embeddings.shape)
#     return context_embeddings



import torch
from transformers import AutoModel, AutoTokenizer
from scipy.spatial.distance import cosine

# Get our models - The package will take care of downloading the models automatically
# For best performance: Muennighoff/SGPT-5.8B-weightedmean-nli-bitfit
tokenizer = AutoTokenizer.from_pretrained("Muennighoff/SGPT-125M-weightedmean-nli-bitfit")
model = AutoModel.from_pretrained("Muennighoff/SGPT-125M-weightedmean-nli-bitfit")
# Deactivate Dropout (There is no dropout in the above models so it makes no difference here but other SGPT models may have dropout)
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
        #print(parts)
        for p in parts:
            if p.strip():
                v += p[0].upper()+p[1:] if len(p) > 1 else p[0].upper()
        return v
    else:
        return s

def get_embedding(v, preprocess=True):
    # Tokenize input texts
    if preprocess:
        v = to_camel_case(v)
        v = split_camel_case(v)
    
    texts = [ " ".join(v).lower() ]
    batch_tokens = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

    # Get the embeddings
    with torch.no_grad():
        # Get hidden state of shape [bs, seq_len, hid_dim]
        last_hidden_state = model(**batch_tokens, output_hidden_states=True, return_dict=True).last_hidden_state

    # Get weights of shape [bs, seq_len, hid_dim]
    weights = (
        torch.arange(start=1, end=last_hidden_state.shape[1] + 1)
        .unsqueeze(0)
        .unsqueeze(-1)
        .expand(last_hidden_state.size())
        .float().to(last_hidden_state.device)
    )

    # Get attn mask of shape [bs, seq_len, hid_dim]
    input_mask_expanded = (
        batch_tokens["attention_mask"]
        .unsqueeze(-1)
        .expand(last_hidden_state.size())
        .float()
    )

    # Perform weighted mean pooling across seq_len: bs, seq_len, hidden_dim -> bs, hidden_dim
    sum_embeddings = torch.sum(last_hidden_state * input_mask_expanded * weights, dim=1)
    sum_mask = torch.sum(input_mask_expanded * weights, dim=1)

    embeddings = sum_embeddings / sum_mask

    # Calculate cosine similarities
    # Cosine similarities are in [-1, 1]. Higher means more similar
    # cosine_sim_0_1 = 1 - cosine(embeddings[0], embeddings[1])
    # cosine_sim_0_2 = 1 - cosine(embeddings[0], embeddings[2])
    # cosine_sim_0_3 = 1 - cosine(embeddings[0], embeddings[3])

    # print("Cosine similarity between \"%s\" and \"%s\" is: %.3f" % (texts[0], texts[1], cosine_sim_0_1))
    # print("Cosine similarity between \"%s\" and \"%s\" is: %.3f" % (texts[0], texts[2], cosine_sim_0_2))
    # print("Cosine similarity between \"%s\" and \"%s\" is: %.3f" % (texts[0], texts[3], cosine_sim_0_3))
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
        #print(f"{v1} == {v} == {sim}")
        # if sim > best_sim:
        #     best_var = v
        #     best_sim = sim
        res.append([v, sim])
    sorted_by_second = sorted(res, key=lambda tup: tup[1], reverse=True)
    #return best_var,best_sim
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
            #tmp_var, tmp_sim = find_similarName(vc, code_var_name_list)
            tmp_varlist = find_similarName(vc, code_var_name_list)
            res[k].extend( tmp_varlist )#((tmp_var, tmp_sim))
            # if tmp_sim > best_sim:
            #     best_sim = tmp_sim
            #     best_var = tmp_var
            top_vars.extend( tmp_varlist )
        # print(f"{k} {vars_candidates} === {best_var}, {best_sim}")
        # print(f"{res}")
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
        res_best[k] = sorted_by_second[:top_K] #(best_var, best_sim)
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
                sim = 1 - cosine(v1e, v2e) #F.cosine_similarity(v1e, v2e, dim=0)
                # print(sim)
                tripple_sim.append((v1, v2, sim))
    sorted_triples = sorted(tripple_sim, key=lambda x: x[2], reverse=True)
    best_matches = {}
    used_var = []
    for t in sorted_triples:
        if t[0] not in best_matches:
            if t[1] in used_var:
                continue
            best_matches[t[0]] = t[1] #(t[1], t[2])
            used_var.append(t[1])
    # items = best_matches.items()
    # for k,v in items:
    #     best_matches[v] = k
    return best_matches

