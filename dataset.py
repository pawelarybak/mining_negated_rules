import csv

from itertools import combinations


class DataSet(object):
    def __init__(self, items, data):
        self.items = items
        self.data = data

    @classmethod
    def from_bin_csv(cls, file_path):
        """
        Creates DataSet object from csv file with headers in first row and boolean (0 or 1) value in remaining rows
        :param file_path: path to file
        :return: DataSet object
        """
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar="\"")
            headers = next(reader)
            data = {header: list() for header in headers}
            for line in reader:
                tid = line[0]
                for name, boolean in zip(headers, line[1:]):
                    if int(boolean):
                        data[name].append(int(tid))
                # data.append({name for name, boolean in zip(headers, line[1:]) if int(boolean)})
        return cls(headers, data)


class ItemSet(object):
    def __init__(self, data, tid_list=None):
        """
        :param data: Collection of items from dataset in any form
        :param tid_list: Collection of ints, that represent ids of transactions to which itemset belongs
        """
        self.data = set(data)
        self.tid_list = set(tid_list if tid_list is not None else [])

    @property
    def support(self):
        return len(self.tid_list)

    def split_combinations(self):
        for l in range(len(self.data)):
            for combination in combinations(self.data, l):
                yield (set(combination), set(self.data - set(combination)))

    @classmethod
    def merge(cls, item_set1, item_set2):
            return cls(
                item_set1.data | item_set2.data,
                item_set1.tid_list & item_set2.tid_list,
            )


class Rule(object):
    def __init__(self, antecedents, consequents):
        """
        :param antecedents: Set of tuples for lhs of rule. Each tuple contains (item, is_positive), where is_positive
        means if item is not negated. If element is not tuple, is_positive == True is assumed
        :param consequents: Set of tuples for rhs of rule. Each tuple contains (item, is_positive), where is_positive
        means if item is not negatedIf element is not tuple, is_positive == True is assumed
        """
        self.antecedents = {
            antecedent if isinstance(antecedent, tuple) else (antecedent, True) for antecedent in antecedents
        }
        self.consequents = {
            consequent if isinstance(consequent, tuple) else (consequent, True) for consequent in consequents
        }

    def inverted(self):
        return Rule(
            {(antecedent, not is_positive) for antecedent, is_positive in self.antecedents},
            {(consequent, not is_positive) for consequent, is_positive in self.consequents},
        )

    def inverted_antecedents(self):
        return Rule(
            {(antecedent, not is_positive) for antecedent, is_positive in self.antecedents},
            set(self.consequents),
        )

    def inverted_consequents(self):
        return Rule(
            set(self.antecedents),
            {(consequent, not is_positive) for consequent, is_positive in self.consequents},
        )
