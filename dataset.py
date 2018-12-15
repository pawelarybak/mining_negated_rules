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
        data = list()
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar="\"")
            headers = next(reader)
            for line in reader:
                data.append({name for name, boolean in zip(headers, line[1:]) if int(boolean)})
        return cls(headers, data)


class ItemSet(object):
    def __init__(self, data, tid_list=None):
        self.data = set(data)
        self.tid_list = set(tid_list)

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
    def __init__(self, antecedent, consequent):
        # TODO mark negated (somehow)
        self.antecedent = antecedent
        self.consequent = consequent
