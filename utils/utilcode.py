from datetime import datetime


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
