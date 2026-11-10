"""Sizes and orientations.

The same content on A0, A1 and A2 paper, in portrait and in landscape. The font size is the
same on every paper, so a smaller poster holds less: plan the content for the size the
conference asks for.
"""

from pathlib import Path

import matplotlib.pyplot as plt

from plasma_posters import Poster, preview

HERE = Path(__file__).resolve().parent

TEXT = r"""
The plasma frequency $\omega_p = \sqrt{n e^2 / \varepsilon_0 m_e}$ sets the time scale and the
Debye length $\lambda_D = \sqrt{\varepsilon_0 k_B T / n e^2}$ the length scale of a plasma.
"""

layouts = [
    ("a0", "portrait"),
    ("a1", "portrait"),
    ("a2", "portrait"),
    ("a0", "landscape"),
    ("a1", "landscape"),
    ("a2", "landscape"),
]
fig, axes = plt.subplots(2, 3, figsize=(10, 8))
for ax, (size, orientation) in zip(axes.flat, layouts, strict=True):
    poster = Poster(
        f"{size.upper()} {orientation}",
        authors="Max Lindqvist",
        size=size,
        orientation=orientation,
        columns=2,
    )
    for column in (0, 1):
        poster.block("Scales", TEXT, column=column)
        poster.block("More scales", TEXT, column=column)
    pdf = poster.build(HERE / f"poster_{size}_{orientation}.pdf")
    ax.imshow(plt.imread(preview(pdf, dpi=20)))
    ax.set_title(f"{size.upper()}, {orientation}")
    ax.set_axis_off()
