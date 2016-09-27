def all_lines(file_name_):
    with open(file_name_, 'r') as file:
        lines = file.readlines()
    return lines


def write_file(file_name_, its_contents):
    with open(file_name_, 'w') as f:
        f.writelines(its_contents)


