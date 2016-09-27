from datetime import datetime
from utillist import remove_all_but_last_if_duplicated


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


