# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    docs/config.py: Docs config

    Copyright (C) 2020-2021 Sebastian M. Ernst <ernst@pleiszenburg.de>

<LICENSE_BLOCK>
The contents of this file are subject to the GNU Lesser General Public License
Version 2.1 ("LGPL" or "License"). You may not use this file except in
compliance with the License. You may obtain a copy of the License at
https://www.gnu.org/licenses/old-licenses/lgpl-2.1.txt
https://github.com/pleiszenburg/bewegung/blob/master/LICENSE

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for the
specific language governing rights and limitations under the License.
</LICENSE_BLOCK>

"""

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys

# sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from docs.version import get_version


# -- Project information -----------------------------------------------------

project = 'bewegung'
author = 'Sebastian M. Ernst'
copyright = f'2020-2022 {author:s}'

# The full version, including alpha/beta/rc tags
release = get_version()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_rtd_theme',
    'sphinxembeddedvideos.youtube', # https://github.com/sphinx-contrib/youtube/issues/9#issuecomment-734295832
    'myst_parser',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Values to pass into the template engine's context for all pages.
html_context = {
    'sidebar_external_links_caption': 'Links',
    'sidebar_external_links': [
        # ('<i class="fa fa-rss fa-fw"></i> Blog', 'https://www.000'),
        ('<i class="fa fa-github fa-fw"></i> Source Code', 'https://github.com/pleiszenburg/bewegung'),
        ('<i class="fa fa-bug fa-fw"></i> Issue Tracker', 'https://github.com/pleiszenburg/bewegung/issues'),
        ('<i class="fa fa-envelope fa-fw"></i> Mailing List', 'https://groups.io/g/bewegung-dev'),
        ('<i class="fa fa-comments fa-fw"></i> Chat', 'https://matrix.to/#/#bewegung:matrix.org'),
        # ('<i class="fa fa-file-text fa-fw"></i> Citation', 'https://doi.org/000'),
        ('<i class="fa fa-info-circle fa-fw"></i> pleiszenburg.de', 'http://www.pleiszenburg.de/'),
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

always_document_param_types = True # sphinx_autodoc_typehints

napoleon_include_special_with_doc = True # napoleon
# napoleon_use_param = True
# napoleon_type_aliases = True
