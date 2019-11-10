# The core of this class is to help with train and test a monodimensional signal
# using RBFN (Radial Basis Function Network). File also helps plotting and saving results.

# from scipy import *
from scipy.linalg import norm, pinv
import numpy as np
# from numpy import random
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import os

# internal classes
from Validator import Validator
from ClassCSVUtils import CSVUtils
from Constants import Constants

from scipy import optimize

class RBFN:
    def __init__ (self, training_data=None, target=None):
        self.epsilon = Constants().get_rbfn_deafult_epsilon()
        self.k = Constants().get_rbfn_default_k()
        self.base_function_type = Constants().get_rbfn_gaussian_abbreviation()
        self.training_data = training_data
        self.target = target
        self.solver = Constants().get_solver_ls_abbreviation()
        self.validator = Validator()

    def calculate_base_function (self, center, x):
        #  this function calculate one of all the RBF which will compose the final approximation
        radius = norm(center - x)
        epsilon = self.epsilon
        k = self.k
        function = self.base_function_type
        self.validator.in_list(function, Constants().get_rbfn_base_functions_list())
        if function == Constants().get_rbfn_inv_multq_abbreviation():
            return np.sqrt(1 / (1 + (epsilon * radius) ** 2))
        if function == Constants().get_rbfn_inv_q_abbreviation():
            return 1 / (1 + (epsilon * radius) ** 2)
        if function == Constants().get_rbfn_polyharmonic_abbreviation():
            if (k % 2) == 0:
                return radius ** k
            return radius ** k * np.log(radius)
        if function == Constants().get_rbfn_gaussian_abbreviation():
            return np.exp(- (epsilon * radius) ** 2)
        # Gaussian like default function
        return np.exp(- (epsilon * radius) ** 2)

    def set_centers (self, centers):
        self.centers = centers
        self.num_centers = len(centers)

    def set_epsilon (self, epsilon):
        self.epsilon = epsilon

    def set_base_function_type (self, base_function_type):
        self.base_function_type = base_function_type

    def set_k (self):
        self.k = int(k)

    def set_training_data (self, training_data):
        self.training_data = training_data

    def set_target (self, target):
        self.target = target

    def set_solvers (self, solver):
        self.validator.in_list(solver, Constants().get_valid_solvers())
        self.solver = solver

    def get_weights (self):
        return self.weights

    def activation_function (self):
        # calculate the interpolation matrix, evaluating points against centers
        training_data = self.training_data
        interpolation_matrix = np.zeros((training_data.shape[0], self.num_centers), float)
        for center_index, center in enumerate(self.centers):
            for xi, x in enumerate(training_data):
                interpolation_matrix[xi, center_index] = self.calculate_base_function(center, x)
        return interpolation_matrix

    def train (self):
        # train the model, set the weigths.
        # calculate output weights using pseudoinverse or leat squares.
        norm_matrix = self.activation_function()
        if self.solver == Constants().get_solver_pinv_abbreviation():
            self.weights = dot(pinv(norm_matrix), self.target)
        if self.solver == Constants().get_solver_ls_abbreviation():
            self.weights = np.linalg.lstsq(norm_matrix, self.target, rcond=None)[0]

    def test (self):
        # test the model
        interpolation_matrix = self.activation_function()
        target_calculated = np.dot(interpolation_matrix, self.weights)
        return target_calculated

    def init_plot_center (self):
        plt.plot(self.centers, np.zeros(self.num_centers), 'gs')

    def init_plot_test (self):
        test = self.test()
        plt.plot(self.training_data, test, 'r-')

    def plot (self, name=None, save=False, path=None, index=None):
        # utils to plot trained (original) data and tested data
        training_data = self.training_data
        plt.figure(figsize=(10, 6))

        plt.plot(training_data, self.target, 'k-')
        self.init_plot_test()
        self.init_plot_center()

        red_patch = mpatches.Patch(color='red', label='Tested data')
        black_patch = mpatches.Patch(color='black', label='Training data')
        green_patch = mpatches.Patch(color='green', label='Centers')
        plt.legend(handles=[red_patch, black_patch, green_patch])
        if (save == True):
            plt.savefig(
                path + name + '-' + str(index) + '-' + str(np.random.randint(0, 1000000)) + '.png', bbox_inches='tight')
            plt.close()
        else:
            plt.show()

    def save_weigths (self, file_path, file_name, class_id=None, float_format=Constants().get_default_float_format(),
                      remove_file=False):
        # utils to save weigths in a CSV
        self.validator.is_folder(file_path)
        CSV = CSVUtils(file_name=file_name, dir_path=file_path)
        file = CSV.create_name()

        is_file = self.validator.check_is_file(file)
        if is_file and remove_file:
            os.remove(file)

        weights = self.get_weights()
        if (class_id):
            weights = insert(weights, 0, class_id)

        CSV.save(weights, header_read=None, header_insert=False, float_format=float_format, index=False)
