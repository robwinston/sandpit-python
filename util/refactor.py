import os
from utils import Logger

join = os.path.join

def get_file_list():
    return None


def modify_java_file(file_dir, file_name):
    return None

home_dir = os.environ['HOME']
source_path_name = join(home_dir, 'learn-master/udemy/python-complete-reorg/zips/')
target_path_name = join(home_dir, 'learn-master/udemy/python-complete-reorg/')
file_extensions = ['java', 'py', 'txt']

if not (os.path.isdir(source_path_name) and os.path.isdir(target_path_name)):
    print('One or more invalid input directories: ')
    print('\t' + source_path_name)
    print('\t' + target_path_name)
    exit(1)

log_file_name = Logger.get_log_name(home_dir, 'refactor')

print(log_file_name)

# log_file = open(log_file_name, mode='w')


'''
package com.timbuchalka;

/**
 * Created by dev on 8/3/15.
 */
public class Dog extends Animal {
'''