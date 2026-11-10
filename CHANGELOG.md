# Changelog

All notable changes to this project are documented in this file and maintained manually. The
format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

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
