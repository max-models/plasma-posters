---
title: Installation
description: Create a Python environment and install plasma-posters.
---

Create and activate a Python environment:

```bash
python -m venv env
source env/bin/activate
pip install --upgrade pip
```

Install the package and its requirements with pip:

```bash
pip install -e .
```

Compiling a poster needs a TeX distribution with `lualatex` and the
[tikzposter](https://ctan.org/pkg/tikzposter) class, such as TeX Live, MacTeX or MiKTeX. On
Debian or Ubuntu:

```bash
sudo apt install texlive-luatex texlive-pictures texlive-latex-extra
```

`plasma_posters.preview`, which renders a poster as a PNG, also needs `pdftoppm` from poppler
(`poppler-utils` on Debian and Ubuntu, `brew install poppler` on macOS).

Check the installation with:

```bash
plasma-posters --version
```

## Optional extras

| Extra  | Installs                                                |
| ------ | ------------------------------------------------------- |
| `test` | `pytest` and `coverage`                                 |
| `docs` | the notebook runner and griffe for the API reference    |
| `dev`  | formatters and linters, plus the `test` and `docs` extras |

```bash
pip install -e ".[dev]"
```
