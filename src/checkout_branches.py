from .folder_info import *
from .utils import *

import subprocess
import json
import svn.local
from svn.exception import SvnException

skips_list: list[str] = []


def checkout_branch(path: str, svn_path: str):
    print_out(f"Checkout {path} as {svn_path}...")#, end="\r")
    os.makedirs(path, exist_ok=True)
    process = subprocess.Popen([f'cd "C:/Program Files/TortoiseSVN/bin"', '&&', 'svn', 'checkout', f"{svn_path}", f"{path}"], shell=True)
    # process = subprocess.Popen([f'svn update C:/home/xxLibs'], shell=True)
    process.wait()
    return
    local_client = svn.local.LocalClient(path)

    try:
        info = local_client.info()
    except SvnException:
        print_out(f"Failed to checkout {path}")
        return
    print_out(f"Checkout {path} successful")


def checkout_svn_branches(folders_info_path):
    data = json.load(open(f"{folders_info_path}/branches.jrvs", 'r'))

    folders_info = parse_folders_info(data)

    folder: FolderInfo
    for folder in folders_info:
        folder_path = replace_slashes(f"{folders_info_path}/{folder.folder_path}")
        try:
            svn.local.LocalClient(folder_path).info()
        except SvnException:
            pass
        except EnvironmentError:
            pass
        else:
            continue

        global skips_list

        for skip in folder.skips:
            skips_list.append(replace_slashes(f"{folder_path}/{skip}"))
        checkout_branch(folder_path, folder.svn_main_path)

    print_out("Checkout ended")
