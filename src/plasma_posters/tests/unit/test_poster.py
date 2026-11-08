"""The poster's LaTeX, its checks, and compiling it."""

from __future__ import annotations

import shutil
import subprocess

import pytest

from plasma_posters import Poster, compile_latex
from plasma_posters.main import main


def _poster() -> Poster:
    poster = Poster("Negative ions", authors="A. Author", institute="IPP", columns=2)
    poster.block("Motivation", r"Beams of $\mathrm{H}^-$ ions.")
    poster.figure("Domain", "figures/domain.pdf", caption="The domain.", column=1)
    poster.block("Outlook", "More.", column=1)
    return poster


def test_the_document_has_the_class_title_and_columns():
    tex = _poster().to_latex()
    assert tex.startswith(r"\documentclass[25pt, a0paper, portrait]{tikzposter}")
    assert r"\title{Negative ions}" in tex
    assert r"\author{A. Author}" in tex
    assert r"\institute{IPP}" in tex
    assert tex.count(r"\column{0.5}") == 2
    assert tex.rstrip().endswith(r"\end{document}")


def test_blocks_are_in_their_columns_in_order():
    tex = _poster().to_latex()
    first, second = tex.split(r"\column{0.5}")[1:]
    assert r"\block{Motivation}" in first
    assert r"$\mathrm{H}^-$" in first
    assert second.index(r"\block{Domain}") < second.index(r"\block{Outlook}")


def test_a_figure_is_a_tikzfigure_with_its_caption():
    tex = _poster().to_latex()
    assert r"\begin{tikzfigure}[The domain.]" in tex
    assert r"\includegraphics[width=0.95\linewidth]{figures/domain.pdf}" in tex


def test_a_figure_without_a_caption_has_no_option():
    poster = Poster("T")
    poster.figure("F", "a.png", width=0.5)
    assert "\\begin{tikzfigure}\n" in poster.to_latex()
    assert r"width=0.5\linewidth" in poster.to_latex()


def test_size_and_orientation():
    tex = Poster("T", size="a1", orientation="landscape", columns=3).to_latex()
    assert "a1paper, landscape" in tex
    assert tex.count(r"\column{0.3333}") == 3


@pytest.mark.parametrize(
    "kwargs", [{"size": "a4"}, {"orientation": "square"}, {"columns": 0}]
)
def test_invalid_posters_are_refused(kwargs):
    with pytest.raises(ValueError):
        Poster("T", **kwargs)


def test_invalid_columns_and_widths_are_refused():
    poster = Poster("T", columns=2)
    with pytest.raises(ValueError, match="column"):
        poster.block("B", "text", column=2)
    with pytest.raises(ValueError, match="width"):
        poster.figure("F", "a.pdf", width=1.5)


def test_save_writes_the_document(tmp_path):
    path = _poster().save(tmp_path / "poster.tex")
    assert path.read_text() == _poster().to_latex()


def test_a_missing_latex_is_reported(tmp_path, monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: None)
    with pytest.raises(FileNotFoundError, match="lualatex is not installed"):
        compile_latex(tmp_path / "poster.tex")


def test_a_latex_error_shows_the_log(tmp_path, monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **k: subprocess.CompletedProcess(a, 1, "! Undefined control", ""),
    )
    with pytest.raises(RuntimeError, match="Undefined control"):
        compile_latex(tmp_path / "poster.tex")


def test_the_command_compiles_a_file(tmp_path, monkeypatch, capsys):
    calls = []

    def run(command, **kwargs):
        calls.append((command, kwargs["cwd"]))
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(subprocess, "run", run)
    tex = _poster().save(tmp_path / "poster.tex")
    assert main(["build", str(tex), "--engine", "pdflatex"]) == 0
    assert calls == [
        (
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "poster.tex"],
            tmp_path,
        )
    ]
    assert "poster.pdf" in capsys.readouterr().out


@pytest.mark.skipif(shutil.which("lualatex") is None, reason="needs lualatex")
def test_a_poster_compiles_to_a_pdf(tmp_path):
    poster = Poster("A poster", authors="A. Author", columns=2)
    poster.block("Equation", r"$\nabla \cdot \mathbf{E} = \rho / \varepsilon_0$")
    poster.block("Text", "Plain text.", column=1)
    pdf = poster.build(tmp_path / "poster.pdf")
    assert pdf == (tmp_path / "poster.pdf").resolve()
    assert pdf.read_bytes().startswith(b"%PDF")
