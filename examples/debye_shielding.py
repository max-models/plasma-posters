"""Debye shielding.

A one-column A1 poster: a short story told top to bottom, with an equation, a figure and a
take-home message. The figure compares the Coulomb potential of a test charge with the
shielded Debye-Hückel potential.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plasma_posters import Poster, preview

HERE = Path(__file__).resolve().parent

r = np.linspace(0.05, 5, 400)  # in Debye lengths
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.plot(r, 1 / r, "--", color="gray", label="Coulomb")
ax.plot(r, np.exp(-r) / r, label="Debye-Hückel")
ax.set(xlabel=r"$r / \lambda_D$", ylabel=r"$\phi / \phi_0$", ylim=(0, 4))
ax.legend()
fig.savefig(HERE / "shielding.pdf", bbox_inches="tight")
plt.close(fig)

poster = Poster(
    "How a plasma hides a charge",
    authors="Max Lindqvist",
    institute="Max Planck Institute for Plasma Physics",
    size="a1",
    columns=1,
)
poster.block(
    "The question",
    r"""
    Put a test charge $q$ into a plasma. The electrons crowd around it and the ions move away,
    so how far does its field reach?
    """,
)
poster.block(
    "The answer",
    r"""
    Poisson's equation with Boltzmann electrons gives the Debye-Hückel potential
    \[
      \phi(r) = \frac{q}{4 \pi \varepsilon_0 r}\, e^{-r / \lambda_D},
    \]
    the Coulomb potential cut off at the Debye length $\lambda_D$.
    """,
)
poster.figure(
    "Shielded and bare",
    "shielding.pdf",
    caption="Beyond a few Debye lengths the charge is invisible.",
    width=0.7,
)
poster.block(
    "Take home",
    r"""
    \begin{center}
      \Large A plasma is neutral on scales larger than $\lambda_D$.
    \end{center}
    """,
)
pdf = poster.build(HERE / "debye_shielding.pdf")

# the poster, as the docs show it
fig, ax = plt.subplots(figsize=(6, 8.5))
ax.imshow(plt.imread(preview(pdf)))
ax.set_axis_off()
