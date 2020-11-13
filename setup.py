# -*- coding: utf-8 -*-

"""

BEWEGUNG
a versatile video renderer
https://github.com/pleiszenburg/bewegung

    setup.py: Used for package distribution

    Copyright (C) 2020 Sebastian M. Ernst <ernst@pleiszenburg.de>

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


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORT
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from setuptools import (
    find_packages,
    setup,
)
import ast
import os

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# SETUP
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# List all versions of Python which are supported
python_minor_min = 6
python_minor_max = 8
confirmed_python_versions = [
    "Programming Language :: Python :: 3.{MINOR:d}".format(MINOR=minor)
    for minor in range(python_minor_min, python_minor_max + 1)
]

# Fetch readme file
with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

# Define source directory (path)
SRC_DIR = "src"

# Version
def get_version(code):
    tree = ast.parse(code)
    for item in tree.body:
        if not isinstance(item, ast.Assign):
            continue
        if len(item.targets) != 1:
            continue
        if item.targets[0].id != "__version__":
            continue
        return item.value.s


with open(os.path.join(SRC_DIR, "bewegung", "__init__.py"), "r", encoding="utf-8") as f:
    __version__ = get_version(f.read())

# Requirements
extras_require = {
    "dev": [
        "black",
        "python-language-server[all]",
        "psutil",
        "setuptools",
        "Sphinx",
        "sphinx-rtd-theme",
        "twine",
        "wheel",
    ],
}
extras_require["all"] = list(
    {rq for target in extras_require.keys() for rq in extras_require[target]}
)

# Install package
setup(
    name="bewegung",
    packages=find_packages(SRC_DIR),
    package_dir={"": SRC_DIR},
    version=__version__,
    description="a versatile video renderer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sebastian M. Ernst",
    author_email="ernst@pleiszenburg.de",
    url="https://github.com/pleiszenburg/bewegung",
    download_url="https://github.com/pleiszenburg/bewegung/archive/v%s.tar.gz"
    % __version__,
    license="LGPLv2",
    keywords=[
        "video",
        "animation",
        "animation-framework",
        "rendering",
        "rendering",
        "rendering-engine",
        "compositor",
    ],
    scripts=[],
    include_package_data=True,
    python_requires=">=3.{MINOR:d}".format(MINOR=python_minor_min),
    setup_requires=[],
    install_requires=[
        "datashader",
        "ipython",
        "numba",
        "numpy",
        "pycairo",
        "Pillow",
        "PyGObject",
        "tqdm",
        "typeguard",
        ],
    extras_require=extras_require,
    zip_safe=False,
    entry_points={},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ]
    + confirmed_python_versions
    + [
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Artistic Software",
        "Topic :: Education",
        "Topic :: Multimedia",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Presentation",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Sound/Audio :: Editors",
        "Topic :: Multimedia :: Sound/Audio :: Mixers",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries",
    ],
)
