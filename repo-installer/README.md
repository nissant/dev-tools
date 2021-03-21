 # Env Installer
Repo installer helps to install git repositories and packages in configurable and easy way

## Prequisites 

*  Installation of python >=3.7 

*  User access to repository must be approved by repoistry owner

*  User ssh autethication token setup on local git environment


## Development
```bash
git clone  
cd 
pip install -r requirements.txt     # install requirements
```

## Run
### Example using env installer
##### running full installation
```
python env_installer.py --config_file env_config.json --wd c:\jenkins\workspace\APP\ATLab --only_reset_and_pull 0
```
##### running installation except requirements and general prequisites packages (setuptools, requests, pip)
```
python repo-installer.py --config_file env_config.json --wd c:\jenkins\workspace\APP\ATLab --only_reset_and_pull 1
```

## Configuration
#####  using JSON environment configuration file we can change the installation easily. parameters description:
    "name": "AT",  # Repo data name which is used for metadata
    "repo_dir": "Projects\\gitlab\\AT\\",  # Where to clone the Git repository(relative to the selected working dir)
    "git_url": "git@gitlab-srv:Application-CIS/AT.git", # Git URL
    "branch": "at_lab", # Git branch
    "pre_install": 1, # if to install requirements of the python package
    "install": 1, # install package(or just to clone)
    "editable": 1, # if install is active, so edtiable option is available
    "post_install": 1, # post installation 
    "post_install_py_script": "post_install.py", #if post installation is active what is the python script to run
    "requirement_file_list": ["requirements.txt","requirements_sirc_develop.txt"], #if pre install option is needed what are the requirements 
    "ignore": 0 # in case we want to disable installation of this repo 


