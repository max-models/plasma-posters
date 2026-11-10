"""Landscape poster.

A conference poster on A0 landscape paper in three columns: the introduction and the model on
the left, two figures of results in the middle, conclusions and references on the right. The
physics is Langmuir waves in a warm plasma, with the Bohm-Gross dispersion relation and Landau
damping.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from plasma_posters import Poster, preview

HERE = Path(__file__).resolve().parent

# k in units of 1/Debye length, frequencies in units of the plasma frequency
k = np.linspace(0.01, 0.6, 300)
bohm_gross = np.sqrt(1 + 3 * k**2)
damping = np.sqrt(np.pi / 8) / k**3 * np.exp(-1 / (2 * k**2) - 1.5)

fig, ax = plt.subplots(figsize=(6, 3.8))
ax.plot(k, bohm_gross, label="Bohm-Gross")
ax.plot(k, np.ones_like(k), "--", color="gray", label="cold plasma")
ax.set(xlabel=r"$k \lambda_D$", ylabel=r"$\omega / \omega_p$")
ax.legend()
fig.savefig(HERE / "dispersion.pdf", bbox_inches="tight")
plt.close(fig)

fig, ax = plt.subplots(figsize=(6, 3.8))
ax.semilogy(k, damping)
ax.set(xlabel=r"$k \lambda_D$", ylabel=r"$-\gamma / \omega_p$", ylim=(1e-8, 1))
fig.savefig(HERE / "damping.pdf", bbox_inches="tight")
plt.close(fig)

poster = Poster(
    r"Langmuir waves in a warm plasma",
    authors="Max Lindqvist",
    institute="Max Planck Institute for Plasma Physics, Garching",
    orientation="landscape",
    columns=3,
)
poster.block(
    "Introduction",
    r"""
    Electrons displaced from the ions oscillate at the plasma frequency
    $\omega_p = \sqrt{n e^2 / \varepsilon_0 m_e}$. In a warm plasma the oscillation travels as a
    wave, and the electrons that move with the wave take energy from it.
    """,
)
poster.block(
    "Model",
    r"""
    Linearising the Vlasov-Poisson system about a Maxwellian gives the dispersion relation
    \[
      1 + \frac{1}{k^2 \lambda_D^2}\left[1 + \zeta Z(\zeta)\right] = 0,
      \qquad \zeta = \frac{\omega}{\sqrt{2} k v_{th}},
    \]
    with the plasma dispersion function $Z$. For $k \lambda_D \ll 1$ its real part is
    $\omega^2 = \omega_p^2 + 3 k^2 v_{th}^2$.
    """,
)
poster.figure(
    "Dispersion",
    "dispersion.pdf",
    caption="The frequency grows with the wave number.",
    column=1,
)
poster.figure(
    "Landau damping",
    "damping.pdf",
    caption=r"The damping rate, exponentially small for $k \lambda_D \ll 1$.",
    column=1,
)
poster.block(
    "Conclusions",
    r"""
    \begin{itemize}
      \item Long waves ($k \lambda_D \lesssim 0.2$) are barely damped.
      \item Waves shorter than a few Debye lengths are damped within a few periods.
    \end{itemize}
    """,
    column=2,
)
poster.block(
    "References",
    r"""
    \small
    [1] L. Landau, J. Phys. USSR \textbf{10}, 25 (1946).

    [2] D. Bohm and E. P. Gross, Phys. Rev. \textbf{75}, 1851 (1949).
    """,
    column=2,
)
pdf = poster.build(HERE / "landscape_poster.pdf")

# the poster, as the docs show it
fig, ax = plt.subplots(figsize=(8.5, 6))
ax.imshow(plt.imread(preview(pdf)))
ax.set_axis_off()
