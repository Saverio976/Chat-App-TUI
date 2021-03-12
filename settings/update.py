import os
import sys
import requests
from shutil import unpack_archive

def update():
    """
    goal :
        update all file
    arg : no
    return : no
    """
    repository_download = "https://api.github.com/repos/Saverio976/Chat-App-TUI/zipball/main"
    name = "Chat-App-TUI-main.zip"
    r = requests.get(repository_download, stream=True)
    with open(name, "wb") as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    unpack_archive(name, "..", "zip")

    print("Up To Date")
    sys.exit()

if __name__ == "__main__":
    update()
