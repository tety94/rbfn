# this class helps with an initial, statistical data analisy

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy import stats
from sklearn.preprocessing import normalize
import os

# internal classes
from RBFNClass import RBFN
from Validator import Validator
from ClassCSVUtils import CSVUtils
from Constants import Constants


class DataSetAnalyzer:
    def __init__ (self, file_path, file_name):
        self.validator = Validator()
        self.validator.is_folder(file_path)
        self.normalized = False
        self.norm = None
        self.file_name = file_name
        self.file_path = file_path
        self.data, self.header = self.set_data()
        self.rbfn = RBFN()

    def set_data (self):
        return CSVUtils(dir_path=self.file_path, file_name=self.file_name).get_data(has_header=None, header_line=None,
                                                                                    transpose=False)

    def set_normalized (self, normalized):
        # set if data has to be normalized
        self.validator.is_bool(normalized)
        self.normalized = normalized

    def set_norm (self, norm):
        self.validator.in_list(norm, Constants().get_norms_list())
        if norm is None:
            norm = Constants().get_l2_norm_abbreviation()
        if norm == 1 or norm == Constants().get_l1_norm_abbreviation():
            norm = Constants().get_l1_norm_abbreviation()
        if norm == 2 or norm == Constants().get_l2_norm_abbreviation():
            norm = Constants().get_l2_norm_abbreviation()
        if norm == Constants().get_max_norm_abbreviation():
            norm = Constants().get_max_norm_abbreviation()
        self.norm = norm

    def set_rbfn (self, rbfn):
        self.validator.is_object_type(rbfn, RBFN())
        self.rbfn = rbfn

    def get_data (self, transpose=False):
        if transpose:
            return np.array(self.data).T
        return np.array(self.data)

    def get_header (self):
        return self.header

    def get_file_path (self):
        return self.file_path

    def get_file_name (self):
        return self.file_name

    def get_targets_number (self):
        return len(self.data[0])

    def get_features_number (self):
        return len(self.data)

    def get_feature_axis (self):
        return np.arange(1, len(self.data) + 1, 1)

    def get_targets (self, transpose=True):
        if (self.normalized):
            return self.get_normalized_target(transpose=transpose)
        if transpose == True:
            return np.transpose(self.data)
        return self.data

    def get_average_target (self):
        return np.mean(self.get_targets(), axis=0)

    def get_std_target (self):
        return np.std(self.get_targets(), axis=0)

    def get_variance_target (self):
        return np.var(self.get_targets(), axis=0)

    def get_mode_target (self):
        mode = stats.mode(self.get_targets()).mode
        return np.reshape(mode, self.get_features_number())

    def get_median_target (self):
        return np.median(self.get_targets(), axis=0)

    def get_normalized_target (self, transpose=True):
        if transpose == True:
            data = np.transpose(self.data)
        else:
            data = self.data
        return normalize(data, norm=Constants().get_norm_abbreviation(self.norm), axis=1)

    def base_plot (self, y_axis, type, style='ro'):
        # a base plot which all other plots extend
        feature_axis = self.get_feature_axis()
        plt.plot(feature_axis, y_axis, style)
        title = 'Theoretical target'
        if (self.normalized):
            title += '(norm ' + Constants().get_norm_abbreviation(self.norm) + ') '
            y_label += ' (normalized)'
        title += self.file_name + ' ' + type
        plt.suptitle(title, fontsize=15)
        plt.show()

    def plot_average (self):
        average_target = self.get_average_target()
        self.base_plot(average_target, 'mean', 'ro')

    def plot_std (self):
        std_target = self.get_std_target()
        self.base_plot(std_target, 'standard deviation', 'b^')

    def plot_mode (self):
        mode_target = self.get_mode_target()
        self.base_plot(mode_target, 'mode', 'y-')

    def plot_median (self):
        median_target = self.get_median_target()
        self.base_plot(median_target, 'median', 'k^')

    def plot_variance (self):
        variance_target = self.get_variance_target()
        self.base_plot(variance_target, 'variance', 'go')

    def plot_mean_and_std (self):
        average_target = self.get_average_target()
        std_target = self.get_std_target()
        feature_axis = self.get_feature_axis()

        red_patch = mpatches.Patch(color='red', label='average')
        blue_patch = mpatches.Patch(color='blue', label='standard deviation')
        plt.legend(handles=[red_patch, blue_patch])

        plt.plot(feature_axis, std_target, 'b^', average_target, 'ro')
        plt.suptitle('Theoretical target ' + self.file_name + ' standard deviation and mean', fontsize=15)
        plt.show()

    def save_weigths_in_csv (self, centers, file_path, file_name=None, save_plot=False, class_id=None,
                             float_format='%0.15f', remove_file=False):
        # perform rbfn
        targets = self.get_targets()
        if file_name is None:
            file_name = self.file_name

        rbfn = self.rbfn
        rbfn.set_centers(centers)

        CSV = CSVUtils(dir_path=file_path, file_name=file_name)
        file = CSV.create_name()

        is_file = self.validator.check_is_file(file)
        if is_file and remove_file:
            os.remove(file)
        index = 1
        for p in targets:
            rbfn.set_target(p)
            rbfn.train()
            if save_plot == True:
                rbfn.plot(name=file_name, save=True, path=file_path, index=index)
            rbfn.save_weigths(file_path, file_name, class_id, float_format=float_format)
            index = index + 1
        if (class_id):
            CSV.close_csv()

    def plot (self, centers, index, save=False):
        self.validator.index_exists(targets, index)
        p = targets[index]
        rbfn = self.rbfn
        rbfn.set_target(p)
        rbfn.set_centers(centers)
        rbfn.train()
        rbfn.plot(save)

    def plot_all (self, centers, name, save=False):
        targets = self.get_targets()
        for p in targets:
            rbfn = self.rbfn
            rbfn.set_target(p)
            rbfn.set_centers(centers)
            rbfn.train()
            rbfn.plot(name, save=save)
