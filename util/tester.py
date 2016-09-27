import utils

# test = 'com.timbuchalka.todolist.lecture148.todolist'
# print(test)
# bits = utils.remove_all_but_last_if_duplicated(test.split('.'))
# print('.'.join(bits))

files_to_test = ['../test_data/gotdoc.java', '../test_data/gotnodoc.java']

for afile in files_to_test:
    lines = utils.all_lines(afile)
    # lines = utils.add_or_modify_doc_string(lines)
    # for line in lines:
    #     print(line)
    print(utils.get_existing_package_name(lines))
