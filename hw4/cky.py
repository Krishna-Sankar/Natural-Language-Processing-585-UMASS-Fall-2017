from pprint import pprint

grammar_text = """
S -> NPZ VP
S -> NP VBZ
NP -> Det Noun
PP -> Prep NP
NP -> NP PP
VP -> VP PP
NPZ -> Det Nouns
VP -> Verb NP
VBZ -> Verbs NP
"""

lexicon = {
    'Nouns': set(['cats', 'dogs']),
    'Verbs': set(['attacks', 'attacked']),
    'Noun': set(['cat', 'dog', 'table', 'food']),
    'Verb': set(['saw', 'loved', 'hated', 'attack']),
    'Prep': set(['in', 'of', 'on', 'with']),
    'Det': set(['the', 'a']),
}



# Process the grammar rules.  You should not have to change this.
grammar_rules = []
for line in grammar_text.strip().split("\n"):
    if not line.strip(): continue
    left, right = line.split("->")
    left = left.strip()
    children = right.split()
    rule = (left, tuple(children))
    grammar_rules.append(rule)

syntax_store = {}
for rule in grammar_rules:
    syntax_store[rule[1]] = rule[0]
possible_parents_for_children = {}
for parent, (leftchild, rightchild) in grammar_rules:
    if (leftchild, rightchild) not in possible_parents_for_children:
        possible_parents_for_children[leftchild, rightchild] = []
    possible_parents_for_children[leftchild, rightchild].append(parent)
# Error checking
all_parents = set(x[0] for x in grammar_rules) | set(lexicon.keys())
for par, (leftchild, rightchild) in grammar_rules:
    if leftchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % leftchild
    if rightchild not in all_parents:
        assert False, "Nonterminal %s does not appear as parent of prod rule, nor in lexicon." % rightchild

def parser_list(node, result, N, sentence):
    if node not in result:
        return [node[2], sentence[node[0]]]
    return [node[2], [parser_list(result[node][0], result, N, sentence),parser_list(result[node][1], result, N, sentence)]]



def cky_acceptance(sentence):
    # return True or False depending whether the sentence is parseable by the grammar.
    global grammar_rules, lexicon, syntax_store

    
    N = len(sentence)
    cells = {}
    for i in range(N):
        for j in range(i + 1, N + 1):
            cells[(i, j)] = []

    for i,word in enumerate(sentence):
        for lex in lexicon:
            if word in lexicon[lex]:
                cells[(i,i+1)].append(lex)

    
    result = {}
    for j in range(1,N):
        for i in range(N-j):
            left_index = []
            right_index = []
    
            for partition in range(i+j-i):
                left_cell = (i, i+j-partition)
                right_cell = (i+j-partition, i+j+1)
                
                for val1 in cells[left_cell]:
                    for val2 in cells[right_cell]:
                
                        if (val1, val2) in syntax_store:
                            cells[(i,i+j+1)].append(syntax_store[(val1, val2)])
                            result[(i, i+j+1, syntax_store[(val1, val2)])] = \
                                    ((left_cell[0],left_cell[1],val1), (right_cell[0],right_cell[1],val2))


     

    if (0, N, 'S') in result:
        print(result[(0, N, 'S')])
              
    print(cells)
    
    return 'S' in cells[(0,N)]



def cky_parse(sentence):
    
    global grammar_rules, lexicon

    N = len(sentence)
    cells = {}
    for i in range(N):
        for j in range(i + 1, N + 1):
            cells[(i, j)] = []

    for i, word in enumerate(sentence):
        for lex in lexicon:
            if word in lexicon[lex]:
                cells[(i, i + 1)].append(lex)

    result = {}
    for j in range(1, N):
        for i in range(N - j):
            left_index = []
            right_index = []
            for j_index in range(i, i + j):
                left_index.append((i, j_index + 1))
            for i_index in range(i + 1, i + j + 1):
                right_index.append((i_index, i + j + 1))

            for partition in range(i + j - i):
                left_cell = (i, i + j - partition)
                right_cell = (i + j - partition, i + j + 1)
                for val1 in cells[left_cell]:
                    for val2 in cells[right_cell]:
 
                        if (val1, val2) in syntax_store:
                            cells[(i, i + j + 1)].append(syntax_store[(val1, val2)])
                            result[(i, i + j + 1, syntax_store[(val1, val2)])] = \
                                ((left_cell[0], left_cell[1], val1),
                                 (right_cell[0], right_cell[1], val2))

    if (0, N, 'S') in result:
        print parser_list((0, N, 'S'), result, N, sentence)

    
    return 'S' in cells[(0, N)]


