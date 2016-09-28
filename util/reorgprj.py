import os
import utils
from pathlib import Path

join = os.path.join

home_dir = utils.ShellCommands.home()

source_full_path_name = join(home_dir, 'learn-master/udemy/java8-complete-reorg/lectures/')
target_path_base = join(home_dir, 'learn-master/udemy/java8-complete-reorg/')

# TODO get all regexxy with this ...
source_dir_pattern = 'Lecture'
default_package_dir = 'com/timbuchalka'
default_package_root = 'com.timbuchalka'


if not (os.path.isdir(source_full_path_name) and os.path.isdir(target_path_base)):
    print('One or more invalid working directories: ')
    print('\tSource:' + source_full_path_name)
    print('\tTarget:' + target_path_base)
    exit(1)


utils.ShellCommands.mkdir('master', target_path_base)
target_path_name = join(target_path_base, 'master')


# presently 'other' files are simply copied over -
def process_other_files(files_to_process, new_pkg_root):
    for full_file_name in files_to_process:
        package_dir_name = new_pkg_root.replace('.', '/')
        full_target_dir = join(target_path_name, 'src', package_dir_name)
        utils.ShellCommands.mkdir(full_target_dir)
        utils.ShellCommands.cp(full_file_name, full_target_dir)


def main_process():
    source_path = Path(source_full_path_name)
    for lecture_dir_name in [entry.name for entry in source_path.iterdir()
                             if entry.name.find(source_dir_pattern) != -1]:
        lecture_dir_path_string = join(source_full_path_name, lecture_dir_name)
        print('Processing: ' + lecture_dir_path_string)
        lecture_dir_path = Path(lecture_dir_path_string)

        for prj_dir in [entry for entry in lecture_dir_path.iterdir() if entry.is_dir()]:
            prj_dir_name = prj_dir.name
            prj_full_file_names = [join(lecture_dir_path_string, prj_dir_name, entry.name)
                                   for entry in prj_dir.iterdir() if entry.is_file()]

            processed_java_files = \
                utils.process_java_files([entry for entry in prj_full_file_names
                                          if utils.get_file_ext(entry) == 'java'], default_package_root)

            for (src_path, new_pkg_name, file_contents) in processed_java_files:
                target = os.path.join(target_path_name, 'src', new_pkg_name.replace('.', '/'))
                utils.ShellCommands.mkdir(target)
                file_name = os.path.join(target, os.path.basename(src_path))
                utils.write_file(file_name, file_contents)

            new_pkg_root = utils.common_package_root([pkg_name for _, pkg_name, _ in processed_java_files])
            process_other_files([entry for entry in prj_full_file_names if utils.get_file_ext(entry) != 'java'],
                                new_pkg_root)

main_process()
