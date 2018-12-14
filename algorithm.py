

def frequent_1_itemsets(dataset, min_support):
    counter = dict.fromkeys(dataset.items, 0)
    for itemset in dataset.data:
        for item in dataset.items:
            counter[item] += 1 if item in itemset else 0
    # Using dict as OrderedSet. See: https://stackoverflow.com/a/39835527
    return [{item} for item, val in counter.items() if val/len(dataset.data) > min_support]


def generate_frequent_candidates(Fk, F1):
    new_set = list()
    for k_itemset in Fk:
        for one_itemset in F1:
            if not one_itemset.issubset(k_itemset):
                new_set.append(k_itemset | one_itemset)
    return new_set


def method(dataset, min_support=0.5):
    positiveAR = set()
    negativeAR = set()
    F1 = frequent_1_itemsets(dataset, min_support)
