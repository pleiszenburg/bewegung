![bewegung_logo](https://github.com/pleiszenburg/bewegung/blob/master/docs/_static/logo01.png?raw=true "bewegung logo")

# BEWEGUNG

*/bəˈveːɡʊŋ/ ([German, noun, feminine: motion/movement/animation](https://dict.leo.org/englisch-deutsch/bewegung))*

[![docs_master](https://readthedocs.org/projects/bewegung/badge/?version=latest&style=flat-square "Documentation Status: master / release")](https://bewegung.readthedocs.io/en/latest/)
[![license](https://img.shields.io/pypi/l/bewegung.svg?style=flat-square "LGPL 2.1")](https://github.com/pleiszenburg/bewegung/blob/master/LICENSE)
[![status](https://img.shields.io/pypi/status/bewegung.svg?style=flat-square "Project Development Status")](https://github.com/pleiszenburg/bewegung/issues)
[![pypi_version](https://img.shields.io/pypi/v/bewegung.svg?style=flat-square "pypi version")](https://pypi.python.org/pypi/bewegung)
[![conda_version](https://img.shields.io/conda/vn/conda-forge/bewegung.svg?style=flat-square "conda version")](https://anaconda.org/conda-forge/bewegung)
[![pypi_versions](https://img.shields.io/pypi/pyversions/bewegung.svg?style=flat-square "Available on PyPi - the Python Package Index")](https://pypi.python.org/pypi/bewegung)
[![chat](https://img.shields.io/matrix/bewegung:matrix.org.svg?style=flat-square "Matrix Chat Room")](https://matrix.to/#/#bewegung:matrix.org)
[![mailing_list](https://img.shields.io/badge/mailing%20list-groups.io-8cbcd1.svg?style=flat-square "Mailing List")](https://groups.io/g/bewegung-dev)

## Synopsis

`bewegung` is a versatile video renderer, primarily targeting scientific visualizations of large quantities of data. Its core concepts are *sequences* and *layers*. Sequences describe a certain time span within a video and can overlap. Each sequence can hold multiple layers. Layers can be generated with [`cairo`](https://cairographics.org/), [`Pillow`](https://pillow.readthedocs.io), [`datashader`](https://datashader.org/), [`matplotlib`](https://matplotlib.org/) and `bewegung`'s internal drawing system [`DrawingBoard`](https://bewegung.readthedocs.io/en/latest/canvas.html). Final compositing of every video frame and video effects are implemented via `Pillow`. Video encoding is handled by `ffmpeg`. `bewegung` also includes a simple [vector algebra system](https://bewegung.readthedocs.io/en/latest/vectors.html) and a ["camera" for 3D to 2D projections](https://bewegung.readthedocs.io/en/latest/camera.html). `bewegung` is developed with ease of use, compute time and memory efficiency in mind.

## Installation

`bewegung` can be installed both via ``conda`` and via ``pip``.

### Via `conda`

An almost complete installation can be triggered by running:

```bash
conda install -c conda-forge bewegung
```

Please note that [mplcairo](https://github.com/matplotlib/mplcairo), a dependency of `bewegung` and alternative backend for `matplotlib`, is currently not available via `conda` and must be installed manually. `bewegung` [does also work without `mplcairo` present](https://bewegung.readthedocs.io/en/latest/canvas.html#acceleratingmatplotlib) and falls back to the `cairo` backend of `matplotlib`.

### Via `pip`

A bare **minimum** of `bewegung` can be installed with Python's package manager `pip`:

```bash
pip install -vU bewegung
```

A **complete** installation of all optional Python components and development tools can be triggered by running:

```bash
pip install -vU bewegung[all]
```

Certain non-Python **prerequisites** must installed separately and before invoking the above command. [For detailed instructions, see documentation](https://bewegung.readthedocs.io/en/latest/installation.html). Most notably, `ffmpeg` should be installed for producing actual video files instead of video frames as individual files. See [download section](https://ffmpeg.org/download.html) of the `ffmpeg` project website for further instructions.

## Example

See [`demo.py`](https://github.com/pleiszenburg/bewegung/blob/master/demo/demo.py).

You can directly test it by running:

```bash
curl https://raw.githubusercontent.com/pleiszenburg/bewegung/master/demo/demo.py | python3
```

This resulting `video.mp4` file should look like this:

[![bewegung standard demo](https://img.youtube.com/vi/4NFXQ73weMA/sddefault.jpg)](https://www.youtube.com/watch?v=4NFXQ73weMA)

## Usage

See [documentation](https://bewegung.readthedocs.io).

`bewegung`'s development status is "well-tested alpha". Its API should not be considered stable until the project is labeled "beta" or better.

`bewegung` can be drastically accelerated by deactivating debugging features. See [relevant section in the documentation](https://bewegung.readthedocs.io/en/latest/performance.html#typecheckingperformance).
