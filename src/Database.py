# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('Agg')
import random, os
import numpy as np
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod
import matplotlib.colors as colors


class Database:

    __metaclass__ = ABCMeta

    def __init__(self):
        self.path = ""
        pass

    @abstractmethod
    def load_data(self):
        pass

    def plot(self, rho, data, labels):
        # plt.clf()

        path = self.path

        base_name = os.path.basename(path)
        name = os.path.splitext(base_name)[0]

        data_np = np.asarray(data)
        labels_np = np.asarray(labels)
        colors_values = colors.cnames.values()

        print("#data={} labels={}".format(len(data), len(labels)))
        ls = np.unique(labels_np)
        print ls

        fig = plt.figure()
        title_fig = 'Dataset {}'.format(name)
        fig.suptitle(title_fig, fontsize=18, fontweight='bold')
        ax = fig.add_subplot(111)
        fig.subplots_adjust(top=0.85)
        ax.set_title('rho={}'.format(rho))
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        for l in ls:
            print("labels_np={}".format(labels_np))
            print("l={}".format(l))

            d = data_np[labels_np == l]
            print d
            x = d[:, 0]
            y = d[:, 1]
            print("x={} y={}".format(x.shape, y.shape))
            color_idx = int(l) % len(colors_values)
            ax.scatter(x, y, c=colors_values[color_idx])

        fig_name = "../images/{}_{}.png".format(name, rho)
        fig.savefig(fig_name)
        # plt.show()


# Functions for dealing with Fisher's Iris dataset.
class DatabaseIris(Database):
    # Function to generate vectors from the data. (also used to return length of dataset).

    def __init__(self):
        Database.__init__(self)
        self.path = "../datasets/iris.data.txt"

    def load_data(self):
        feat_vects = []
        # Opening the data file
        with open(self.path) as feat_file:
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
        with open(self.path) as feat_file:
            for line in feat_file:
                # Initiating a counter to count up to the label.
                count = 1
                # Splitting feature by comma and line.
                for w in line.strip().split(','):
                    # When the counter reaches the label index (feature 5), append it.
                    if count >= 5:
                        label_vects.append(w)
                    count += 1
        return label_vects


class TwoDimensionData(Database):

    def __init__(self, path, field_separator='\t'):
        Database.__init__(self)
        self.path = path
        self.field_separator = field_separator
        self.data = []
        self.labels = []
        self.read_file()

    def read_file(self):
        with open(self.path) as row_file:
            for line in row_file:
                split_line = line.strip().split(self.field_separator)
                x = float(split_line[0])
                y = float(split_line[1])
                l = int(split_line[2])
                self.data.append([x, y])
                self.labels.append(l)

    def load_data(self):
        return self.data

    def get_label_vects(self):
        return self.labels


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
