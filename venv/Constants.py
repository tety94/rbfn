from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from sklearn.decomposition import MiniBatchSparsePCA
from Validator import Validator


class Constants:
    def __init__ (self):
        pass

    def get_max_norm_abbreviation (self):
        return 'max'

    def get_l1_norm_abbreviation (self):
        return 'l1'

    def get_l2_norm_abbreviation (self):
        return 'l2'

    def get_norms_list (self):
        return [None, 1, 'l1', 2, 'l2', 'max']

    def get_norm_abbreviation (self, norm):
        if (norm == self.get_l1_norm_abbreviation() or norm == 1):
            return 'l1';
        if (norm == self.get_max_norm_abbreviation()):
            return 'max';
        return 'l2';

    def get_rbfn_base_functions_list (self):
        return [self.get_rbfn_inv_multq_abbreviation(), self.get_rbfn_inv_q_abbreviation(),
                self.get_rbfn_polyharmonic_abbreviation(), self.get_rbfn_gaussian_abbreviation()]

    def get_rbfn_inv_multq_abbreviation (self):
        return 'inverseMultiQuadratic'

    def get_rbfn_inv_q_abbreviation (self):
        return 'inverseQuadratic'

    def get_rbfn_polyharmonic_abbreviation (self):
        return 'polyharmonicSpline'

    def get_rbfn_gaussian_abbreviation (self):
        return 'gaussian'

    def get_rbfn_deafult_epsilon(self):
        return 1/14

    def get_rbfn_default_k(self):
        return 2

    def get_valid_solvers (self):
        return [self.get_solver_ls_abbreviation(), self.get_solver_pinv_abbreviation()]

    def get_solver_ls_abbreviation (self):
        return 'leastSquares'

    def get_solver_pinv_abbreviation (self):
        return 'pinv'

    def get_default_float_format (self):
        return '%0.15f'

    def get_csv_format (self):
        return '.csv'

