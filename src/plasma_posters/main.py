"""The ``plasma-posters`` command: compile a poster's LaTeX file to a PDF."""

from __future__ import annotations

import argparse

from plasma_posters import __version__
from plasma_posters.poster import compile_latex


def main(argv: list[str] | None = None) -> int:
    """Run the ``plasma-posters`` command.

    ``plasma-posters build poster.tex`` compiles a poster written by
    :meth:`plasma_posters.Poster.save`, for example after editing it by hand.

    Args:
        argv: The arguments; the command line's when None.

    Returns:
        The exit status.
    """
    parser = argparse.ArgumentParser(
        prog="plasma-posters", description="Scientific posters from Python."
    )
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build", help="compile a poster's .tex file to a PDF")
    build.add_argument("tex", help="the poster's .tex file")
    build.add_argument("--engine", default="lualatex", choices=("lualatex", "pdflatex"))
    args = parser.parse_args(argv)
    pdf = compile_latex(args.tex, args.engine)
    print(f"wrote {pdf}")
    return 0
