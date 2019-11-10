from ClassDataSetAnalyzer import DataSetAnalyzer
from ClassRBFN import RBFN
from ClassCSVUtils import CSVUtils

import os
import numpy as np

dirpath = os.path.dirname(os.path.abspath(__file__)) + '\\..\\examples\\'
file_name = 'sin'

DA = DataSetAnalyzer(file_path=dirpath, file_name=file_name);
DA.set_normalized(True);
DA.set_norm(1);

axis = DA.get_feature_axis()
centers = np.linspace(1,len(axis), 30, dtype=int)

rbfn = RBFN(axis)
rbfn.set_epsilon(1 / 50)

DA.set_rbfn(rbfn)
dirpath = dirpath + 'plots\\'

DA.save_weigths_in_csv(centers, dirpath, file_name='sin_weigths', save_plot=True, class_id=None,
                             float_format='%0.15f', remove_file=True)
