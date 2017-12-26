from pprint import pprint

grammar_rules = []
lexicon = {}
probabilities = {}
possible_parents_for_children = {}

def parser_list(node, path_dict, N, sentence):
    if node not in path_dict:
        return [node[2], sentence[node[0]]]
    return [node[2], [parser_list(path_dict[node][0], path_dict, N, sentence),parser_list(path_dict[node][1], path_dict, N, sentence)]]


def populate_grammar_rules():
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    f = open('pcfg_grammar_modified','rb')
    grammar_text = f.readlines()
    f.close()
    grammar_rules = []
    test_flag = False
    for line in grammar_text:
        line = line.strip()

        if not line.strip(): continue
        if line == "##":
            test_flag = True
            continue

        left, right = line.split("->")
        left = left.strip()
        if test_flag:
            children = right.split()[:1]
            if children[0] != "":
                if left not in lexicon:
                    lexicon[left.strip()] = set([children[0].strip()])
                else:
                    lexicon[left.strip()].add(children[0].strip())
        else:
            children = right.split()[:2]
        probability = float(right.split()[-1])

        rule = (left, tuple(children), probability)
        grammar_rules.append(rule)
        possible_parents_for_children[tuple(children)] = left
        probabilities[(left, tuple(children))] = probability

def pcky_parse(sentence):
    
    populate_grammar_rules()
    baseline_prob = -50
    result_text = None
    global grammar_rules, lexicon, probabilities, possible_parents_for_children
    grammar_dict = {}

    
    for rule in grammar_rules:
        grammar_dict[rule[1]] = []
    for rule in grammar_rules:
        grammar_dict[rule[1]].append((rule[0], rule[2]))

    
    N = len(sentence)
    cells = {}
    for i in range(N):
        for j in range(i + 1, N + 1):
            cells[(i, j)] = []


    for i, word in enumerate(sentence):
        for lex in lexicon:
            if word in lexicon[lex]:
                cells[(i, i + 1)].append((lex, probabilities[(lex, tuple([word]))]))
    
    path_dict = {}
    for j in range(1, N):
        for i in range(N - j):
            left_index = []
            right_index = []
            for i_cell in range(i, i + j):
                left_index.append((i, i_cell + 1))
            for j_cell in range(i + 1, i + j + 1):
                right_index.append((j_cell, i + j + 1))

            for partition in range(i+j-i):
                left_cell = (i, i+j-partition)
                down_cell = (i+j-partition, i+j+1)
                
                for val1 in cells[left_cell]:
                    for val2 in cells[down_cell]:
                            l = val1[0]
                            r = val2[0]
                            if (l,r) in grammar_dict:
                                
                                for r in grammar_dict[(l,r)]:
                                    cells[(i, i + j + 1)].append((r[0], val1[1]*val2[1]*r[1]))
                                    path_dict[(i, i + j + 1, r[0], val1[1]*val2[1]*r[1])] = \
                                        ((left_cell[0], left_cell[1], val1[0], val1[1]),
                                         (down_cell[0], down_cell[1], val2[0], val2[1]))

    
    for key in path_dict:
        if key[0]==0 and key[1]==N:
            if key[2] == 'S':
                if key[3] > baseline_prob:
                    baseline_prob = key[3]
                    result_text = key
    print result_text
    pprint("Sentence: "+ " ".join(sentence))
    if baseline_prob == -50:
        pprint("Not a valid parse tree for this sentence")
        return False
    pprint("Parse tree with max probability of "+ str(baseline_prob))
    print parser_list(result_text, path_dict, N, sentence)

    


    # TODO complete the implementation
    return True

