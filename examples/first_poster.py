"""First poster.

A two-column A0 poster with an equation and a Matplotlib figure. The script writes
``first_poster.tex`` next to itself and compiles it to ``first_poster.pdf`` when lualatex is
installed; the figure on the poster appears below the source.
"""

import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plasma_posters import Poster

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

if shutil.which("lualatex"):
    print(f"wrote {poster.build(HERE / 'first_poster.pdf')}")
else:
    print(f"wrote {poster.save(HERE / 'first_poster.tex')} (no lualatex for the PDF)")
