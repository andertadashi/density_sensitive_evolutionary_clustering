import random
import numpy as np
from abc import ABCMeta, abstractmethod


class Database:

    __metaclass__ = ABCMeta

    def __init__(self):
        self.feat_vects = None

    @abstractmethod
    def load_data(self):
        pass

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
                splited_line = np.asarray(line.strip().split(','))
                x = []
                for c in self.used_columns_idx:
                    if c >= self.data_start_index:
                        x.append(float(splited_line[c]))
                    else:
                        x.append(splited_line[c])
                feat_vects.append(x)
        self.feat_vects = feat_vects
        return feat_vects
