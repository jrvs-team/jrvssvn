import os


def replace_slashes(path: str) -> str:
    path = path.replace("//", "/")
    path = path.replace("\\", "/")
    if path[-1] == "/":
        return path[:-1]
    return path


# __output_source = curses.initscr()
# __output_source.encoding = "utf_8"
__output_last_line: int = int(0)
__output_last_line_length: int = int(0)


def print_out(line: str = "", position: tuple[int, int] = (-1, -1), end: str = "\n"):
    global __output_last_line_length

    if len(line) > 0:
        print(" "*__output_last_line_length, end="\r")
    print(line, end=end)
    # print(f"\033[K{line}", end=end)

    __output_last_line_length = len(line)
    if end != "\r":
        __output_last_line_length = 0


def check_if_folder_exists(path: str) -> bool:
    return os.path.exists(path)
