# The core of this class is to give some utils to use CSV files

import pandas as pd
import numpy as np

# internal classes
from Constants import Constants
from Validator import Validator

class CSVUtils:

    def __init__ (self, dir_path, file_name=None):
        self.validator = Validator()
        self.validator.is_folder(dir_path)
        self.file_name = file_name
        self.dir_path = dir_path
        self.delimiter = ';'
        self.sep = ';'

    def get_data (self, has_header=None, header_line=None, transpose=False):
        # this funcion helps to retrive data from csv
        file = self.create_name()
        self.validator.is_csv(file)
        header = [];
        df = pd.read_csv(file, header=header_line, delimiter=self.delimiter)
        if transpose is True:
            df = df.T
        data = df.values.tolist()
        if has_header:
            header = np.transpose(data[0]);
            data.pop(0)
            data = np.transpose(data);
        return data, header;

    def save (self, data, header_read=None, header_insert=False, float_format=Constants().get_default_float_format(),
              index=False):
        # this function help to save data in a CSV
        file = self.create_name()
        is_file = self.validator.check_is_csv(file)

        if is_file:
            self.validator.is_csv(file)
            df = pd.read_csv(file, header=header_read, delimiter=self.delimiter)
            df.loc[len(df)] = data
            df.to_csv(file, sep=self.sep, float_format=float_format, header=header_insert, index=index)
        else:
            df = pd.DataFrame(data).T
            df.to_csv(file, sep=self.sep, float_format=float_format, header=header_insert, index=index)

    def close_csv (self, file=None):
        # this function perform a CSV clousure
        if file is None:
            file = self.create_name()

        pd.set_option('display.precision', 15)
        df = pd.read_csv(file, header=None, delimiter=self.delimiter, dtype=np.float64)
        df[0] = df[0].astype(int)

        index = 1
        columns_number = len(df.columns)
        while index < columns_number:
            df[index] = df[index].astype(np.float64)
            index = index + 1
        df.to_csv(file, sep=self.sep, header=False, index=False)

    def create_name (self, file_name=None):
        # utils to return file name
        if file_name is None:
            file_name = self.file_name
        dir_path = self.dir_path
        ext = '.' + file_name.split('.')[-1].lower()
        if ext != Constants().get_csv_format():
            file = dir_path + file_name + Constants().get_csv_format()
        else:
            file = dir_path + file_name
        return file

    def get_csv_files (self, dir_path=None):
        # utils to read all CSV in a folder
        if dir_path is None:
            dir_path = self.dir_path
        return [f for f in listdir(dir_path) if self.validator.check_is_csv(join(dir_path, f))]

    def generate_pairs (self):
        files = self.get_csv_files()
        return [(files[i], files[j]) for i in range(len(files)) for j in range(i + 1, len(files))]

    def generate_combinations (self):
        pairs = self.generate_pairs()
        all_files_tuple = tuple(self.get_csv_files())
        pairs.append(all_files_tuple)
        return pairs

    def merge_csv (self, csv_tuple, final_dir_path, final_name, float_format=Constants().get_default_float_format()):
        # merge differnte CSV in one
        df_list = []
        final_name = final_dir_path + final_name
        for csv in csv_tuple:
            file = self.create_name(csv)
            df = pd.read_csv(file, header=None, delimiter=self.delimiter, dtype=np.float64)
            df_list.append(df)
        final_df = pd.concat(df_list)
        final_df.to_csv(final_name, sep=self.sep, float_format=float_format, header=False, index=False)
        self.close_csv(final_name)

    def generate_csv_merged_name (self, csv_tuple):
        name = ''
        for file_name in csv_tuple:
            name += file_name.split(Constants().get_csv_format())[0].upper()
        return name + Constants().get_csv_format()

    def merge_csv_combinations (self, final_dir_path):
        # merge all CSV combinations in a folder
        csv_list = self.generate_combinations()
        for csv_tuple in csv_list:
            name = self.generate_csv_merged_name(csv_tuple)
            self.merge_csv(csv_tuple=csv_tuple, final_dir_path=final_dir_path, final_name=name)
