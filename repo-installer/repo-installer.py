import os
import pip
import git
import json
import click
import sys
import argparse
import subprocess
from pathlib import Path
from git import Repo
from git import Git
from git import RemoteProgress
from dataclasses import dataclass

@dataclass
class RepoData:
   name: str
   repo_dir: str
   git_url: str
   branch: str
   pre_install: int
   install: int
   editable: int
   post_install: int
   post_install_py_script: str
   requirement_file_name: str

class CloneProgress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        if message:
            print(message)

def pre_install(python, repo_dir, requirement_file_name = 'requirements_37.txt'):

    call_list = [python, '-m', 'pip', 'install', '-r', str(Path(repo_dir) / requirement_file_name)]

    print(call_list)
    subprocess.call(call_list)


def post_install(python, repo_dir, post_install_py_script):
    call_list = [python,  str(Path(repo_dir) / post_install_py_script)]
    print(call_list)

    with Path(repo_dir):
        # current working directory is now repo_dir
        subprocess.call(call_list, cwd=repo_dir)

    # current working directory is restored to its original value.


def install(python, repo_dir, editable):
    if editable:
        call_list = [python , '-m', 'pip', 'install', '-e', repo_dir]
    else:
        call_list = [python , '-m', 'pip', 'install', repo_dir]

    print(call_list)
    subprocess.call(call_list)


def reset_hard_and_pull(repo, branch_name):
    # ensure master is checked out
    repo.heads[branch_name].checkout()
    # blast any changes there (only if it wasn't checked out)
    repo.git.reset('--hard')
    # remove any extra non-tracked files (.pyc, etc)
    repo.git.clean('-xdf')
    # pull in the changes from from the remote
    repo.remotes.origin.pull()


def clone_repo(repo_dir,git_url, branch = 'master'):
    git.Repo.clone_from(git_url, repo_dir,
                        branch= branch, progress=CloneProgress())


def upgrade_pip(python):
    call_list = [python ,'-m', 'pip', 'install', '--upgrade', 'pip']
    print(call_list)
    subprocess.call(call_list)


def upgrade_setuptools(python):
    call_list = [python ,'-m', 'pip', 'install', 'setuptools',  '--upgrade']
    print(call_list)
    subprocess.call(call_list)


def upgrade_requests(python):
    call_list = [python ,'-m', 'pip', 'install', 'requests', ]
    print(call_list)
    subprocess.call(call_list)

@click.command()
@click.argument('config_file')
@click.option('--python', type=str, default=r'C:\Python37\python.exe')
def extract_args(config_file,python):
    print(config_file,python)
    return config_file,python


def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("--config_file", help="Configuration file.", type=str)

    #optional arguments
    parser.add_argument("-s", "--venv_dir", help="Venv root dir.", type=str,
                        default=None)

    # optional arguments
    parser.add_argument("-t", "--wd", help="Working dir.", type=str,
                        default='C:/')

    parser.add_argument("-u", "--only_fetch", help="This flag defines if we only fetch.", type=int,
                        default=0)

    # Parse arguments
    args = parser.parse_args()

    return args


def update_repos(config_file,python, wd, only_fetch):
    """Update Repos according to config file content."""
    # click.echo(config_file)
    config_file = Path(config_file)
    # read from json file the list of repositories
    try:
        with config_file.open() as f:
            repo_dic =  json.load(f)
    except OSError:
            general_message = f'reading the json file {str(config_file)} '
            warning_message = 'Failed ' + general_message
            print('Failed ' + general_message)
            return
    repo_list = repo_dic["repo_list"]
    for item in repo_list:
        repo_data = RepoData(**item)
        repo_data.repo_dir = str(wd / repo_data.repo_dir)
        print(repo_data.repo_dir)
        # establish folder
        Path(repo_data.repo_dir).mkdir(parents=True, exist_ok=True)

        try:
            # reset and pull
            repo = Repo(repo_data.repo_dir)
            reset_hard_and_pull(repo,  repo_data.branch)
            print(f'pull reset {repo_data}')

        except git.exc.InvalidGitRepositoryError:
            #clone
            clone_repo(repo_data.repo_dir,repo_data.git_url, repo_data.branch)
            print(f'clone {repo_data}')

        if repo_data.pre_install and not only_fetch:
            pre_install(python, repo_data.repo_dir, repo_data.requirement_file_name)

        #install part
        if repo_data.install and not only_fetch:
            install(python, repo_data.repo_dir, repo_data.editable)

        if repo_data.post_install and not only_fetch:
            #in case the sim repo and editable we need to patch instead of change install_sim.py
            if repo_data.name == 'sim' and repo_data.editable == 1:
                post_install_sim(repo_data.repo_dir)
            else:
                post_install(python, repo_data.repo_dir, repo_data.post_install_py_script)


def post_install_sim(repo_dir):
    import shutil
    from distutils.sysconfig import get_python_lib

    with Path(repo_dir):
        sirc_platform_dir = Path(repo_dir) / r'sirc_platform'
        sirc_platform_dir.mkdir(parents=True, exist_ok=True)

        print("Copying ImageWriter.dll")
        try:
            shutil.copyfile(r'\\netapp\joint\Kfir\Compilers\Python37-64bit\libs\ImageWriter.dll',
                            Path(repo_dir) / r'stream\64_ARCH\ImageWriter.dll')
            print("Finished copying ImageWriter.dll")
        except Exception as e:
            print(
                'Error when trying to copy ImageWriter.dll, trying to delete current file and copy again. Exception: ' + str(
                    e))
            try:
                if not os.path.isdir(Path(repo_dir) / r'stream\64_ARCH'):
                    os.makedirs(Path(repo_dir) / r'stream\64_ARCH')
                    print('Created directory: ' + str(Path(repo_dir) / r'stream\64_ARCH'))
                else:
                    os.remove(Path(repo_dir) / r'\stream\64_ARCH\ImageWriter.dll')
                    print('Deleted ImageWriter from path: ' + Path(r'\stream\64_ARCH\ImageWriter.dll').absolute())
                shutil.copyfile(r"\\netapp\joint\Kfir\Compilers\Python37-64bit\libs\ImageWriter.dll",
                                 Path(repo_dir) / r'stream\64_ARCH\ImageWriter.dll')
                print("Finished copying ImageWriter.dll")
            except Exception as e2:
                print('Failed to copy ImageWriter for the second time. Exception: ' + str(e2))

        print("Copying SimpleISP")
        shutil.copyfile(r"\\netapp\joint\Kfir\Compilers\Python37-64bit\libs\SimpleISP.dll",
                        Path(repo_dir) / r'stream\SimpleISP.dll')
        shutil.copyfile(r"\\netapp\joint\Kfir\Compilers\Python37-64bit\libs\SimpleISPRunner.exe",
                        Path(repo_dir) / r'stream\SimpleISPRunner.exe')
        print("Finished copying SimpleISPRunner")

        if not os.path.exists(Path(repo_dir) / r'sirc_platform\sirc_streamer_tcp_ports_file.txt'):
            print("Copying sirc_streamer_tcp_ports_file.txt")
            shutil.copyfile(r"\\netapp\joint\Kfir\Compilers\sirc_streamer_tcp_ports_file.txt",
                            Path(repo_dir) / r'sirc_platform\sirc_streamer_tcp_ports_file.txt')
            print("Finished copying sirc_streamer_tcp_ports_file.txt")
        else:
            print("sirc_streamer_tcp_ports_file.txt already exists, skipping copy.")

        print("Running install_sim")
        install_file = str(Path(repo_dir) / r'sim\install_sim.py')
        os.system("python " + install_file + ' install')
        print("Finished Running install_sim")

        if not os.path.exists(Path(repo_dir) / r'sim\sip.pyd'):
            print("Copying sip.pyd")
            shutil.copyfile(r"\\netapp\joint\Kfir\Compilers\Python37-64bit\Lib\site-packages\sip.pyd", Path(repo_dir) / r'sip.pyd')
            print("Finished copying sip.pyd")
        else:
            print("sip.pyd already exists, skipping copy.")


def program_esp32(wd):
    import sys
    import glob
    import serial

    def serial_ports():
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    from artifactory import ArtifactoryPath
    #get files from artifactory to espfw
    from artifactory import ArtifactoryPath
    path = ArtifactoryPath(
        "http://artifactory:8081/artifactory/SircApplicationMain/ImageInjectTools/build_output/")

    # create esp32 dir
    espfw_dir = str(Path(wd) / 'espfw')
    Path(espfw_dir).mkdir(parents=True, exist_ok=True)

    # create filw for every artifact
    for file in path:
        with file.open() as fd:
            with open( Path(espfw_dir)/file.name, "wb") as out:
                out.write(fd.read())
                print(f'{file.name} was copied to {espfw_dir}')

    #find available com
    serial_ports = serial_ports()

    print(f'available serial ports: {serial_ports}')

    for serial_port in serial_ports:
        try:
            # program flash
            program_cmd = f'python {espfw_dir}/esptool.py -p {serial_port} -b 460800 --after hard_reset write_flash --flash_mode dio --flash_size detect \
--flash_freq 40m 0x1000 {espfw_dir}/bootloader.bin 0x8000 {espfw_dir}/partition-table.bin 0x10000 {espfw_dir}/spi-and-eth.bin'
            print(f'Program ESP32 wait...')
            os.system(program_cmd)
            print(f'Success program esp32 with {serial_port}')
        except:
            print(f'failed to program esp32 with com: {serial_port} cmd: {program_cmd}')


if __name__ == '__main__':
    args = parse_arguments()

    wd = Path(args.wd)
    python = 'python'

    #if virtual env create one else use default python
    if args.venv_dir:
        #create dir
        Path(args.venv_dir).mkdir(parents=True, exist_ok=True)
        # create and activate the virtual environment
        venv_root_dir = str(Path(args.venv_dir).parent)
        env_name = str(Path(args.venv_dir).stem)

        # change WD
        os.chdir(Path(venv_root_dir))
        subprocess.call(f'virtualenv {env_name}')

        python = str(Path(args.venv_dir) / 'Scripts/python.exe')
        print(python)


    #create projects/sim dir
    (wd / 'Projects\sim\working').mkdir(parents=True, exist_ok=True)

    if not args.only_fetch:
        upgrade_pip(python)

        upgrade_setuptools(python)

        upgrade_requests(python)

    update_repos(args.config_file, python,wd, args.only_fetch)






