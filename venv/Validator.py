import os.path
from os import path

class Validator:
    def __init__ (self, data=None):
        self.data = data

    def is_csv (self, file_name):
        if not self.check_is_csv(file_name):
            error = str(file_name) + ' Is not a valid CSV .'
            raise ValueError(error)

    def check_is_file (self, file_name):
        return path.isfile(file_name)

    def is_file (self, file_name):
        if not self.check_is_file(file_name):
            error = str(file_name) + ' Is not a valid file .'
            raise ValueError(error)

    def index_exists (self, list, index):
        if not 0 <= index < len(list):
            error = str(file_name) + ' Is not a valid index .'
            raise ValueError(error)

    def is_bool (self, value):
        if not isinstance(value, bool):
            raise ValueError('Value not valid.')

    def in_list (self, value, values_list):
        if value not in values_list:
            raise ValueError('Value not valid.')

    def is_object_type (self, object, object_class):
        if not self.check_is_object_type(object, object_class):
            raise ValueError('Value not valid.')

    def check_is_object_type (self, object, object_class):
        if type(object) is not type(object_class):
            return False
        return True

    def is_folder (self, folder):
        if not self.check_is_folder(folder):
            raise ValueError('Folder not exists.')

    def check_is_folder (self, folder):
        if not path.isdir(folder):
            return False
        return True

    def check_is_csv (self, file_name):
        is_folder = self.check_is_folder(file_name)
        if is_folder:
            return False
        ext = os.path.splitext(file_name)[-1].lower()
        check = self.check_is_file(file_name)
        if not check:
            return False
        if ext != '.csv':
            return False
        return True
