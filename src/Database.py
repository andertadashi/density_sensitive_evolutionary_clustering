import random
import numpy as np
import networkx as nx
from abc import ABCMeta, abstractmethod


class Database:

    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def load_data(self):
        pass


# Functions for dealing with Fisher's Iris dataset.
class DatabaseIris(Database):
    # Function to generate vectors from the data. (also used to return length of dataset).

    def load_data(self):
        feat_vects = []
        # Opening the data file
        with open("../database/iris.data.txt") as feat_file:
            for line in feat_file:
                x = []
                # Initiating a counter to count up to the label.
                count = 1
                # Splitting feature by comma and line.
                for w in line.strip().split(','):
                    # If the counter is less than the label index (feature 5).
                    if count < 5:
                        # Converting string representations into floats
                        x.append(float(w))
                    # When it reaches the label, ignore it.
                    else:
                        continue
                    count += 1
                feat_vects.append(x)
        return feat_vects

    # Function to generate a corresponding label array from the data.
    def get_label_vects(self):
        label_vects = []
        # Opening the data file
        with open("../database/iris.data.txt") as feat_file:
            for line in feat_file:
                # Initiating a counter to count up to the label.
                count = 1
                # Splitting feature by comma and line.
                for w in line.strip().split(','):
                    # When the counter reaches the label index (feature 5), append it.
                    if (count >= 5):
                        label_vects.append(w)
                    count += 1
        return label_vects


class DatabaseSimepar(Database):

    def __init__(self, file_path):
        Database.__init__(self)
        self.file_path = file_path
        self.data_start_index = 2
        self.columns = [
            'station',
            'date',
            'pressaomedia',
            'tempmaxima',
            'tempminima',
            'tempmedia',
            'radsolarmedia',
            'umidademedia',
            'velventomedio',
            'dirventomedio',
            'velrajadamedia',
            'precipitacao',
            'rajadamaxima'
        ]
        self.used_columns = [
            # 'pressaomedia',
            # 'tempmaxima',
            'tempminima',
            # 'tempmedia',
            # 'radsolarmedia',
            # 'umidademedia',
            # 'velventomedio',
            # 'dirventomedio',
            # 'velrajadamedia',
            'precipitacao',
            # 'rajadamaxima'
        ]
        self.used_columns_idx = []

        for idx, column in enumerate(self.columns):
            if column in self.used_columns:
                self.used_columns_idx.append(idx)

    def load_data(self):
        feat_vects = []
        # Opening the data file
        with open(self.file_path) as feat_file:
            for line in feat_file:
                split_line = np.asarray(line.strip().split(','))
                x = []
                for c in self.used_columns_idx:
                    if c >= self.data_start_index:
                        x.append(float(split_line[c]))
                    else:
                        x.append(split_line[c])
                feat_vects.append(x)
        return feat_vects
