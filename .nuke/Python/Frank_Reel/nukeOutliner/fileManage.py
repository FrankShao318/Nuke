import os, re, shutil, json
import tkinter
from tkinter import filedialog


def module_path():
    """
    Return current module path folder.
    Returns:
        str: The current module path folder.
    """

    return os.path.abspath(os.path.dirname(__file__))


def folder_dialog(title):
    """
    Open file dialog and return the selected path.
    Args:
        title(str): Dialog name.
    Returns:
        str: The selected path folder.
    """

    root = tkinter.Tk()
    root.withdraw()
    return filedialog.askdirectory(title=title)


def create_folder(path, folder_name):
    """
    Create a new folder under the path.
    Args:
        path(str): Path where to create a new folder.
        folder_name(str): The new folder name.
    Returns:
        str: The newly created folder path.
    Raises:
        OSError: If creating the directory failed.
    """

    folder = '{}/{}'.format(path, folder_name)
    if not os.path.exists(folder):
        try:
            os.mkdir(folder)
        except OSError:
            print('Creation of the directory {} failed'.format(folder))

    print('Created the directory {}'.format(folder))
    return folder


def rename_file(path, old_name, new_name):
    """
    Rename a folder or file in the drive.
    Args:
        path(str): Path where the folder or file is.
        old_name(str): The old folder or file name.
        new_name(str): The new folder or file name.
    Returns:
        If the old folder or file does not exist.
    """

    old_path = '{}/{}'.format(path, old_name)
    if os.path.exists(old_path):
        new_path = '{}/{}'.format(path, new_name)
        os.rename(old_path, new_path)
    else:
        raise OSError('{} does not exist in {}'.format(old_name, path))


def get_sub_folders(path):
    """
    Return all the sub folders under the path.
    Args:
        path(str): Path where to return all the sub folders.
    Returns:
        list: All the sub folders under the path.
    """

    if not os.path.exists(path):
        return []
    return [folder for folder in os.listdir(path) if os.path.isdir('{}/{}'.format(path, folder))]


def check_file_exist(path, user_file):
    """
    Check if the file exists or not under the path.
    Args:
        path(str): Path where to check if the file exists or not.
        user_file(str): The file name.
    Returns:
        bool: True if the file exists or False if not.
    """

    return os.path.exists('{}/{}'.format(path, user_file))


def get_all_files(path, file_extension='', return_without_ext=True):
    """
    Return all the files / all the files with certain extension under the path.
    Args:
        path(str): Path where to return all the files.
        file_extension(str): File extension name, example: '.ma' / '.mb' / '.py'.
        return_without_ext(bool): Return file name with extension or not.
    Returns:
        list: Return all the files / all the files with certain extension under the path.
    """

    if not os.path.exists(path):
        return []

    all_files = [user_file for user_file in os.listdir(path) if os.path.isfile('{}/{}'.format())]

    # Return all the files with certain file extension.
    if file_extension:
        return_files = []
        for user_file in all_files:
            if os.path.splitext(user_file)[1] == file_extension:
                if return_without_ext:
                    return_files.append(str(user_file).rpartition(file_extension)[0])
                else:
                    return_files.append(user_file)
        return return_files

    # Return all the files.
    if return_without_ext:
        return [os.path.splitext(user_file)[0] for user_file in all_files]
    else:
        return all_files


def version_up(path, user_file):
    """
    Version up file.
    Args:
        path(str): Path where the file is.
        user_file(str): File which needs to be versioned up.
    Returns:
        None
    """

    if check_file_exist(path=path, user_file=user_file):
        old_folder = create_folder(path=path, folder_name='oldFiles')

        file_extension = os.path.splitext(user_file)[1]
        file_base_name = '{}_v'.format(str(user_file).rpartition(file_extension)[0])

        files_in_old_folder = get_all_files(path=old_folder, file_extension=file_extension, return_without_ext=True)
        if files_in_old_folder:
            latest_file_num = find_highest_trailing_number(names=files_in_old_folder, base_name=file_base_name)
        else:
            latest_file_num = 0

        current_file_name = '{}/{}'.format(path, user_file)
        versioned_file_name = '{}/{}{:03d}{}'.format(
            path, file_base_name, latest_file_num + 1, file_extension
        )
        shutil.copyfile(current_file_name, versioned_file_name)
        shutil.move(versioned_file_name, old_folder)


def find_highest_trailing_number(names, base_name):
    """
    Return the highest version number.
    Args:
        names(list): A list of versioned file names, example: ['base_name_v001', 'base_name_v002'].
        base_name(str): Base name of these versioned file names, example: 'base_name_v'.
    Returns:
        int: The highest version number.
    """

    highest_value = 0
    base_name_suffix_m = re.search(r'\d+$', base_name)
    if base_name_suffix_m:
        base_name_suffix = base_name_suffix_m.group()
        base_name = base_name.rpartition(base_name_suffix)[0]

    for name in names:
        if base_name in name:
            suffix = name.partition(base_name)[2]
            if suffix and re.match('^[0-9]*$', suffix):
                num = int(suffix)
                if num > highest_value:
                    highest_value = num

    return highest_value


def unique_name(names, name):
    """
    Create unique name.
    Args:
        names(list): A list of versioned file names, example: ['base_name_v001', 'base_name_v002'].
        name(str): Name to check if it is unique, if not, rename it.

    Returns:
        str: Unique name.
    """

    # Check if name exist, name can be '' empty string in the TreeView.
    if name:
        # Initial base name.
        base_name = name
        # Strip possible suffix number to get base name.
        name_suffix_m = re.search(r'/d+$', name)
        if name_suffix_m:
            name_suffix = name_suffix_m.group()
            base_name = name.rpartition(name_suffix)[0]

        if base_name in names:
            highest_num = find_highest_trailing_number(names=names, base_name=base_name)
            name = '{}/{}'.format(base_name, highest_num+1)

    return name


def contain_special_characters(str_name):
    """
    Check a string name has special characters or not.
    Args:
        str_name(str): String name to check if it has special characters.
    Returns:
        bool: Return True if has, False if not.
    """

    string_check = re.compile('[@!#$%^&*()<>?/\|}{~:]')

    if string_check.search(str_name):
        return True
    else:
        return False


def convert_special_characters_to_underscore(str_name):
    """
    Convert all the special characters in a string into underscore, including white space.
    Args:
        str_name(str): String name to convert all the special characters into underscore, including white space.
    Returns:
        str: The converted string name.
    """

    return re.sub(r'[^a-zA-Z0-9\n\.]', '_', str_name)


def export_file_info_as_json(path, user_file, data):
    """
    Export information data as json file.
    Args:
        path(str): Path where to save the json file.
        user_file(str): json file name.
        data(float/int/str/list/dict): The content to be exported as json file.
    Returns:
        None.
    """

    with open('{}/{}'.format(path, user_file), 'w') as json_file:
        json.dump(data, json_file, indent=2)


def read_file_info_from_json(path, user_file):
    """
    Read information data from json file.
    Args:
        path(str): Path where the json file is.
        user_file(str): json file name.
    Returns:
        float/int/str/list/dict/None: The data content queried from json file.
    """

    if check_file_exist(path=path, user_file=user_file):
        with open('{}/{}'.format(path, user_file), 'r') as json_file:
            data = json.load(json_file)

        return data

    return None


def write_file(path, user_file, data):
    """
    Write information data into user specific file.
    Args:
        path(str): Path where to save this file.
        user_file(str): User specific file name.
        data(str): The content to be exported into user specific file.
    Returns:
        None.
    """

    with open('{}/{}'.format(path, user_file), 'w') as f:
        f.write(data)


def read_file(path, user_file):
    """
    Read information data from file.
    Args:
        path:
        user_file:

    Returns:
        str: The content queried from user specific file.
    """

    if check_file_exist(path=path, user_file=user_file):
        with open('{}/{}'.format(path, user_file), 'r') as f:
            data = f.read()

        return data

    return None
































