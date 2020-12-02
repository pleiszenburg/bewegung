# BEWEGUNG

## Synopsis

[`bewegung`](https://dict.leo.org/englisch-deutsch/bewegung) is a versatile video renderer, primarily targeting scientific visualizations of large quantities of data. Its core concepts are *sequences* and *layers*. Sequences describe a certain time span within a video and can overlap. Each sequence can hold multiple layers. Layers can be generated with [`cairo`](https://cairographics.org/), [`Pillow`](https://pillow.readthedocs.io), [`datashader`](https://datashader.org/), [`matplotlib`](https://matplotlib.org/) and `bewegung`'s internal drawing system [`DrawingBoard`](https://bewegung.readthedocs.io/en/latest/canvas.html). Final compositing of every video frame and video effects are implemented via `Pillow`. Video encoding is handled by `ffmpeg`. `bewegung` also includes a simple [vector algebra system](https://bewegung.readthedocs.io/en/latest/vectors.html) and a ["camera" for 3D to 2D projections](https://bewegung.readthedocs.io/en/latest/camera.html). `bewegung` is developed with ease of use, compute time and memory efficiency in mind.

## Installation

A bare minimum of `bewegung` can be installed with Python's package manager `pip`:

```bash
pip install -vU bewegung
```

A complete installation of all optional Python components and development tools can be triggered by running:

```bash
pip install -vU bewegung[all]
```

Certain non-Python components must installed separately and before invoking the above command. [For detailed instructions, see documentation](https://bewegung.readthedocs.io/en/latest/installation.html). Most notably, `ffmpeg` should be installed for producing actual video files instead of video frames as individual files. See [download section](https://ffmpeg.org/download.html) of the `ffmpeg` project website for further instructions.

## Example

See [`demo.py`](https://github.com/pleiszenburg/bewegung/blob/master/demo/demo.py).

## Usage

See [documentation](https://bewegung.readthedocs.io) (work in progress).

`bewegung`'s development status is "well-tested alpha". Its API should not be considered stable until the project is labeled "beta" or better, although significant changes are very unlikely.

`bewegung` can be drastically accelerated by deactivating debugging features. See [relevant section in the documentation](https://bewegung.readthedocs.io/en/latest/debug.html).
