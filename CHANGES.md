# Changes

## 0.0.6 (2021-XX-XX)

- FEATURE: All vector and vector array classes expose `ndim`, number of dimensions.
- FEATURE: Common base class, `VectorABC`, for all vector classes.
- FEATURE: Common base class, `VectorArrayABC`, for all vector array classes.
- FEATURE: Vector arrays are iterators.
- FEATURE: The `Color` class, using RGBA internally, can now import HSV values.
- FEATURE: Added equality check, "is close" check, tuple export and copy to `Matrix`.
- FEATURE: New dedicated sub-module for core animation engine named `bewegung.animation`.
- FEATURE: New dedicated sub-module for `DrawingBoard` named `bewegung.drawingboard`, now allowing direct import.
- FEATURE: New dedicated sub-module for linear algebra named `bewegung.lingalg`.
- FEATURE: Cleanup of internal type hierarchy.
- FIX: Development dependency switched from unmaintained `python-language-server` to `python-lsp-server`.
- FIX: Imports in `contrib` were broken.
- FIX: `test` target in `makefile` was broken.
- FIX: `typeguard` was not really an optional dependency.

## 0.0.5 (2021-07-30)

- FEATURE: Python 3.9 support.
- FEATURE: Added `draw_bezier` method to `DrawgingBoard`.
- FEATURE: `Matrix` can rotate vector arrays.
- FEATURE: Added operations (add, subtract) between vectors and vector arrays.
- FEATURE: Vectors and vector arrays expose angles.
- FEATURE: Matrix chat room for support.
- FEATURE: Groups.io mailing list for support.
- FIX: Some text anchors would fail with activated type checking.
- DOCS: Added project logo.
- DOCS: Small corrections in various places.

## 0.0.4 (2020-12-14)

- FIX: Center offset in `DrawgingBoard` cares about subpixels.
- FIX: `bewegung` would fail to work at all without `numpy` present.
- DOCS: Completed vector chapters on algebra and camera as well as cross-references to classes and methods.

## 0.0.3 (2020-12-06)

- FEATURE: `DrawingBoard.make_svg` can generate SVG object handles from raw binary data.
- FEATURE: Demos are self-contained.
- FIX: `DrawingBoard.draw_svg` can draw raw SVG data without crashing.
- DOCS: Prerequisites when installing via `pip`

## 0.0.2 (2020-12-05)

- FEATURE: `mplcairo` becomes an optional dependency. The `matplotlib` backend can fall back to its own `cairo` backend while also showing a warning.
- DOCS: Package installation via `conda`

## 0.0.1 (2020-12-02)

- Initial release.
