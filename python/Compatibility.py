
import winreg
from os.path import exists
from os import mkdir

import logging

from python.global_variables import global_variables as gv



def get_software_list(hive, flag):
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                        0, winreg.KEY_READ | flag)
    count_subkey = winreg.QueryInfoKey(aKey)[0]
    software_list = []
    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]
            try:
                software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            software_list.append(software)
        except EnvironmentError:
            continue
    return software_list


def check_program_is_loaded(program_name):
    software_list = get_software_list(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + get_software_list(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + get_software_list(winreg.HKEY_CURRENT_USER, 0)
    for software in software_list:
        if software['name'] == program_name:
            # print(f"{software['name']} is loaded, version: {software['version']}")
            logging.info(f"{software['name']} is loaded, version: {software['version']}")
            name = software['name']
            program_version = software['version']
            publisher = software['publisher']
            return (name, program_version, publisher)
    logging.fatal(f"{program_name} is not loaded")
    return (None,None,None)


def check_folder():
    for folder in gv.FOLDER_NAME:
        if not exists(folder):
            mkdir(folder)




