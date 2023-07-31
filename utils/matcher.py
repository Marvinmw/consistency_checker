import networkx as nx
import collections
from collections import Counter, defaultdict
import copy
import itertools
import utils.extractSrcExpression as extractor
import re
import jellyfish
import operator
import sys  
import matplotlib.colors as mcolors
import matplotlib.pylab as plt
from colorama import Fore, Style
from .bert_varname_match import distance_2Names
colorlist= list(mcolors.TABLEAU_COLORS.values())

def duplicates(lst):
    cnt= Counter(lst)
    return [key for key in cnt.keys() if cnt[key]> 1]

def indices(lst, items= None):
    items, ind= set(lst) if items is None else items, defaultdict(list)
    for i, v in enumerate(lst):
        if v in items: ind[v].append(i)
    return ind


def get_root(tree):
    for n in tree.nodes:
        if tree.in_degree(n) == 0:
            return n
    return None   
 
def is_sublist(list1, list2):
    """
    """
    if len(list1) > len(list2):
        return False,-1
    
    i = 0
    j = 0
    
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            i += 1
        j += 1
    
    return i == len(list1), j

def bfs_order(G, root):
    edges = nx.bfs_edges(G, root)
    nodes = [root] + [v for u, v in edges]
    return nodes

def check_pair(wG, dG, wp, dp):
    index = [i for i in range(len(wp))]
    pair_index = list(itertools.product(index, index))
    pair_index = list(filter(lambda x: True if x[0]!=x[1] else False,  pair_index))
    for p in pair_index:
        return nx.has_path(wG, wp[p[0]], wp[p[1]]) == nx.has_path(dG, dp[p[0]], dp[p[1]])
    
def backbone_match(white_tree, dev_tree):
    root_white = get_root(white_tree)
    white_tree_node_bfsorder = bfs_order(white_tree, root_white)
    white_tree_node_bfsorder = list( filter( lambda x: True if white_tree.nodes[x]['type'] in ['OperatorNode', 'FunctionNode'] else False , white_tree_node_bfsorder ) )
    
    root_dev_tree = get_root(dev_tree)
    dev_tree_node_bfsorder = bfs_order(dev_tree, root_dev_tree)
    dev_tree_node_bfsorder = list( filter( lambda x: True if dev_tree.nodes[x]['type'] in ['OperatorNode', 'FunctionNode'] else False , dev_tree_node_bfsorder ) )
   
    candidates_nodes_mapping = collections.defaultdict(list)
    for wn in white_tree_node_bfsorder:
        white_path = nx.shortest_path(white_tree, source=root_white, target=wn)
        white_path_ops = [  white_tree.nodes[n]['value'] for n in white_path ]
        candidates = []
        for dn in dev_tree_node_bfsorder:
            if white_tree.nodes[wn]['value'] == dev_tree.nodes[dn]['value']:
                dev_path = nx.shortest_path(dev_tree, source=root_dev_tree, target=dn)
                dev_path_ops = [ dev_tree.nodes[n]['value'] for n in dev_path ]
                isub, mapped_j = is_sublist(white_path_ops, dev_path_ops)
                if isub:
                    candidates.append(  dn )
                    candidates_nodes_mapping[wn].append( dn )
    
    white_paper_mapped_nodes =  [ i for i in list(candidates_nodes_mapping.keys()) if i in white_tree_node_bfsorder ]
    white_path_ops = [  white_tree.nodes[n]['value'] for n in white_paper_mapped_nodes ]
    producs_input = [ candidates_nodes_mapping[i] for i in white_paper_mapped_nodes ]

    #selected_candidates =[]
    mapped_pair = []
    for combination in list(itertools.product(*producs_input)):
        combination = list(combination)
        if len(set(combination))!=len(combination):
            # handle duplicated elements, generate unique combinations
            duplicated_index = indices(combination)
            duplicated_index = list( duplicated_index.values() )
            for duplicated_combination in list(itertools.product(*duplicated_index)):
                combination_new = copy.deepcopy( combination )
                white_paper_mapped_nodes_new = copy.deepcopy( white_paper_mapped_nodes )
                flat_list = list(itertools.chain(*duplicated_index))
                for j in flat_list:
                    if j not in duplicated_combination:
                        combination_new.pop( j )
                        white_paper_mapped_nodes_new.pop( j )
                un_mapped_nodes  = list( set(white_tree_node_bfsorder) - set(white_paper_mapped_nodes_new) )
                un_mapped_nodes_reverse  = list( set(white_paper_mapped_nodes_new) - set(white_tree_node_bfsorder) )
                if check_pair(white_tree, dev_tree,white_paper_mapped_nodes_new,  combination_new):
                    mapped_pair.append( [white_paper_mapped_nodes_new,combination_new, un_mapped_nodes,un_mapped_nodes_reverse ]  )
        else:
            un_mapped_nodes  = list( set(white_tree_node_bfsorder) - set(white_paper_mapped_nodes) )
            un_mapped_nodes_reverse  = list( set(white_paper_mapped_nodes) - set(white_tree_node_bfsorder) )
            if check_pair(white_tree, dev_tree,white_paper_mapped_nodes,  combination):
                mapped_pair.append( [white_paper_mapped_nodes, combination, un_mapped_nodes,un_mapped_nodes_reverse ]  )
                
    return mapped_pair

def getWords(v):
    v = re.sub(r'([a-z])([A-Z])', r'\1_\2', v)
    words = re.split('[^a-zA-Z0-9]+', v)   
    words = [ w.lower() for w in words]
    return " ".join( words )

    
def compare_nodes(wG, dG, wn, dn, mapped_dict):
    if wn in mapped_dict and mapped_dict[wn] == dn:
        return 0
    # if wG.out_degree(wn) == 0 and dG.out_degree(dn) == 0:
    # check key words
    wn_value = str(wG.nodes[wn]['value'])
    dn_value = str(dG.nodes[dn]['value'])
    wn_words = getWords(wn_value)
    dn_words = getWords(dn_value)
    #print(f"{wn_value} ~ {dn_value}")
    dist = distance_2Names(wn_value, dn_value) #jellyfish.levenshtein_distance(wn_words, dn_words)
    return dist

  
def fine_grained_match(white_G, dev_G, white_paper_mapped_nodes, dev_mapped_nodes):
    mapped_dict = { v: dev_mapped_nodes[i] for  i, v in enumerate(white_paper_mapped_nodes) }
    res_mapped_dict = copy.deepcopy( mapped_dict )
    distance = []
    for mapped_pair in zip(white_paper_mapped_nodes, dev_mapped_nodes):
        # check children
        wn = mapped_pair[0]
        wn_children = list( white_G.successors(wn) )
        dn = mapped_pair[1]
        dn_children = list( dev_G.successors(dn) )
        perm_wn_children = list(itertools.permutations(wn_children))
        perm_dn_children = list(itertools.permutations(dn_children))
        dist_sum = {}
        min_index, min_value = sys.maxsize, sys.maxsize
        for i, p1 in enumerate(perm_wn_children):
            for j, p2 in  enumerate(perm_dn_children):
                dist_s = []
                for n1 in p1:
                    for n2 in p2:
                        d = compare_nodes(white_G, dev_G, n1, n2, mapped_dict)
                        dist_s.append(d)
                dist_sum[(i,j)] = sum(dist_s)/len(dist_s)
                if  sum(dist_s)/len(dist_s) < min_value:
                    min_value =  sum(dist_s)/len(dist_s)
                    min_index = (i,j)
       # distance += min_value
        distance.append(min_value)
        i,j = min_index[0], min_index[1]
        for k1 in perm_wn_children[i]:
            for k2 in perm_dn_children[j]:
                res_mapped_dict[k1] = k2
    return res_mapped_dict, sum(distance)/len(distance)

def draw_with_colors(G, color_nodes, ax):
    color_map = [ ]
    for node in G:
        if node in color_nodes:
            index=color_nodes.index(node)
            color_map.append(colorlist[index+1])
        else:
            color_map.append("blue")
    pos = nx.drawing.nx_agraph.graphviz_layout(G, prog="dot")
    #fig=plt.figure(figsize=(8,8))
    nx.draw(
                                G,
                                pos=pos,
                                font_size=8,
                                labels={n: attr["value"] for n, attr in G.nodes(data=True)},
                                with_labels=True,
                                ax=ax,
                                node_color=color_map
                            )
       # plt.savefig(f"{exp}.pdf")
    #plt.show()


def matching(whitepaper_vlist, project_data):
    matched_queations = {}
    for fn_list in whitepaper_vlist:
        vlist = whitepaper_vlist[fn_list]
        for wg in  vlist['return']:
            wG, wexp = wg[0], wg[1]
            min_pari = sys.maxsize
            min_dist = sys.maxsize
            maximum_matched_ops = []
            maximum_matched_ops_num = 0
            matched_devG = []
            for dev_file in project_data:
                dev_vlist = project_data[dev_file][1]
                for dev_fn in dev_vlist:
                    dvlist = dev_vlist[dev_fn]
                    for dg in  dvlist['return']: 
                        if len(dg) == 0:
                            continue
                        dev_G,dev_exp, dg_raw = dg[0], dg[1], dg[-1]
                        mapped_pair = backbone_match(wG, dev_G)
                        for v, p in enumerate(mapped_pair):
                            white_paper_mapped_nodes, selected_candidates = p[0], p[1]
                            if maximum_matched_ops_num <= len(white_paper_mapped_nodes):
                                maximum_matched_ops.append(mapped_pair)
                                maximum_matched_ops_num = len(white_paper_mapped_nodes)
                                matched_devG.append((dev_G,dev_exp, dg_raw))
                            #flat_list = list(itertools.chain(*selected_candidates))

            for ind, mapped_pair in enumerate(maximum_matched_ops):
                dev_G, dev_exp, dg_raw = matched_devG[ind][0],  matched_devG[ind][1], matched_devG[ind][2]
                for v, p in enumerate(mapped_pair):
                        white_paper_mapped_nodes, selected_candidates = p[0], p[1]
                        if len(selected_candidates) == 0:
                            #print(Fore.RED + f" {wexp} does not match {dev_exp} \n")
                            continue
                        
                        res_mapped_dict, distance = fine_grained_match(wG, dev_G, white_paper_mapped_nodes, selected_candidates)
                        if min_dist > distance:
                            min_dist = distance
                            min_pari = p + [distance, dev_exp, dg_raw, dev_G]
            if isinstance(min_pari, list):
                white_paper_mapped_nodes,selected_candidates, backbone_dis, backbone_dis_reverse, fine_dist,dev_exp, dg_raw, dev_G = min_pari[0], min_pari[1], len(min_pari[2]), len(min_pari[3]), min_pari[4],min_pari[-3],min_pari[-2],min_pari[-1]
                # print(backbone_dis)
                # print(len(min_pari[2]))
                if backbone_dis==0 and backbone_dis_reverse==0 and fine_dist<1:
                    print(Fore.BLACK + f"{wexp} \n VS. \n {dev_exp} \n \n")
                    matched_queations[fn_list] = [white_paper_mapped_nodes, selected_candidates,dev_exp, dg_raw, dev_G ]
                else:
                    print(Fore.BLUE + f"{wexp} \n VS. \n {dev_exp} \n \n")
                # fig, ax = plt.subplots(1, 2)
                # draw_with_colors(wG, white_paper_mapped_nodes, ax[0])
                # draw_with_colors(dev_G, selected_candidates, ax[1])
                # plt.show()
            else:
                print(Fore.RED + f" {wexp} does not match {dev_exp} \n \n")
                matched_queations[fn_list] = []
    return matched_queations



def whitepaperChecker(project_dir, white_paper_file, isCleanCode=True):
    '''
    Given one reference sol implementation file, check if we find the mapping code.
    '''
    project_data, whitepaper_data = extractor.process_projects( project_dir, white_paper_file, isCleanCode )
    wvlist = whitepaper_data[1]
    matched_queations = matching(wvlist, project_data)
    return matched_queations