"""Lists and tables.

Block bodies are LaTeX, so anything LaTeX typesets goes on a poster: bullet and numbered
lists, tables, aligned equations, bold and coloured text. This poster collects the parameters
of a hydrogen plasma in an ion source and the steps of a particle-in-cell cycle.
"""

from pathlib import Path

import matplotlib.pyplot as plt

from plasma_posters import Poster, preview

HERE = Path(__file__).resolve().parent

poster = Poster(
    "A hydrogen ion source in numbers",
    authors="Max Lindqvist",
    institute="Max Planck Institute for Plasma Physics",
    columns=2,
)
poster.block(
    "Parameters",
    r"""
    \begin{center}
    \begin{tabular}{lll}
      \hline
      Quantity & Symbol & Value \\
      \hline
      Electron density & $n_e$ & $10^{17}\,\mathrm{m^{-3}}$ \\
      Electron temperature & $T_e$ & $2\,\mathrm{eV}$ \\
      Debye length & $\lambda_D$ & $33\,\mu\mathrm{m}$ \\
      Plasma frequency & $\omega_p / 2\pi$ & $2.8\,\mathrm{GHz}$ \\
      \hline
    \end{tabular}
    \end{center}
    """,
)
poster.block(
    "Scales",
    r"""
    \begin{align*}
      \lambda_D &= \sqrt{\frac{\varepsilon_0 k_B T_e}{n_e e^2}}, &
      \omega_p &= \sqrt{\frac{n_e e^2}{\varepsilon_0 m_e}}.
    \end{align*}
    A cell must resolve $\lambda_D$ and a time step $\omega_p^{-1}$: \textbf{both set the cost}.
    """,
)
poster.block(
    "One particle-in-cell step",
    r"""
    \begin{enumerate}
      \item Deposit the charges of the markers on the grid.
      \item Solve Poisson's equation for the potential.
      \item Interpolate the field to the markers.
      \item Push the markers and apply the boundary conditions.
      \item Collide them with the background gas.
    \end{enumerate}
    """,
    column=1,
)
poster.block(
    "Why it matters",
    r"""
    \begin{itemize}
      \item The ion source supplies the $\mathrm{H}^-$ ions of a neutral beam.
      \item Its plasma sets the current and the divergence of the beam.
      \item \textcolor{red}{Co-extracted electrons} must stay below the ion current.
    \end{itemize}
    """,
    column=1,
)
pdf = poster.build(HERE / "lists_and_tables.pdf")

# the poster, as the docs show it
fig, ax = plt.subplots(figsize=(6, 8.5))
ax.imshow(plt.imread(preview(pdf)))
ax.set_axis_off()
