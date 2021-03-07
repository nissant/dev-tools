import datetime
import os
import shutil

GOOGLE_DRIVE_DIRECTORY = 'C:\\Users\\Jeff\\Google Drive\\Manifest_Destiny'
MAIN_BACKUP_DIRECTORY = 'C:\\Users\\Jeff\\Desktop\\Manifest_Destiny_Backups\\md_backup_{0}'
EXTERNAL_DRIVE_DIRECTORY = 'F:\\My Files\\Manifest_Destiny_Backups\\md_backup_{0}'


def get_backup_directory(base_directory):
    date = str(datetime.datetime.now())[:16]
    date = date.replace(' ', '_').replace(':', '')
    return base_directory.format(date)


def copy_files(directory):
    for file in os.listdir(GOOGLE_DRIVE_DIRECTORY):
        file_path = os.path.join(GOOGLE_DRIVE_DIRECTORY, file)
        if os.path.isfile(file_path):
            shutil.copy(file_path, directory)


def perform_backup(base_directory):
    backup_directory = get_backup_directory(base_directory)
    os.makedirs(backup_directory)
    copy_files(backup_directory)


def main():
    perform_backup(MAIN_BACKUP_DIRECTORY)
    perform_backup(EXTERNAL_DRIVE_DIRECTORY)


if __name__ == '__main__':
    main()

