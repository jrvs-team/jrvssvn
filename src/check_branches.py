"""
Script to check if your SVN branches are different of what expected

© vrbszk
2023
"""

import os
import svn.local
from enum import Enum
import json

from svn.exception import SvnException
from .folder_info import *
from .utils import *


class SVNCheck(Enum):
    CheckAllFiles = 0
    CheckOnlyRootFolders = 1


check_encoding: bool = True
check_non_versioned: bool = True
mode: SVNCheck = SVNCheck.CheckAllFiles


folders_info: list[FolderInfo] = []
skips_list: list[str] = []


def check_svn_branch(path: str, expected_svn_path: str) -> None:
    path = replace_slashes(path)
    do_check_svn_branch(path, 0, "", expected_svn_path)


def do_check_svn_branch(path: str, index: int = 0, parent_path="", parent_svn_path: str = "") -> None:
    path = replace_slashes(path)
    if path in skips_list:
        print_out(f"skipping {path}...\r", end="")
        return

    print_out(f"processing file {path}...", end="\r")

    local_client = svn.local.LocalClient(path)
    parent_client = None
    if parent_path != "":
        parent_client = svn.local.LocalClient(parent_path)

    slash = path.rfind('/')
    backslash = path.rfind('\\')
    if slash < backslash:
        slash = backslash
    name = path[slash + 1:]

    tab = " " * slash

    try:
        info = local_client.info()

    except SvnException:
        print_out(f"{tab}{name:<40} non-versioned")
        return

    r_url = info["relative_url"]
    pr_url = ""
    if parent_client is not None:
        pr_url = parent_client.info()["relative_url"]

    if index == 0 or r_url != pr_url + "/" + name:
        print_out(f"{tab}{name:<40} {r_url}")

    if not os.path.isfile(path) and mode == SVNCheck.CheckAllFiles:
        check_all_files_in_branch(path, index)

    elif os.path.isfile(path) and check_encoding:
        if path[-4:] == ".cpp" or path[-2:] == ".h":
            do_check_encoding(path)


def do_check_encoding(path):
    print(f"checking encode {path}...", end="\r")
    file = open(path, 'r', encoding='utf-8')
    is_closed = False
    try:

        content = file.readlines()
        file.close()
        is_closed = True
        symbol_found = False
        for line in content:
            for symbol in line:
                if '\x80' < symbol < '\xff' and symbol != '°':
                    if not symbol_found:
                        print_out()
                    print_out(symbol, end="")
                    symbol_found = True
        if symbol_found:
            print_out()
            command = input("Symbol found. Press any key when ready to recheck or \"skip\" if you want to skip file...")
            if command != "skip":
                do_check_encoding(path)
    except UnicodeDecodeError:
        if not is_closed:
            file.close()
        print_out(f"Error at checking encoding for {path}")
        command = input("Press any key when ready to recheck or \"skip\" if you want to skip file...")
        if command != "skip":
            do_check_encoding(path)


def check_all_files_in_branch(path: str, index: int = 0) -> None:
    with os.scandir(path) as it:
        for entry in it:
            if not entry.name.startswith('.'):
                if entry.is_file():
                    do_check_svn_branch(entry.path, index + 1, path)
                else:
                    do_check_svn_branch(entry.path, index + 1, path)


def check_svn_branches(folders_info_path, check_all = True):
    global mode
    if check_all:
        mode = SVNCheck.CheckAllFiles
    else:
        mode = SVNCheck.CheckOnlyRootFolders
        
    data = json.load(open(f"{folders_info_path}/branches.jrvs", 'r'))
    global folders_info
    folders_info = parse_folders_info(data)

    folder: FolderInfo
    for folder in folders_info:
        folder_path = replace_slashes(f"{folders_info_path}/{folder.folder_path}")
        global skips_list

        for skip in folder.skips:
            skips_list.append(replace_slashes(f"{folder_path}/{skip}"))
        check_svn_branch(folder_path, folder.svn_main_path)
