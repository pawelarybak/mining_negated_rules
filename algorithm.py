from dataset import ItemSet, Rule


def frequent_1_itemsets(dataset, min_support):
    tid_lists = dict.fromkeys(dataset.items, set())
    for idx, itemset in enumerate(dataset.data):
        for item in dataset.items:
            if item in itemset:
                tid_lists[item].add(idx)
    return [
        ItemSet(item, tid_list) for item, tid_list in tid_lists.items()
        if len(tid_list)/len(dataset.data) > min_support
    ]


def generate_frequent_candidates(fk, f1):
    candidates = list()
    for k_itemset in fk:
        for one_itemset in f1:
            if not one_itemset.issubset(k_itemset):
                candidates.append(ItemSet.merge(k_itemset, one_itemset))
    return candidates


def correlation(set_one, set_two):
    # TODO
    pass


def confidence(rule):
    # TODO
    pass


def mine_rules(dataset, min_support, min_confidence, min_corr=0.5):
    positiveAR = set()
    negativeAR = set()
    f1 = frequent_1_itemsets(dataset, min_support)
    fk_1 = f1
    k = 2
    while True:
        ck = generate_frequent_candidates(fk_1, f1)
        fk = list()
        for itemset in ck:
            if itemset.support > min_support:
                fk.append(itemset)
            for x, y in itemset.split_combinations():
                corr = correlation(x, y)
                if corr > min_corr :
                    if itemset.support > min_support:
                        orig_rule = Rule(x, y)
                        if confidence(orig_rule) >= min_confidence:
                            positiveAR.add(orig_rule)
                    elif confidence(Rule(x, y).inverted()) > min_confidence
                        and :

