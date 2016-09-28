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


def full_package_dir():
    pass


def add_original_package_names(file_content_pairs):
    return [(file_name, get_existing_package_name(its_lines), its_lines)
            for (file_name, its_lines) in file_content_pairs]


def unique_package_names(file_package_pairs):
    return set([package_name for (_, package_name, _) in file_package_pairs]) - {None}


def common_package_root(package_names):
    if len(package_names) == 0:
        return None
    if len(package_names) == 1:
        return list(package_names)[0]

    package_nodes = [package_name.split('.') for package_name in package_names]
    shortest_len = min([len(nodes) for nodes in package_nodes])
    root_nodes = []
    for idx in range(0, shortest_len):
        if len(set([nodes[idx] for nodes in package_nodes])) == 1:
            root_nodes.append(package_nodes[0][idx])
        else:
            break
    return '.'.join(root_nodes) if len(root_nodes) > 0 else None


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


def add_or_modify_package_name(file_with_pkg_and_content, common_pkg_root):
    src_file_name, original_package_name, original_file_contents = file_with_pkg_and_content

    pkg_suffix = None if original_package_name is None or len(original_package_name) == len(common_pkg_root) \
        else original_package_name[len(common_pkg_root.split('.')):]

    # TODO this approach seems ugly ...
    src_path_bits = src_file_name.split('/')
    prj_node = src_path_bits[-2]
    lecture_node = src_path_bits[-3]

    new_package_name = cleanse_package_name('.'.join([common_pkg_root, lecture_node, prj_node]))
    if pkg_suffix is not None:
        '.'.join([new_package_name, pkg_suffix])

    new_package_line = str.format('package {};', new_package_name)

    if original_package_name is None:
        new_file_contents = [new_package_line] + original_file_contents
    else:
        new_file_contents = [new_package_line] + original_file_contents[1:]

    return new_package_name, new_file_contents


def modify_imports(lines):
    return lines


# java files need their package names altered to match their destination
def process_java_files(files_to_process):
    # create a list of pairs ("pathless" file name, its content as a list of lines)
    files_with_content = [(file_to_process, all_lines(file_to_process)) for file_to_process in files_to_process]
    files_with_pkg_and_content = add_original_package_names(files_with_content)
    unique_pkg_names = unique_package_names(files_with_pkg_and_content)
    common_pkg_root = common_package_root(unique_pkg_names)
    for file_with_pkg_and_content in files_with_pkg_and_content:
        new_pkg_name, new_file_contents = add_or_modify_package_name(file_with_pkg_and_content, common_pkg_root)
        new_file_contents = modify_imports(new_file_contents)
        new_file_contents = add_or_modify_doc_string(new_file_contents)
        print('here')






