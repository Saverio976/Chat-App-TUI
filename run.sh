#!/bin/bash

# look what is the python 3 command
if [[ `python --version 2>/dev/null` == *"Python 3"* ]]; then
        python_exec="python"
        echo "variable path : python"
elif [[ `py3 --version 2>/dev/null` == *"Python 3"* ]]; then
        python_exec="py3"
        echo "variable path : py3"
elif [[ `python3 --version 2>/dev/null` == *"Python 3"* ]]; then
        python_exec="python3"
        echo "variable path : python3"
else
    python_exec="0"
fi

if [[ $python_exec != "0" ]]; then
    echo "install all required library"
    $python_exec -m pip install --upgrade pip &>/dev/null
    $python_exec -m pip install -r assets/requirements/lin.txt --exists-action i &> /dev/null
    echo "chat app will start in few seconds"
    $python_exec main.py
    echo "good by"
else
    echo "did you have python ?"
fi