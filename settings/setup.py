"""
file to setup first installation of required package
"""
import sys
import subprocess

if int(sys.version[0]) != 3:
    print("you run on python 2\nWe need python 3")
    sys.exit("Need Python 3")

python_exec = sys.executable

def setup():
    """
    goal :
        initialize the first installation of all dependencies
    arg : no
    return : no
    """
    pip_upgrade = ("-m", "pip", "install", "--upgrade", "pip")

    install_library = ["-m", "pip", "install", "-r", "assets/requirements/"]
    if sys.platform == "windows":
        install_library[-1] += "win.txt"
    else:
        install_library[-1] += "lin.txt"

    if int(sys.version[2]) >= 4:
        subprocess.run([python_exec, *pip_upgrade], stdout=subprocess.PIPE)
        subprocess.run([python_exec, *install_library], stdout=subprocess.PIPE)
    else:
        subprocess.call(python_exec, *pip_upgrade, stdout=subprocess.PIPE)
        subprocess.call(python_exec, *install_library, stdout=subprocess.PIPE)

    print("Setup Pass Well")
    sys.exit()

if __name__ == "__main__":
    setup()