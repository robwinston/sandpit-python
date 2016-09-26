import sh
import os


home_dir = os.environ['HOME']
'''
repo_dir = os.path.join(home_dir, 'learn-me/misc/git-sh')

git = sh.git.bake(_cwd=repo_dir)

print(git.status())

# checkout and track a remote branch
print(git.checkout('-b', 'test-branch'))

# add a file
print(git.add('test-file'))

# commit
print(git.commit(m='commit using python!'))

# now we are one commit ahead
print(git.status())
'''

mkdir_cmd = sh.Command('/bin/mkdir')


def git_init(dir_to_use):
    if os.path.isdir(dir_to_use):
        print(dir_to_use + ": already exists")
        return None

    mkdir_cmd(dir_to_use)
    git_cmd = sh.git.bake(_cwd=dir_to_use)
    print(git_cmd.init())
    return git_cmd



repo_dir = os.path.join(home_dir, 'learn-me/misc/git-sh2')

git = git_init(repo_dir)

print("From returned command ...\n{}".format(git.status()))










