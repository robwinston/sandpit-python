import os
import utils
from datetime import datetime
from pathlib import Path

join = os.path.join

home_dir = utils.ShellCommands.home()

source_full_path_name = join(home_dir, 'learn-master/udemy/java8-complete-reorg/lectures/')
target_path_name = join(home_dir, 'learn-master/udemy/java8-complete-reorg/')

# TODO get all regexxy with this ...
source_dir_pattern = 'Lecture'
default_package_root = 'com.timbuchalka'
default_package_dir = 'com/timbuchalka'

# some of the sample projects have a name matching a java keyword
# consequently, the generated package name will be invalid
# this list numerates those instances so script can obfuscate name accordingly
# presumably, for the script to carry on working if used elsewhere, this list should be exhaustive
reserved_words = ['while', 'final', 'static', 'switch']


if not (os.path.isdir(source_full_path_name) and os.path.isdir(target_path_name)):
    print('One or more invalid input directories: ')
    print('\t' + source_full_path_name)
    print('\t' + target_path_name)
    exit(1)

utils.ShellCommands.mkdir('master', target_path_name)
target_path_name = join(target_path_name, 'master')

current_datetime = datetime.now().date()


def process_package_line(line_to_process, package_suffix):
    original_package_name = line_to_process.split()[1][:-1]
    new_package_name = '.'\
        .join(utils.remove_all_but_last_if_duplicated('{}.{}'.format(original_package_name, package_suffix).split('.')))
    return 'package {};\n'.format(new_package_name)


# TODO add a date / time to this ...
def process_doc_line(line_to_process):
    return line_to_process + ' * Modified by getify.py on {}.\n'.format(current_datetime)


def get_file_ext(the_file_name):
    its_bits = the_file_name.split('.')
    if len(its_bits) == 2:
        return its_bits[1]
    else:
        return None


def write_file(file_name, its_contents):
    with open(file_name, 'w') as f:
        f.writelines(its_contents)


def cleanse_package_name(pkg_name):
    if pkg_name is None:
        return None
    pkg_name = pkg_name.replace(' ', '_')
    # TODO for fun & profit, derive a functional way to do this ...
    if any(rw in pkg_name for rw in reserved_words):
        its_bits = pkg_name.split('.')
        its_bits_fixed = []
        for abit in its_bits:
            if abit in reserved_words:
                its_bits_fixed.append('_' + abit)
            else:
                its_bits_fixed.append(abit)
        # some package names already had project name in it,  if so remove duplicate
        its_bits_fixed = utils.remove_all_but_last_if_duplicated(its_bits_fixed)
        pkg_name_new = '.'.join(its_bits_fixed)
        return pkg_name_new
    else:
        return '.'.join(utils.remove_all_but_last_if_duplicated(pkg_name.split('.')))


def process_java_file(file_to_process):
    out_lines = []
    new_package_line = None
    pkg_name = None

    with open(file_to_process, 'r') as source_file:
        for line in source_file.readlines():
            if line.find('package') == 0:
                if line.find('todolist') != -1:
                    print('here')
                new_package_line = process_package_line(line, '{}.{}'.format(package_lecture, package_project))
                pkg_name = new_package_line.split()[1][:-1]
                out_lines.append(new_package_line)
            elif line.find('* Created by ') != -1:
                out_lines.append(process_doc_line(line))
            else:
                out_lines.append(line)
    if new_package_line == '':
        print('no package name in source')
    return pkg_name, out_lines

source_path = Path(source_full_path_name)
# num_to_process = 10
# num_processed = 0
for lecture_dir in [sd for sd in source_path.iterdir() if sd.name.find(source_dir_pattern) != -1]:

    package_lecture = str.lower(lecture_dir.name)
    source_dir_full_path = join(source_full_path_name, lecture_dir.name)
    print('Processing: ' + source_dir_full_path)
    its_path = Path(source_dir_full_path)

    for prj_dir in [entry for entry in its_path.iterdir() if entry.is_dir()]:
        prj_dir_name = prj_dir.name.replace(' ', '_')
        package_project = str.lower(prj_dir_name)

        for file_name in [entry.name for entry in prj_dir.iterdir() if entry.is_file()]:
            print('Processing: ' + file_name)
            full_file_name = join(source_dir_full_path, prj_dir.name, file_name)
            file_ext = get_file_ext(file_name)
            if file_ext == 'java':
                package_name, file_contents = process_java_file(full_file_name)
                if package_name is not None:
                    package_dir = package_name.replace('.', '/')
                else:
                    package_dir = join(default_package_dir, str.lower(lecture_dir.name), prj_dir_name)
                full_target_dir = join(target_path_name, 'src', package_dir)
                utils.ShellCommands.mkdir(full_target_dir)
                full_file_name = join(full_target_dir, file_name)
                write_file(full_file_name, file_contents)
            else:
                # for anything else, just copy the file over ...
                package_dir = join(default_package_dir, str.lower(lecture_dir.name), str.lower(prj_dir_name))
                full_target_dir = join(target_path_name, 'src', package_dir)
                utils.ShellCommands.mkdir(full_target_dir)
                utils.ShellCommands.cp(full_file_name, full_target_dir)
    # num_processed += 1
    # if num_processed == num_to_process:
    #     break

