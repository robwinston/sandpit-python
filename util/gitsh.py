import sh
import os

home_dir = os.environ['HOME']
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


