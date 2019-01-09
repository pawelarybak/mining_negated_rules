import csv
import operator
from functools import reduce

from itertools import combinations

################################################
# IMPORTANT - This project assumes that item
# with all uppercase name is negated and all
# lowercase is positive
################################################


class DataSet(object):
    def __init__(self, items, data, size):
        self.items = items
        self.data = data
        self.size = size
        self.all_tids = set(range(1, size + 1))

    def __getitem__(self, item):
        if item.islower():
            return self.data[item]
        else:
            return self.all_tids - self.data[item.lower()]

    @classmethod
    def from_bin_csv(cls, file_path):
        """
        Creates DataSet object from csv file with headers in first row and boolean (0 or 1) value in remaining rows
        :param file_path: path to file
        :return: DataSet object
        """
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar="\"")
            next(reader)
            length = sum(1 for _ in reader)

            csv_file.seek(0)
            reader = csv.reader(csv_file, delimiter=',', quotechar="\"")
            headers = (name.lower() for name in next(reader))
            data = {header: set() for header in headers}
            for line in reader:
                tid = line[0]
                for name, boolean in zip(headers, line[1:]):
                    if int(boolean):
                        data[name].add(int(tid))
        return cls(headers, data, length)


class ItemSet(object):
    def __init__(self, items, dataset):
        """
        :param data: Collection of items from dataset in any form
        :param tid_list: Collection of ints, that represent ids of transactions to which itemset belongs
        """
        self.items = frozenset(items)
        self.dataset = dataset

    def __str__(self):
        return str(self.items)

    def __iter__(self):
        return iter(self.items)

    def __cmp__(self, other):
        return self.items.__cmp__(other.items)

    def __eq__(self, other):
        return self.items == other.items

    def __hash__(self):
        return hash(self.items)

    def issubset(self, other):
        return self.items.issubset(other.items)

    @property
    def tid_list(self):
        return reduce(
            operator.and_,
            [self.dataset[item] for item in self.items],
        )

    @property
    def support(self):
        return len(self.tid_list)

    @property
    def probability(self):
        return self.support / self.dataset.size

    def split_combinations(self):
        for l in range(1, len(self.items)):
            for combination in combinations(self.items, l):
                yield (
                    ItemSet(combination, self.dataset),
                    ItemSet(self.items - set(combination), self.dataset),
                )

    def negated(self):
        return ItemSet(
            (item.upper() if item.islower() else item.lower() for item in self.items),
            self.dataset,
        )

    @classmethod
    def merge(cls, item_set1, item_set2):
        assert item_set1.dataset is item_set2.dataset
        return cls(
            item_set1.items | item_set2.items,
            item_set1.dataset,
        )


class Rule(object):
    def __init__(self, antecedents, consequents):
        self.antecedents = antecedents
        self.consequents = consequents

    def inverted(self):
        return Rule(
            self.antecedents.negated(),
            self.consequents.negated(),
        )

    def inverted_antecedents(self):
        return Rule(
            ItemSet(
                (item.upper() if item.islower() else item.lower() for item in self.antecedents),
                self.antecedents.dataset,
            ),
            self.consequents,
        )

    def inverted_consequents(self):
        return Rule(
            self.antecedents,
            ItemSet(
                (item.upper() if item.islower() else item.lower() for item in self.consequents),
                self.consequents.dataset,
            ),
        )

    @property
    def support(self):
        return self.antecedents.support

    @property
    def confidence(self):
        try:
            return ItemSet.merge(self.antecedents, self.consequents).support / self.antecedents.support
        except ZeroDivisionError:
            return 0
