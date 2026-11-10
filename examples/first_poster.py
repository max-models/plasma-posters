"""First poster.

A two-column A0 poster with an equation and a Matplotlib figure: the smallest complete poster.
The script writes ``first_poster.tex`` and ``first_poster.pdf`` next to itself and shows the
poster below the source.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plasma_posters import Poster, preview

HERE = Path(__file__).resolve().parent

# the figure: a Maxwellian at three temperatures
v = np.linspace(0, 4, 300)
fig, ax = plt.subplots(figsize=(6, 3.5))
for temperature in (0.5, 1.0, 2.0):
    f = v**2 * np.exp(-(v**2) / temperature) / temperature**1.5
    ax.plot(v, f / f.max(), label=f"T = {temperature}")
ax.set(xlabel="speed v", ylabel="f(v) / max f")
ax.legend()
fig.savefig(HERE / "maxwellian.pdf", bbox_inches="tight")
plt.close(fig)

poster = Poster(
    "Speeds in a thermal plasma",
    authors="Max Lindqvist",
    institute="Max Planck Institute for Plasma Physics",
    columns=2,
)
poster.block(
    "The distribution",
    r"""
    The speeds of particles of mass $m$ in a plasma at temperature $T$ follow
    \[
      f(v) \propto v^2 \exp\left(-\frac{m v^2}{2 k_B T}\right).
    \]
    Hotter plasmas have faster and more spread-out particles.
    """,
)
poster.figure(
    "Three temperatures",
    "maxwellian.pdf",
    caption="The distribution, normalised to its peak.",
    column=1,
)
pdf = poster.build(HERE / "first_poster.pdf")

# the poster, as the docs show it
fig, ax = plt.subplots(figsize=(6, 8.5))
ax.imshow(plt.imread(preview(pdf)))
ax.set_axis_off()
