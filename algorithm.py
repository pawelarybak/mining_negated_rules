from math import sqrt

from dataset import ItemSet, Rule


def frequent_1_itemsets(dataset, min_support):
    return [
        ItemSet([item], dataset) for item, tid_list in dataset.data.items()
        if len(tid_list)/dataset.size > min_support
    ]


def generate_frequent_candidates(fk, f1):
    candidates = set()
    for k_itemset in fk:
        for one_itemset in f1:
            if not one_itemset.issubset(k_itemset):
                itemset = ItemSet.merge(k_itemset, one_itemset)
                candidates.add(itemset)
    return candidates


def correlation(itemset1, itemset2):
    p1 = itemset1.probability
    p2 = itemset2.probability
    cov = ItemSet.merge(itemset1, itemset2).probability - (p1 * p2)
    sig1 = sqrt(p1 - p1 ** 2)
    sig2 = sqrt(p2 - p2 ** 2)
    try:
        return cov / (sig1 * sig2)
    except ZeroDivisionError:  # One of itemsets has probability of 1
        return 1


def mine_rules(dataset, min_support, min_confidence, min_corr=0.5, max_len=None, verbose=False):
    positiveAR = set()
    negativeAR = set()
    f1 = frequent_1_itemsets(dataset, min_support)
    fk_1 = f1  # F_(k-1)
    k = 2
    while len(fk_1) != 0 and (max_len is None or k > max_len):
        ck = generate_frequent_candidates(fk_1, f1)
        fk = list()
        if verbose:
            print('Finding rules of length: {} ({} frequent candidates)'.format(k, len(ck)))
        for itemset in ck:
            supp = itemset.rsupport
            if supp > min_support:
                fk.append(itemset)
            for x, y in itemset.split_combinations():
                corr = correlation(x, y)
                if corr > min_corr:
                    if supp > min_support:
                        orig_rule = Rule(x, y)
                        if orig_rule.confidence >= min_confidence:
                            positiveAR.add(orig_rule)
                    else:
                        x_neg = x.negated()
                        y_neg = y.negated()
                        if ItemSet.merge(x_neg, y_neg).rsupport > min_support:
                            neg_rule = Rule(x_neg, y_neg)
                            if neg_rule.confidence > min_confidence:
                                negativeAR.add(neg_rule)
                elif corr < -min_corr:
                    x_neg = x.negated()
                    y_neg = y.negated()
                    neg_adj = Rule(x_neg, y)
                    neg_cons = Rule(x, y_neg)
                    if neg_adj.confidence > min_confidence:
                        negativeAR.add(neg_adj)
                    if neg_cons.confidence > min_confidence:
                        negativeAR.add(neg_cons)
        if verbose:
            print('Frequent itemsets of length {}: {}'.format(k, len(fk)))
        fk_1 = list(fk)
        k += 1
    found_rules = negativeAR | positiveAR
    if verbose:
        print('Found: {} rules'.format(len(found_rules)))
    return found_rules

