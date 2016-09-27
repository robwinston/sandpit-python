def all_lines(file_name_):
    with open(file_name_, 'r') as file:
        lines = file.readlines()
    return lines


def write_file(file_name_, its_contents):
    with open(file_name_, 'w') as f:
        f.writelines(its_contents)


def get_file_ext(the_file_name):
    its_bits = the_file_name.split('.')
    if len(its_bits) == 2:
        return its_bits[1]
    else:
        return None

