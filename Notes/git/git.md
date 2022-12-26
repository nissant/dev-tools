$git clone git@gitlab-srv:Application-CIS/AT.git
$git clone git@gitlab-srv:Application-CIS/dashboard-backend.git
$git clone git@gitlab-srv:Application-CIS/dashboard-frontend.git

/> git fetch  		-> so that your local repository gets all the new info from github. It just takes the information about new branches and no actual code. After that the git checkout should work fine.
/> git reset 			-> soft HEAD~1  -> If you have committed junk but not pushed,HEAD~1 is a shorthand for the commit before head. Alternatively you can refer to the SHA-1 of the hash you want to reset to. --soft option will delete the commit but it will leave all your changed files "Changes to be committed", as git status would put it.
/> git revert HEAD	-> This will create a new commit that reverses everything introduced by the accidental commit.

## Show local commited 
/> git log --branches --not --remotes - > This will show you all not pushed commits from all branches
