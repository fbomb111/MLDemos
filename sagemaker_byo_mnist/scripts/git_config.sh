# git_config.sh

# add the source remote
git remote add upstream 'https://github.com/captechconsulting/aaml-tc01-mnist.git'
git fetch upstream master
git pull upstream --allow-unrelated-histories --no-edit master
git push origin master

# create and checkout new branch for student to work on 
git checkout -b develop

# protect against master commits
chmod +x githooks/pre-commit
git config core.hooksPath githooks