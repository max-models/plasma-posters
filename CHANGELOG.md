# Changelog

All notable changes to this project are documented in this file and maintained manually. The
format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- `preview(pdf, page=...)` renders any page, and `preview_pages(pdf)` every page of a PDF as
  `<name>-<page>.png`, in page order, e.g. the slides of a talk.

- Example posters with plasma-plots figures of real data: "Neutral beam poster" (a
  freeofcharge run of a 1 MeV beam in an ITER-sized plasma), "Stellarator poster" (GVEC's
  tutorial stellarator, solved when the script runs) and "Optimised stellarators poster"
  (DESC's example equilibria), each with a 3-D view rendered by PyVista: the beam through three
  quarters of the plasma edge, and the stellarators cut open on a flux surface. Their packages
  are in `docs/requirements-examples.txt`, installed by the docs build.
- A long title wraps instead of running off the title box.
- `preview(pdf)`: the first page of a poster as a PNG, with poppler's `pdftoppm`, to check a
  layout.
- The preamble loads `amssymb` too (`\lesssim`, `\mathbb` and the other AMS symbols), and
  block bodies are dedented, so they can be indented triple-quoted strings.
- Example posters in the docs, each shown as compiled: "Debye shielding" (one column on A1),
  "Landscape poster" (three columns), "Lists and tables" and "Sizes and orientations"; the
  docs build installs TeX Live and poppler to compile them.
- `Poster`: a title, authors and institute, and blocks of text (`block`) and figures
  (`figure`) in equal columns, on A0, A1 or A2 paper in portrait or landscape; text, titles and
  captions are LaTeX. `to_latex` writes a tikzposter document, `save` a `.tex` file and `build`
  compiles it to a PDF with lualatex (or pdflatex).
- `compile_latex` and the `plasma-posters build poster.tex` command, for a `.tex` edited by
  hand; compiling is the opt-in scope-profiler region `plasma_posters.compile`.
- Docs: installation, quickstart, the "Blocks and columns" notebook and the "First poster"
  example script.
