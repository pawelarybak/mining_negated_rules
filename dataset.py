import csv


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
