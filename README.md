# BEWEGUNG

## SYNOPSIS

[`bewegung`](https://dict.leo.org/englisch-deutsch/bewegung) is a versatile video renderer, primarily targeting scientific visualizations of large quantities of data. Its core concepts are *sequences* and *layers*. Sequences describe a certain time span within a video and can overlap. Each sequence can hold multiple layers. Layers can be generated with [`cairo`](https://cairographics.org/), [`Pillow`](https://pillow.readthedocs.io), [`datashader`](https://datashader.org/) and `bewegung`'s internal drawing system [`DrawingBoard`](https://github.com/pleiszenburg/bewegung/blob/master/src/bewegung/core/drawingboard.py). Final compositing of every video frame and video effects are implemented via `Pillow`. `bewegung` also includes a simple [vector algebra system](https://github.com/pleiszenburg/bewegung/tree/master/src/bewegung/core/vector) and a ["camera" for 3D to 2D projections](https://github.com/pleiszenburg/bewegung/blob/master/src/bewegung/core/camera.py). `bewegung` is developed with ease of use, compute time and memory efficiency in mind.

## INSTALLATION

The prerequisites of [PyQObject](https://pygobject.readthedocs.io/en/latest/getting_started.html) have to be fulfilled. In addition, [Pango](https://pango.gnome.org/), its headers (development package) and [ffmpeg](https://ffmpeg.org/download.html) must be installed. Once all prerequisites are met, `bewegung` can be installed with Python's package manager `pip`:

```bash
pip install -vU git+https://github.com/pleiszenburg/bewegung.git@master
```

In principle, `bewegung` works across all modern operating systems. In terms of memory usage and performance, it behaves best on Unix-like systems due to [Windows's lack of "fork"](https://stackoverflow.com/q/985281/1672565).

## EXAMPLE

See [`demo.py`](https://github.com/pleiszenburg/bewegung/blob/master/demo.py).

## USAGE

The API is not stable yet. It will remain subject to changes until the project is labeled "beta" or better.
