from .utils import *


class FolderInfo:
    folder_path: str = ""
    svn_main_path: str = ""
    skips: list[str] = []


def parse_folders_info(data: list) -> list[FolderInfo]:
    folders = []
    for info in data:
        folder = FolderInfo()
        folder.folder_path = replace_slashes(info.get("folder_path", ""))
        folder.svn_main_path = replace_slashes(info.get("svn_main_path", ""))
        skips = info.get("skip", [])

        for skip in skips:
            folder.skips.append(replace_slashes(skip))
        folders.append(folder)

    return folders
