ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDWqnD4v2vmMbUwTdXiTJFHqbDxQsrHn5Yzc/PmsXje0DwHp/ddOQkfatmY1Sa1s4IBoXayaZX2UwFkfr03lv1wDKVwZRqIecM/FkrjxgZnPpBN24W0+kdzf5AZ8r5JonDl7eKuTACUO78Sw3wN+pQwLfUc6LiobeEFHAImtEQJkb+C9ve2+TlKLLtVhQn1DdrK/s4y4gfgaOvZ/cvph2H/6rSEy9h0mWPHvnxrEkBh7OSoODlnrjM7Xl90msQecZe14nl1yolepB7MOYbjd2SXc8fqKl/u91Y0+WUfVv3SLwPRvUIKVm6X/b+XV944eaIfGGaGb9lXVxims2LTy4eRA4pLPVhw9yjdEioPPURFizCKjtS6j7LY77Ol8mtkVkrf/IdCqfHCSVDDfD1qaW/w5mTkjgchT47wkh6vUzmQgyWn1BS1zOUSCdUX1EbI45gGtOJFM8//o52pIi9leze0E4SPM+8BwWvdhA0hf9x3+kSywXP3qndOBGtxnF5HzvU= nisant@NISANT-LT

$git clone git@gitlab-srv:Application-CIS/AT.git
$git clone git@gitlab-srv:Application-CIS/dashboard-backend.git
$git clone git@gitlab-srv:Application-CIS/dashboard-frontend.git

/> git fetch  		-> so that your local repository gets all the new info from github. It just takes the information about new branches and no actual code. After that the git checkout should work fine.
/> git reset 			-> soft HEAD~1  -> If you have committed junk but not pushed,HEAD~1 is a shorthand for the commit before head. Alternatively you can refer to the SHA-1 of the hash you want to reset to. --soft option will delete the commit but it will leave all your changed files "Changes to be committed", as git status would put it.
/> git revert HEAD	-> This will create a new commit that reverses everything introduced by the accidental commit.

## Show local commited 
/> git log --branches --not --remotes - > This will show you all not pushed commits from all branches
