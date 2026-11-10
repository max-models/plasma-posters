r"""A poster: blocks of text and figures in columns, written as LaTeX and compiled to PDF.

The LaTeX uses the `tikzposter <https://ctan.org/pkg/tikzposter>`_ class. Text, titles and
captions are LaTeX, so they can hold maths (``$E = mc^2$``) and commands; they are not escaped.

>>> poster = Poster("Negative ion beams", authors="Max Lindqvist", columns=2)
>>> poster.block("Motivation", r"Beams of $\mathrm{H}^-$ ions.")
>>> poster.figure("Domain", "domain.pdf", caption="The extraction region.", column=1)
>>> poster.to_latex().startswith(r"\documentclass")
True
"""

from __future__ import annotations

import shutil
import subprocess
import textwrap
from dataclasses import dataclass, field
from pathlib import Path

import scope_profiler as sp

from plasma_posters._profiling import PROFILE_TAGS

#: Paper sizes of the tikzposter class.
SIZES = ("a0", "a1", "a2")

#: Orientations of the tikzposter class.
ORIENTATIONS = ("portrait", "landscape")


def preview(pdf: str | Path, png: str | Path | None = None, dpi: int = 30) -> Path:
    """Render the first page of a poster's PDF as a PNG, to check its layout.

    Uses ``pdftoppm`` from poppler (``poppler-utils`` on Debian and Ubuntu, ``poppler`` in
    Homebrew).

    Args:
        pdf: The poster's PDF.
        png: The PNG to write; next to the PDF with the same name when None.
        dpi: The resolution; 30 gives an A0 page about 1000 pixels high.

    Returns:
        The PNG's path.

    Raises:
        FileNotFoundError: If pdftoppm is not installed.
        RuntimeError: If pdftoppm fails.
    """
    pdf = Path(pdf).resolve()
    png = pdf.with_suffix(".png") if png is None else Path(png).resolve()
    if shutil.which("pdftoppm") is None:
        raise FileNotFoundError("pdftoppm is not installed: install poppler")
    result = subprocess.run(
        [
            "pdftoppm",
            "-png",
            "-r",
            str(dpi),
            "-singlefile",
            str(pdf),
            str(png.with_suffix("")),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pdftoppm failed on {pdf}: {result.stderr.strip()}")
    return png


@dataclass
class Block:
    """A titled block of a poster column.

    Attributes:
        title: The block's heading (LaTeX).
        body: The block's content (LaTeX).
        column: The index of the column the block is in, from 0.
    """

    title: str
    body: str
    column: int = 0


@sp.profile("plasma_posters.compile", tags=PROFILE_TAGS)
def compile_latex(tex: str | Path, engine: str = "lualatex") -> Path:
    """Compile a LaTeX file to a PDF next to it.

    Args:
        tex: The ``.tex`` file; figure paths in it are relative to its folder.
        engine: The LaTeX program, ``"lualatex"`` or ``"pdflatex"``.

    Returns:
        The PDF's path.

    Raises:
        FileNotFoundError: If the LaTeX program is not installed.
        RuntimeError: If LaTeX fails; the message ends with the end of its log.
    """
    tex = Path(tex).resolve()
    if shutil.which(engine) is None:
        raise FileNotFoundError(
            f"{engine} is not installed: install a TeX distribution with the tikzposter "
            "class (TeX Live, MiKTeX or MacTeX)"
        )
    result = subprocess.run(
        [engine, "-interaction=nonstopmode", "-halt-on-error", tex.name],
        cwd=tex.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        log = "\n".join(result.stdout.splitlines()[-20:])
        raise RuntimeError(f"{engine} failed on {tex}:\n{log}")
    return tex.with_suffix(".pdf")


@dataclass
class Poster:
    """A scientific poster: a title, authors, and blocks of text and figures in columns.

    Attributes:
        title: The poster's title (LaTeX).
        authors: The authors, as one line (LaTeX).
        institute: The authors' institute, below the authors (LaTeX); empty for none.
        size: The paper size, one of :data:`SIZES`.
        orientation: ``"portrait"`` or ``"landscape"``.
        columns: The number of columns, of equal width.
        blocks: The blocks, in the order they were added.
    """

    title: str
    authors: str = ""
    institute: str = ""
    size: str = "a0"
    orientation: str = "portrait"
    columns: int = 2
    blocks: list[Block] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Check the size, orientation and number of columns."""
        if self.size not in SIZES:
            raise ValueError(f"size must be one of {SIZES}, not {self.size!r}")
        if self.orientation not in ORIENTATIONS:
            raise ValueError(
                f"orientation must be one of {ORIENTATIONS}, not {self.orientation!r}"
            )
        if self.columns < 1:
            raise ValueError(f"columns must be at least 1, not {self.columns}")

    def block(self, title: str, body: str, column: int = 0) -> None:
        """Add a block of text.

        Args:
            title: The block's heading (LaTeX).
            body: The text (LaTeX); paragraphs are separated by blank lines. Its common
                indentation is removed, so it can be an indented triple-quoted string.
            column: The column to put the block in, from 0; blocks of a column are stacked
                in the order they are added.

        Raises:
            ValueError: If the column does not exist.
        """
        if not 0 <= column < self.columns:
            raise ValueError(
                f"column must be between 0 and {self.columns - 1}, not {column}"
            )
        self.blocks.append(Block(title, textwrap.dedent(body).strip(), column))

    def figure(
        self,
        title: str,
        path: str | Path,
        caption: str = "",
        width: float = 0.95,
        column: int = 0,
    ) -> None:
        """Add a block with a figure.

        Args:
            title: The block's heading (LaTeX).
            path: The figure file (PDF, PNG or JPEG), relative to the poster's ``.tex`` file
                or absolute.
            caption: The caption below the figure (LaTeX); empty for none.
            width: The figure's width as a fraction of the column's width.
            column: The column to put the block in, from 0.

        Raises:
            ValueError: If the width is not in (0, 1] or the column does not exist.
        """
        if not 0 < width <= 1:
            raise ValueError(f"width must be in (0, 1], not {width}")
        graphic = (
            rf"\includegraphics[width={width:g}\linewidth]{{{Path(path).as_posix()}}}"
        )
        option = f"[{caption}]" if caption else ""
        body = f"\\begin{{tikzfigure}}{option}\n  {graphic}\n\\end{{tikzfigure}}"
        self.block(title, body, column)

    def to_latex(self) -> str:
        """The poster as a LaTeX document.

        Returns:
            The complete document, for ``lualatex`` or ``pdflatex``.
        """
        lines = [
            rf"\documentclass[25pt, {self.size}paper, {self.orientation}]{{tikzposter}}",
            r"\usepackage{graphicx}",
            r"\usepackage{amsmath, amssymb}",
            r"\usetheme{Simple}",
            "",
            # a parbox, so a long title wraps instead of running off the title box
            rf"\title{{\parbox{{0.8\linewidth}}{{\centering {self.title}}}}}",
            rf"\author{{{self.authors}}}",
            rf"\institute{{{self.institute}}}",
            "",
            r"\begin{document}",
            r"\maketitle",
            r"\begin{columns}",
        ]
        width = f"{1 / self.columns:.4g}"
        for column in range(self.columns):
            lines.append(rf"\column{{{width}}}")
            for block in self.blocks:
                if block.column == column:
                    lines += [rf"\block{{{block.title}}}{{", block.body, "}"]
        lines += [r"\end{columns}", r"\end{document}", ""]
        return "\n".join(lines)

    def save(self, path: str | Path) -> Path:
        """Write the poster's LaTeX to a file.

        Args:
            path: The ``.tex`` file to write.

        Returns:
            The path written.
        """
        path = Path(path)
        path.write_text(self.to_latex())
        return path

    def build(self, path: str | Path, engine: str = "lualatex") -> Path:
        """Write the poster's LaTeX next to ``path`` and compile it to a PDF.

        Args:
            path: The PDF to write, e.g. ``"poster.pdf"``; its ``.tex`` is written next to it.
            engine: The LaTeX program, ``"lualatex"`` or ``"pdflatex"``.

        Returns:
            The PDF's path.
        """
        tex = self.save(Path(path).with_suffix(".tex"))
        return compile_latex(tex, engine)
