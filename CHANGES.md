# Changes

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
