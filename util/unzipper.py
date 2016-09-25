from pathlib import Path
from zipfile import ZipFile
import os
import shutil

# Examine a downloaded 'lecture' zip file from Udemy - The Complete Java 8 Developer Course
# For each 'project' (usually just one per zip, but sometimes more), extract all of the java files
# and place them in a 'lecture/proj_name' folder -
# ... in this instance ignoring 'package' directories, because the intent is to refactor these later
# (so multiple versions of the same java Class can co-exist, qualified by the lecture/project they appeared in)
# for unduly nested zips, flatten  / after files are moved remove orphaned directories

home_dir = os.environ['HOME']
source_path_name = home_dir + '/learn-master/udemy/java8-complete-reorg/zips/'
target_path_name = home_dir + '/learn-master/udemy/java8-complete-reorg/lectures/'

if not (os.path.isdir(source_path_name) and os.path.isdir(target_path_name)):
    print('One or more invalid input directories: ')
    print('\t' + source_path_name)
    print('\t' + target_path_name)
    exit(1)


source_path = Path(source_path_name)

interactive = False


def dir_name_for_file(file_name):
    bits = str.split(file_name)
    return "{}{}{:03d}".format(target_path_name, bits[0], int(bits[1]))


def get_root_dirs(zip_file_filelist):

    dirs_ending_with_src = set([elem.filename[:-1] for elem in zip_file_filelist if elem.filename.endswith('src/')])

    roots = set([elem[:elem.rfind('/')] for elem in dirs_ending_with_src])

    return roots

# alt 'troublesome' code (used for debugging zip files which tripped up 1st-cut logic):
# source_files = ['Lecture 117 - Sets Challenge Part 1 - Source code.zip']
# source_files = ['Lecture 190 - Fair Locks and Live Locks - Source code.zip']

# alt 'troublesome' code:
# for source_file in source_files:

for source_file in [entry for entry in source_path.iterdir() if entry.is_file()]:

    # alt 'troublesome' code:
    # source_file_name = source_file

    source_file_name = source_file.name

    if source_file_name[-3:] != 'zip':
        print("Skipping: " + source_file_name)
        continue

    if interactive:
        ok = str.lower(input("Processing: " + source_file_name + ", proceed? "))
        if ok[0] != 'y':
            break
    else:
        print("Processing: " + source_file_name)

    lecture_dir_name = dir_name_for_file(source_file_name)
    if os.path.isdir(lecture_dir_name):
        shutil.rmtree(lecture_dir_name)

    zip_file = ZipFile(source_path_name + source_file_name, mode="r")

    root_dirs = get_root_dirs(zip_file.filelist)

    # some zip files contain multiple projects ...
    for root_dir in root_dirs:
        project_dir_name = lecture_dir_name + '/' + root_dir
        # find and extract the ".java" files
        zfile_names = [zf.filename for zf in zip_file.filelist if
                       zf.filename[-4:] == 'java' and zf.filename.find(root_dir) == 0]
        for zfile_name in zfile_names:
            zip_file.extract(zfile_name, project_dir_name)

        # move them to the root (we'll be refactoring them to different packages later ...)
        for dirName, subdirList, fileList in os.walk(project_dir_name):
            for fileName in fileList:
                shutil.move(dirName + '/' + fileName, project_dir_name)

        # some of the zip files have an empty 'root' dir or one without java files
        # if so, nothing gets extracted and 'project_dir_name' doesn't get created, so we need to check
        if os.path.isdir(project_dir_name):
            pd = Path(project_dir_name)
            # now that source files have been moved to project's 'root dir', remove all sub-dirs
            for entry in [entry for entry in pd.iterdir() if entry.is_dir()]:
                shutil.rmtree(project_dir_name + '/' + entry.name)

    # some zip files have an extra level of nesting at the root ... fix this
    lp = Path(lecture_dir_name)
    for entry in [entry for entry in lp.iterdir() if entry.is_dir()]:
        entry_full_name = lecture_dir_name + '/' + entry.name
        # if there's a '__MACOSX' dir ... remove it
        if entry.name == '__MACOSX':
            shutil.rmtree(entry_full_name)
        else:
            lpp = Path(entry_full_name)
            remove_parent = False
            for entry_sub in [entry for entry in lpp.iterdir() if entry.is_dir()]:
                # if we get here, we've discovered an extra level of nesting ...
                entry_sub_full_name = entry_full_name + '/' + entry_sub.name
                print("Moving: " + entry_sub_full_name)
                shutil.move(entry_sub_full_name, lecture_dir_name)
                remove_parent = True
            if remove_parent:
                shutil.rmtree(entry_full_name)


    # create a readme with the name of of the zip file from which it all came
    with open(lecture_dir_name + '/readme.txt', 'w') as rm:
        rm.writelines(source_file_name)
