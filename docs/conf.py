# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../'))
import subprocess
from datetime import datetime

# -- Project information -----------------------------------------------------

project = 'nautical'
author = 'Brent Barbachem'
copyright = f'{datetime.now().year}, {author}'

'''This section will grab the installed version of the project
installed on PIP. using a similar method to:
pip3 show nautical| grep \'Version\' | awk \'{print $2}\''
'''
command = f'pip3 show {project}'
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

if error is not	None:
    raise RuntimeError("Failed to run pip and generate output")

release = None
output = output.decode('utf-8').split("\n")
for line in output:
    if line.startswith('Version'):
        release = str(line.split()[1])

if release is None:
    raise ValueError("Failed to find a version")


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.githubpages',
    'sphinx.ext.ifconfig',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',]

# Set values for Napoleon
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['venv', '__pycache__']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
