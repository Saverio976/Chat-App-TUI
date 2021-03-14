"""
file to update the directory (download from github)
"""
import sys
import requests
from shutil import unpack_archive, rmtree

def update():
    """
    goal :
        update all file
    arg : no
    return : no
    """
    repository_download = "https://github.com/Saverio976/Chat-App-TUI/archive/main.zip"
    name = "../Chat-App-TUI-main.zip"
    r = requests.get(repository_download, stream=True)
    with open(name, "wb") as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    try:
        rmtree("../Chat-App-TUI-main", ignore_errors=True)
    except:
        pass
    unpack_archive(name, "..", "zip")
    try:
        rmtree(name, ignore_errors=True)
    except:
        pass
    print("Up To Date")
    sys.exit()

if __name__ == "__main__":
    update()
