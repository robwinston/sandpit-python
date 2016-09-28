def all_lines(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    return lines


def write_file(file_name, its_contents):
    its_contents_with_line_breaks = []
    for line in its_contents:
        if line == '':
            new_line = '\n'
        elif line[-1] != '\n':
            new_line = line + '\n'
        else:
            new_line = line
        its_contents_with_line_breaks.append(new_line)

    with open(file_name, 'w') as f:
        f.writelines(its_contents_with_line_breaks)


def get_file_ext(the_file_name):
    its_bits = the_file_name.split('.')
    if len(its_bits) == 2:
        return its_bits[1]
    else:
        return None

