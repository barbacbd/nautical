#!/bin/bash

#----------------------------------------------
# This script is meant to execute from the home
# directory of the project. It will establish
# a python virtual environment, run the
# Static Code Analysis for the project and 
# teardown the virtual environment.
#----------------------------------------------

# Exit if python 3 is not python3.6 or greater
pyv=$(python3 -c 'import sys; print("{}.{}".format(sys.version_info.major, sys.version_info.minor))')

if [[ "$pyv" < "3.6" ]]; then
    echo "";
    echo "No python version > 3.6 found.";
    echo "If you believe that your python version meets the requirements, then";
    echo "please set an alias for python3 to python.";
    echo "";
    exit;
fi

# determine if we created the virtual environment or someone else did
[ -d "venv" ] && created=0 ||  created=1 
if [ -d "venv" ]; then
    echo "virtual environment detected. Initializing ..."
    echo "";
else
    python3 -m venv venv
fi

# activate the virtual environment
source venv/bin/activate;

# install the python package
pip install . --upgrade;

# install the python requirements for testing.
pip install -r tests/requirements.txt;

[ -f ".pylintrc" ] && created_pylintrc=0 ||  created_pylintrc=1 
if [ ! -f ".pylintrc" ]; then
    echo "Pulling pylintrc file ...";
    wget https://raw.githubusercontent.com/barbacbd/tools/main/lint/python/.pylintrc;
fi

# Run the linter over this code base
pylint nautical/* --rcfile=.pylintrc

if [[ $created_pylintrc == 1 ]]; then
    echo "Removing the pylintrc file ...";
    rm -rf .pylintrc;
fi

# deactivate the venv
deactivate;

# if the virtual environment was created by us, remove it
if [[ $created == 1 ]]; then
    echo "Removing venv ...";
    rm -rf venv
fi




