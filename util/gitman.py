import os
from git import Repo
join = os.path.join

home_dir = os.environ['HOME']

pyth_dir = 'learn-me/udemy/python-complete/course'
java_dir = 'learn-me/udemy/java8-complete/course'
test_dir = 'learn-sandpit/sandpit-python'

repo_working_tree_dir = join(home_dir, test_dir)

# pasting in a bunch of fragments from:
# https://gitpython.readthedocs.io/en/stable/tutorial.html
# to get familiar ...

repo = Repo(repo_working_tree_dir)
assert not repo.bare

# print(repo.active_branch.name)

# to init a bare repo:
# bare_repo = Repo.init(join(rw_dir, 'bare-repo'), bare=True)
# assert bare_repo.bare

cr = repo.config_reader()             # get a config reader for read-only access
crv = cr.values()

# cw = repo.config_writer()             # get a config writer to change configuration
# cw.release()                          # call release() to be sure changes are written and locks are released

is_dirty = repo.is_dirty()                 # check the dirty state

if is_dirty:
    untracked_files = repo.untracked_files  # retrieve a list of untracked files
    print("{} has {} untracked_files".format(repo.working_tree_dir, len(untracked_files)))
    for file in untracked_files:
        print(file)


