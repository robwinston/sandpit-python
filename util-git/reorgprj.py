import os
import utils
from pathlib import Path

join = os.path.join

home_dir = utils.ShellCommands.home()

source_full_path_name = join(home_dir, 'learn-master/udemy/java8-complete-reorg/lectures/')
target_path_base = join(home_dir, 'learn-master/udemy/java8-complete-reorg/')

# TODO get all regexxy with this ...
source_dir_pattern = 'Lecture'
default_package_root = 'com.timbuchalka'
default_package_dir = 'com/timbuchalka'

if not (os.path.isdir(source_full_path_name) and os.path.isdir(target_path_base)):
    print('One or more invalid working directories: ')
    print('\tSource:' + source_full_path_name)
    print('\tTarget:' + target_path_base)
    exit(1)


utils.ShellCommands.mkdir('master', target_path_base)
target_path_name = join(target_path_base, 'master')


def full_package_dir():
    pass


def all_package_names(file_content_pairs):
    return [(file_name, utils.get_existing_package_name(its_lines)) for (file_name, its_lines) in file_content_pairs]


def unique_package_names(file_package_pairs):
    return set([package_name for (_, package_name) in file_package_pairs])


def common_package_root(package_names):
    node_sets = []
    # TODO derive functional equivalent
    for package_name in package_names:
        its_nodes = package_name.split('.')
        for node_idx in range(0, len(its_nodes)):
            if len(node_sets) > node_idx:
                node_sets[node_idx].add(its_nodes[node_idx])
            else:
                node_sets.append(set())
                node_sets[node_idx].add(its_nodes[node_idx])
    print('here')


def process_java_lines(its_lines):

    pkg_name, its_lines = utils.add_or_modify_package_name(its_lines)
    its_lines = utils.modify_imports(its_lines)
    its_lines = utils.add_or_modify_doc_string(its_lines)

    return pkg_name, its_lines


# java files need their package names altered to match their destination
def process_java_files(files_to_process):
    # create a list of pairs ("pathless" file name, its content as a list of lines)
    file_content_pairs = [(os.path.basename(file_to_process), utils.all_lines(file_to_process))
                          for file_to_process in files_to_process]
    all_pkg_names = all_package_names(file_content_pairs)


# presently 'other' files are simply copied over -
def process_other_files(files_to_process, lecture_dir_name, prj_dir_name):
    for full_file_name in files_to_process:
        package_dir_name = join(default_package_dir, str.lower(lecture_dir_name), str.lower(prj_dir_name))
        full_target_dir = join(target_path_name, 'src', package_dir_name)
        utils.ShellCommands.mkdir(full_target_dir)
        utils.ShellCommands.cp(full_file_name, full_target_dir)


def main_process():
    source_path = Path(source_full_path_name)
    for lecture_dir_name in [entry.name for entry in source_path.iterdir() if entry.name.find(source_dir_pattern) != -1]:
        lecture_dir_path_string = join(source_full_path_name, lecture_dir_name)
        print('Processing: ' + lecture_dir_path_string)
        lecture_dir_path = Path(lecture_dir_path_string)

        for prj_dir in [entry for entry in lecture_dir_path.iterdir() if entry.is_dir()]:
            prj_dir_name = prj_dir.name
            prj_full_file_names = [join(lecture_dir_path_string, prj_dir_name, entry.name) for entry in prj_dir.iterdir() if entry.is_file()]
            process_java_files([entry for entry in prj_full_file_names if utils.get_file_ext(entry) == 'java'])
            process_other_files([entry for entry in prj_full_file_names if utils.get_file_ext(entry) != 'java'],
                                lecture_dir_name, prj_dir_name)
