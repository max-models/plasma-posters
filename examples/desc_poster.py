"""Optimised stellarators poster.

A three-column A0 landscape poster on optimised stellarators, from the equilibria that
`DESC <https://desc-docs.readthedocs.io/>`_ ships: W7-X, the precise quasi-axisymmetric and
quasi-helical configurations, NCSX, HELIOTRON, ESTELL and the tokamak DSHAPE.
`plasma-plots <https://max-models.github.io/plasma-plots/>`_ evaluates them (``from_desc``) and
draws the poloidal planes, ``|B|`` on the boundary in PEST angles and W7-X's profiles. It needs
``pip install desc-opt``.
"""

import warnings
from pathlib import Path

import desc.examples
import matplotlib.pyplot as plt
import numpy as np
import plasma_plots
from plasma_plots import save_figure

from plasma_posters import Poster, preview

HERE = Path(__file__).resolve().parent
warnings.filterwarnings("ignore", module="desc")  # DESC's notes on JAX and resolutions


def example(name):
    """One of DESC's example equilibria."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return desc.examples.get(name)


# --- W7-X: three poloidal planes over half a field period, and its profiles -----------------
w7x = example("W7-X")
planes = plasma_plots.from_desc(
    w7x,
    ["|B|", "theta_PEST"],
    rho=13,
    theta=96,
    zeta=np.linspace(0, np.pi / w7x.NFP, 3),
)
result = planes["|B|"].plasma.plot.panels(
    sweep="zeta",
    coords="physical",
    plane="RZ",
    nrows=3,
    ncols=1,
    overlays={"coordinate_lines": {"rho": 4, "theta_P": 12}},
)
result.fig.set_size_inches(4.5, 9)
save_figure(result, HERE / "desc_w7x_planes", formats=("pdf",))

profiles = plasma_plots.from_desc(w7x, ["iota", "D_Mercier"], rho=17, theta=8, zeta=4)
with plasma_plots.figure(1, 2, figsize=(7, 3)) as fig:
    profiles.iota.plasma.plot.lineout(rationals=4, ax=fig[0])
    profiles.D_Mercier.sel(rho=slice(0.1, None)).plasma.plot.lineout(ax=fig[1])
save_figure(fig, HERE / "desc_w7x_profiles", formats=("pdf",))

# --- DESC's example library at zeta = 0 -------------------------------------------------------
gallery = ["precise_QA", "precise_QH", "NCSX", "HELIOTRON", "ESTELL", "DSHAPE"]
with plasma_plots.figure(3, 2, figsize=(7, 10)) as fig:
    for ax, name in zip(fig, gallery, strict=True):
        plane = plasma_plots.from_desc(
            example(name), ["|B|", "theta_PEST"], rho=9, theta=64, zeta=[0.0]
        )
        plane["|B|"].plasma.plot.slice(
            coords="physical",
            plane="RZ",
            zeta=0.0,
            title=name,
            overlays={"coordinate_lines": {"rho": 4, "theta_P": 8}},
            ax=ax,
        )
save_figure(fig, HERE / "desc_gallery", formats=("pdf",))

# --- quasi-symmetry: |B| on the boundary in PEST angles ---------------------------------------
with plasma_plots.figure(2, 1, figsize=(6, 6.5)) as fig:
    for ax, name in zip(fig, ["precise_QA", "precise_QH"], strict=True):
        surface = plasma_plots.from_desc(
            example(name), "|B|", rho=[0.5, 1.0], theta=64, zeta=64, sfl="pest"
        )
        surface["|B|"].plasma.plot.slice(
            x="zeta", y="theta_P", rho=1.0, levels=12, title=name, ax=ax
        )
save_figure(fig, HERE / "desc_quasisymmetry", formats=("pdf",))
plt.close("all")

# --- the poster -------------------------------------------------------------------------------
poster = Poster(
    "Optimised stellarators from DESC",
    authors="Max Lindqvist",
    institute="Max Planck Institute for Plasma Physics",
    orientation="landscape",
    columns=3,
)
poster.block(
    "Optimised stellarators",
    r"""
    A stellarator confines a plasma with twisted coils alone, without a plasma current. Its
    shape is chosen by optimisation: W7-X for small neoclassical transport, the precise
    configurations for quasi-symmetry, in which $|B|$ depends on one helical angle only.
    """,
)
poster.figure(
    "W7-X",
    "desc_w7x_planes.pdf",
    caption="$|B|$ over half a field period, with flux-coordinate lines.",
    width=0.5,
)
poster.figure(
    "DESC's example library",
    "desc_gallery.pdf",
    caption=r"$|B|$ on the poloidal plane $\zeta = 0$.",
    column=1,
)
poster.figure(
    "Quasi-symmetry",
    "desc_quasisymmetry.pdf",
    caption="$|B|$ on the boundary in PEST angles: its contours follow one direction.",
    column=2,
)
poster.figure(
    "W7-X profiles",
    "desc_w7x_profiles.pdf",
    caption=r"The rotational transform with its rationals, and the Mercier criterion.",
    column=2,
)
pdf = poster.build(HERE / "desc_poster.pdf")

# the poster, as the docs show it
fig, ax = plt.subplots(figsize=(8.5, 6))
ax.imshow(plt.imread(preview(pdf)))
ax.set_axis_off()
