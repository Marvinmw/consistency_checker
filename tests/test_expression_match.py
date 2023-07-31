from parser_imp_js.tree_matcher import match_graphs, build_express_tree, match_expressions

def test_match_expressions_case1():
    dist = match_expressions("delta =  mul(log_2(globalRank)-10, TERM_AMPLIFIER)", "a =  mul(log_2(b)-10, c)")
    assert dist == 0.0


def test_match_expressions_case2():
    dist = match_expressions("delta =  mul(log_2(globalRank), TERM_AMPLIFIER)", "a =  mul(log_2(b), c)")
    assert dist == 0.0

def test_match_expressions_case3():
    dist = match_expressions("max(a,b)", "max(dd, dfd)")
    assert dist == 0.0


def test_match_expressions_case4():
    dist = match_expressions("a+10+b", "c+10+b")
    assert dist == 0.0



def test_match_expressions_case5():
    dist = match_expressions("a+10+b", "c+b")
    assert dist != 0.0

