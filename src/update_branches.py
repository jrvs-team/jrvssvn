from .folder_info import *
from .utils import *

import json
import svn.local
from svn.exception import SvnException

skips_list: list[str] = []


def update_branch(path: str, svn_path: str):
    local_client = svn.local.LocalClient(path)

    try:
        print_out(f"Updating {path} as {local_client.info()['relative_url']}...", end="\r")
        info = local_client.update()

    except SvnException:
        print_out(f"Unable to update {path}")
        return

    print_out(f"Updated  {path}")


def update_svn_branches(folders_info_path):
    data = json.load(open(f"{folders_info_path}/branches.jrvs", 'r'))

    folders_info = parse_folders_info(data)

    folder: FolderInfo
    for folder in folders_info:
        folder_path = replace_slashes(f"{folders_info_path}/{folder.folder_path}")
        if not check_if_folder_exists(folder_path):
            continue

        global skips_list

        for skip in folder.skips:
            skips_list.append(replace_slashes(f"{folder_path}/{skip}"))
        update_branch(folder_path, folder.svn_main_path)
