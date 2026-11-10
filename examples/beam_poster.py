"""Neutral beam poster.

A two-column A0 poster on neutral beam injection, made from a run of
`freeofcharge <https://max-models.github.io/freeofcharge/>`_: a 1 MeV deuterium beam in an
ITER-sized Solov'ev equilibrium, its fast ions slowed down on their flux surfaces. The profiles
and the density scan are drawn with `plasma-plots <https://max-models.github.io/plasma-plots/>`_
from labelled xarray data, the beam in 3-D with PyVista. The run takes about
20 seconds.
"""

from pathlib import Path

import freeofcharge as foc
import matplotlib.pyplot as plt
import numpy as np
import plasma_plots
import pyvista as pv
import xarray as xr
from plasma_plots import save_figure

from plasma_posters import Poster, preview

HERE = Path(__file__).resolve().parent

# --- the run: an ITER-like beam, as in freeofcharge's "ITER-like injection" example --------
equilibrium = foc.Equilibrium.solovev(6.2, 1.8, 1.7, 5.3, wall_psi_n=1.3)
origin, direction = foc.tangential_injection(5.3, 12.0)
beam = foc.NeutralBeam.gaussian(
    origin, direction, 1.0e6, 16.5e6, width=0.3, divergence=0.005, markers=2000, seed=1
)
ions = {"D": (2, 1, 0.96), "He": (4, 2, 0.02)}
rho_edges = np.linspace(0.0, 1.0, 26)
surfaces = equilibrium.flux_surfaces(rho_edges)

densities = np.array([1.5e19, 2e19, 3e19, 5e19, 7e19, 1e20])
shine = []
for ne0 in densities:
    plasma = foc.Plasma.parabolic(ne0, 2.0e4, ions=ions)
    result = foc.deposit(
        beam, equilibrium, plasma, step=0.02, births_per_marker=0, rho_edges=rho_edges
    )
    shine.append(100 * result.shine_through_fraction)
shine = xr.DataArray(
    shine,
    coords={
        "ne0": ("ne0", densities, {"long_name": "central density", "units": "1/m^3"})
    },
    dims="ne0",
    attrs={"long_name": "shine-through", "units": "%"},
)

plasma = foc.Plasma.parabolic(1e20, 2.0e4, ions=ions)
deposition = foc.deposit(
    beam,
    equilibrium,
    plasma,
    step=0.02,
    births_per_marker=4,
    rho_edges=rho_edges,
    seed=2,
)
steady = foc.slow_down(deposition, plasma, surfaces)
fast = steady.to_dataset()
heating = fast.heating / xr.DataArray(surfaces.volume, dims="rho") / 1e3
heating.attrs.update(long_name="heating power density", units="kW/m^3")
current = fast.current_density / 1e3
current.attrs.update(long_name="driven current density", units="kA/m^2")

# --- the figures ------------------------------------------------------------------------------
# 3-D: three quarters of the plasma edge, the beam's paths and where the fast ions are born
edge = equilibrium.boundary.vertices  # (R, Z) of the last closed flux surface
phi = np.linspace(0, 1.5 * np.pi, 120)[:, None]  # three quarters of the torus
r, z = edge[:, 0][None, :], edge[:, 1][None, :]
plasma_edge = pv.StructuredGrid(
    r * np.cos(phi), r * np.sin(phi), np.repeat(z, len(phi), axis=0)
)
plotter = pv.Plotter(off_screen=True)
plotter.add_mesh(plasma_edge, color="lightsteelblue", opacity=0.35, smooth_shading=True)
births = np.asarray(deposition.births.positions)
plotter.add_mesh(
    pv.PolyData(births), color="tab:red", point_size=3, render_points_as_spheres=True
)
starts = np.asarray(beam.markers.positions)[::40]
for start in starts:
    plotter.add_mesh(pv.Line(start, start + 16.0 * np.asarray(direction)), color="gray")
# looking down from behind the cut, at a point between the torus and the beam's entry
plotter.camera_position = [(-10.0, -30.0, 16.0), (2.0, -3.0, -1.0), (0.0, 0.0, 1.0)]
plasma_plots.scene(plotter, window_size=[1000, 800]).save_png(HERE / "beam_3d.png")
plotter.close()

with plasma_plots.figure(figsize=(6, 3.5)) as fig:
    shine.plasma.plot.lineout(x="ne0", ax=fig[0])
    fig[0].set_yscale("log")
save_figure(fig, HERE / "beam_shine_through", formats=("pdf",))

with plasma_plots.figure(2, 1, figsize=(6, 6.5)) as fig:
    heating.plasma.plot.profiles(x="rho", over="species", ax=fig[0])
    current.plasma.plot.lineout(x="rho", ax=fig[1])
save_figure(fig, HERE / "beam_profiles", formats=("pdf",))
plt.close("all")

# --- the poster -------------------------------------------------------------------------------
electrons = steady.electron_heating.sum() / 1e6
ions_heating = steady.ion_heating.sum() / 1e6
poster = Poster(
    "Heating and current drive by a 1 MeV neutral beam",
    authors="Max Lindqvist",
    institute="Max Planck Institute for Plasma Physics",
    columns=2,
)
poster.block(
    "The beam",
    r"""
    A $16.5\,\mathrm{MW}$ beam of $1\,\mathrm{MeV}$ deuterium atoms, tangent to
    $R = 5.3\,\mathrm{m}$, enters an ITER-sized plasma ($R_0 = 6.2\,\mathrm{m}$,
    $a = 1.8\,\mathrm{m}$, $B = 5.3\,\mathrm{T}$). Each marker is attenuated by ionisation and
    charge exchange; the fast ions it leaves slow down on their flux surface.
    """,
)
poster.figure(
    "Where the ions are born",
    "beam_3d.png",
    caption=(
        "The beam's paths (grey) through three quarters of the plasma edge, and the birth "
        "points of the fast ions (red)."
    ),
)
poster.figure(
    "Shine-through",
    "beam_shine_through.pdf",
    caption="The power that crosses the plasma onto the inboard wall.",
    column=1,
)
poster.figure(
    "Heating and current",
    "beam_profiles.pdf",
    caption=r"Steady-state profiles at $n_{e0} = 10^{20}\,\mathrm{m^{-3}}$.",
    column=1,
)
poster.block(
    "Results",
    rf"""
    \begin{{itemize}}
      \item The beam may only be switched on above a minimum density: the shine-through
        falls from {shine.values[0]:.0f}\,\% at $1.5 \times 10^{{19}}\,\mathrm{{m^{{-3}}}}$
        to {shine.values[-1]:.2f}\,\% at $10^{{20}}\,\mathrm{{m^{{-3}}}}$.
      \item At $1\,\mathrm{{MeV}}$ the beam heats mostly the electrons:
        {electrons:.1f}\,MW to the electrons, {ions_heating:.1f}\,MW to the ions.
      \item It drives {steady.driven_current / 1e6:.2f}\,MA along the field.
    \end{{itemize}}
    """,
    column=1,
)
pdf = poster.build(HERE / "beam_poster.pdf")

# the poster, as the docs show it
fig, ax = plt.subplots(figsize=(6, 8.5))
ax.imshow(plt.imread(preview(pdf)))
ax.set_axis_off()
