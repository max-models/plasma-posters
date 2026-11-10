"""Stellarator poster.

A two-column A0 poster on a stellarator equilibrium computed with
`GVEC <https://gvec.readthedocs.io/>`_: GVEC's tutorial stellarator, three field periods of a
rotating ellipse. The equilibrium is solved when the script runs (a few seconds) and evaluated
on a grid; `plasma-plots <https://max-models.github.io/plasma-plots/>`_ reads the evaluations
(``from_gvec``) and draws the poloidal planes, ``|B|`` on a flux surface in GVEC's and Boozer's
angles, and the profiles. It needs ``pip install gvec``, which builds GVEC's Fortran core.
"""

import os

os.environ.setdefault("OMP_NUM_THREADS", "2")  # before importing gvec

import tempfile
from pathlib import Path

import gvec
import matplotlib.pyplot as plt
import numpy as np
import plasma_plots
from plasma_plots import save_figure

from plasma_posters import Poster, preview

HERE = Path(__file__).resolve().parent

# --- the equilibrium: GVEC's tutorial stellarator ---------------------------------------------
parameters = {
    "ProjectName": "stellarator",
    "which_hmap": 1,
    "PhiEdge": 1.0,
    "iota": {"type": "polynomial", "coefs": [0.625, 0.35]},
    "pres": {"type": "polynomial", "coefs": [1.0, -1.0], "scale": 1000.0},
    "nfp": 3,
    "X1_b_cos": {(0, 0): 3.0, (1, 0): 1.0, (1, 1): 0.4},
    "X2_b_sin": {(1, 0): 1.0, (1, 1): -0.4, (0, 1): -0.25},
    "init_average_axis": True,
    "sgrid_nElems": 2,
    "X1_mn_max": [3, 3],
    "X2_mn_max": [3, 3],
    "LA_mn_max": [3, 3],
    "X1X2_deg": 5,
    "LA_deg": 5,
    "totalIter": 1000,
    "minimize_tol": 1.0e-6,
}
state = gvec.run(parameters, runpath=tempfile.mkdtemp(), quiet=True).state

# one field period on GVEC's angles, and the same field period on a Boozer grid
ev = plasma_plots.from_gvec(
    state.evaluate(
        *("mod_B", "pos", "X1", "X2", "iota", "p", "theta_P", "N_FP"),
        rho=17,
        theta=64,
        zeta=40,
    )
)
boozer = plasma_plots.from_gvec(
    state.evaluate_sfl(
        *("mod_B", "pos", "N_FP"),
        rho=np.linspace(0.1, 1.0, 10),
        theta=64,
        zeta=40,
        sfl="boozer",
    )
)

# --- the figures ------------------------------------------------------------------------------
planes = ev.mod_B.plasma.plot.panels(
    sweep="zeta",
    coords="physical",
    plane="RZ",
    nrows=3,
    ncols=1,
    overlays={"coordinate_lines": {"rho": 4, "theta_P": 8}},
)
planes.fig.set_size_inches(5, 11)
save_figure(planes, HERE / "stellarator_planes", formats=("pdf",))

with plasma_plots.figure(2, 1, figsize=(6, 6.5)) as fig:
    ev.mod_B.plasma.plot.slice(x="zeta", y="theta", rho=0.5, levels=12, ax=fig[0])
    boozer.mod_B.plasma.plot.slice(
        x="zeta_B", y="theta_B", rho=0.5, levels=12, ax=fig[1]
    )
save_figure(fig, HERE / "stellarator_surface", formats=("pdf",))

with plasma_plots.figure(1, 2, figsize=(7, 3)) as fig:
    ev.iota.plasma.plot.lineout(rationals=4, ax=fig[0])
    ev.p.plasma.plot.lineout(ax=fig[1])
save_figure(fig, HERE / "stellarator_profiles", formats=("pdf",))
plt.close("all")

# --- the poster -------------------------------------------------------------------------------
poster = Poster(
    "A three-period stellarator with GVEC",
    authors="Max Lindqvist",
    institute="Max Planck Institute for Plasma Physics",
    columns=2,
)
poster.block(
    "The equilibrium",
    r"""
    GVEC minimises the MHD energy
    \[
      W = \int_V \left(\frac{B^2}{2\mu_0} + \frac{p}{\gamma - 1}\right) \mathrm{d}V
    \]
    for a given boundary, pressure $p(\rho)$ and rotational transform $\iota(\rho)$. The
    boundary here is an ellipse that turns three times around the torus ($N_{FP} = 3$).
    """,
)
poster.figure(
    "Poloidal planes",
    "stellarator_planes.pdf",
    caption=r"$|B|$ across one field period, with flux-coordinate lines.",
    width=0.8,
)
poster.figure(
    r"$|B|$ on the surface $\rho = 0.5$",
    "stellarator_surface.pdf",
    caption="In GVEC's angles (top) and in Boozer angles (bottom), where the field lines are straight.",
    column=1,
)
poster.figure(
    "Profiles",
    "stellarator_profiles.pdf",
    caption=r"The rotational transform with its low-order rationals, and the pressure.",
    column=1,
)
pdf = poster.build(HERE / "stellarator_poster.pdf")

# the poster, as the docs show it
fig, ax = plt.subplots(figsize=(6, 8.5))
ax.imshow(plt.imread(preview(pdf)))
ax.set_axis_off()
