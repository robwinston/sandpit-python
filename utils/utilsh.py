import shutil

import sh
import os

home = os.environ['HOME']


class ShellCommands(object):

    @staticmethod
    def mkdir(dir_to_make, dir_to_make_it_in=home):
        """
        Issue mkdir command to create the requested directory
        :param dir_to_make: relative path of directory to make, may have multiple levels
        :param dir_to_make_it_in: absolute path to make it in, default = user's home dir
        :return: True if dir was created; False if directory was already present
        """
        target_dir = os.path.join(dir_to_make_it_in, dir_to_make)
        if not os.path.isdir(target_dir):
            sh.Command('/bin/mkdir')('-p', os.path.join(dir_to_make_it_in, dir_to_make))
            return True
        else:
            return False

    @staticmethod
    def cp(from_file, to_dir):
        ShellCommands.mkdir(to_dir)
        return shutil.copy(from_file, to_dir)

    @staticmethod
    def home():
        return os.environ['HOME']
