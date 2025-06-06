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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Galyleo'
copyright = '2021, engageLively'
author = 'Andreas Bergen, Mahdi Biazi, Tim Braman, Matthew Hemmings, Rick McGeer, Robin Schreiber'

# The full version, including alpha/beta/rc tags
release = '0.5'


# -- General configuration ---------------------------------------------------
import sphinx_rtd_theme


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.autodoc",
    "rst2pdf.pdfbuilder"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

import sys
# pull the galyleo client and set the root directory in the environment, e.g.
# export GALYLEO_CLIENT=/Users/rick/Projects/engageLively/el-galyleo-client
import os
# sys.path.append(os.environ["GALYLEO_CLIENT"])
sys.path.append('./source')

# Use engageLively orange

html_theme_options = {
    'style_nav_header_background': '#f87c04'
}

pdf_documents = [('index', 'index.pdf', 'Galyleo User Guide', 'Andreas Bergen, Mahdi Biazi, Matt Hemmings, Rick McGeer, Robin Schreiber')]

pdf_stylesheets = ['twocolumn']
