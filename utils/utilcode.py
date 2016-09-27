import os
from datetime import datetime
from utillist import remove_all_but_last_if_duplicated
from utilfile import all_lines


def get_datetime_string():
    now = datetime.now()
    return '{:4d}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)


def add_or_modify_doc_string(lines):
    lines_out = []
    existing_doc_strings = []
    put_doc_strings = False
    for line in lines:
        line = line[:-1]
        if put_doc_strings:
            lines_out.append(line)
        elif 'class' in line.split():
            lines_out = lines_out + generate_doc_lines(existing_doc_strings)
            lines_out.append(line)
            put_doc_strings = True
        elif line.find('/**') == 0 or line.find(' */') == 0:
            continue
        elif line.find(' *') == 0:
            if len(line) > 2:
                existing_doc_strings.append(line[2:])
        else:
            lines_out.append(line)

    return lines_out


def generate_doc_lines(lines_to_include):
    doc_lines = ['/*']
    doc_lines = doc_lines + [' * ' + line_to_include for line_to_include in lines_to_include]
    doc_lines.append(' *  Modified by getify.py at {}.'.format(get_datetime_string()))
    doc_lines.append('*/')
    return doc_lines


def get_existing_package_name(lines):
    package_names = [line.split(' ')[1][:-2] for line in lines if line.find('package') == 0]
    if len(package_names) == 0:
        return None
    elif len(package_names) == 1:
        return package_names[0]
    else:
        raise ValueError('Found multiple package statements: {0}'.format(package_names))


# some of the sample projects have a name matching a java keyword
# consequently, the generated package name will be invalid
# this list numerates those instances so script can obfuscate name accordingly
# presumably, for the script to carry on working if used elsewhere, this list should be exhaustive
reserved_words = ['while', 'final', 'static', 'switch']


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
        its_bits_fixed = remove_all_but_last_if_duplicated(its_bits_fixed)
        pkg_name_new = '.'.join(its_bits_fixed)
        return pkg_name_new
    else:
        return '.'.join(remove_all_but_last_if_duplicated(pkg_name.split('.')))


def add_or_modify_package_name(lines):
    return '', lines


def modify_imports(lines):
    return lines

def full_package_dir():
    pass


def all_package_names(file_content_pairs):
    return [(file_name, get_existing_package_name(its_lines)) for (file_name, its_lines) in file_content_pairs]


def unique_package_names(file_package_pairs):
    return set([package_name for (_, package_name) in file_package_pairs]) - {None}


def common_package_root(package_names):
    if len(package_names) == 0:
        return None
    if len(package_names) == 1:
        return package_names[0]
    
    package_nodes = [package_name.split('.') for package_name in package_names]
    shortest_len = min([len(nodes) for nodes in package_nodes])
    root_nodes = []
    for idx in range(0, shortest_len):
        if len(set([nodes[idx] for nodes in package_nodes])) == 1:
            root_nodes.append(package_nodes[0][idx])
        else:
            break
    return '.'.join(root_nodes) if len(root_nodes) > 0 else None



def process_java_lines(its_lines):

    pkg_name, its_lines = add_or_modify_package_name(its_lines)
    its_lines = modify_imports(its_lines)
    its_lines = add_or_modify_doc_string(its_lines)

    return pkg_name, its_lines


# java files need their package names altered to match their destination
def process_java_files(files_to_process):
    # create a list of pairs ("pathless" file name, its content as a list of lines)
    file_content_pairs = [(os.path.basename(file_to_process), all_lines(file_to_process))
                          for file_to_process in files_to_process]
    all_pkg_names = all_package_names(file_content_pairs)
    unique_pkg_names = unique_package_names(all_pkg_names)
    print('Files: {}, pkg names: {}, unq pns: {}'.format(len(file_content_pairs), len(all_pkg_names), len(unique_pkg_names)))
    if len(unique_pkg_names) > 1:
        print(unique_pkg_names)
        cpr = common_package_root(unique_pkg_names)
        print("common root: " + cpr)




